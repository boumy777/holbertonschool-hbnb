# business/models/amenity.py

from business.models.base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, *args, **kwargs):
        self.name = ""
        super().__init__(*args, **kwargs)
