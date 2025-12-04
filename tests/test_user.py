import unittest
from src.models.user import User

class TestUser(unittest.TestCase):
    def test_user_creation(self):
        user = User(user_id="u001", name="Alice")
        self.assertEqual(user.user_id, "u001")
        self.assertEqual(user.name, "Alice")
        self.assertEqual(user.borrowed_books, [])

if __name__ == "__main__":
    unittest.main()
