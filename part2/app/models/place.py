import uuid
from uuid import UUID
from datetime import datetime

class Place:
    def __init__(self, title, description, price, latitude, longitude, created_at, updated_at, id=None, owner_id=None):
        if id is None:
            self.id = uuid.uuid4()
        else:
            self.id = UUID(id)
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self._created_at = datetime.utcnow()
        self._updated_at = datetime.utcnow()
        if owner_id is None:
            raise ValueError("Invalid owner_id")
        else:
            self.owner_id = UUID(owner_id)
    @property
    def price(self):
        return (self._price)
    @price.setter
    def price(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError("Price must be a float")
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = value

    @property
    def latitude(self):
        return (self._latitude)
    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, float):
            raise TypeError("Latitude must be a float")
        if value < -90 or value > 90:
            raise ValueError("Latitude must be between -90 and 90")
        self._latitude = value

    @property
    def longitude(self):
        return (self._longitude)
    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, float):
            raise TypeError("Longitude must be a float")
        if value < -180 or value > 180:
            raise ValueError("Longitude must be between -180 and 180")
        self._longitude = value
    
    @property
    def created_at(self):
        return self._created_at

    @property
    def updated_at(self):
        return self._updated_at

    def create_place(self, place_data):

    def get_place(self, place_id):

    pass

    def get_all_places(self):

    pass

    def update_place(self, place_id, place_data):

    pass