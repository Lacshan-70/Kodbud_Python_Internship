"""
================================================================================
                NUMBER GUESSING GAME - TEST CASES
================================================================================

TEST SUITE DESCRIPTION:
    This test module validates all functionalities of the Number Guessing Game
    including input validation, guess comparison, win conditions, and edge cases.

TEST COVERAGE:
    1. Input validation (valid and invalid inputs)
    2. Range validation (1-100 boundaries)
    3. Guess comparison logic (too low, too high, correct)
    4. Win condition checking
    5. Edge cases and boundary conditions

DEVELOPED BY: Lacshan Shakthivel
DATE: December 3, 2025

================================================================================
"""

import unittest
import sys
import os

# Get the directory of the current script and add it to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from guessing_game_logic import validate_guess, compare_guess, check_win_condition


class TestValidateGuess(unittest.TestCase):
    """
    Test cases for the validate_guess() function.
    Validates input validation for guesses.
    """
    
    def test_valid_guess_single_digit(self):
        """Test valid single digit guess: '5'"""
        is_valid, guess = validate_guess('5')
        self.assertTrue(is_valid)
        self.assertEqual(guess, 5)
    
    def test_valid_guess_two_digits(self):
        """Test valid two digit guess: '50'"""
        is_valid, guess = validate_guess('50')
        self.assertTrue(is_valid)
        self.assertEqual(guess, 50)
    
    def test_valid_guess_three_digits(self):
        """Test valid three digit guess: '100'"""
        is_valid, guess = validate_guess('100')
        self.assertTrue(is_valid)
        self.assertEqual(guess, 100)
    
    def test_valid_guess_minimum(self):
        """Test valid minimum guess: '1'"""
        is_valid, guess = validate_guess('1')
        self.assertTrue(is_valid)
        self.assertEqual(guess, 1)
    
    def test_valid_guess_maximum(self):
        """Test valid maximum guess: '100'"""
        is_valid, guess = validate_guess('100')
        self.assertTrue(is_valid)
        self.assertEqual(guess, 100)
    
    def test_invalid_guess_negative(self):
        """Test invalid guess: negative number"""
        is_valid, guess = validate_guess('-5')
        self.assertFalse(is_valid)
        self.assertIsNone(guess)
    
    def test_invalid_guess_zero(self):
        """Test invalid guess: zero (outside range 1-100)"""
        is_valid, guess = validate_guess('0')
        self.assertFalse(is_valid)
        self.assertIsNone(guess)
    
    def test_invalid_guess_above_max(self):
        """Test invalid guess: 101 (above max range)"""
        is_valid, guess = validate_guess('101')
        self.assertFalse(is_valid)
        self.assertIsNone(guess)
    
    def test_invalid_guess_large_number(self):
        """Test invalid guess: 999 (well above max)"""
        is_valid, guess = validate_guess('999')
        self.assertFalse(is_valid)
        self.assertIsNone(guess)
    
    def test_invalid_guess_string(self):
        """Test invalid guess: 'abc'"""
        is_valid, guess = validate_guess('abc')
        self.assertFalse(is_valid)
        self.assertIsNone(guess)
    
    def test_invalid_guess_float(self):
        """Test invalid guess: '50.5' (float format)"""
        is_valid, guess = validate_guess('50.5')
        self.assertFalse(is_valid)
        self.assertIsNone(guess)
    
    def test_invalid_guess_empty_string(self):
        """Test invalid guess: empty string"""
        is_valid, guess = validate_guess('')
        self.assertFalse(is_valid)
        self.assertIsNone(guess)
    
    def test_invalid_guess_whitespace(self):
        """Test invalid guess: whitespace only"""
        is_valid, guess = validate_guess('   ')
        self.assertFalse(is_valid)
        self.assertIsNone(guess)
    
    def test_invalid_guess_special_characters(self):
        """Test invalid guess: special characters '@50'"""
        is_valid, guess = validate_guess('@50')
        self.assertFalse(is_valid)
        self.assertIsNone(guess)
    
    def test_invalid_guess_mixed_alphanumeric(self):
        """Test invalid guess: mixed '50a'"""
        is_valid, guess = validate_guess('50a')
        self.assertFalse(is_valid)
        self.assertIsNone(guess)


class TestCompareGuess(unittest.TestCase):
    """
    Test cases for the compare_guess() function.
    Validates guess comparison logic.
    """
    
    def test_guess_too_low(self):
        """Test when guess is lower than secret number"""
        result = compare_guess(25, 50)
        self.assertEqual(result, 'too_low')
    
    def test_guess_too_high(self):
        """Test when guess is higher than secret number"""
        result = compare_guess(75, 50)
        self.assertEqual(result, 'too_high')
    
    def test_guess_correct(self):
        """Test when guess equals secret number"""
        result = compare_guess(50, 50)
        self.assertEqual(result, 'correct')
    
    def test_guess_minimum_too_low(self):
        """Test minimum boundary: guess 1, secret 2"""
        result = compare_guess(1, 2)
        self.assertEqual(result, 'too_low')
    
    def test_guess_maximum_too_high(self):
        """Test maximum boundary: guess 100, secret 99"""
        result = compare_guess(100, 99)
        self.assertEqual(result, 'too_high')
    
    def test_guess_minimum_correct(self):
        """Test minimum correct: guess 1, secret 1"""
        result = compare_guess(1, 1)
        self.assertEqual(result, 'correct')
    
    def test_guess_maximum_correct(self):
        """Test maximum correct: guess 100, secret 100"""
        result = compare_guess(100, 100)
        self.assertEqual(result, 'correct')
    
    def test_guess_off_by_one_low(self):
        """Test off-by-one: guess 49, secret 50"""
        result = compare_guess(49, 50)
        self.assertEqual(result, 'too_low')
    
    def test_guess_off_by_one_high(self):
        """Test off-by-one: guess 51, secret 50"""
        result = compare_guess(51, 50)
        self.assertEqual(result, 'too_high')
    
    def test_guess_large_difference_low(self):
        """Test large difference: guess 10, secret 90"""
        result = compare_guess(10, 90)
        self.assertEqual(result, 'too_low')
    
    def test_guess_large_difference_high(self):
        """Test large difference: guess 90, secret 10"""
        result = compare_guess(90, 10)
        self.assertEqual(result, 'too_high')


