from app.models.base_model import BaseModel

class Place(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = kwargs.get('title', "")
        self.description = kwargs.get('description', "")
        self.price = kwargs.get('price', 0.0)
        self.latitude = kwargs.get('latitude', 0.0)
        self.longitude = kwargs.get('longitude', 0.0)
        self.owner_id = kwargs.get('owner_id', "")

