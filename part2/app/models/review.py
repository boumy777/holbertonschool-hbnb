from app.models.base_model import BaseModel
from app.models.place import Place
from app.models.user import User


class Review(BaseModel):
    def __init__(self, text, place_id, user_id, rating=0):
        super().__init__()

        # Validate text, must be a non-empty string
        if not isinstance(text, str) or not text.strip(): # strip() removes leading and trailing whitespace
            raise ValueError("Text must be a non-empty string")
        self.text = text

        # Validate attributes
        self.place_id = place_id
        self.user_id = user_id
        self.rating = rating

    @property
    def rating(self):
        # Rating should be a private attribute to ensure encapsulation
        return self._rating

    @rating.setter
    def rating(self, value):
        # Validate if rating is an integer
        if not isinstance(value, int):
            raise TypeError("Rating must be an integer")
        # Validate if rating is between 1 and 5
        if not (1 <= value <= 5):
            raise ValueError("Rating must be between 1 and 5")
        self._rating = value

    @property
    def place_id(self):
        # Place ID should be a private attribute to ensure encapsulation
        return self._place_id

    @place_id.setter
    def place_id(self, value):
        # Validate if place_id is a non-empty string
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Place ID must be a non-empty string")
        # Validate if place_id refers to an existing Place
        if not storage.get(Place, value):
            raise ValueError("Place ID must refer to an existing Place")
        self._place_id = value

    @property
    def user_id(self):
        # User ID should be a private attribute to ensure encapsulation
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        # Validate if user_id is a non-empty string and refers to an existing User
        if not isinstance(value, str) or not value.strip():
            raise ValueError("User ID must be a non-empty string")
        if not storage.get(User, value):
            raise ValueError("User ID must refer to an existing User")
        self._user_id = value
