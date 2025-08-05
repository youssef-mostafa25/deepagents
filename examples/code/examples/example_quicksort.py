"""
Example: Quicksort Implementation with Debugging Demo

This file demonstrates how the coding agent would debug and fix a quicksort implementation.
Shows the original buggy version and the corrected version.
"""

from typing import List, TypeVar

T = TypeVar('T')


def quicksort_buggy(arr: List[T]) -> List[T]:
    """
    BUGGY VERSION: This implementation has a bug with duplicate elements.
    
    This version demonstrates the kind of bug the debugger sub-agent would identify and fix.
    
    Args:
        arr: List of comparable elements to sort
        
    Returns:
        Sorted list (but may lose duplicate elements due to bug)
    """
    if len(arr) <= 1:
        return arr
    
    pivot = arr[0]
    less = [x for x in arr[1:] if x < pivot]
    greater = [x for x in arr[1:] if x > pivot]  # BUG: Missing equal elements!
    
    return quicksort_buggy(less) + [pivot] + quicksort_buggy(greater)


def quicksort(arr: List[T]) -> List[T]:
    """
    FIXED VERSION: Corrected quicksort implementation.
    
    Implements the quicksort algorithm with proper handling of duplicate elements.
    Uses the first element as pivot and partitions the array into three parts:
    elements less than pivot, equal to pivot, and greater than pivot.
    
    Args:
        arr: List of comparable elements to sort
        
    Returns:
        New sorted list (original list is not modified)
        
    Raises:
        TypeError: If the list contains elements that cannot be compared
        
    Time Complexity: O(n log n) average case, O(n²) worst case
    Space Complexity: O(log n) due to recursion stack
    
    Examples:
        >>> quicksort([3, 6, 8, 10, 1, 2, 1])
        [1, 1, 2, 3, 6, 8, 10]
        >>> quicksort([])
        []
        >>> quicksort([42])
        [42]
        >>> quicksort(['banana', 'apple', 'cherry'])
        ['apple', 'banana', 'cherry']
    """
    if len(arr) <= 1:
        return arr
    
    pivot = arr[0]
    less = [x for x in arr[1:] if x < pivot]
    equal = [x for x in arr if x == pivot]  # FIX: Include all equal elements
    greater = [x for x in arr[1:] if x > pivot]
    
    return quicksort(less) + equal + quicksort(greater)


def quicksort_inplace(arr: List[T], low: int = 0, high: int = None) -> None:
    """
    In-place quicksort implementation for better space efficiency.
    
    This version modifies the original array instead of creating new arrays,
    providing better space complexity.
    
    Args:
        arr: List to sort (modified in-place)
        low: Starting index of the portion to sort
        high: Ending index of the portion to sort (exclusive)
        
    Time Complexity: O(n log n) average case, O(n²) worst case
    Space Complexity: O(log n) due to recursion stack
    
    Examples:
        >>> arr = [3, 6, 8, 10, 1, 2, 1]
        >>> quicksort_inplace(arr)
        >>> arr
        [1, 1, 2, 3, 6, 8, 10]
    """
    if high is None:
        high = len(arr)
    
    if low < high - 1:
        pivot_index = _partition(arr, low, high)
        quicksort_inplace(arr, low, pivot_index)
        quicksort_inplace(arr, pivot_index + 1, high)


def _partition(arr: List[T], low: int, high: int) -> int:
    """
    Partition helper function for in-place quicksort.
    
    Rearranges the array so that elements less than the pivot come before it,
    and elements greater than the pivot come after it.
    
    Args:
        arr: Array to partition
        low: Start index
        high: End index (exclusive)
        
    Returns:
        Index of the pivot after partitioning
    """
    pivot = arr[low]
    i = low + 1
    j = high - 1
    
    while True:
        # Find element greater than or equal to pivot from left
        while i <= j and arr[i] < pivot:
            i += 1
        
        # Find element less than or equal to pivot from right
        while i <= j and arr[j] > pivot:
            j -= 1
        
        if i <= j:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
            j -= 1
        else:
            break
    
    # Place pivot in correct position
    arr[low], arr[j] = arr[j], arr[low]
    return j


def demonstrate_bug():
    """
    Demonstrate the bug in the original implementation.
    
    This function shows how the buggy version loses duplicate elements,
    which the debugger sub-agent would identify.
    """
    test_array = [3, 6, 8, 10, 1, 2, 1]
    print("Original array:", test_array)
    
    print("\nBuggy quicksort result:")
    buggy_result = quicksort_buggy(test_array.copy())
    print("Result:", buggy_result)
    print("Length:", len(buggy_result), "(should be 7)")
    print("Missing elements: The duplicate '1' is lost!")
    
    print("\nFixed quicksort result:")
    fixed_result = quicksort(test_array.copy())
    print("Result:", fixed_result)
    print("Length:", len(fixed_result), "(correct)")
    
    print("\nIn-place quicksort result:")
    inplace_array = test_array.copy()
    quicksort_inplace(inplace_array)
    print("Result:", inplace_array)


if __name__ == "__main__":
    demonstrate_bug()