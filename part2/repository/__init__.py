# repository/__init__.py

from repository.in_memory_repo import InMemoryRepository

# Singleton de stockage utilisé dans toute l'application
storage = InMemoryRepository()
