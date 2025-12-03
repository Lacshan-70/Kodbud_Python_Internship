"""
================================================================================
                    PASSWORD CHECKER - TEST CASES
================================================================================

TEST SUITE DESCRIPTION:
    This test module validates all functionalities of the Password Checker
    including length checks, character type checks, strength calculation,
    and requirements validation.

TEST COVERAGE:
    1. Length validation (8+ characters)
    2. Uppercase letter detection
    3. Lowercase letter detection
    4. Digit detection
    5. Special character detection
    6. Overall password strength determination
    7. Unmet requirements listing
    8. Met requirements listing
    9. Edge cases and boundary conditions

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

from password_checker_logic import (
    check_length, check_uppercase, check_lowercase, check_digits,
    check_special_chars, is_strong_password, get_password_strength,
    get_unmet_requirements, get_met_requirements
)


class TestLengthCheck(unittest.TestCase):
    """
    Test cases for the check_length() function.
    """
    
    def test_length_exact_minimum(self):
        """Test password with exactly 8 characters"""
        self.assertTrue(check_length("abcdefgh"))
    
    def test_length_above_minimum(self):
        """Test password longer than minimum"""
        self.assertTrue(check_length("abcdefghijklmnop"))
    
    def test_length_very_long(self):
        """Test very long password"""
        self.assertTrue(check_length("a" * 100))
    
    def test_length_below_minimum(self):
        """Test password shorter than 8 characters"""
        self.assertFalse(check_length("abcdefg"))
    
    def test_length_one_short(self):
        """Test password 1 character short of minimum"""
        self.assertFalse(check_length("abcdefg"))
    
    def test_length_empty(self):
        """Test empty password"""
        self.assertFalse(check_length(""))
    
    def test_length_single_char(self):
        """Test single character password"""
        self.assertFalse(check_length("a"))


class TestUppercaseCheck(unittest.TestCase):
    """
    Test cases for the check_uppercase() function.
    """
    
    def test_uppercase_single(self):
        """Test with single uppercase letter"""
        self.assertTrue(check_uppercase("Aabcdefgh"))
    
    def test_uppercase_multiple(self):
        """Test with multiple uppercase letters"""
        self.assertTrue(check_uppercase("ABCDefgh"))
    
    def test_uppercase_all(self):
        """Test with all uppercase letters"""
        self.assertTrue(check_uppercase("ABCDEFGH"))
    
    def test_uppercase_none(self):
        """Test with no uppercase letters"""
        self.assertFalse(check_uppercase("abcdefgh"))
    
    def test_uppercase_at_start(self):
        """Test uppercase at start"""
        self.assertTrue(check_uppercase("Aabcdefgh"))
    
    def test_uppercase_at_end(self):
        """Test uppercase at end"""
        self.assertTrue(check_uppercase("abcdefghZ"))
    
    def test_uppercase_empty(self):
        """Test empty string"""
        self.assertFalse(check_uppercase(""))


class TestLowercaseCheck(unittest.TestCase):
    """
    Test cases for the check_lowercase() function.
    """
    
    def test_lowercase_single(self):
        """Test with single lowercase letter"""
        self.assertTrue(check_lowercase("aABCDEFGH"))
    
    def test_lowercase_multiple(self):
        """Test with multiple lowercase letters"""
        self.assertTrue(check_lowercase("ABCDefgh"))
    
    def test_lowercase_all(self):
        """Test with all lowercase letters"""
        self.assertTrue(check_lowercase("abcdefgh"))
    
    def test_lowercase_none(self):
        """Test with no lowercase letters"""
        self.assertFalse(check_lowercase("ABCDEFGH"))
    
    def test_lowercase_at_start(self):
        """Test lowercase at start"""
        self.assertTrue(check_lowercase("aABCDEFGH"))
    
    def test_lowercase_at_end(self):
        """Test lowercase at end"""
        self.assertTrue(check_lowercase("ABCDEFGHz"))
    
    def test_lowercase_empty(self):
        """Test empty string"""
        self.assertFalse(check_lowercase(""))


class TestDigitsCheck(unittest.TestCase):
    """
    Test cases for the check_digits() function.
    """
    
    def test_digits_single(self):
        """Test with single digit"""
        self.assertTrue(check_digits("abcdefgh1"))
    
    def test_digits_multiple(self):
        """Test with multiple digits"""
        self.assertTrue(check_digits("abcdef1234"))
    
    def test_digits_all(self):
        """Test with only digits"""
        self.assertTrue(check_digits("12345678"))
    
    def test_digits_none(self):
        """Test with no digits"""
        self.assertFalse(check_digits("abcdefgh"))
    
    def test_digits_at_start(self):
        """Test digit at start"""
        self.assertTrue(check_digits("1abcdefgh"))
    
    def test_digits_at_end(self):
        """Test digit at end"""
        self.assertTrue(check_digits("abcdefgh9"))
    
    def test_digits_zero(self):
        """Test with zero"""
        self.assertTrue(check_digits("abcdefgh0"))
    
    def test_digits_empty(self):
        """Test empty string"""
        self.assertFalse(check_digits(""))


class TestSpecialCharsCheck(unittest.TestCase):
    """
    Test cases for the check_special_chars() function.
    """
    
    def test_special_at(self):
        """Test with @ character"""
        self.assertTrue(check_special_chars("abcdefgh@"))
    
    def test_special_hash(self):
        """Test with # character"""
        self.assertTrue(check_special_chars("abcdefgh#"))
    
    def test_special_dollar(self):
        """Test with $ character"""
        self.assertTrue(check_special_chars("abcdefgh$"))
    
    def test_special_percent(self):
        """Test with % character"""
        self.assertTrue(check_special_chars("abcdefgh%"))
    
    def test_special_caret(self):
        """Test with ^ character"""
        self.assertTrue(check_special_chars("abcdefgh^"))
    
    def test_special_ampersand(self):
        """Test with & character"""
        self.assertTrue(check_special_chars("abcdefgh&"))
    
    def test_special_asterisk(self):
        """Test with * character"""
        self.assertTrue(check_special_chars("abcdefgh*"))
    
    def test_special_exclamation(self):
        """Test with ! character"""
        self.assertTrue(check_special_chars("abcdefgh!"))
    
    def test_special_multiple(self):
        """Test with multiple special characters"""
        self.assertTrue(check_special_chars("abc@def#gh"))
    
    def test_special_none(self):
        """Test with no special characters"""
        self.assertFalse(check_special_chars("abcdefgh"))
    
    def test_special_invalid_chars(self):
        """Test with invalid special characters"""
        self.assertFalse(check_special_chars("abcdefgh-"))
    
    def test_special_empty(self):
        """Test empty string"""
        self.assertFalse(check_special_chars(""))


