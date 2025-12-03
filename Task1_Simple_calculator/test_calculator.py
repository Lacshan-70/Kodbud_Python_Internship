"""
================================================================================
                    SIMPLE CALCULATOR - TEST CASES
================================================================================

TEST SUITE DESCRIPTION:
    This test module validates all functionalities of the Simple Calculator
    program including input validation, calculation operations, error handling,
    and user interactions.

TEST COVERAGE:
    1. Choice validation (valid and invalid inputs)
    2. Arithmetic operations (Addition, Subtraction, Multiplication, Division)
    3. Division by zero error handling
    4. Numeric input validation
    5. Continue/Exit functionality

DEVELOPED BY: Lacshan Shakthivel
DATE: December 3, 2025

================================================================================
"""

import unittest
from io import StringIO
import sys
import os

# Get the directory of the current script and add it to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from calculator_functions import validate_choice, perform_calculation


class TestValidateChoice(unittest.TestCase):
    """
    Test cases for the validate_choice() function.
    Validates input choice validation for options 1-5.
    """
    
    def test_valid_choice_1(self):
        """Test valid choice: 1 (Addition)"""
        self.assertTrue(validate_choice('1'))
    
    def test_valid_choice_2(self):
        """Test valid choice: 2 (Subtraction)"""
        self.assertTrue(validate_choice('2'))
    
    def test_valid_choice_3(self):
        """Test valid choice: 3 (Multiplication)"""
        self.assertTrue(validate_choice('3'))
    
    def test_valid_choice_4(self):
        """Test valid choice: 4 (Division)"""
        self.assertTrue(validate_choice('4'))
    
    def test_valid_choice_5(self):
        """Test valid choice: 5 (Exit)"""
        self.assertTrue(validate_choice('5'))
    
    def test_invalid_choice_zero(self):
        """Test invalid choice: 0 (out of range)"""
        self.assertFalse(validate_choice('0'))
    
    def test_invalid_choice_six(self):
        """Test invalid choice: 6 (out of range)"""
        self.assertFalse(validate_choice('6'))
    
    def test_invalid_choice_negative(self):
        """Test invalid choice: -1 (negative number)"""
        self.assertFalse(validate_choice('-1'))
    
    def test_invalid_choice_string(self):
        """Test invalid choice: 'abc' (non-numeric string)"""
        self.assertFalse(validate_choice('abc'))
    
    def test_invalid_choice_empty(self):
        """Test invalid choice: empty string"""
        self.assertFalse(validate_choice(''))
    
    def test_invalid_choice_float(self):
        """Test invalid choice: '1.5' (float as string)"""
        self.assertFalse(validate_choice('1.5'))


class TestArithmeticOperations(unittest.TestCase):
    """
    Test cases for the perform_calculation() function.
    Validates all arithmetic operations.
    """
    
    def setUp(self):
        """Capture print output for each test"""
        self.held_output = StringIO()
        sys.stdout = self.held_output
    
    def tearDown(self):
        """Restore normal output"""
        sys.stdout = sys.__stdout__
    
    def test_addition_positive_numbers(self):
        """Test Addition: 5 + 3 = 8"""
        result = perform_calculation('1', 5, 3)
        self.assertTrue(result)
        self.assertIn('Result: 8', self.held_output.getvalue())
    
    def test_addition_negative_numbers(self):
        """Test Addition: -5 + 3 = -2"""
        result = perform_calculation('1', -5, 3)
        self.assertTrue(result)
        self.assertIn('Result: -2', self.held_output.getvalue())
    
    def test_addition_zero(self):
        """Test Addition: 0 + 0 = 0"""
        result = perform_calculation('1', 0, 0)
        self.assertTrue(result)
        self.assertIn('Result: 0', self.held_output.getvalue())
    
    def test_addition_decimals(self):
        """Test Addition: 2.5 + 1.5 = 4.0"""
        result = perform_calculation('1', 2.5, 1.5)
        self.assertTrue(result)
        self.assertIn('Result: 4.0', self.held_output.getvalue())
    
    def test_subtraction_positive_numbers(self):
        """Test Subtraction: 10 - 4 = 6"""
        result = perform_calculation('2', 10, 4)
        self.assertTrue(result)
        self.assertIn('Result: 6', self.held_output.getvalue())
    
    def test_subtraction_negative_result(self):
        """Test Subtraction: 5 - 10 = -5"""
        result = perform_calculation('2', 5, 10)
        self.assertTrue(result)
        self.assertIn('Result: -5', self.held_output.getvalue())
    
    def test_subtraction_negative_numbers(self):
        """Test Subtraction: -5 - (-3) = -2"""
        result = perform_calculation('2', -5, -3)
        self.assertTrue(result)
        self.assertIn('Result: -2', self.held_output.getvalue())
    
    def test_multiplication_positive_numbers(self):
        """Test Multiplication: 6 * 4 = 24"""
        result = perform_calculation('3', 6, 4)
        self.assertTrue(result)
        self.assertIn('Result: 24', self.held_output.getvalue())
    
    def test_multiplication_by_zero(self):
        """Test Multiplication: 5 * 0 = 0"""
        result = perform_calculation('3', 5, 0)
        self.assertTrue(result)
        self.assertIn('Result: 0', self.held_output.getvalue())
    
    def test_multiplication_negative_numbers(self):
        """Test Multiplication: -3 * 4 = -12"""
        result = perform_calculation('3', -3, 4)
        self.assertTrue(result)
        self.assertIn('Result: -12', self.held_output.getvalue())
    
    def test_multiplication_decimals(self):
        """Test Multiplication: 2.5 * 4 = 10.0"""
        result = perform_calculation('3', 2.5, 4)
        self.assertTrue(result)
        self.assertIn('Result: 10.0', self.held_output.getvalue())
    
    def test_division_positive_numbers(self):
        """Test Division: 20 / 4 = 5.0"""
        result = perform_calculation('4', 20, 4)
        self.assertTrue(result)
        self.assertIn('Result: 5.0', self.held_output.getvalue())
    
    def test_division_by_zero(self):
        """Test Division by zero error handling"""
        result = perform_calculation('4', 10, 0)
        self.assertFalse(result)
        self.assertIn('Cannot divide by zero!', self.held_output.getvalue())
    
    def test_division_negative_numbers(self):
        """Test Division: -20 / 4 = -5.0"""
        result = perform_calculation('4', -20, 4)
        self.assertTrue(result)
        self.assertIn('Result: -5.0', self.held_output.getvalue())
    
    def test_division_decimals(self):
        """Test Division: 7.5 / 2.5 = 3.0"""
        result = perform_calculation('4', 7.5, 2.5)
        self.assertTrue(result)
        self.assertIn('Result: 3.0', self.held_output.getvalue())
    
    def test_division_result_with_decimals(self):
        """Test Division: 10 / 3 = 3.333..."""
        result = perform_calculation('4', 10, 3)
        self.assertTrue(result)
        output = self.held_output.getvalue()
        self.assertIn('Result:', output)


