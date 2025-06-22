from app.models.base_model import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()
        # Validate inputs
        if not title or not isinstance(title, str):
            raise ValueError("Title must be a non-empty string")
        
        # Validate description, must be a non-empty string
        if not description or not isinstance(description, str):
            raise ValueError("Description must be a non-empty string")
        
        # Validate price, must be a number and non-negative
        if not isinstance(price, (int, float)):
            raise ValueError("Price must be a number")
        if price < 0:
            raise ValueError("Price must be a non-negative number")
        
        # Validate latitude and longitude, must be floats
        if not isinstance(latitude, float):
            raise ValueError("Latitude must be a float")
        if latitude < -90 or latitude > 90:
            raise ValueError("Latitude must be between -90 and 90")

        # Validate longitude, must be a float
        if not isinstance(longitude, float):
            raise ValueError("Longitude must be a float")
        if longitude < -180 or longitude > 180:
            raise ValueError("Longitude must be between -180 and 180")

        # Validate owner_id, must be a non-empty string
        if not owner_id or not isinstance(owner_id, str):
            raise ValueError("Owner ID must be a non-empty string")

        # Initialize attributes
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.amenities = []
