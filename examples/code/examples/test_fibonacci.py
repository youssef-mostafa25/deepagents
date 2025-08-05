"""
Comprehensive test suite for the Fibonacci implementation.

This demonstrates the kind of thorough testing the coding agent would create.
"""

import unittest
import sys
from pathlib import Path

# Add the parent directory to the path so we can import example_fibonacci
sys.path.append(str(Path(__file__).parent))
from example_fibonacci import fibonacci, fibonacci_sequence


class TestFibonacci(unittest.TestCase):
    """Test cases for the fibonacci function."""
    
    def test_base_cases(self):
        """Test the base cases F(0) = 0 and F(1) = 1."""
        self.assertEqual(fibonacci(0), 0)
        self.assertEqual(fibonacci(1), 1)
    
    def test_small_values(self):
        """Test small Fibonacci numbers."""
        expected_values = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
        for i, expected in enumerate(expected_values):
            with self.subTest(n=i):
                self.assertEqual(fibonacci(i), expected)
    
    def test_larger_values(self):
        """Test larger Fibonacci numbers."""
        self.assertEqual(fibonacci(20), 6765)
        self.assertEqual(fibonacci(30), 832040)
    
    def test_negative_input(self):
        """Test that negative inputs raise ValueError."""
        with self.assertRaises(ValueError) as context:
            fibonacci(-1)
        self.assertIn("negative", str(context.exception).lower())
        
        with self.assertRaises(ValueError):
            fibonacci(-10)
    
    def test_non_integer_input(self):
        """Test that non-integer inputs raise TypeError."""
        invalid_inputs = [3.14, "5", None, [5], {"n": 5}]
        for invalid_input in invalid_inputs:
            with self.subTest(input=invalid_input):
                with self.assertRaises(TypeError):
                    fibonacci(invalid_input)
    
    def test_type_hints(self):
        """Test that the function returns the correct type."""
        result = fibonacci(5)
        self.assertIsInstance(result, int)


class TestFibonacciSequence(unittest.TestCase):
    """Test cases for the fibonacci_sequence function."""
    
    def test_empty_sequence(self):
        """Test generating an empty sequence."""
        self.assertEqual(fibonacci_sequence(0), [])
    
    def test_single_element(self):
        """Test generating a sequence with one element."""
        self.assertEqual(fibonacci_sequence(1), [0])
    
    def test_small_sequences(self):
        """Test generating small sequences."""
        test_cases = [
            (2, [0, 1]),
            (3, [0, 1, 1]),
            (5, [0, 1, 1, 2, 3]),
            (10, [0, 1, 1, 2, 3, 5, 8, 13, 21, 34])
        ]
        
        for count, expected in test_cases:
            with self.subTest(count=count):
                self.assertEqual(fibonacci_sequence(count), expected)
    
    def test_sequence_consistency(self):
        """Test that sequence matches individual fibonacci calls."""
        for count in [1, 5, 10, 15]:
            with self.subTest(count=count):
                sequence = fibonacci_sequence(count)
                expected = [fibonacci(i) for i in range(count)]
                self.assertEqual(sequence, expected)
    
    def test_negative_count(self):
        """Test that negative count raises ValueError."""
        with self.assertRaises(ValueError) as context:
            fibonacci_sequence(-1)
        self.assertIn("negative", str(context.exception).lower())
    
    def test_non_integer_count(self):
        """Test that non-integer count raises TypeError."""
        invalid_inputs = [3.14, "5", None, [5]]
        for invalid_input in invalid_inputs:
            with self.subTest(input=invalid_input):
                with self.assertRaises(TypeError):
                    fibonacci_sequence(invalid_input)
    
    def test_return_type(self):
        """Test that the function returns a list of integers."""
        result = fibonacci_sequence(5)
        self.assertIsInstance(result, list)
        for item in result:
            self.assertIsInstance(item, int)


class TestFibonacciPerformance(unittest.TestCase):
    """Performance-related tests for Fibonacci functions."""
    
    def test_large_fibonacci_performance(self):
        """Test that large Fibonacci numbers can be calculated efficiently."""
        import time
        
        start_time = time.time()
        result = fibonacci(100)
        end_time = time.time()
        
        # Should complete quickly (under 1 second)
        self.assertLess(end_time - start_time, 1.0)
        
        # Verify the result is correct (100th Fibonacci number)
        self.assertEqual(result, 354224848179261915075)
    
    def test_sequence_performance(self):
        """Test that generating sequences is reasonably efficient."""
        import time
        
        start_time = time.time()
        result = fibonacci_sequence(100)
        end_time = time.time()
        
        # Should complete quickly
        self.assertLess(end_time - start_time, 1.0)
        self.assertEqual(len(result), 100)


class TestFibonacciDocumentation(unittest.TestCase):
    """Test that functions have proper documentation."""
    
    def test_fibonacci_has_docstring(self):
        """Test that fibonacci function has a docstring."""
        self.assertIsNotNone(fibonacci.__doc__)
        self.assertIn("Calculate", fibonacci.__doc__)
        self.assertIn("Args:", fibonacci.__doc__)
        self.assertIn("Returns:", fibonacci.__doc__)
        self.assertIn("Raises:", fibonacci.__doc__)
    
    def test_fibonacci_sequence_has_docstring(self):
        """Test that fibonacci_sequence function has a docstring."""
        self.assertIsNotNone(fibonacci_sequence.__doc__)
        self.assertIn("Generate", fibonacci_sequence.__doc__)
        self.assertIn("Args:", fibonacci_sequence.__doc__)
        self.assertIn("Returns:", fibonacci_sequence.__doc__)


if __name__ == "__main__":
    # Run all tests
    unittest.main(verbosity=2)