class TestIsStrongPassword(unittest.TestCase):
    """
    Test cases for the is_strong_password() function.
    """
    
    def test_strong_password_all_requirements(self):
        """Test password meeting all requirements"""
        self.assertTrue(is_strong_password("Password123!"))
    
    def test_strong_password_minimal(self):
        """Test minimal strong password"""
        self.assertTrue(is_strong_password("Abc1234!"))
    
    def test_strong_password_complex(self):
        """Test complex strong password"""
        self.assertTrue(is_strong_password("MyP@ssw0rd!"))
    
    def test_weak_no_uppercase(self):
        """Test weak password - no uppercase"""
        self.assertFalse(is_strong_password("password123!"))
    
    def test_weak_no_lowercase(self):
        """Test weak password - no lowercase"""
        self.assertFalse(is_strong_password("PASSWORD123!"))
    
    def test_weak_no_digits(self):
        """Test weak password - no digits"""
        self.assertFalse(is_strong_password("Password!"))
    
    def test_weak_no_special(self):
        """Test weak password - no special characters"""
        self.assertFalse(is_strong_password("Password123"))
    
    def test_weak_too_short(self):
        """Test weak password - too short"""
        self.assertFalse(is_strong_password("Pass1!"))
    
    def test_weak_empty(self):
        """Test weak password - empty string"""
        self.assertFalse(is_strong_password(""))


