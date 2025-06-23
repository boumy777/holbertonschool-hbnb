import unittest
from app.models.place import Place

class TestPlace(unittest.TestCase):
    def test_instance(self):
        p = Place()
        self.assertIsInstance(p, Place)

    def test_attributes(self):
        p = Place(name="Paris", description="City of Light")
        self.assertEqual(p.name, "Paris")
        self.assertEqual(p.description, "City of Light")

if __name__ == "__main__":
    unittest.main()

