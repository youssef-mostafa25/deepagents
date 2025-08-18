#!/usr/bin/env python3
"""
avocado.py - A comprehensive Python basics demonstration

This file demonstrates all the fundamental concepts of Python programming
including data types, control structures, functions, classes, and more.
"""

import math
import random
import datetime
from typing import List, Dict, Optional, Union
from functools import reduce


# ============================================================================
# 1. VARIABLES AND DATA TYPES
# ============================================================================

def demonstrate_variables():
    """Demonstrate Python's basic data types and variables."""
    print("=== VARIABLES AND DATA TYPES ===")
    
    # Numbers
    integer_num = 42
    float_num = 3.14159
    complex_num = 3 + 4j
    
    # Strings
    single_quoted = 'Hello'
    double_quoted = "World"
    multiline_string = """This is a
    multiline string"""
    formatted_string = f"Integer: {integer_num}, Float: {float_num}"
    
    # Boolean
    is_true = True
    is_false = False
    
    # None type
    nothing = None
    
    print(f"Integer: {integer_num} (type: {type(integer_num)})")
    print(f"Float: {float_num} (type: {type(float_num)})")
    print(f"Complex: {complex_num} (type: {type(complex_num)})")
    print(f"String: {single_quoted} {double_quoted} (type: {type(single_quoted)})")
    print(f"Boolean: {is_true} (type: {type(is_true)})")
    print(f"None: {nothing} (type: {type(nothing)})")
    print(f"Formatted: {formatted_string}")
    print()


# ============================================================================
# 2. DATA STRUCTURES
# ============================================================================

def demonstrate_data_structures():
    """Demonstrate Python's built-in data structures."""
    print("=== DATA STRUCTURES ===")
    
    # Lists (mutable, ordered)
    fruits = ['apple', 'banana', 'cherry']
    numbers = [1, 2, 3, 4, 5]
    mixed_list = [1, 'hello', 3.14, True]
    
    # Tuples (immutable, ordered)
    coordinates = (10, 20)
    rgb_color = (255, 128, 0)
    
    # Dictionaries (mutable, key-value pairs)
    person = {
        'name': 'Alice',
        'age': 30,
        'city': 'New York',
        'hobbies': ['reading', 'swimming']
    }
    
    # Sets (mutable, unordered, unique elements)
    unique_numbers = {1, 2, 3, 4, 5, 5, 5}  # duplicates will be removed
    vowels = set('aeiou')
    
    print(f"List: {fruits}")
    print(f"Tuple: {coordinates}")
    print(f"Dictionary: {person}")
    print(f"Set: {unique_numbers}")
    print(f"Vowels set: {vowels}")
    
    # List operations
    fruits.append('date')
    fruits.extend(['elderberry', 'fig'])
    print(f"Modified list: {fruits}")
    print(f"List slicing [1:3]: {fruits[1:3]}")
    
    # Dictionary operations
    person['email'] = 'alice@example.com'
    age = person.get('age', 0)
    print(f"Person's age: {age}")
    print()


# ============================================================================
# 3. CONTROL STRUCTURES
# ============================================================================

def demonstrate_control_structures():
    """Demonstrate if/elif/else, loops, and control flow."""
    print("=== CONTROL STRUCTURES ===")
    
    # If/elif/else statements
    score = 85
    if score >= 90:
        grade = 'A'
    elif score >= 80:
        grade = 'B'
    elif score >= 70:
        grade = 'C'
    else:
        grade = 'F'
    
    print(f"Score: {score}, Grade: {grade}")
    
    # For loops
    print("For loop with range:")
    for i in range(5):
        print(f"  {i}", end=" ")
    print()
    
    print("For loop with list:")
    colors = ['red', 'green', 'blue']
    for color in colors:
        print(f"  Color: {color}")
    
    print("For loop with enumerate:")
    for index, color in enumerate(colors):
        print(f"  {index}: {color}")
    
    # While loop
    print("While loop:")
    count = 0
    while count < 3:
        print(f"  Count: {count}")
        count += 1
    
    # List comprehensions
    squares = [x**2 for x in range(5)]
    even_squares = [x**2 for x in range(10) if x % 2 == 0]
    print(f"Squares: {squares}")
    print(f"Even squares: {even_squares}")
    
    # Dictionary comprehension
    square_dict = {x: x**2 for x in range(5)}
    print(f"Square dictionary: {square_dict}")
    print()


# ============================================================================
# 4. FUNCTIONS
# ============================================================================

