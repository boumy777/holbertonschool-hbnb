from app.models.base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name, category, description="", available=True):
        self.name = name                # nom de l'amenity (ex: "WiFi")
        self.category = category        # catégorie (ex: "confort", "divertissement", etc.)
        self.description = description  # description facultative
        self.available = available      # booléen : disponible ou non
        super().__init__(id=None)       # appelle le constructeur de BaseModel

    def toggle_availability(self):
        """Inverse la disponibilité de l'amenity."""
        self.available = not self.available
        self.save()

    def to_dict(self):
        """Retourne un dictionnaire complet de l'amenity."""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "available": self.available,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

