# app/persistence/repository.py

class InMemoryRepository:
    def __init__(self):
        self._data = {}

    def save(self, obj):
        key = f"{obj.__class__.__name__}.{obj.id}"
        self._data[key] = obj

    def get(self, model_cls, obj_id):
        key = f"{model_cls.__name__}.{obj_id}"
        return self._data.get(key)

    def all(self, model_cls):
        return {
            key: obj
            for key, obj in self._data.items()
            if key.startswith(f"{model_cls.__name__}.")
        }

    def delete(self, model_cls, obj_id):
        key = f"{model_cls.__name__}.{obj_id}"
        return self._data.pop(key, None)

# 👇 Instance globale
storage = InMemoryRepository()
