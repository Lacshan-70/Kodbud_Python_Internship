def get_user_input():
    """
    Collects user input for the calculator operation.
    Displays menu options and prompts for operation choice and two operands.
    
    Returns:
        tuple: (choice, num1, num2) where choice is the operation selection (1-5)
               and num1, num2 are the operands. Returns (None, None, None) if user
               chooses to exit.
    """
    print("\n--- Simple Calculator ---")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")
    print("5. Exit")

    choice = input("Enter choice (1-5): ")

    if choice == '5':
        print("Exiting...")
        return None, None, None

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
