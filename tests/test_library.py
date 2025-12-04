import unittest
from src.models.book import Book
from src.models.user import User
from src.services.library import Library

class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.library = Library()
        self.book = Book(isbn="111", title="Data Structures", author="Jane Smith", publication_year=2021)
        self.user = User(user_id="u002", name="Bob")
        self.library.add_book(self.book)
        self.library.register_user(self.user)

    def test_add_book(self):
        self.assertIn("111", self.library.books)

    def test_register_user(self):
        self.assertIn("u002", self.library.users)

    def test_borrow_and_return_book(self):
        self.assertTrue(self.library.borrow_book("u002", "111"))
        self.assertFalse(self.book.available)
        self.assertIn("111", self.user.borrowed_books)
        self.assertTrue(self.library.return_book("u002", "111"))
        self.assertTrue(self.book.available)
        self.assertNotIn("111", self.user.borrowed_books)

    def test_search_books(self):
        results = self.library.search_books("data")
        self.assertGreaterEqual(len(results), 1)
        self.assertEqual(results[0].title, "Data Structures")

if __name__ == "__main__":
    unittest.main()
