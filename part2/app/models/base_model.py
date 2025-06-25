import uuid
from datetime import datetime

class BaseModel:
    def __init__(self, id=None, created_at=None, updated_at=None):
        # Initialize a new BaseModel instance
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def save(self):
        # Simulate saving the model to a database
        self.updated_at = datetime.utcnow()

    def update(self, data):
        # Update the model's attributes with the provided data
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def to_dict(self):
        # Convert the model's attributes to a dictionary
        return self.__dict__