class TestCheckWinCondition(unittest.TestCase):
    """
    Test cases for the check_win_condition() function.
    Validates win condition logic.
    """
    
    def test_win_condition_correct_guess(self):
        """Test win condition: guess equals secret"""
        result = check_win_condition(50, 50)
        self.assertTrue(result)
    
    def test_win_condition_incorrect_guess_low(self):
        """Test lose condition: guess too low"""
        result = check_win_condition(25, 50)
        self.assertFalse(result)
    
    def test_win_condition_incorrect_guess_high(self):
        """Test lose condition: guess too high"""
        result = check_win_condition(75, 50)
        self.assertFalse(result)
    
    def test_win_condition_minimum(self):
        """Test win condition at minimum: 1 == 1"""
        result = check_win_condition(1, 1)
        self.assertTrue(result)
    
    def test_win_condition_maximum(self):
        """Test win condition at maximum: 100 == 100"""
        result = check_win_condition(100, 100)
        self.assertTrue(result)
    
    def test_win_condition_off_by_one(self):
        """Test lose condition: off by one"""
        result = check_win_condition(49, 50)
        self.assertFalse(result)


class TestEdgeCases(unittest.TestCase):
    """
    Test cases for edge cases and boundary conditions.
    """
    
    def test_consecutive_low_guesses(self):
        """Test multiple consecutive low guesses"""
        secret = 50
        guesses = [10, 20, 30, 40]
        for guess in guesses:
            result = compare_guess(guess, secret)
            self.assertEqual(result, 'too_low')
    
    def test_consecutive_high_guesses(self):
        """Test multiple consecutive high guesses"""
        secret = 50
        guesses = [100, 90, 80, 70]
        for guess in guesses:
            result = compare_guess(guess, secret)
            self.assertEqual(result, 'too_high')
    
    def test_alternating_guesses(self):
        """Test alternating low and high guesses"""
        secret = 50
        low_guess = 25
        high_guess = 75
        
        self.assertEqual(compare_guess(low_guess, secret), 'too_low')
        self.assertEqual(compare_guess(high_guess, secret), 'too_high')
        self.assertEqual(compare_guess(low_guess, secret), 'too_low')
    
    def test_guess_all_single_digits(self):
        """Test all single digit guesses are valid"""
        for i in range(1, 10):
            is_valid, guess = validate_guess(str(i))
            self.assertTrue(is_valid)
            self.assertEqual(guess, i)
    
    def test_guess_boundary_values(self):
        """Test all boundary values"""
        boundaries = ['1', '2', '50', '99', '100']
        for val in boundaries:
            is_valid, guess = validate_guess(val)
            self.assertTrue(is_valid)
            self.assertIsNotNone(guess)


class TestIntegration(unittest.TestCase):
    """
    Integration tests combining multiple functions.
    """
    
    def test_full_game_flow_correct_first_guess(self):
        """Test game flow: correct guess on first try"""
        secret = 50
        guess_input = '50'
        
        # Validate input
        is_valid, guess = validate_guess(guess_input)
        self.assertTrue(is_valid)
        
        # Compare guess
        result = compare_guess(guess, secret)
        self.assertEqual(result, 'correct')
        
        # Check win
        self.assertTrue(check_win_condition(guess, secret))
    
    def test_full_game_flow_multiple_guesses(self):
        """Test game flow: multiple guesses before correct"""
        secret = 50
        guesses_data = [
            ('25', 'too_low'),
            ('75', 'too_high'),
            ('40', 'too_low'),
            ('60', 'too_high'),
            ('50', 'correct')
        ]
        
        for guess_str, expected_result in guesses_data:
            is_valid, guess = validate_guess(guess_str)
            self.assertTrue(is_valid)
            
            result = compare_guess(guess, secret)
            self.assertEqual(result, expected_result)
            
            if result == 'correct':
                self.assertTrue(check_win_condition(guess, secret))
    
    def test_binary_search_pattern(self):
        """Test binary search pattern of guessing"""
        secret = 37
        guesses = [
            (50, 'too_high'),
            (25, 'too_low'),
            (37, 'correct')
        ]
        
        for guess, expected in guesses:
            result = compare_guess(guess, secret)
            self.assertEqual(result, expected)
    
    def test_invalid_input_recovery(self):
        """Test that invalid inputs can be recovered from"""
        invalid_guesses = ['abc', '-5', '101', '', '50.5']
        valid_guess = '50'
        
        # All invalid guesses should fail
        for invalid in invalid_guesses:
            is_valid, guess = validate_guess(invalid)
            self.assertFalse(is_valid)
        
        # Valid guess should work
        is_valid, guess = validate_guess(valid_guess)
        self.assertTrue(is_valid)
        self.assertEqual(guess, 50)


def run_test_summary():
    """
    Run all tests and display a summary report.
    """
    print("\n" + "="*80)
    print("RUNNING NUMBER GUESSING GAME TEST SUITE")
    print("="*80 + "\n")
    
    # Create a test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestValidateGuess))
    suite.addTests(loader.loadTestsFromTestCase(TestCompareGuess))
    suite.addTests(loader.loadTestsFromTestCase(TestCheckWinCondition))
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
