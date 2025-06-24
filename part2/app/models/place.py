from app.models import user
from app.models import storage
from app.models.base_model import BaseModel
from exo8 import User
class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()
        # Validate if title is a non-empty string
        if not title or not isinstance(title, str):
            raise ValueError("Title must be a non-empty string")
        if len(title) > 100:
            raise ValueError("Title must not exceed 100 characters")
        
        # Validate if description is a non-empty string
        if not description or not isinstance(description, str):
            raise ValueError("Description must be a non-empty string")
        
        # Validate if price is a non-negative number
        if not owner_id or not isinstance(owner_id, str):
            raise ValueError("Owner ID must be a non-empty string")

        # Initialize attributes with validation
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id

        # Initialize additional attributes
        self.amenities = [] # List to hold amenities associated with the place
        self.reviews = []  # List to hold reviews associated with the place

    # ----------- Propriété : price -----------

    @property
    def price(self):
        # Price should be a private attribute to ensure encapsulation
        return self._price

    @price.setter
    def price(self, value):
        # Validate if price is a number and non-negative
        if not isinstance(value, (int, float)):
            raise ValueError("Price must be a number")
        if value < 0:
            raise ValueError("Price must be a non-negative number")
        self._price = float(value)

    # ----------- Propriété : latitude -----------

    @property
    def latitude(self):
        # Latitude should be a private attribute to ensure encapsulation
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        # Validate if latitude is a float and within the valid range
        if not isinstance(value, float):
            raise ValueError("Latitude must be a float")
        if not (-90 <= value <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        self._latitude = value

    # ----------- Propriété : longitude -----------

    @property
    def longitude(self):
        # Longitude should be a private attribute to ensure encapsulation
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        # Validate if longitude is a float and within the valid range
        if not isinstance(value, float):
            raise ValueError("Longitude must be a float")
        if not (-180 <= value <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        self._longitude = value

    # ----------- Propriété : owner_id -----------

    @property
    def owner_id(self):
        # Owner ID should be a private attribute to ensure encapsulation
        return self._owner_id

    @owner_id.setter
    def owner_id(self, value):
        # Validate if owner_id is a non-empty string
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Owner ID must be a non-empty string")
        
        # Check if the owner_id refers to an existing User
        if not storage.get(User, value):
            raise ValueError("Owner with ID {} does not exist".format(value))
        self._owner_id = value

    # ----------- Méthodes : Gestion des avis et des équipements -----------

    def add_review(self, review):
        # Add a review to the place.
        self.reviews.append(review)

    def add_amenity(self, amenity):
        # Add an amenity to the place.
        self.amenities.append(amenity)
