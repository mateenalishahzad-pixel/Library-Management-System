import unittest
from src.models.book import Book

class TestBook(unittest.TestCase):
    def test_book_creation(self):
        book = Book(isbn="1234567890", title="Python 101", author="John Doe", publication_year=2020)
        self.assertEqual(book.title, "Python 101")
        self.assertEqual(book.author, "John Doe")
        self.assertEqual(book.isbn, "1234567890")
        self.assertEqual(book.publication_year, 2020)
        self.assertTrue(book.available)

if __name__ == "__main__":
    unittest.main()