class TestPasswordStrengthLevel(unittest.TestCase):
    """
    Test cases for the get_password_strength() function.
    """
    
    def test_strength_strong(self):
        """Test strong password strength level"""
        strength = get_password_strength("Password123!")
        self.assertEqual(strength, "Strong")
    
    def test_strength_good(self):
        """Test good password strength level (4/5 requirements)"""
        strength = get_password_strength("Password123")  # Missing special char
        self.assertEqual(strength, "Good")
    
    def test_strength_fair(self):
        """Test fair password strength level (3/5 requirements)"""
        strength = get_password_strength("password123")  # Missing uppercase, special
        self.assertEqual(strength, "Fair")
    
    def test_strength_weak(self):
        """Test weak password strength level (< 3 requirements)"""
        strength = get_password_strength("password")  # Missing digits, uppercase, special
        self.assertEqual(strength, "Weak")
    
    def test_strength_very_weak(self):
        """Test very weak password"""
        strength = get_password_strength("pass")
        self.assertEqual(strength, "Weak")


class TestUnmetRequirements(unittest.TestCase):
    """
    Test cases for the get_unmet_requirements() function.
    """
    
    def test_unmet_all_met(self):
        """Test when all requirements are met"""
        unmet = get_unmet_requirements("Password123!")
        self.assertEqual(len(unmet), 0)
    
    def test_unmet_all_failed(self):
        """Test when all requirements fail"""
        unmet = get_unmet_requirements("abcdefgh")
        # Missing uppercase, digits, and special chars (3 unmet)
        self.assertGreaterEqual(len(unmet), 3)
    
    def test_unmet_no_uppercase(self):
        """Test unmet - no uppercase"""
        unmet = get_unmet_requirements("password123!")
        self.assertIn("At least one uppercase letter (A-Z)", unmet)
    
    def test_unmet_no_lowercase(self):
        """Test unmet - no lowercase"""
        unmet = get_unmet_requirements("PASSWORD123!")
        self.assertIn("At least one lowercase letter (a-z)", unmet)
    
    def test_unmet_no_digits(self):
        """Test unmet - no digits"""
        unmet = get_unmet_requirements("Password!")
        self.assertIn("At least one digit (0-9)", unmet)
    
    def test_unmet_no_special(self):
        """Test unmet - no special characters"""
        unmet = get_unmet_requirements("Password123")
        self.assertIn("At least one special character (@ # $ % ^ & * !)", unmet)
    
    def test_unmet_too_short(self):
        """Test unmet - too short"""
        unmet = get_unmet_requirements("Pass1!")
        self.assertIn("Minimum 8 characters", unmet)
    
    def test_unmet_empty(self):
        """Test unmet - empty string"""
        unmet = get_unmet_requirements("")
        self.assertEqual(len(unmet), 5)
    
    def test_unmet_multiple(self):
        """Test multiple unmet requirements"""
        unmet = get_unmet_requirements("password")
        self.assertTrue(len(unmet) >= 2)
        self.assertIn("At least one uppercase letter (A-Z)", unmet)


class TestMetRequirements(unittest.TestCase):
    """
    Test cases for the get_met_requirements() function.
    """
    
    def test_met_all_requirements(self):
        """Test all requirements met"""
        met = get_met_requirements("Password123!")
        self.assertEqual(len(met), 5)
    
    def test_met_none(self):
        """Test no requirements met"""
        met = get_met_requirements("")
        self.assertEqual(len(met), 0)
    
    def test_met_contains_length(self):
        """Test met requirements include length"""
        met = get_met_requirements("Password123!")
        self.assertIn("Minimum 8 characters", met)
    
    def test_met_contains_uppercase(self):
        """Test met requirements include uppercase"""
        met = get_met_requirements("Password123!")
        self.assertIn("At least one uppercase letter (A-Z)", met)
    
    def test_met_partial(self):
        """Test partially met requirements"""
        met = get_met_requirements("Password123")  # Missing special
        self.assertEqual(len(met), 4)


