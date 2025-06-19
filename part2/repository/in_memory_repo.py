# repository/in_memory_repo.py

import uuid
from datetime import datetime


class InMemoryRepository:
    """Stockage temporaire en mémoire"""

    __objects = {}

    def all(self, cls=None):
        if cls:
            return {
                k: v for k, v in self.__objects.items()
                if isinstance(v, cls)
            }
        return self.__objects.copy()

    def get(self, cls, obj_id):
        key = f"{cls.__name__}.{obj_id}"
        return self.__objects.get(key)

    def save(self, obj):
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def delete(self, obj):
        key = f"{obj.__class__.__name__}.{obj.id}"
        if key in self.__objects:
            del self.__objects[key]

