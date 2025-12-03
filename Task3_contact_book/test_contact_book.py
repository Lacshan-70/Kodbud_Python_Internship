"""
================================================================================
                    CONTACT BOOK - TEST CASES
================================================================================

TEST SUITE DESCRIPTION:
    This test module validates all functionalities of the Contact Book
    including contact validation, CRUD operations, search, delete, and
    edge cases.

TEST COVERAGE:
    1. Name validation (valid and invalid inputs)
    2. Phone validation (valid and invalid inputs)
    3. Add contact functionality
    4. View contacts functionality
    5. Search contact functionality
    6. Delete contact functionality
    7. Duplicate contact handling
    8. Case-insensitive operations

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

from contact_book_logic import (
    validate_name, validate_phone, add_contact, view_contacts,
    search_contact, delete_contact, contact_exists, get_all_contacts,
    clear_all_contacts
)


class TestNameValidation(unittest.TestCase):
    """
    Test cases for the validate_name() function.
    """
    
    def test_valid_name_simple(self):
        """Test valid simple name"""
        is_valid, msg = validate_name("John")
        self.assertTrue(is_valid)
        self.assertEqual(msg, "")
    
    def test_valid_name_full(self):
        """Test valid full name"""
        is_valid, msg = validate_name("John Doe")
        self.assertTrue(is_valid)
        self.assertEqual(msg, "")
    
    def test_valid_name_long(self):
        """Test valid long name"""
        is_valid, msg = validate_name("Alexander Christopher")
        self.assertTrue(is_valid)
        self.assertEqual(msg, "")
    
    def test_valid_name_two_characters(self):
        """Test valid minimum length (2 chars)"""
        is_valid, msg = validate_name("Jo")
        self.assertTrue(is_valid)
        self.assertEqual(msg, "")
    
    def test_valid_name_with_spaces(self):
        """Test valid name with multiple spaces"""
        is_valid, msg = validate_name("Mary Jane Watson")
        self.assertTrue(is_valid)
        self.assertEqual(msg, "")
    
    def test_invalid_name_empty(self):
        """Test invalid empty name"""
        is_valid, msg = validate_name("")
        self.assertFalse(is_valid)
        self.assertEqual(msg, "Name cannot be empty")
    
    def test_invalid_name_whitespace_only(self):
        """Test invalid whitespace-only name"""
        is_valid, msg = validate_name("   ")
        self.assertFalse(is_valid)
        self.assertEqual(msg, "Name cannot be empty")
    
    def test_invalid_name_single_character(self):
        """Test invalid single character"""
        is_valid, msg = validate_name("J")
        self.assertFalse(is_valid)
        self.assertEqual(msg, "Name must be at least 2 characters long")
    
    def test_invalid_name_with_numbers(self):
        """Test invalid name with numbers"""
        is_valid, msg = validate_name("John123")
        self.assertFalse(is_valid)
        self.assertEqual(msg, "Name can only contain letters and spaces")
    
    def test_invalid_name_with_special_chars(self):
        """Test invalid name with special characters"""
        is_valid, msg = validate_name("John@Doe")
        self.assertFalse(is_valid)
        self.assertEqual(msg, "Name can only contain letters and spaces")
    
    def test_invalid_name_too_long(self):
        """Test invalid name exceeding max length"""
        long_name = "A" * 51
        is_valid, msg = validate_name(long_name)
        self.assertFalse(is_valid)
        self.assertEqual(msg, "Name must not exceed 50 characters")
    
    def test_valid_name_with_leading_trailing_spaces(self):
        """Test valid name with leading/trailing spaces"""
        is_valid, msg = validate_name("  John Doe  ")
        self.assertTrue(is_valid)
        self.assertEqual(msg, "")
    
    def test_invalid_name_with_hyphens(self):
        """Test invalid name with hyphens"""
        is_valid, msg = validate_name("Mary-Jane")
        self.assertFalse(is_valid)


class TestPhoneValidation(unittest.TestCase):
    """
    Test cases for the validate_phone() function.
    """
    
    def test_valid_phone_simple_digits(self):
        """Test valid simple phone number"""
        is_valid, msg = validate_phone("1234567890")
        self.assertTrue(is_valid)
        self.assertEqual(msg, "")
    
    def test_valid_phone_with_dashes(self):
        """Test valid phone with dashes"""
        is_valid, msg = validate_phone("123-456-7890")
        self.assertTrue(is_valid)
        self.assertEqual(msg, "")
    
    def test_valid_phone_with_plus(self):
        """Test valid phone with plus (international)"""
        is_valid, msg = validate_phone("+1-123-456-7890")
        self.assertTrue(is_valid)
        self.assertEqual(msg, "")
    
    def test_valid_phone_with_parentheses(self):
        """Test valid phone with parentheses"""
        is_valid, msg = validate_phone("(123) 456-7890")
        self.assertTrue(is_valid)
        self.assertEqual(msg, "")
    
    def test_valid_phone_minimum_digits(self):
        """Test valid phone with minimum 7 digits"""
        is_valid, msg = validate_phone("1234567")
        self.assertTrue(is_valid)
        self.assertEqual(msg, "")
    
    def test_valid_phone_maximum_digits(self):
        """Test valid phone with maximum 15 digits"""
        is_valid, msg = validate_phone("123456789012345")
        self.assertTrue(is_valid)
        self.assertEqual(msg, "")
    
    def test_invalid_phone_empty(self):
        """Test invalid empty phone"""
        is_valid, msg = validate_phone("")
        self.assertFalse(is_valid)
        self.assertEqual(msg, "Phone number cannot be empty")
    
    def test_invalid_phone_whitespace_only(self):
        """Test invalid whitespace-only phone"""
        is_valid, msg = validate_phone("   ")
        self.assertFalse(is_valid)
        self.assertEqual(msg, "Phone number cannot be empty")
    
    def test_invalid_phone_too_short(self):
        """Test invalid phone too short (less than 7 digits)"""
        is_valid, msg = validate_phone("123456")
        self.assertFalse(is_valid)
        self.assertEqual(msg, "Phone number must have at least 7 digits")
    
    def test_invalid_phone_too_long(self):
        """Test invalid phone too long (more than 15 digits)"""
        is_valid, msg = validate_phone("1234567890123456")
        self.assertFalse(is_valid)
        self.assertEqual(msg, "Phone number must not exceed 15 digits")
    
    def test_invalid_phone_with_letters(self):
        """Test invalid phone with letters"""
        is_valid, msg = validate_phone("123ABC7890")
        self.assertFalse(is_valid)
        self.assertEqual(msg, "Phone number contains invalid characters")
    
    def test_invalid_phone_with_special_chars(self):
        """Test invalid phone with special characters"""
        is_valid, msg = validate_phone("123@456#7890")
        self.assertFalse(is_valid)
        self.assertEqual(msg, "Phone number contains invalid characters")


class TestAddContact(unittest.TestCase):
    """
    Test cases for the add_contact() function.
    """
    
    def setUp(self):
        """Initialize empty contacts list for each test"""
        self.contacts = []
    
    def test_add_valid_contact(self):
        """Test adding a valid contact"""
        success, msg = add_contact(self.contacts, "John Doe", "1234567890")
        self.assertTrue(success)
        self.assertEqual(msg, "Contact added successfully")
        self.assertEqual(len(self.contacts), 1)
        self.assertEqual(self.contacts[0]["name"], "John Doe")
    
    def test_add_multiple_contacts(self):
        """Test adding multiple contacts"""
        add_contact(self.contacts, "John Doe", "1234567890")
        add_contact(self.contacts, "Jane Smith", "0987654321")
        self.assertEqual(len(self.contacts), 2)
    
    def test_add_contact_with_invalid_name(self):
        """Test adding contact with invalid name"""
        success, msg = add_contact(self.contacts, "J", "1234567890")
        self.assertFalse(success)
        self.assertEqual(len(self.contacts), 0)
    
    def test_add_contact_with_invalid_phone(self):
        """Test adding contact with invalid phone"""
        success, msg = add_contact(self.contacts, "John Doe", "123")
        self.assertFalse(success)
        self.assertEqual(len(self.contacts), 0)
    
    def test_add_duplicate_contact(self):
        """Test adding duplicate contact (same name)"""
        add_contact(self.contacts, "John Doe", "1234567890")
        success, msg = add_contact(self.contacts, "John Doe", "9999999999")
        self.assertFalse(success)
        self.assertEqual(msg, "Contact already exists")
        self.assertEqual(len(self.contacts), 1)
    
    def test_add_duplicate_case_insensitive(self):
        """Test duplicate detection is case-insensitive"""
        add_contact(self.contacts, "John Doe", "1234567890")
        success, msg = add_contact(self.contacts, "john doe", "9999999999")
        self.assertFalse(success)
        self.assertEqual(len(self.contacts), 1)
    
    def test_add_contact_with_leading_trailing_spaces(self):
        """Test adding contact with spaces stripped"""
        add_contact(self.contacts, "  John Doe  ", "  1234567890  ")
        self.assertEqual(self.contacts[0]["name"], "John Doe")
        self.assertEqual(self.contacts[0]["phone"], "1234567890")


class TestViewContacts(unittest.TestCase):
    """
    Test cases for the view_contacts() function.
    """
    
    def test_view_empty_contacts(self):
        """Test viewing empty contact list"""
        contacts = []
        result = view_contacts(contacts)
        self.assertEqual(result, "No contacts saved yet.")
    
    def test_view_single_contact(self):
        """Test viewing single contact"""
        contacts = [{"name": "John Doe", "phone": "1234567890"}]
        result = view_contacts(contacts)
        self.assertIn("John Doe", result)
        self.assertIn("1234567890", result)
        self.assertIn("1.", result)
    
    def test_view_multiple_contacts(self):
        """Test viewing multiple contacts"""
        contacts = [
            {"name": "John Doe", "phone": "1234567890"},
            {"name": "Jane Smith", "phone": "0987654321"},
            {"name": "Bob Wilson", "phone": "1111111111"}
        ]
        result = view_contacts(contacts)
        self.assertIn("John Doe", result)
        self.assertIn("Jane Smith", result)
        self.assertIn("Bob Wilson", result)
        self.assertIn("1.", result)
        self.assertIn("2.", result)
        self.assertIn("3.", result)
    
    def test_view_contacts_formatting(self):
        """Test that view output is properly formatted"""
        contacts = [{"name": "John Doe", "phone": "1234567890"}]
        result = view_contacts(contacts)
        self.assertIn("--- Contact List ---", result)


class TestSearchContact(unittest.TestCase):
    """
    Test cases for the search_contact() function.
    """
    
    def setUp(self):
        """Initialize contacts for each test"""
        self.contacts = [
            {"name": "John Doe", "phone": "1234567890"},
            {"name": "Jane Smith", "phone": "0987654321"},
            {"name": "Bob Wilson", "phone": "1111111111"}
        ]
    
    def test_search_existing_contact(self):
        """Test searching for existing contact"""
        found, result = search_contact(self.contacts, "John Doe")
        self.assertTrue(found)
        self.assertEqual(result["name"], "John Doe")
        self.assertEqual(result["phone"], "1234567890")
    
    def test_search_non_existing_contact(self):
        """Test searching for non-existing contact"""
        found, result = search_contact(self.contacts, "Unknown Person")
        self.assertFalse(found)
        self.assertEqual(result, "Contact not found")
    
    def test_search_case_insensitive(self):
        """Test search is case-insensitive"""
        found, result = search_contact(self.contacts, "john doe")
        self.assertTrue(found)
        self.assertEqual(result["name"], "John Doe")
    
    def test_search_uppercase(self):
        """Test search with uppercase"""
        found, result = search_contact(self.contacts, "JANE SMITH")
        self.assertTrue(found)
        self.assertEqual(result["name"], "Jane Smith")
    
    def test_search_with_leading_trailing_spaces(self):
        """Test search handles leading/trailing spaces"""
        found, result = search_contact(self.contacts, "  Bob Wilson  ")
        self.assertTrue(found)
        self.assertEqual(result["name"], "Bob Wilson")
    
    def test_search_empty_name(self):
        """Test search with empty name"""
        found, result = search_contact(self.contacts, "")
        self.assertFalse(found)
        self.assertEqual(result, "Search name cannot be empty")


class TestDeleteContact(unittest.TestCase):
    """
    Test cases for the delete_contact() function.
    """
    
    def setUp(self):
        """Initialize contacts for each test"""
        self.contacts = [
            {"name": "John Doe", "phone": "1234567890"},
            {"name": "Jane Smith", "phone": "0987654321"},
            {"name": "Bob Wilson", "phone": "1111111111"}
        ]
    
    def test_delete_existing_contact(self):
        """Test deleting existing contact"""
        success, msg = delete_contact(self.contacts, "John Doe")
        self.assertTrue(success)
        self.assertEqual(msg, "Contact deleted successfully")
        self.assertEqual(len(self.contacts), 2)
        self.assertFalse(any(c["name"] == "John Doe" for c in self.contacts))
    
    def test_delete_non_existing_contact(self):
        """Test deleting non-existing contact"""
        success, msg = delete_contact(self.contacts, "Unknown Person")
        self.assertFalse(success)
        self.assertEqual(msg, "Contact not found")
        self.assertEqual(len(self.contacts), 3)
    
    def test_delete_case_insensitive(self):
        """Test delete is case-insensitive"""
        success, msg = delete_contact(self.contacts, "jane smith")
        self.assertTrue(success)
        self.assertEqual(len(self.contacts), 2)
    
    def test_delete_all_contacts_one_by_one(self):
        """Test deleting all contacts one by one"""
        delete_contact(self.contacts, "John Doe")
        self.assertEqual(len(self.contacts), 2)
        
        delete_contact(self.contacts, "Jane Smith")
        self.assertEqual(len(self.contacts), 1)
        
        delete_contact(self.contacts, "Bob Wilson")
        self.assertEqual(len(self.contacts), 0)


class TestContactExists(unittest.TestCase):
    """
    Test cases for the contact_exists() function.
    """
    
    def setUp(self):
        """Initialize contacts for each test"""
        self.contacts = [
            {"name": "John Doe", "phone": "1234567890"},
            {"name": "Jane Smith", "phone": "0987654321"}
        ]
    
    def test_contact_exists_true(self):
        """Test when contact exists"""
        exists = contact_exists(self.contacts, "John Doe")
        self.assertTrue(exists)
    
    def test_contact_exists_false(self):
        """Test when contact doesn't exist"""
        exists = contact_exists(self.contacts, "Unknown Person")
        self.assertFalse(exists)
    
    def test_contact_exists_case_insensitive(self):
        """Test existence check is case-insensitive"""
        exists = contact_exists(self.contacts, "john doe")
        self.assertTrue(exists)


