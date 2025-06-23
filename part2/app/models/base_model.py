
# business/models/base_model.py

import uuid
from datetime import datetime
from app.persistence.repository import storage


class BaseModel:
    """Classe de base commune à toutes les entités"""

    def __init__(self, *args, **kwargs):
        """Initialise l'objet avec UUID et timestamps"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

        for key, value in kwargs.items():
            if key not in ('id', 'created_at', 'updated_at'):
                setattr(self, key, value)

    def save(self):
        """Met à jour l'objet et le sauvegarde en mémoire"""
        self.updated_at = datetime.utcnow()
        storage.save(self)

    def to_dict(self, strip_password=False):
        """Convertit l'objet en dict pour JSON"""
        result = self.__dict__.copy()
        result['created_at'] = self.created_at.isoformat()
        result['updated_at'] = self.updated_at.isoformat()

        if strip_password and 'password' in result:
            del result['password']

        return result
