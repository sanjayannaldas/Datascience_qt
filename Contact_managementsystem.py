# Define the Contact class
class Contact:
    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email

    def __str__(self):
        return f"Name: {self.name}, Phone: {self.phone}, Email: {self.email}"

# Define the ContactManager class
class ContactManager:
    def __init__(self):
        self.contacts = []

    def add_contact(self, contact):
        self.contacts.append(contact)
        print(f"Contact '{contact.name}' added successfully.")

    def remove_contact(self, name):
        for contact in self.contacts:
            if contact.name.lower() == name.lower():
                self.contacts.remove(contact)
                print(f"Contact '{contact.name}' removed successfully.")
                return
        print("Contact not found.")

    def search_contact(self, name):
        found_contacts = [contact for contact in self.contacts if name.lower() in contact.name.lower()]
        if found_contacts:
            print("Search results:")
            for contact in found_contacts:
                print(contact)
        else:
            print("No contacts found with that name.")

    def list_contacts(self):
        if self.contacts:
            print("Contact List:")
            for contact in self.contacts:
                print(contact)
        else:
            print("No contacts in the list.")

# Define the user interface
def main():
    contact_manager = ContactManager()
    while True:
        print("\nContact Management System")
        print("1. Add a contact")
        print("2. Remove a contact")
        print("3. Search for a contact")
        print("4. List all contacts")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter the name of the contact: ")
            phone = input("Enter the phone number of the contact: ")
            email = input("Enter the email of the contact: ")
            contact = Contact(name, phone, email)
            contact_manager.add_contact(contact)
        elif choice == '2':
            name = input("Enter the name of the contact to remove: ")
            contact_manager.remove_contact(name)
        elif choice == '3':
            name = input("Enter the name to search for: ")
            contact_manager.search_contact(name)
        elif choice == '4':
            contact_manager.list_contacts()
        elif choice == '5':
            print("Exiting the contact management system.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

