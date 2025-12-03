contacts = []

def add_contact():
    name = input("Enter name: ")
    phone = input("Enter phone number: ")

    contacts.append({"name": name, "phone": phone})
    print("Contact added successfully!\n")


def view_contacts():
    if not contacts:
        print("No contacts saved yet.\n")
        return

    print("\n--- Contact List ---")
    for idx, contact in enumerate(contacts, start=1):
        print(f"{idx}. {contact['name']} - {contact['phone']}")
    print()


def search_contact():
    name = input("Enter the name to search: ")
    found = False

    for contact in contacts:
        if contact["name"].lower() == name.lower():
            print(f"Found: {contact['name']} - {contact['phone']}\n")
            found = True
            break

    if not found:
        print("Contact not found.\n")


def delete_contact():
    name = input("Enter the name to delete: ")

    for contact in contacts:
        if contact["name"].lower() == name.lower():
            contacts.remove(contact)
            print("Contact deleted successfully!\n")
            return

    print("Contact not found.\n")


while True:
    print("----- CONTACT BOOK -----")
    print("1. Add Contact")
    print("2. View Contacts")
    print("3. Search Contact")
    print("4. Delete Contact")
    print("5. Exit")

    choice = input("Choose an option (1-5): ")

    if choice == "1":
        add_contact()
    elif choice == "2":
        view_contacts()
    elif choice == "3":
        search_contact()
    elif choice == "4":
        delete_contact()
    elif choice == "5":
        print("Exiting Contact Book...")
        break
    else:
        print("Invalid choice! Try again.\n")