class TestIntegration(unittest.TestCase):
    """
    Integration tests for complete contact book operations.
    """
    
    def setUp(self):
        """Initialize empty contacts for each test"""
        self.contacts = []
    
    def test_full_crud_operation(self):
        """Test complete CRUD: Create, Read, Update (delete+add), Delete"""
        # Create
        add_contact(self.contacts, "John Doe", "1234567890")
        self.assertEqual(len(self.contacts), 1)
        
        # Read
        found, result = search_contact(self.contacts, "John Doe")
        self.assertTrue(found)
        
        # Update (delete and add new)
        delete_contact(self.contacts, "John Doe")
        add_contact(self.contacts, "Jane Doe", "0987654321")
        self.assertEqual(len(self.contacts), 1)
        
        # Delete
        delete_contact(self.contacts, "Jane Doe")
        self.assertEqual(len(self.contacts), 0)
    
    def test_add_search_delete_workflow(self):
        """Test typical add, search, delete workflow"""
        # Add contacts
        add_contact(self.contacts, "Alice", "1111111111")
        add_contact(self.contacts, "Bob", "2222222222")
        add_contact(self.contacts, "Charlie", "3333333333")
        
        # Search and verify
        found, result = search_contact(self.contacts, "Bob")
        self.assertTrue(found)
        self.assertEqual(result["phone"], "2222222222")
        
        # Delete middle contact
        delete_contact(self.contacts, "Bob")
        found, _ = search_contact(self.contacts, "Bob")
        self.assertFalse(found)
        
        # Others should still exist
        found, _ = search_contact(self.contacts, "Alice")
        self.assertTrue(found)


