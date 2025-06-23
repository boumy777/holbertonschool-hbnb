import unittest
from app.models.user import User

class TestUser(unittest.TestCase):
    def test_instance(self):
        u = User()
        self.assertIsInstance(u, User)

    def test_attributes(self):
        u = User(name="Alice", email="alice@example.com")
        self.assertEqual(u.name, "Alice")
        self.assertEqual(u.email, "alice@example.com")

if __name__ == "__main__":
    unittest.main()

