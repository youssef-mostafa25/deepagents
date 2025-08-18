#!/usr/bin/env python3
"""
test_avocado.py - Comprehensive test suite for avocado.py

This file tests all the functions and classes defined in avocado.py
using pytest framework for thorough validation.
"""

import pytest
import os
import sys
from unittest.mock import patch, mock_open
from io import StringIO

# Add the current directory to Python path to import avocado
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from avocado import (
    Animal, Dog, Cat, 
    get_demo_data, calculate_statistics,
    demonstrate_variables, demonstrate_data_structures,
    demonstrate_control_structures, demonstrate_functions,
    demonstrate_classes, demonstrate_error_handling,
    demonstrate_file_handling, demonstrate_modules,
    demonstrate_advanced_features
)


class TestAnimalClasses:
    """Test cases for Animal, Dog, and Cat classes."""
    
    def test_animal_creation(self):
        """Test Animal class instantiation."""
        animal = Animal("Fluffy", "Generic")
        assert animal.name == "Fluffy"
        assert animal.species == "Generic"
        assert isinstance(animal, Animal)
    
    def test_animal_speak(self):
        """Test Animal speak method."""
        animal = Animal("Buddy", "Generic")
        result = animal.speak()
        assert result == "Buddy makes a sound"
    
    def test_animal_str_representation(self):
        """Test Animal string representation."""
        animal = Animal("Rex", "Dog")
        assert str(animal) == "Rex the Dog"
    
    def test_animal_repr_representation(self):
        """Test Animal repr representation."""
        animal = Animal("Mittens", "Cat")
        assert repr(animal) == "Animal('Mittens', 'Cat')"
    
    def test_dog_creation(self):
        """Test Dog class instantiation."""
        dog = Dog("Buddy", "Labrador")
        assert dog.name == "Buddy"
        assert dog.species == "Dog"
        assert dog.breed == "Labrador"
        assert isinstance(dog, Dog)
        assert isinstance(dog, Animal)  # Test inheritance
    
    def test_dog_speak(self):
        """Test Dog speak method override."""
        dog = Dog("Max", "Poodle")
        result = dog.speak()
        assert result == "Max barks: Woof!"
    
    def test_dog_fetch(self):
        """Test Dog fetch method."""
        dog = Dog("Spot", "Beagle")
        result = dog.fetch()
        assert result == "Spot fetches the ball"
    
    def test_cat_creation(self):
        """Test Cat class instantiation."""
        cat = Cat("Whiskers", "Black")
        assert cat.name == "Whiskers"
        assert cat.species == "Cat"
        assert cat.color == "Black"
        assert isinstance(cat, Cat)
        assert isinstance(cat, Animal)  # Test inheritance
    
    def test_cat_speak(self):
        """Test Cat speak method override."""
        cat = Cat("Fluffy", "White")
        result = cat.speak()
        assert result == "Fluffy meows: Meow!"
    
    def test_cat_purr(self):
        """Test Cat purr method."""
        cat = Cat("Shadow", "Gray")
        result = cat.purr()
        assert result == "Shadow purrs contentedly"
    
    def test_class_variable_tracking(self):
        """Test that class variable tracks animal count."""
        initial_count = Animal.species_count
        Animal("Test1", "TestSpecies1")
        Animal("Test2", "TestSpecies2")
        Dog("Test3", "TestBreed")
        Cat("Test4", "TestColor")
        
        # Should have increased by 4
        assert Animal.species_count == initial_count + 4


class TestUtilityFunctions:
    """Test cases for utility functions."""
    
    def test_get_demo_data(self):
        """Test get_demo_data function."""
        data = get_demo_data()
        
        assert isinstance(data, dict)
        assert 'numbers' in data
        assert 'text' in data
        assert 'count' in data
        assert 'nested' in data
        
        assert data['numbers'] == [1, 2, 3, 4, 5]
        assert data['text'] == 'Hello, Python!'
        assert data['count'] == 42
        assert isinstance(data['nested'], dict)
    
    def test_calculate_statistics_valid_numbers(self):
        """Test calculate_statistics with valid number list."""
        numbers = [1, 2, 3, 4, 5]
        stats = calculate_statistics(numbers)
        
        assert stats['count'] == 5
        assert stats['sum'] == 15
        assert stats['mean'] == 3.0
        assert stats['min'] == 1
        assert stats['max'] == 5
    
    def test_calculate_statistics_empty_list(self):
        """Test calculate_statistics with empty list."""
        stats = calculate_statistics([])
        
        assert stats['count'] == 0
        assert stats['sum'] == 0
        assert stats['mean'] == 0
        assert stats['min'] == 0
        assert stats['max'] == 0
    
    def test_calculate_statistics_single_number(self):
        """Test calculate_statistics with single number."""
        numbers = [42]
        stats = calculate_statistics(numbers)
        
        assert stats['count'] == 1
        assert stats['sum'] == 42
        assert stats['mean'] == 42.0
        assert stats['min'] == 42
        assert stats['max'] == 42
    
    def test_calculate_statistics_floats(self):
        """Test calculate_statistics with float numbers."""
        numbers = [1.5, 2.5, 3.5]
        stats = calculate_statistics(numbers)
        
        assert stats['count'] == 3
        assert stats['sum'] == 7.5
        assert abs(stats['mean'] - 2.5) < 0.0001  # Float precision
        assert stats['min'] == 1.5
        assert stats['max'] == 3.5


