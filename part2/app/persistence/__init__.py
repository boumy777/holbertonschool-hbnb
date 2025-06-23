# repository/__init__.py

from .repository import InMemoryRepository

# Singleton de stockage utilisé dans toute l'application
storage = InMemoryRepository()
