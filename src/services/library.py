from typing import Dict, List, Optional
from models.book import Book
from models.user import User

class Library:
    def __init__(self):
        self.books: Dict[str, Book] = {}  
        self.users: Dict[str, User] = {} 

    def add_book(self, book: Book) -> bool:
        if book.isbn in self.books:
            return False
        self.books[book.isbn] = book
        return True

    def register_user(self, user: User) -> bool:
        if user.user_id in self.users:
            return False
        self.users[user.user_id] = user
        return True

    def search_books(self, query: str) -> List[Book]:
        query = query.lower()
        return [
            book for book in self.books.values()
            if query in book.title.lower() or query in book.author.lower() or query in book.isbn
        ]

    def borrow_book(self, user_id: str, isbn: str) -> bool:
        if isbn not in self.books or user_id not in self.users:
            return False
        book = self.books[isbn]
        user = self.users[user_id]
        if not book.available:
            return False
        book.available = False
        user.borrowed_books.append(isbn)
        return True

    def return_book(self, user_id: str, isbn: str) -> bool:
        if isbn not in self.books or user_id not in self.users:
            return False
        book = self.books[isbn]
        user = self.users[user_id]
        if isbn not in user.borrowed_books:
            return False
        book.available = True
        user.borrowed_books.remove(isbn)
        return True

    def view_all_books(self) -> List[Book]:
        return list(self.books.values())

    def view_borrowed_books(self, user_id: str) -> List[Book]:
        if user_id not in self.users:
            return []
        user = self.users[user_id]
        return [self.books[isbn] for isbn in user.borrowed_books if isbn in self.books]
