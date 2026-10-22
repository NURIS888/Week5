# Sort List

LeetCode: https://leetcode.com/problems/sort-list/description/

## 1. Problem

I'm given the head of a singly linked list containing integers in no
particular order, and I need to return the head of a new (or rearranged)
linked list where the values are sorted in ascending order. Like the
companion "Sort an Array" problem, this one is listed under the
"merge-sort" practice set, so the goal is to implement merge sort
specifically — not just extract the values, sort them some other way,
and rebuild the list (which I discuss further down, since I actually
tried that first).

## 2. Approach

This uses the exact same divide-and-conquer idea as "Sort an Array":
split into two halves, recursively sort each half, then merge the two
sorted halves back together. The merging step is identical in spirit to
the "Merge Two Sorted Lists" assignment from a previous week (re-link
existing nodes using a dummy head, rather than creating new nodes).

**The real difference from sorting an array is the SPLITTING step.**
With an array, I can instantly slice `nums[:mid]` and `nums[mid:]`
because I already know the length and can jump straight to any index. A
singly linked list has neither: I don't know the length up front, and I
can't jump to the middle directly — I can only walk forward one node at
a time following `.next` pointers.

To find the middle of a linked list in a single pass, I use the
**slow/fast pointer trick**: `slow` advances 1 node per step, `fast`
advances 2 nodes per step. Since `fast` covers ground twice as quickly,
by the time `fast` reaches the end of the list, `slow` is sitting almost
exactly at the middle. I keep a `prev` pointer trailing just behind
`slow` so that once I know where the middle is, I can physically cut the
list in two by setting `prev.next = None`.

Full algorithm:
1. **Base case:** if `head` is `None` or `head.next` is `None` (0 or 1
   node), the list is already sorted — return it as-is.
2. **Split:** walk `slow`/`fast`/`prev` pointers to find the middle, then
   cut the list into `left` (from `head` up to, but not including, the
   middle) and `right` (from the middle to the end).
3. **Recurse:** call `sort_list` on `left` and on `right` separately.
4. **Merge:** merge the two now-sorted lists together using the dummy-
   head merging technique, and return the merged head.

### Manual trace

Example: `4 -> 2 -> 1 -> 3`

**Finding the middle (step 2), traced:**

The loop condition is `fast is not None and fast.next is not None`,
checked fresh before each iteration.

| Iteration | Check loop condition | prev (updates to old slow) | slow moves to | fast moves to |
|---|---|---|---|---|
| start | — | None | 4 (1st node) | 4 (1st node) |
| 1 | fast=4 not None, fast.next=2 not None → run | 4 | 2 (2nd node) | 1 (3rd node) |
| 2 | fast=1 not None, fast.next=3 not None → run | 2 | 1 (3rd node) | fast.next.next = None |
| 3 | fast is None → stop | — | — | — |

Final state: `slow` = node `1` (3rd node), `prev` = node `2` (2nd node).
Cutting: `prev.next = None` turns `4 -> 2` into the left half, and
`1 -> 3` (starting from `slow`) becomes the right half.

**Recursive sorting of each half:**
```
sort_list(4 -> 2)
  split into [4] and [2] (each base case)
  merge([4], [2]) -> 2 -> 4

sort_list(1 -> 3)
  split into [1] and [3] (each base case)
  merge([1], [3]) -> 1 -> 3
```

**Final merge:** merge `2 -> 4` with `1 -> 3`

| Step | list1 head | list2 head | Compare | Attach | list1 after | list2 after |
|------|-----------|-----------|---------|--------|-------------|-------------|
| 1 | 2 | 1 | 2<=1? no | take list2 (1) | [2,4] | [3] |
| 2 | 2 | 3 | 2<=3? yes | take list1 (2) | [4] | [3] |
| 3 | 4 | 3 | 4<=3? no | take list2 (3) | [4] | [] |
| 4 | list2 empty | — | stop loop | attach remaining list1 (4) | — | — |

Final result: `1 -> 2 -> 3 -> 4` — correctly sorted.

Edge cases checked:
- Empty list (`head = None`): base case triggers immediately, returns
  `None`.
- Single node: `head.next is None` triggers the base case, returns the
  node unchanged.
- All duplicates (`[3,3,3,3]`): splitting and merging both still work
  correctly since comparisons use `<=`, which handles ties fine.

### Challenges / what didn't work first

