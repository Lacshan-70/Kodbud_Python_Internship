"""
PASSWORD CHECKER - PASSWORD VALIDATION LOGIC MODULE
===================================================

This module contains the core logic for password strength validation,
separated from the interactive UI for easier testing.

FUNCTIONS:
    - check_length(password): Checks if password has minimum 8 characters
    - check_uppercase(password): Checks for uppercase letters
    - check_lowercase(password): Checks for lowercase letters
    - check_digits(password): Checks for digit characters
    - check_special_chars(password): Checks for special characters
    - get_password_strength(password): Determines overall password strength
    - get_unmet_requirements(password): Returns list of failed requirements

DEVELOPED BY: Lacshan Shakthivel
DATE: December 3, 2025
"""

import re


def check_length(password):
    """
    Checks if password has minimum length of 8 characters.
    
    Args:
        password (str): The password to check
    
    Returns:
        bool: True if length >= 8, False otherwise
    """
    return len(password) >= 8


def check_uppercase(password):
    """
    Checks if password contains at least one uppercase letter (A-Z).
    
    Args:
        password (str): The password to check
    
    Returns:
        bool: True if contains uppercase, False otherwise
    """
    return bool(re.search(r"[A-Z]", password))


def check_lowercase(password):
    """
    Checks if password contains at least one lowercase letter (a-z).
    
    Args:
        password (str): The password to check
    
    Returns:
        bool: True if contains lowercase, False otherwise
    """
    return bool(re.search(r"[a-z]", password))


def check_digits(password):
    """
    Checks if password contains at least one digit (0-9).
    
    Args:
        password (str): The password to check
    
    Returns:
        bool: True if contains digit, False otherwise
    """
    return bool(re.search(r"[0-9]", password))


def check_special_chars(password):
    """
    Checks if password contains at least one special character (@#$%^&*!).
    
    Args:
        password (str): The password to check
    
    Returns:
        bool: True if contains special character, False otherwise
    """
    return bool(re.search(r"[@#$%^&*!]", password))


def is_strong_password(password):
    """
    Determines if password meets all strength requirements.
    
    Args:
        password (str): The password to check
    
    Returns:
        bool: True if password is strong, False otherwise
    """
    return (check_length(password) and 
            check_uppercase(password) and 
            check_lowercase(password) and 
            check_digits(password) and 
            check_special_chars(password))


def get_password_strength(password):
    """
    Determines the password strength level (Weak, Fair, Good, Strong).
    
    Args:
        password (str): The password to check
    
    Returns:
        str: Strength level ('Weak', 'Fair', 'Good', 'Strong')
    """
    checks_passed = sum([
        check_length(password),
        check_uppercase(password),
        check_lowercase(password),
        check_digits(password),
        check_special_chars(password)
    ])
    
    if checks_passed == 5:
        return 'Strong'
    elif checks_passed >= 4:
        return 'Good'
    elif checks_passed >= 3:
        return 'Fair'
    else:
        return 'Weak'


def get_unmet_requirements(password):
    """
    Returns a list of unmet password requirements.
    
    Args:
        password (str): The password to check
    
    Returns:
        list: List of failed requirement messages
    """
    requirements = []
    
    if not check_length(password):
        requirements.append("Minimum 8 characters")
    
    if not check_uppercase(password):
        requirements.append("At least one uppercase letter (A-Z)")
    
    if not check_lowercase(password):
        requirements.append("At least one lowercase letter (a-z)")
    
    if not check_digits(password):
        requirements.append("At least one digit (0-9)")
    
    if not check_special_chars(password):
        requirements.append("At least one special character (@ # $ % ^ & * !)")
    
    return requirements


def get_met_requirements(password):
    """
    Returns a list of met password requirements.
    
    Args:
        password (str): The password to check
    
    Returns:
        list: List of passed requirement messages
    """
    requirements = []
    
    if check_length(password):
        requirements.append("Minimum 8 characters")
    
    if check_uppercase(password):
        requirements.append("At least one uppercase letter (A-Z)")
    
    if check_lowercase(password):
        requirements.append("At least one lowercase letter (a-z)")
    
    if check_digits(password):
        requirements.append("At least one digit (0-9)")
    
    if check_special_chars(password):
        requirements.append("At least one special character (@ # $ % ^ & * !)")
    
    return requirements
