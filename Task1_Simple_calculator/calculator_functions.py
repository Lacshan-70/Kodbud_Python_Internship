"""
Calculator functions module - Contains all calculator logic functions
without the main execution loop.
"""


def validate_choice(choice):
    """
    Validates if the user's choice is valid (1-5).
    
    Args:
        choice (str): The user's input choice
    
    Returns:
        bool: True if choice is valid, False otherwise
    """
    try:
        choice_num = int(choice)
        return 1 <= choice_num <= 5
    except ValueError:
        return False


def perform_calculation(choice, num1, num2):
    """
    Performs the arithmetic operation based on the user's choice.
    Handles addition, subtraction, multiplication, and division operations.
    Includes error handling for division by zero.
    
    Args:
        choice (str): The operation choice ('1' for add, '2' for subtract, etc.)
        num1 (float): The first operand
        num2 (float): The second operand
    
    Returns:
        bool: True if calculation was successful, False if invalid input
    """
    if choice == '1':
        result = num1 + num2
        print("Result:", result)
    elif choice == '2':
        result = num1 - num2
        print("Result:", result)
    elif choice == '3':
        result = num1 * num2
        print("Result:", result)
    elif choice == '4':
        if num2 != 0:
            result = num1 / num2
            print("Result:", result)
        else:
            print("Cannot divide by zero!")
            return False
    else:
        print("Invalid choice!")
        return False
    
    return True
