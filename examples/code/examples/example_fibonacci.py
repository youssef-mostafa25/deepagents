"""
Example: Fibonacci Implementation with Tests

This file demonstrates how the coding agent would implement a fibonacci function
with proper error handling, documentation, and comprehensive tests.
"""

def fibonacci(n: int) -> int:
    """
    Calculate the nth Fibonacci number.
    
    The Fibonacci sequence is defined as:
    F(0) = 0, F(1) = 1, F(n) = F(n-1) + F(n-2) for n > 1
    
    Args:
        n: The position in the Fibonacci sequence (non-negative integer)
        
    Returns:
        The nth Fibonacci number
        
    Raises:
        ValueError: If n is negative
        TypeError: If n is not an integer
        
    Examples:
        >>> fibonacci(0)
        0
        >>> fibonacci(1)
        1
        >>> fibonacci(5)
        5
        >>> fibonacci(10)
        55
    """
    if not isinstance(n, int):
        raise TypeError(f"Expected integer, got {type(n).__name__}")
    
    if n < 0:
        raise ValueError("Fibonacci is not defined for negative numbers")
    
    if n <= 1:
        return n
    
    # Use iterative approach for better performance
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    
    return b


def fibonacci_sequence(count: int) -> list[int]:
    """
    Generate a list of the first 'count' Fibonacci numbers.
    
    Args:
        count: Number of Fibonacci numbers to generate (non-negative integer)
        
    Returns:
        List of the first 'count' Fibonacci numbers
        
    Raises:
        ValueError: If count is negative
        TypeError: If count is not an integer
        
    Examples:
        >>> fibonacci_sequence(5)
        [0, 1, 1, 2, 3]
        >>> fibonacci_sequence(0)
        []
    """
    if not isinstance(count, int):
        raise TypeError(f"Expected integer, got {type(count).__name__}")
    
    if count < 0:
        raise ValueError("Count must be non-negative")
    
    return [fibonacci(i) for i in range(count)]


if __name__ == "__main__":
    # Demonstrate the functions
    print("Fibonacci Examples:")
    print(f"fibonacci(0) = {fibonacci(0)}")
    print(f"fibonacci(1) = {fibonacci(1)}")
    print(f"fibonacci(10) = {fibonacci(10)}")
    print(f"fibonacci_sequence(10) = {fibonacci_sequence(10)}")