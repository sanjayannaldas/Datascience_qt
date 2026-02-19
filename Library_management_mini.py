def display_menu():
    print("\n===== Library Management Menu =====")
    print("1. Add Book")
    print("2. Display All Books")
    print("3. Borrow Book")
    print("4. Return Book")
    print("5. Remove Book")
    print("6. Search Book")
    print("7. Exit")

def add_book():
    book_id = input("Enter Book ID: ")
    title = input("Enter Book Title: ")
    author = input("Enter Author Name: ")
    with open("books.txt", "a") as f:
        f.write(f"{book_id},{title},{author},Available\n")
    print("Book added successfully!")

def display_books():
    try:
        with open("books.txt", "r") as f:
            print("\nBookID | Title | Author | Status")
            for line in f:
                print(" | ".join(line.strip().split(",")))
    except FileNotFoundError:
        print("No books found.")

def borrow_book():
    book_id = input("Enter Book ID to borrow: ")
    found = False
    updated_lines = []
    with open("books.txt", "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if parts[0] == book_id and parts[3] == "Available":
                parts[3] = "Borrowed"
                found = True
            updated_lines.append(",".join(parts))
    
    with open("books.txt", "w") as f:
        for line in updated_lines:
            f.write(line + "\n")
    
    if found:
        print("Book borrowed successfully!")
    else:
        print("Book not found or already borrowed.")

def return_book():
    book_id = input("Enter Book ID to return: ")
    found = False
    updated_lines = []
    with open("books.txt", "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if parts[0] == book_id and parts[3] == "Borrowed":
                parts[3] = "Available"
                found = True
            updated_lines.append(",".join(parts))

    with open("books.txt", "w") as f:
        for line in updated_lines:
            f.write(line + "\n")
    
    if found:
        print("Book returned successfully!")
    else:
        print("Book not found or already available.")

def remove_book():
    book_id = input("Enter Book ID to remove: ")
    removed = False
    with open("books.txt", "r") as f:
        lines = f.readlines()
    
    with open("books.txt", "w") as f:
        for line in lines:
            if line.split(",")[0] != book_id:
                f.write(line)
            else:
                removed = True

    if removed:
        print("Book removed.")
    else:
        print("Book not found.")

def search_book():
    keyword = input("Enter keyword to search (Title or Author): ").lower()
    with open("books.txt", "r") as f:
        print("\nSearch Results:")
        found = False
        for line in f:
            if keyword in line.lower():
                print(" | ".join(line.strip().split(",")))
                found = True
        if not found:
            print("No matching books found.")

# Main program
while True:
    display_menu()
    choice = input("Enter choice (1-7): ")
    
    if choice == '1':
        add_book()
    elif choice == '2':
        display_books()
    elif choice == '3':
        borrow_book()
    elif choice == '4':
        return_book()
    elif choice == '5':
        remove_book()
    elif choice == '6':
        search_book()
    elif choice == '7':
        print("Thank you! Exiting...")
        break
    else:
        print("Invalid choice. Try again.")


Method-II
Using SQLite

import sqlite3
# Connect to SQLite DB (creates file if not exists)
conn = sqlite3.connect('library.db')
cursor = conn.cursor()
# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS books (
    book_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    status TEXT DEFAULT 'Available'
)
''')
conn.commit()

PYCODE:
# Menu
def display_menu():
    print("\n===== Library Menu =====")
    print("1. Add Book")
    print("2. Display All Books")
    print("3. Borrow Book")
    print("4. Return Book")
    print("5. Remove Book")
    print("6. Search Book")
    print("7. Exit")

# Add Book
def add_book():
    book_id = input("Enter Book ID: ")
    title = input("Enter Title: ")
    author = input("Enter Author: ")
    try:
        cursor.execute("INSERT INTO books (book_id, title, author) VALUES (?, ?, ?)",
                       (book_id, title, author))
        conn.commit()
        print("Book added successfully!")
    except sqlite3.IntegrityError:
        print("Book ID already exists!")

# Display Books
def display_books():
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    print("\nBookID | Title | Author | Status")
    print("-"*40)
    for row in rows:
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")

# Borrow Book
def borrow_book():
    book_id = input("Enter Book ID to borrow: ")
    cursor.execute("SELECT status FROM books WHERE book_id=?", (book_id,))
    row = cursor.fetchone()
    if row:
        if row[0] == "Available":
            cursor.execute("UPDATE books SET status='Borrowed' WHERE book_id=?", (book_id,))
            conn.commit()
            print("Book borrowed.")
        else:
            print("Book already borrowed.")
    else:
        print("Book not found.")

# Return Book
def return_book():
    book_id = input("Enter Book ID to return: ")
    cursor.execute("SELECT status FROM books WHERE book_id=?", (book_id,))
    row = cursor.fetchone()
    if row:
        if row[0] == "Borrowed":
            cursor.execute("UPDATE books SET status='Available' WHERE book_id=?", (book_id,))
            conn.commit()
            print("Book returned.")
        else:
            print("Book is not borrowed.")
    else:
        print("Book not found.")

# Remove Book
def remove_book():
    book_id = input("Enter Book ID to remove: ")
    cursor.execute("DELETE FROM books WHERE book_id=?", (book_id,))
    if cursor.rowcount:
        conn.commit()
        print("Book removed.")
    else:
        print("Book not found.")

# Search Book
def search_book():
    keyword = input("Enter keyword (title/author): ")
    cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", 
                   ('%' + keyword + '%', '%' + keyword + '%'))
    rows = cursor.fetchall()
    if rows:
        print("\nSearch Results:")
        for row in rows:
            print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")
    else:
        print("No matching books found.")

# Main loop
while True:
    display_menu()
    choice = input("Enter choice (1-7): ")
    
    if choice == '1':
        add_book()
    elif choice == '2':
        display_books()
    elif choice == '3':
        borrow_book()
    elif choice == '4':
        return_book()
    elif choice == '5':
        remove_book()
    elif choice == '6':
        search_book()
    elif choice == '7':
        print("Goodbye!")
        break
    else:
        print("Invalid choice.")

# Close connection at end
conn.close()

