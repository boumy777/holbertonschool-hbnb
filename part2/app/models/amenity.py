# app/models/amenity.py

from app.models.base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name="", id=None, created_at=None, updated_at=None):
        super().__init__(id, created_at, updated_at)
        self.name = name

