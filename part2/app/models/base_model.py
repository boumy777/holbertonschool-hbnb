import uuid
from datetime import datetime

class BaseModel:
    # BaseModel serves as a base class for all models in the application.
    def __init__(self, id, created_at=None, updated_at=None):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def save(self):
        # Update the updated_at attribute with the current datetime.
        self.updated_at = datetime.utcnow()

    def update(self, data):
        # Update the instance attributes with the provided data.
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def to_dict(self):
        # Convert the instance to a dictionary.
        return self.__dict__