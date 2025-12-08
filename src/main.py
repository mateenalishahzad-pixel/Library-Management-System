from models.book import Book
from models.user import User
from services.library import Library


def display_header():
    print("=" * 50)
    print("     Library Management System")
    print("=" * 50)


def main():
    display_header()
    library = Library()
    print("Welcome to the Library Management System!")
    while True:
        print("\nSelect an option:")
        print("1. Add Book")
        print("2. Register User")
        print("3. Search Book")
        print("4. Borrow Book")
        print("5. Return Book")
        print("6. View All Books")
        print("7. View Borrowed Books")
        print("8. View System Stats")
        print("0. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            isbn = input("ISBN: ").strip()
            title = input("Title: ").strip()
            author = input("Author: ").strip()
            year = int(input("Publication Year: ").strip())
            book = Book(isbn=isbn, title=title, author=author, publication_year=year)
            if library.add_book(book):
                print("Book added.")
            else:
                print("Book already exists.")
        elif choice == "2":
            user_id = input("User ID: ").strip()
            name = input("Name: ").strip()
            user = User(user_id=user_id, name=name)
            if library.register_user(user):
                print("User registered.")
            else:
                print("User already exists.")
        elif choice == "3":
            query = input("Search by title, author, or ISBN: ").strip()
            results = library.search_books(query)
            if results:
                for b in results:
                    print(b, "- Available" if b.available else "- Borrowed")
            else:
                print("No books found.")
        elif choice == "4":
            user_id = input("User ID: ").strip()
            isbn = input("Book ISBN: ").strip()
            if library.borrow_book(user_id, isbn):
                print("Book borrowed.")
            else:
                print("Cannot borrow book. Check availability or user ID.")
        elif choice == "5":
            user_id = input("User ID: ").strip()
            isbn = input("Book ISBN: ").strip()
            if library.return_book(user_id, isbn):
                print("Book returned.")
            else:
                print("Cannot return book. Check if user borrowed this book.")
        elif choice == "6":
            books = library.view_all_books()
            if books:
                for b in books:
                    print(b, "- Available" if b.available else "- Borrowed")
            else:
                print("No books in library.")
        elif choice == "7":
            user_id = input("User ID: ").strip()
            books = library.view_borrowed_books(user_id)
            if books:
                for b in books:
                    print(b)
            else:
                print("No borrowed books for this user.")
        elif choice == "8":
            total_books = len(library.books)
            total_users = len(library.users)
            available_books = sum(1 for b in library.books.values() if b.available)
            borrowed_books = total_books - available_books
            print("\nSystem Statistics:")
            print(f"Total Books: {total_books}")
            print(f"Available Books: {available_books}")
            print(f"Borrowed Books: {borrowed_books}")
            print(f"Total Users: {total_users}")
        elif choice == "0":
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