My very first idea (kept in `solution.py` as `sort_list_brute_force`)
was: walk the list once to dump every value into a Python array, call
the array's built-in `.sort()`, then walk the list a second time
overwriting each node's `.val` with the now-sorted values in order. This
works, and I kept it specifically to cross-check my merge sort's output
on every test case. But I didn't use it as my main solution for two
reasons: (1) it leans entirely on Python's built-in sort rather than
implementing the sorting algorithm myself, which defeats the purpose of
an assignment about understanding merge sort, and (2) it doesn't
actually restructure the linked list at all — it just overwrites values
in the existing nodes, which feels like "cheating" the structure of the
problem rather than genuinely working with linked list mechanics (no
`.next` pointer manipulation happens at all).

The part I genuinely struggled with, moving to a real merge-sort
version, was the **splitting step**. My first attempt at finding the
middle didn't use a `prev` pointer at all — I tried to find `slow` first
and then do a SECOND pass starting from `head`, walking up to
`length // 2 - 1` to find the node just before the middle so I could cut
there. This worked but required first computing the full length (a third
full traversal, if you count finding `slow`/`fast` separately from
counting length), which felt redundant. I then realized I could just
track `prev` simultaneously, in the SAME loop that finds `slow`/`fast` —
updating `prev = slow` right before advancing `slow` forward — so the
split point is known the moment the slow/fast loop finishes, with no
extra pass needed. This was the same "aha" as using slow/fast pointers
for cycle detection in an earlier assignment: the pointer trick can
often be extended slightly (here, adding one more trailing pointer) to
get an extra piece of information "for free" within the same single
pass, instead of needing a separate pass to compute it.

I also initially forgot to actually CUT the list (`prev.next = None`)
after finding the middle. Without that cut, the "left" half I passed
into the recursive call would still have its `.next` chain running all
the way through the "right" half too, since they're still the same
physical nodes connected together — the recursive call on `left` would
then process every node from `head` to the very end of the entire
original list, not just the first half, because nothing had actually
been disconnected yet. Running the test cases immediately showed
something was wrong (results looked almost right but with repeated or
oddly ordered values from infinite-feeling recursion on overlapping
sublists), which led me to realize the cut step isn't optional — merge
sort on a linked list requires genuinely splitting the node chain in two
separate, disconnected lists before recursing, not just finding where
the midpoint conceptually is.

## 3. Time Complexity

**Time Complexity: O(n log n)**, where `n` is the number of nodes in the
list.

### Why

Same reasoning as the array version: picture the recursion as a tree.
Each level of recursion splits every sublist in half, so after
`log₂(n)` levels, we reach individual nodes (base case). At each level
of the tree, finding the middle of every sublist takes time proportional
to that sublist's length (the slow/fast pointer walk visits roughly half
the sublist's nodes), and merging all the sublists at that level back
together also takes time proportional to their combined length. Since
the sublists at any one level always add up to `n` total nodes, the
total work done at each level is O(n). With `log n` levels, the overall
time is `O(n) × O(log n)` = **O(n log n)**.

**Space Complexity: O(log n)** for the recursion call stack (since the
recursion is `log n` levels deep), which is notably BETTER than the
array version's O(n). This is because, unlike the array version (which
allocates brand-new arrays with every `nums[:mid]` slice and every
`merged = []`), this linked-list version doesn't create any new nodes at
all — it only rewires existing `.next` pointers, both when splitting
(`prev.next = None`) and when merging (relinking into the `dummy`/`tail`
chain). So the only extra memory this solution uses is the recursion
stack itself, which is O(log n), not O(n).

## 4. Reflection / Improvement

- Is there a more efficient approach in terms of time? Not
  asymptotically — O(n log n) is the proven lower bound for any
  comparison-based sort, so this is already optimal in that sense,
  exactly like the array version.
- What about space? My version is already fairly efficient at
  O(log n) extra space (just the recursion stack), since reusing
  existing nodes instead of allocating new ones is a natural fit for
  linked lists. A further improvement that's commonly discussed for this
  exact problem is a **bottom-up (iterative) merge sort**: instead of
  using recursion to repeatedly split the list in half, iteratively
  merge sublists of size 1, then size 2, then size 4, then size 8, and so
  on, doubling each pass, until the sublist size covers the whole list.
  This achieves the same O(n log n) time but drives extra space down to
  **O(1)**, since it removes the recursion call stack entirely (no
  recursive calls at all — just loops).
- What would I need to change for that? I'd need to compute the list's
  length once up front (one O(n) pass), then loop over increasing
  "sublist sizes" (1, 2, 4, 8, ...), and for each pass, walk through the
  whole list merging adjacent pairs of sublists of the current size
  using pointer manipulation, reconnecting everything into one list
  before starting the next pass with a doubled size. This is
  conceptually the same merging logic I already have, just organized
  iteratively (bottom-up) instead of recursively (top-down), which is
  exactly how I'd remove the call stack's O(log n) space usage and reach
  true O(1) auxiliary space while keeping O(n log n) time.