class TestEdgeCases(unittest.TestCase):
    """
    Test cases for edge cases and boundary conditions.
    """
    
    def setUp(self):
        """Capture print output for each test"""
        self.held_output = StringIO()
        sys.stdout = self.held_output
    
    def tearDown(self):
        """Restore normal output"""
        sys.stdout = sys.__stdout__
    
    def test_invalid_operation_choice(self):
        """Test invalid operation choice handling"""
        result = perform_calculation('9', 5, 3)
        self.assertFalse(result)
        self.assertIn('Invalid choice!', self.held_output.getvalue())
    
    def test_large_numbers_addition(self):
        """Test Addition with large numbers"""
        result = perform_calculation('1', 1000000, 2000000)
        self.assertTrue(result)
        self.assertIn('Result: 3000000', self.held_output.getvalue())
    
    def test_very_small_decimals(self):
        """Test Division with very small decimal results"""
        result = perform_calculation('4', 1, 1000)
        self.assertTrue(result)
        output = self.held_output.getvalue()
        self.assertIn('Result: 0.001', output)


class TestIntegration(unittest.TestCase):
    """
    Integration tests for multiple operations.
    """
    
    def setUp(self):
        """Capture print output for each test"""
        self.held_output = StringIO()
        sys.stdout = self.held_output
    
    def tearDown(self):
        """Restore normal output"""
        sys.stdout = sys.__stdout__
    
    def test_multiple_operations_sequence(self):
        """Test a sequence of different operations"""
        # Test: 10 + 5 = 15
        result1 = perform_calculation('1', 10, 5)
        self.assertTrue(result1)
        
        # Test: 20 - 7 = 13
        result2 = perform_calculation('2', 20, 7)
        self.assertTrue(result2)
        
        # Test: 4 * 5 = 20
        result3 = perform_calculation('3', 4, 5)
        self.assertTrue(result3)
        
        # Test: 100 / 4 = 25.0
        result4 = perform_calculation('4', 100, 4)
        self.assertTrue(result4)
    
    def test_mixed_positive_negative_operations(self):
        """Test operations with mixed positive and negative numbers"""
        # Test: -5 + 10 = 5
        result1 = perform_calculation('1', -5, 10)
        self.assertTrue(result1)
        
        # Test: -20 * -2 = 40
        result2 = perform_calculation('3', -20, -2)
        self.assertTrue(result2)


def run_test_summary():
    """
    Run all tests and display a summary report.
    """
    print("\n" + "="*80)
    print("RUNNING CALCULATOR TEST SUITE")
    print("="*80 + "\n")
    
    # Create a test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestValidateChoice))
    suite.addTests(loader.loadTestsFromTestCase(TestArithmeticOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Tests Run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*80 + "\n")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_test_summary()
    sys.exit(0 if success else 1)
