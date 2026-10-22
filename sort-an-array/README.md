# Sort an Array

LeetCode: https://leetcode.com/problems/sort-an-array/description/

## 1. Problem

I'm given an array of integers (which can include duplicates and negative
numbers) and need to return it sorted in ascending order. The array isn't
pre-sorted in any way, and I can't assume anything special about it. This
problem is listed under LeetCode's "merge-sort" practice set, so the
expected technique is merge sort rather than just calling a built-in
sort function.

## 2. Approach

Merge sort is a **divide and conquer** algorithm, built on one simple
observation: merging two arrays that are ALREADY sorted into one sorted
array is easy and fast — just walk both arrays with one pointer each,
always taking whichever current element is smaller, and advance that
pointer. This is the exact same "merge" logic I used for the "Merge Two
Sorted Lists" assignment, just applied to plain arrays instead of linked
list nodes.

Given that merging is easy, the rest of the algorithm is about getting
two sorted halves to merge in the first place:

1. **Base case:** if the array has 0 or 1 elements, it's already sorted
   by definition — return it as-is.
2. **Divide:** split the array into two halves at the midpoint.
3. **Conquer:** recursively sort each half using this exact same
   function (so eventually, recursion breaks every half down to the
   1-or-0-element base case).
4. **Combine:** merge the two now-sorted halves back together into one
   sorted array, using the merge routine described above.

### Manual trace

Example: `[5, 2, 3, 1]`

**Dividing (going down):**
```
sort_array([5, 2, 3, 1])
  mid = 2
  left_half  = sort_array([5, 2])
                 mid = 1
                 left_half  = sort_array([5])  -> base case, returns [5]
                 right_half = sort_array([2])  -> base case, returns [2]
                 merge([5], [2]) -> [2, 5]
  right_half = sort_array([3, 1])
                 mid = 1
                 left_half  = sort_array([3])  -> base case, returns [3]
                 right_half = sort_array([1])  -> base case, returns [1]
                 merge([3], [1]) -> [1, 3]
  merge([2, 5], [1, 3]) -> ?
```

**The final merge step, traced in detail:** merging `[2, 5]` and `[1, 3]`

| Step | left[i] | right[j] | Compare | Append | merged so far |
|------|---------|----------|---------|--------|----------------|
| 1 | 2 (i=0) | 1 (j=0) | 2 <= 1? no | take right[0]=1, j=1 | [1] |
| 2 | 2 (i=0) | 3 (j=1) | 2 <= 3? yes | take left[0]=2, i=1 | [1, 2] |
| 3 | 5 (i=1) | 3 (j=1) | 5 <= 3? no | take right[1]=3, j=2 | [1, 2, 3] |
| 4 | right exhausted (j=2 == len) | — | loop ends | — | [1, 2, 3] |
| 5 | leftover: left[1:] = [5] | — | append remainder | — | [1, 2, 3, 5] |

Final result: `[1, 2, 3, 5]` — correctly sorted.

Edge cases checked:
- Empty array: base case triggers immediately (`len(nums) <= 1`), returns
  `[]` unchanged.
- All duplicates (`[3,3,3,3]`): merges still work correctly since `<=`
  handles ties by preferring the left element, keeping the sort stable.
- Negative numbers: comparisons use standard `<=`, which works the same
  regardless of sign.

### Challenges / what didn't work first

My very first instinct, before committing to merge sort, was
**selection sort** (kept in `solution.py` as `sort_array_brute_force`):
repeatedly scan the unsorted remainder of the array for the minimum
element and swap it into place. This is simple to reason about and I got
it working correctly right away, and I kept it in the file specifically
to cross-check my merge sort's output against it on every test case. But
I didn't submit it as the main solution for two reasons: (1) it's O(n²)
time, which is clearly worse than what's achievable, and (2) this
problem is explicitly grouped under the "merge-sort" practice set, so
the point of the exercise is to actually practice and understand merge
sort specifically, not just get a sorted array back by any means.

