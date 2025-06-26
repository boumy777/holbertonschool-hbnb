# repository/__init__.py
from app.persistence.repository import InMemoryRepository
from .repository import InMemoryRepository

user_repo = InMemoryRepository()
place_repo = InMemoryRepository()
review_repo = InMemoryRepository()
amenity_repo = InMemoryRepository()




# Singleton de stockage utilisé dans toute l'application
storage = InMemoryRepository()