def demonstrate_functions():
    """Demonstrate function definitions, parameters, and return values."""
    print("=== FUNCTIONS ===")
    
    # Basic function
    def greet(name):
        return f"Hello, {name}!"
    
    # Function with default parameters
    def calculate_area(length, width=1):
        return length * width
    
    # Function with variable arguments
    def sum_all(*args):
        return sum(args)
    
    # Function with keyword arguments
    def create_profile(**kwargs):
        return kwargs
    
    # Function with type hints
    def multiply(a: int, b: int) -> int:
        return a * b
    
    # Lambda functions
    square = lambda x: x**2
    add = lambda x, y: x + y
    
    # Higher-order functions
    numbers = [1, 2, 3, 4, 5]
    squared_numbers = list(map(square, numbers))
    even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
    sum_of_numbers = reduce(add, numbers)
    
    print(f"Greeting: {greet('Python')}")
    print(f"Area (10, 5): {calculate_area(10, 5)}")
    print(f"Area (10): {calculate_area(10)}")  # uses default width=1
    print(f"Sum all: {sum_all(1, 2, 3, 4, 5)}")
    print(f"Profile: {create_profile(name='Bob', age=25, city='Boston')}")
    print(f"Multiply: {multiply(6, 7)}")
    print(f"Squared numbers: {squared_numbers}")
    print(f"Even numbers: {even_numbers}")
    print(f"Sum using reduce: {sum_of_numbers}")
    print()


# ============================================================================
# 5. CLASSES AND OBJECTS
# ============================================================================

class Animal:
    """Base class demonstrating basic OOP concepts."""
    
    # Class variable
    species_count = 0
    
    def __init__(self, name: str, species: str):
        """Initialize an Animal instance."""
        self.name = name
        self.species = species
        Animal.species_count += 1
    
    def speak(self) -> str:
        """Make the animal speak."""
        return f"{self.name} makes a sound"
    
    def __str__(self) -> str:
        """String representation of the animal."""
        return f"{self.name} the {self.species}"
    
    def __repr__(self) -> str:
        """Developer representation of the animal."""
        return f"Animal('{self.name}', '{self.species}')"


class Dog(Animal):
    """Dog class demonstrating inheritance."""
    
    def __init__(self, name: str, breed: str):
        """Initialize a Dog instance."""
        super().__init__(name, "Dog")
        self.breed = breed
    
    def speak(self) -> str:
        """Override the speak method."""
        return f"{self.name} barks: Woof!"
    
    def fetch(self) -> str:
        """Dog-specific method."""
        return f"{self.name} fetches the ball"


class Cat(Animal):
    """Cat class demonstrating inheritance."""
    
    def __init__(self, name: str, color: str):
        """Initialize a Cat instance."""
        super().__init__(name, "Cat")
        self.color = color
    
    def speak(self) -> str:
        """Override the speak method."""
        return f"{self.name} meows: Meow!"
    
    def purr(self) -> str:
        """Cat-specific method."""
        return f"{self.name} purrs contentedly"


def demonstrate_classes():
    """Demonstrate classes, objects, and inheritance."""
    print("=== CLASSES AND OBJECTS ===")
    
    # Create instances
    generic_animal = Animal("Generic", "Unknown")
    dog = Dog("Buddy", "Golden Retriever")
    cat = Cat("Whiskers", "Orange")
    
    # Demonstrate polymorphism
    animals = [generic_animal, dog, cat]
    
    for animal in animals:
        print(f"Animal: {animal}")
        print(f"  {animal.speak()}")
        
        # Check for specific methods
        if hasattr(animal, 'fetch'):
            print(f"  {animal.fetch()}")
        if hasattr(animal, 'purr'):
            print(f"  {animal.purr()}")
    
    print(f"Total animals created: {Animal.species_count}")
    print()


# ============================================================================
# 6. ERROR HANDLING
# ============================================================================

def demonstrate_error_handling():
    """Demonstrate exception handling."""
    print("=== ERROR HANDLING ===")
    
    # Try/except/else/finally
    def safe_divide(a, b):
        try:
            result = a / b
        except ZeroDivisionError:
            print("Error: Cannot divide by zero!")
            return None
        except TypeError:
            print("Error: Invalid types for division!")
            return None
        else:
            print(f"Division successful: {a} / {b} = {result}")
            return result
        finally:
            print("Division operation completed")
    
    # Test error handling
    safe_divide(10, 2)
    safe_divide(10, 0)
    safe_divide("10", 2)
    
    # Custom exceptions
    class CustomError(Exception):
        """Custom exception class."""
        def __init__(self, message):
            self.message = message
            super().__init__(self.message)
    
    def check_positive_number(num):
        if num < 0:
            raise CustomError(f"Number must be positive, got {num}")
        return num
    
    try:
        check_positive_number(5)
        check_positive_number(-3)
    except CustomError as e:
        print(f"Custom error caught: {e.message}")
    
    print()


