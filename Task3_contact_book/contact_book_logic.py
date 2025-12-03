"""
CONTACT BOOK - CONTACT MANAGEMENT LOGIC MODULE
===============================================

This module contains the core logic for contact management operations,
separated from the interactive UI for easier testing.

FUNCTIONS:
    - validate_name(name): Validates contact name
    - validate_phone(phone): Validates phone number
    - add_contact(contacts, name, phone): Adds new contact
    - view_contacts(contacts): Returns formatted contact list
    - search_contact(contacts, name): Searches for contact
    - delete_contact(contacts, name): Deletes contact
    - contact_exists(contacts, name): Checks if contact exists

DEVELOPED BY: Lacshan Shakthivel
DATE: December 3, 2025
"""


def validate_name(name):
    """
    Validates if the name is valid (non-empty, contains only letters and spaces).
    
    Args:
        name (str): The contact name to validate
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if not name or not name.strip():
        return False, "Name cannot be empty"
    
    name = name.strip()
    
    # Check if name contains only letters and spaces
    if not all(c.isalpha() or c.isspace() for c in name):
        return False, "Name can only contain letters and spaces"
    
    if len(name) < 2:
        return False, "Name must be at least 2 characters long"
    
    if len(name) > 50:
        return False, "Name must not exceed 50 characters"
    
    return True, ""


def validate_phone(phone):
    """
    Validates if the phone number is valid (numeric, reasonable length).
    
    Args:
        phone (str): The phone number to validate
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if not phone or not phone.strip():
        return False, "Phone number cannot be empty"
    
    phone = phone.strip()
    
    # Allow digits and some common formatting characters
    if not all(c.isdigit() or c in ['-', '+', ' ', '(', ')'] for c in phone):
        return False, "Phone number contains invalid characters"
    
    # Count only digits
    digits_only = ''.join(c for c in phone if c.isdigit())
    
    if len(digits_only) < 7:
        return False, "Phone number must have at least 7 digits"
    
    if len(digits_only) > 15:
        return False, "Phone number must not exceed 15 digits"
    
    return True, ""


def contact_exists(contacts, name):
    """
    Checks if a contact with the given name exists.
    
    Args:
        contacts (list): List of contact dictionaries
        name (str): The name to search for
    
    Returns:
        bool: True if contact exists, False otherwise
    """
    for contact in contacts:
        if contact["name"].lower() == name.lower().strip():
            return True
    return False


def add_contact(contacts, name, phone):
    """
    Adds a new contact to the contacts list.
    
    Args:
        contacts (list): List of contact dictionaries
        name (str): Contact name
        phone (str): Contact phone number
    
    Returns:
        tuple: (success, message)
    """
    # Validate inputs
    is_valid_name, name_msg = validate_name(name)
    if not is_valid_name:
        return False, name_msg
    
    is_valid_phone, phone_msg = validate_phone(phone)
    if not is_valid_phone:
        return False, phone_msg
    
    # Check if contact already exists
    if contact_exists(contacts, name):
        return False, "Contact already exists"
    
    # Add contact
    contacts.append({
        "name": name.strip(),
        "phone": phone.strip()
    })
    return True, "Contact added successfully"


def view_contacts(contacts):
    """
    Returns a formatted string of all contacts.
    
    Args:
        contacts (list): List of contact dictionaries
    
    Returns:
        str: Formatted contact list or empty message
    """
    if not contacts:
        return "No contacts saved yet."
    
    result = "\n--- Contact List ---\n"
    for idx, contact in enumerate(contacts, start=1):
        result += f"{idx}. {contact['name']} - {contact['phone']}\n"
    return result


def search_contact(contacts, name):
    """
    Searches for a contact by name.
    
    Args:
        contacts (list): List of contact dictionaries
        name (str): The name to search for
    
    Returns:
        tuple: (found, contact_dict or message)
    """
    if not name or not name.strip():
        return False, "Search name cannot be empty"
    
    for contact in contacts:
        if contact["name"].lower() == name.lower().strip():
            return True, contact
    
    return False, "Contact not found"


def delete_contact(contacts, name):
    """
    Deletes a contact by name.
    
    Args:
        contacts (list): List of contact dictionaries
        name (str): The name of contact to delete
    
    Returns:
        tuple: (success, message)
    """
    if not name or not name.strip():
        return False, "Name cannot be empty"
    
    for contact in contacts:
        if contact["name"].lower() == name.lower().strip():
            contacts.remove(contact)
            return True, "Contact deleted successfully"
    
    return False, "Contact not found"


def get_all_contacts(contacts):
    """
    Returns a copy of all contacts.
    
    Args:
        contacts (list): List of contact dictionaries
    
    Returns:
        list: Copy of contacts list
    """
    return list(contacts)


def clear_all_contacts(contacts):
    """
    Clears all contacts from the list.
    
    Args:
        contacts (list): List of contact dictionaries
    
    Returns:
        int: Number of contacts deleted
    """
    count = len(contacts)
    contacts.clear()
    return count
