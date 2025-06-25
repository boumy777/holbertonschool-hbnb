# app/persistence/repository.py

class InMemoryRepository:
    def __init__(self):
        self._data = {}

    def add(self, obj):
        self._data[obj.id] = obj

    def get(self, obj_id):
        return self._data.get(obj_id)

    def get_all(self):
        return list(self._data.values())

    def delete(self, obj_id):
        return self._data.pop(obj_id, None)

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
        return obj

    def get_by_attribute(self, attr_name, attr_value):
        for obj in self._data.values():
            if getattr(obj, attr_name, None) == attr_value:
                return obj
        return None
