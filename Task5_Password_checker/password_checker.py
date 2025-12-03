import re

password = input("Enter a password to check its strength: ")

# Conditions for strong password
length_condition = len(password) >= 8
upper_condition = re.search(r"[A-Z]", password)
lower_condition = re.search(r"[a-z]", password)
digit_condition = re.search(r"[0-9]", password)
special_condition = re.search(r"[@#$%^&*!]", password)

if length_condition and upper_condition and lower_condition and digit_condition and special_condition:
    print("✔ Strong Password")
else:
    print("❌ Weak Password")

    print("\nRequirements for a Strong Password:")
    print("- Minimum 8 characters")
    print("- At least one uppercase letter (A-Z)")
    print("- At least one lowercase letter (a-z)")
    print("- At least one digit (0-9)")
    print("- At least one special character (@ # $ % ^ & * !)")