# ============================================================================
# 7. FILE HANDLING
# ============================================================================

def demonstrate_file_handling():
    """Demonstrate file operations."""
    print("=== FILE HANDLING ===")
    
    filename = "sample.txt"
    
    # Writing to a file
    try:
        with open(filename, 'w') as file:
            file.write("Hello, Python!\n")
            file.write("This is a sample file.\n")
            file.writelines(["Line 1\n", "Line 2\n", "Line 3\n"])
        print(f"Successfully wrote to {filename}")
        
        # Reading from a file
        with open(filename, 'r') as file:
            content = file.read()
            print("File content:")
            print(content)
        
        # Reading line by line
        with open(filename, 'r') as file:
            print("Reading line by line:")
            for line_num, line in enumerate(file, 1):
                print(f"  Line {line_num}: {line.strip()}")
    
    except IOError as e:
        print(f"File error: {e}")
    
    print()


# ============================================================================
# 8. MODULES AND IMPORTS
# ============================================================================

def demonstrate_modules():
    """Demonstrate module usage and imports."""
    print("=== MODULES AND IMPORTS ===")
    
    # Using math module
    print(f"Pi: {math.pi}")
    print(f"Square root of 16: {math.sqrt(16)}")
    print(f"Factorial of 5: {math.factorial(5)}")
    
    # Using random module
    print(f"Random integer (1-10): {random.randint(1, 10)}")
    print(f"Random choice from list: {random.choice(['apple', 'banana', 'cherry'])}")
    
    # Using datetime module
    now = datetime.datetime.now()
    print(f"Current date and time: {now}")
    print(f"Formatted date: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    
    print()


# ============================================================================
# 9. ADVANCED FEATURES
# ============================================================================

def demonstrate_advanced_features():
    """Demonstrate some advanced Python features."""
    print("=== ADVANCED FEATURES ===")
    
    # Decorators
    def timer(func):
        """Simple timer decorator."""
        import time
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print(f"{func.__name__} took {end - start:.4f} seconds")
            return result
        return wrapper
    
    @timer
    def slow_function():
        """A function that takes some time."""
        import time
        time.sleep(0.1)
        return "Done!"
    
    result = slow_function()
    print(f"Result: {result}")
    
    # Generators
    def fibonacci_generator(n):
        """Generate fibonacci sequence up to n terms."""
        a, b = 0, 1
        for _ in range(n):
            yield a
            a, b = b, a + b
    
    print("Fibonacci sequence (first 10 numbers):")
    fib_gen = fibonacci_generator(10)
    print(list(fib_gen))
    
    # Context managers
    class CustomContext:
        def __enter__(self):
            print("Entering custom context")
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            print("Exiting custom context")
            return False
    
    with CustomContext():
        print("Inside custom context")
    
    print()


# ============================================================================
# 10. MAIN EXECUTION
# ============================================================================

def main():
    """Main function to run all demonstrations."""
    print("🥑 PYTHON BASICS DEMONSTRATION 🥑")
    print("=" * 50)
    
    demonstrate_variables()
    demonstrate_data_structures()
    demonstrate_control_structures()
    demonstrate_functions()
    demonstrate_classes()
    demonstrate_error_handling()
    demonstrate_file_handling()
    demonstrate_modules()
    demonstrate_advanced_features()
    
    print("🎉 All demonstrations completed successfully!")


# ============================================================================
# UTILITY FUNCTIONS FOR TESTING
# ============================================================================

def get_demo_data() -> Dict[str, Union[int, str, List]]:
    """Return sample data for testing."""
    return {
        'numbers': [1, 2, 3, 4, 5],
        'text': 'Hello, Python!',
        'count': 42,
        'nested': {'key': 'value', 'items': [1, 2, 3]}
    }


def calculate_statistics(numbers: List[Union[int, float]]) -> Dict[str, float]:
    """Calculate basic statistics for a list of numbers."""
    if not numbers:
        return {'count': 0, 'sum': 0, 'mean': 0, 'min': 0, 'max': 0}
    
    return {
        'count': len(numbers),
        'sum': sum(numbers),
        'mean': sum(numbers) / len(numbers),
        'min': min(numbers),
        'max': max(numbers)
    }


if __name__ == "__main__":
    main()