When I first implemented the merge sort `_merge` helper, I made a
mistake: I forgot the final two `extend()` calls for leftover elements,
and just stopped once either pointer reached the end of its array. This
silently dropped elements — for example, merging `[2, 5]` and `[1, 3]`
would stop after placing `1, 2, 3` and never add the `5`, because my
while loop condition `i < len(left) and j < len(right)` becomes false as
soon as `right` is exhausted, at which point `left` might still have
elements left that were never copied over. Running my test cases
immediately caught this (output arrays were shorter than expected), which
reminded me that this "exhaust the remainder" step isn't an
afterthought — it's a required part of the merge, since at least one of
the two arrays will almost always have leftover elements once the other
runs out (unless both happen to end at exactly the same time).

I also briefly considered slicing the array using indices (`lo`, `mid`,
`hi`) into one shared array instead of creating new sub-arrays with
`nums[:mid]` and `nums[mid:]`, to try to save memory. I decided against
implementing that version here because it adds real complexity (keeping
track of index ranges correctly, and needing a temporary buffer for
merging in place) for a problem where clarity was more valuable to me
than shaving constant-factor memory usage — but I describe this
index-based variant more in the "Reflection" section below, since it is
a legitimate improvement in practice.

## 3. Time Complexity

**Time Complexity: O(n log n)**, where `n` is the number of elements in
the array.

### Why

Think of the recursion as a tree. At the top level, I split the array of
size `n` into two halves of size `n/2` each. Each of those splits again
into halves of size `n/4`, and so on, until I reach sub-arrays of size 1.
Since the array size is halved at every level, the recursion tree has
`log₂(n)` levels.

At EVERY level of this tree, the total amount of work done across all
the merge calls at that level is O(n) — because even though there are
more merge calls at deeper levels, each one handles a proportionally
smaller piece, and merging is always linear in the total number of
elements being merged at that level (every element gets looked at and
placed exactly once per level).

So the total work is: (work per level) × (number of levels) =
`O(n) × O(log n)` = **O(n log n)**.

**Space Complexity: O(n)**. Unlike selection sort (which sorts in place,
O(1) extra space), merge sort creates brand new arrays at every merge
step (`merged = []`, plus the `nums[:mid]` and `nums[mid:]` slices). At
any given moment, the total extra memory used across all the arrays
being merged adds up to O(n) (plus O(log n) extra for the recursion call
stack itself, which is dominated by the O(n) from the arrays). This is a
real trade-off compared to the brute-force selection sort, which uses
O(1) extra space but is much slower in time.

## 4. Reflection / Improvement

- Is there a more efficient approach in terms of time? Not
  asymptotically for a comparison-based sort — O(n log n) is the proven
  lower bound for any sorting algorithm that only compares elements
  pairwise (this is a well-known result), so merge sort is already
  optimal in that sense. Algorithms like quicksort also achieve O(n log
  n) on average, but have an O(n²) worst case (e.g., on already-sorted
  or adversarial input), so merge sort's **guaranteed** O(n log n) in all
  cases is actually a point in its favor, not a weakness.
- What about space? Yes, there's a real opportunity here: an
  **index-based, bottom-up (or in-place-merging) version** of merge sort
  can reduce the auxiliary space from O(n) new arrays down to using a
  single reusable temporary buffer array, rather than allocating fresh
  arrays (`nums[:mid]`, `nums[mid:]`, `merged = []`) at every single
  recursive call. That change alone significantly reduces the *constant
  factor* of the space usage (fewer allocations), though the complexity
  class is still technically O(n) since some buffer is still needed.
- Could it become truly O(1) extra space? There does exist an
  "in-place merge sort" that achieves O(1) auxiliary space, but it's
  considerably more complex to implement correctly and, in most
  practical implementations, sacrifices some speed (worse constant
  factors) to achieve that in-place property. For an array that doesn't
  need to be sorted in place or under tight memory constraints, I think
  the straightforward O(n)-space version I wrote is the right trade-off
  between clarity, correctness, and performance.
- If I only cared about raw average-case speed and not worst-case
  guarantees, **quicksort** (with a good pivot strategy) is typically
  faster in practice than merge sort due to better cache locality and
  lower constant factors, despite sharing the same O(n log n) average
  time complexity — but that wasn't the focus of this exercise, which
  was specifically to practice and understand merge sort.
