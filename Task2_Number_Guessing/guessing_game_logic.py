"""
NUMBER GUESSING GAME - GAME LOGIC MODULE
=========================================

This module contains the core game logic for the Number Guessing Game,
separated from the interactive UI for easier testing.

FUNCTIONS:
    - validate_guess(guess_str): Validates if input is a valid number
    - compare_guess(guess, secret): Compares guess with secret number
    - play_game(secret_number, guess): Executes one round of game logic

DEVELOPED BY: Lacshan Shakthivel
DATE: December 3, 2025
"""


def validate_guess(guess_str):
    """
    Validates if the input is a valid positive integer.
    
    Args:
        guess_str (str): The user's input string
    
    Returns:
        tuple: (is_valid, guess_int) where is_valid is bool and guess_int is int or None
    """
    if not guess_str or not guess_str.strip():
        return False, None
    
    if not guess_str.isdigit():
        return False, None
    
    guess_int = int(guess_str)
    
    # Check if number is in valid range (1-100)
    if guess_int < 1 or guess_int > 100:
        return False, None
    
    return True, guess_int


def compare_guess(guess, secret_number):
    """
    Compares the guess with the secret number.
    
    Args:
        guess (int): The player's guess
        secret_number (int): The secret number to guess
    
    Returns:
        str: 'too_low', 'too_high', or 'correct'
    """
    if guess < secret_number:
        return 'too_low'
    elif guess > secret_number:
        return 'too_high'
    else:
        return 'correct'


def check_win_condition(guess, secret_number):
    """
    Checks if the player has won (guessed correctly).
    
    Args:
        guess (int): The player's guess
        secret_number (int): The secret number
    
    Returns:
        bool: True if guess equals secret_number, False otherwise
    """
    return guess == secret_number
