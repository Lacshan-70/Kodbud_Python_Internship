"""
================================================================================
                        SIMPLE CALCULATOR PROGRAM
================================================================================

PROGRAM DESCRIPTION:
    This is an interactive calculator application that performs basic arithmetic
    operations. Users can select from various mathematical operations and input
    two operands to get the calculated result. The program continues to run until
    the user chooses to exit.

SUPPORTED OPERATIONS:
    1. Addition        - Adds two numbers (a + b)
    2. Subtraction     - Subtracts second number from first (a - b)
    3. Multiplication  - Multiplies two numbers (a × b)
    4. Division        - Divides first number by second (a ÷ b)
                         * Includes zero-division error handling
    5. Exit            - Terminates the program

FEATURES:
    • User-friendly menu interface
    • Input validation for numeric values
    • Error handling for division by zero
    • Continuous operation until user chooses to exit
    • User confirmation after each calculation

DEVELOPED BY: Lacshan Shakthivel (student ID: 24MZ301)
College Name: St.Josephs College of Engineering
DATE: December 3, 2025
PROJECT: Kodbud Internship Dec 2025 - Python Programming

================================================================================
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


def get_user_input():
    """
    Collects user input for the calculator operation.
    Displays menu options and prompts for operation choice and two operands.
    Validates choice before requesting numeric inputs.
    
    Returns:
        tuple: (choice, num1, num2) where choice is the operation selection (1-5)
               and num1, num2 are the operands. Returns (None, None, None) if user
               chooses to exit or enters invalid choice.
    """
    print("\n--- Simple Calculator ---")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")
    print("5. Exit")

    while True:
        choice = input("Enter choice (1-5): ")
        
        if validate_choice(choice):
            if choice == '5':
                print("Exiting...")
                return None, None, None
            break
        else:
            print("❌ Invalid choice! Please enter a number between 1 and 5.")

    try:
        a = float(input("Enter first number: "))
        b = float(input("Enter second number: "))
        return choice, a, b
    except ValueError:
        print("Invalid input! Please enter valid numbers.")
        return None, None, None


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


def ask_continue():
    """
    Prompts the user to continue or end the program after a calculation.
    
    Returns:
        bool: True if user wants to continue, False if user wants to exit
    """
    while True:
        response = input("\nDo you want to continue? (yes/no): ").strip().lower()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            print("Thank you for using the calculator!")
            return False
        else:
            print("Invalid input! Please enter 'yes' or 'no'.")


def calculator():
    """
    Main calculator function that orchestrates user input and calculations.
    Calls get_user_input() to collect input and perform_calculation() to process it.
    After calculation, asks the user if they want to continue.
    
    Returns:
        bool: True to continue the calculator loop, False to exit
    """
    choice, num1, num2 = get_user_input()
    
    if choice is None:
        return False
    
    perform_calculation(choice, num1, num2)
    return ask_continue()


while True:
    running = calculator()
    if not running:
        break
