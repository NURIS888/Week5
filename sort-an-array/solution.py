# Sort an Array
# https://leetcode.com/problems/sort-an-array/description/

def sort_array(nums: list[int]) -> list[int]:
    """
    Sort an array of integers in ascending order using merge sort.

    Idea:
    Merge sort is a "divide and conquer" algorithm. The insight is that
    merging two ALREADY-SORTED lists into one sorted list is easy and
    fast (just walk both with a pointer each, always taking the smaller
    current element). So instead of trying to sort the whole array in
    one go, I:
      1. Split the array into two halves.
      2. Recursively sort each half (using the exact same function).
      3. Merge the two now-sorted halves together into one sorted array.

    The recursion bottoms out when a sub-array has 0 or 1 elements, since
    that's already "sorted" by definition - nothing to do.

    This is different from an in-place sort like insertion sort or bubble
    sort: merge sort always creates new arrays as it merges pieces back
    together, which is why it costs O(n) extra space (explained more in
    the README's complexity section).
    """
    if len(nums) <= 1:
        return nums

    mid = len(nums) // 2
    left_half = sort_array(nums[:mid])
    right_half = sort_array(nums[mid:])

    return _merge(left_half, right_half)


def _merge(left: list[int], right: list[int]) -> list[int]:
    """
    Merge two already-sorted lists into a single sorted list.
    Same merging idea as in "Merge Two Sorted Lists" from an earlier
    assignment, just operating on Python lists/arrays instead of linked
    list nodes.
    """
    merged = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # Whichever list still has leftover elements is already sorted,
    # so just append the rest directly.
    merged.extend(left[i:])
    merged.extend(right[j:])

    return merged


# ---------- Brute-force version I tried first, kept for comparison ----------

def sort_array_brute_force(nums: list[int]) -> list[int]:
    """
    Simple selection sort: repeatedly find the minimum of the remaining
    unsorted portion and move it to the front. Correct, but O(n^2), and
    was my very first instinct before switching to merge sort. See README.
    """
    nums = nums[:]  # work on a copy, don't mutate caller's list
    n = len(nums)
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if nums[j] < nums[min_index]:
                min_index = j
        nums[i], nums[min_index] = nums[min_index], nums[i]
    return nums


if __name__ == "__main__":
    test_cases = [
        [5, 2, 3, 1],
        [5, 1, 1, 2, 0, 0],
        [],
        [1],
        [2, 1],
        [3, 3, 3, 3],
        [-5, 10, -3, 0, 7, -1],
    ]

    for nums in test_cases:
        result = sort_array(nums[:])  # pass a copy, keep original for display
        expected = sorted(nums)
        status = "OK" if result == expected else "FAIL"
        print(f"{nums} -> {result} (expected {expected}) [{status}]")

        # cross-check against brute force
        bf_result = sort_array_brute_force(nums)
        assert bf_result == expected, "Brute force mismatch!"