class TestDemonstrationFunctions:
    """Test cases for demonstration functions."""
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_demonstrate_variables(self, mock_stdout):
        """Test demonstrate_variables function."""
        demonstrate_variables()
        output = mock_stdout.getvalue()
        
        assert "VARIABLES AND DATA TYPES" in output
        assert "Integer: 42" in output
        assert "Float: 3.14159" in output
        assert "Boolean: True" in output
        assert "None: None" in output
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_demonstrate_data_structures(self, mock_stdout):
        """Test demonstrate_data_structures function."""
        demonstrate_data_structures()
        output = mock_stdout.getvalue()
        
        assert "DATA STRUCTURES" in output
        assert "List:" in output
        assert "Tuple:" in output
        assert "Dictionary:" in output
        assert "Set:" in output
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_demonstrate_control_structures(self, mock_stdout):
        """Test demonstrate_control_structures function."""
        demonstrate_control_structures()
        output = mock_stdout.getvalue()
        
        assert "CONTROL STRUCTURES" in output
        assert "Grade: B" in output
        assert "For loop" in output
        assert "While loop" in output
        assert "Squares:" in output
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_demonstrate_functions(self, mock_stdout):
        """Test demonstrate_functions function."""
        demonstrate_functions()
        output = mock_stdout.getvalue()
        
        assert "FUNCTIONS" in output
        assert "Hello, Python!" in output
        assert "Area" in output
        assert "Sum all:" in output
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_demonstrate_classes(self, mock_stdout):
        """Test demonstrate_classes function."""
        demonstrate_classes()
        output = mock_stdout.getvalue()
        
        assert "CLASSES AND OBJECTS" in output
        assert "barks: Woof!" in output
        assert "meows: Meow!" in output
        assert "fetches the ball" in output
        assert "purrs contentedly" in output
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_demonstrate_error_handling(self, mock_stdout):
        """Test demonstrate_error_handling function."""
        demonstrate_error_handling()
        output = mock_stdout.getvalue()
        
        assert "ERROR HANDLING" in output
        assert "Cannot divide by zero!" in output
        assert "Custom error caught:" in output
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_demonstrate_modules(self, mock_stdout):
        """Test demonstrate_modules function."""
        demonstrate_modules()
        output = mock_stdout.getvalue()
        
        assert "MODULES AND IMPORTS" in output
        assert "Pi:" in output
        assert "Square root" in output
        assert "Random" in output
        assert "Current date" in output
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_demonstrate_advanced_features(self, mock_stdout):
        """Test demonstrate_advanced_features function."""
        with patch('time.sleep'):  # Mock sleep to speed up test
            demonstrate_advanced_features()
        output = mock_stdout.getvalue()
        
        assert "ADVANCED FEATURES" in output
        assert "took" in output and "seconds" in output  # Timer decorator
        assert "Fibonacci sequence" in output
        assert "Entering custom context" in output
        assert "Exiting custom context" in output


class TestFileOperations:
    """Test cases for file operations."""
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=StringIO)
    def test_demonstrate_file_handling_success(self, mock_stdout, mock_file):
        """Test file handling demonstration with successful operations."""
        # Configure the mock to simulate successful file operations
        mock_file.return_value.read.return_value = "Hello, Python!\nThis is a sample file.\nLine 1\nLine 2\nLine 3\n"
        
        demonstrate_file_handling()
        output = mock_stdout.getvalue()
        
        assert "FILE HANDLING" in output
        assert "Successfully wrote" in output or "File content:" in output
    
    @patch('builtins.open', side_effect=IOError("File not found"))
    @patch('sys.stdout', new_callable=StringIO)
    def test_demonstrate_file_handling_error(self, mock_stdout, mock_open):
        """Test file handling demonstration with file errors."""
        demonstrate_file_handling()
        output = mock_stdout.getvalue()
        
        assert "FILE HANDLING" in output
        assert "File error:" in output


class TestIntegration:
    """Integration tests."""
    
    def test_all_classes_work_together(self):
        """Test that all animal classes work together properly."""
        animals = [
            Animal("Generic", "Unknown"),
            Dog("Buddy", "Golden Retriever"),
            Cat("Whiskers", "Orange")
        ]
        
        # Test polymorphism
        sounds = [animal.speak() for animal in animals]
        assert len(sounds) == 3
        assert "makes a sound" in sounds[0]
        assert "barks: Woof!" in sounds[1]
        assert "meows: Meow!" in sounds[2]
        
        # Test specific methods
        assert hasattr(animals[1], 'fetch')
        assert hasattr(animals[2], 'purr')
        assert not hasattr(animals[0], 'fetch')
        assert not hasattr(animals[0], 'purr')
    
    def test_statistics_with_demo_data(self):
        """Test statistics function with demo data."""
        demo_data = get_demo_data()
        numbers = demo_data['numbers']
        stats = calculate_statistics(numbers)
        
        assert stats['count'] == len(numbers)
        assert stats['sum'] == sum(numbers)
        assert stats['mean'] == sum(numbers) / len(numbers)


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_animal_empty_name(self):
        """Test animal with empty name."""
        animal = Animal("", "TestSpecies")
        assert animal.name == ""
        assert animal.species == "TestSpecies"
    
    def test_calculate_statistics_negative_numbers(self):
        """Test statistics with negative numbers."""
        numbers = [-5, -3, -1, 0, 1, 3, 5]
        stats = calculate_statistics(numbers)
        
        assert stats['count'] == 7
        assert stats['sum'] == 0
        assert stats['mean'] == 0
        assert stats['min'] == -5
        assert stats['max'] == 5
    
    def test_calculate_statistics_large_numbers(self):
        """Test statistics with large numbers."""
        numbers = [1e6, 2e6, 3e6]
        stats = calculate_statistics(numbers)
        
        assert stats['count'] == 3
        assert abs(stats['mean'] - 2e6) < 0.001


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "--tb=short"])