class TestEdgeCases(unittest.TestCase):
    """
    Test cases for edge cases and boundary conditions.
    """
    
    def setUp(self):
        """Initialize contacts for each test"""
        self.contacts = []
    
    def test_add_many_contacts(self):
        """Test adding many contacts"""
        names = ["Alice Smith", "Bob Jones", "Charlie Brown", "David Lee", "Eve Wilson", 
                 "Frank Miller", "Grace Taylor", "Henry Anderson", "Ivy Thomas", "Jack White"]
        for i, name in enumerate(names):
            phone = f"{1000000 + i:07d}"
            add_contact(self.contacts, name, phone)
        self.assertEqual(len(self.contacts), 10)
    
    def test_phone_with_all_formatting(self):
        """Test phone number with various formatting"""
        add_contact(self.contacts, "Test User", "+1(555) 123-4567")
        self.assertEqual(len(self.contacts), 1)
    
    def test_name_with_multiple_spaces(self):
        """Test name with multiple consecutive spaces"""
        add_contact(self.contacts, "John    Doe", "1234567890")
        # Should still be valid
        self.assertEqual(len(self.contacts), 1)


def run_test_summary():
    """
    Run all tests and display a summary report.
    """
    print("\n" + "="*80)
    print("RUNNING CONTACT BOOK TEST SUITE")
    print("="*80 + "\n")
    
    # Create a test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestNameValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestPhoneValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestAddContact))
    suite.addTests(loader.loadTestsFromTestCase(TestViewContacts))
    suite.addTests(loader.loadTestsFromTestCase(TestSearchContact))
    suite.addTests(loader.loadTestsFromTestCase(TestDeleteContact))
    suite.addTests(loader.loadTestsFromTestCase(TestContactExists))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    
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