class TestEdgeCases(unittest.TestCase):
    """
    Test cases for edge cases and boundary conditions.
    """
    
    def test_only_special_chars(self):
        """Test password with only special characters"""
        self.assertFalse(is_strong_password("!@#$%^&*"))
    
    def test_only_numbers(self):
        """Test password with only numbers"""
        self.assertFalse(is_strong_password("12345678"))
    
    def test_space_character(self):
        """Test password with spaces"""
        # Spaces are not special characters, but all other requirements are met
        # Pass (uppercase), word (lowercase), 1 (digit), ! (special), 10 chars (length)
        self.assertTrue(is_strong_password("Pass word1!"))
    
    def test_repeated_characters(self):
        """Test password with repeated characters"""
        self.assertTrue(is_strong_password("Aaaaaaaa1!"))
    
    def test_unicode_characters(self):
        """Test password with unicode characters"""
        result = is_strong_password("Pässwörd123!")
        # Unicode letters may not be recognized as uppercase/lowercase
        # Depending on regex interpretation
    
    def test_boundary_exactly_8_chars_strong(self):
        """Test exactly 8 character strong password"""
        self.assertTrue(is_strong_password("Abc1234!"))
    
    def test_boundary_7_chars_weak(self):
        """Test 7 character password (too short)"""
        self.assertFalse(is_strong_password("Abc123!"))


class TestIntegration(unittest.TestCase):
    """
    Integration tests for password validation workflows.
    """
    
    def test_password_evaluation_workflow(self):
        """Test complete password evaluation workflow"""
        password = "MyPassword123!"
        
        # Check strength
        strength = get_password_strength(password)
        self.assertEqual(strength, "Strong")
        
        # Verify it's strong
        self.assertTrue(is_strong_password(password))
        
        # Check unmet requirements (should be none)
        unmet = get_unmet_requirements(password)
        self.assertEqual(len(unmet), 0)
    
    def test_weak_password_feedback(self):
        """Test feedback for weak password"""
        password = "weak"
        
        # Check strength
        strength = get_password_strength(password)
        self.assertEqual(strength, "Weak")
        
        # Verify it's not strong
        self.assertFalse(is_strong_password(password))
        
        # Check unmet requirements
        unmet = get_unmet_requirements(password)
        self.assertTrue(len(unmet) > 0)
    
    def test_good_password_feedback(self):
        """Test feedback for good password"""
        password = "Password123"  # Missing special character
        
        # Check strength
        strength = get_password_strength(password)
        self.assertEqual(strength, "Good")
        
        # Should not be strong
        self.assertFalse(is_strong_password(password))
        
        # Should have exactly 1 unmet requirement
        unmet = get_unmet_requirements(password)
        self.assertEqual(len(unmet), 1)
        self.assertIn("special character", unmet[0])
    
    def test_password_improvement_workflow(self):
        """Test improving a weak password"""
        weak_password = "password"
        strong_password = "Password123!"
        
        # Weak password
        self.assertFalse(is_strong_password(weak_password))
        weak_unmet = get_unmet_requirements(weak_password)
        self.assertTrue(len(weak_unmet) > 0)
        
        # Strong password
        self.assertTrue(is_strong_password(strong_password))
        strong_unmet = get_unmet_requirements(strong_password)
        self.assertEqual(len(strong_unmet), 0)


class TestAllSpecialCharacters(unittest.TestCase):
    """
    Test all allowed special characters individually.
    """
    
    def test_all_special_chars_individually(self):
        """Test each allowed special character"""
        special_chars = ['@', '#', '$', '%', '^', '&', '*', '!']
        base_password = "Abcdefg1"
        
        for char in special_chars:
            password = base_password + char
            self.assertTrue(check_special_chars(password),
                          f"Failed for special character: {char}")


def run_test_summary():
    """
    Run all tests and display a summary report.
    """
    print("\n" + "="*80)
    print("RUNNING PASSWORD CHECKER TEST SUITE")
    print("="*80 + "\n")
    
    # Create a test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestLengthCheck))
    suite.addTests(loader.loadTestsFromTestCase(TestUppercaseCheck))
    suite.addTests(loader.loadTestsFromTestCase(TestLowercaseCheck))
    suite.addTests(loader.loadTestsFromTestCase(TestDigitsCheck))
    suite.addTests(loader.loadTestsFromTestCase(TestSpecialCharsCheck))
    suite.addTests(loader.loadTestsFromTestCase(TestIsStrongPassword))
    suite.addTests(loader.loadTestsFromTestCase(TestPasswordStrengthLevel))
    suite.addTests(loader.loadTestsFromTestCase(TestUnmetRequirements))
    suite.addTests(loader.loadTestsFromTestCase(TestMetRequirements))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestAllSpecialCharacters))
    
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
