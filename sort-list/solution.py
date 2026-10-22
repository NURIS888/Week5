# Sort List
# https://leetcode.com/problems/sort-list/description/

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def sort_list(head: ListNode) -> ListNode:
    """
    Sort a singly linked list in ascending order, using merge sort.

    Idea:
    Same divide-and-conquer idea as sorting an array with merge sort:
    split the list into two halves, recursively sort each half, then
    merge the two sorted halves back into one sorted list.

    The tricky part compared to arrays is SPLITTING. With an array I can
    just slice `nums[:mid]` and `nums[mid:]` directly because I know the
    length and can index into it instantly. A singly linked list has no
    index access and I don't know its length up front, so I can't slice
    it the same way.

    To find the middle of a linked list, I use the classic slow/fast
    pointer trick (the same one used for cycle detection in an earlier
    assignment): `slow` moves 1 node at a time, `fast` moves 2 nodes at a
    time. When `fast` reaches the end, `slow` is sitting at the middle.
    I then cut the list into two halves right there (`prev.next = None`,
    where `prev` is the node right before `slow`).

    Steps:
    1. Base case: if `head` is None or `head.next` is None (0 or 1 node),
       the list is already "sorted" - return it as-is.
    2. Find the middle using slow/fast pointers, and physically split the
       list into `left` (head .. node before slow) and `right` (slow ..
       end) by cutting the `.next` link.
    3. Recursively sort `left` and recursively sort `right`.
    4. Merge the two sorted linked lists together (identical merging
       logic to "Merge Two Sorted Lists" from an earlier assignment) and
       return the merged head.
    """
    if head is None or head.next is None:
        return head

    left, right = _split_in_half(head)

    sorted_left = sort_list(left)
    sorted_right = sort_list(right)

    return _merge(sorted_left, sorted_right)


def _split_in_half(head: ListNode) -> tuple[ListNode, ListNode]:
    """
    Split a linked list of 2+ nodes into two halves using slow/fast
    pointers, and return (left_head, right_head).
    """
    slow = head
    fast = head
    prev = None  # will end up being the node right before `slow`

    while fast is not None and fast.next is not None:
        prev = slow
        slow = slow.next
        fast = fast.next.next

    # Cut the link: everything before `slow` becomes the left half,
    # everything from `slow` onward becomes the right half.
    prev.next = None

    return head, slow


def _merge(list1: ListNode, list2: ListNode) -> ListNode:
    """
    Merge two sorted linked lists into one sorted linked list.
    Identical technique to the "Merge Two Sorted Lists" assignment:
    re-link existing nodes using a dummy head, instead of creating new
    nodes for values.
    """
    dummy = ListNode(-1)
    tail = dummy

    while list1 is not None and list2 is not None:
        if list1.val <= list2.val:
            tail.next = list1
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next
        tail = tail.next

    tail.next = list1 if list1 is not None else list2

    return dummy.next


# ---------- Brute-force version I tried first, kept for comparison ----------

def sort_list_brute_force(head: ListNode) -> ListNode:
    """
    Simplest approach: dump every node's value into a Python list, sort
    that list with the built-in sort, then rebuild/overwrite the linked
    list's values in sorted order. Correct and easy, but doesn't really
    engage with the linked-list structure, and relies on Python's
    built-in sort instead of implementing the sorting logic myself. Kept
    here only to cross-check correctness. See README for why this isn't
    my main solution.
    """
    if head is None:
        return None

    values = []
    node = head
    while node is not None:
        values.append(node.val)
        node = node.next

    values.sort()

    node = head
    i = 0
    while node is not None:
        node.val = values[i]
        i += 1
        node = node.next

    return head


# ---------- Helper functions used only for manual testing ----------

def build_linked_list(values):
    dummy = ListNode(-1)
    tail = dummy
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def linked_list_to_list(head):
    result = []
    while head is not None:
        result.append(head.val)
        head = head.next
    return result


if __name__ == "__main__":
    test_cases = [
        [4, 2, 1, 3],
        [-1, 5, 3, 4, 0],
        [],
        [1],
        [2, 1],
        [3, 3, 3, 3],
    ]

    for values in test_cases:
        head = build_linked_list(values)
        result = sort_list(head)
        expected = sorted(values)
        actual = linked_list_to_list(result)
        status = "OK" if actual == expected else "FAIL"
        print(f"{values} -> {actual} (expected {expected}) [{status}]")

        # cross-check against brute force
        head_bf = build_linked_list(values)
        result_bf = sort_list_brute_force(head_bf)
        assert linked_list_to_list(result_bf) == expected, "Brute force mismatch!"
