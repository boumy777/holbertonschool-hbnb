import re
import uuid
from datetime import datetime


class User(BaseModel):
    EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")

    def __init__(self, first_name: str, last_name: str, email: str, is_admin: bool = False):
        super().__init__()

        # Validation des champs
        self.first_name = None
        self.last_name = None
        self.email = None
        self.is_admin = is_admin

        self.set_first_name(first_name)
        self.set_last_name(last_name)
        self.set_email(email)

    def set_first_name(self, first_name: str):
        if not first_name or not isinstance(first_name, str):
            raise ValueError("first_name est requis et doit être une chaîne.")
        if len(first_name) > 50:
            raise ValueError("first_name ne peut pas dépasser 50 caractères.")
        self.first_name = first_name

    def set_last_name(self, last_name: str):
        if not last_name or not isinstance(last_name, str):
            raise ValueError("last_name est requis et doit être une chaîne.")
        if len(last_name) > 50:
            raise ValueError("last_name ne peut pas dépasser 50 caractères.")
        self.last_name = last_name

    def set_email(self, email: str):
        if not email or not isinstance(email, str):
            raise ValueError("email est requis et doit être une chaîne.")
        if len(email) > 254:
            raise ValueError("email est trop long.")
        if not User.EMAIL_REGEX.match(email):
            raise ValueError("email n'est pas dans un format valide.")
        self.email = email

    def update(self, data: dict):
        """Surcharge la méthode update pour valider les champs."""
        if "first_name" in data:
            self.set_first_name(data["first_name"])
        if "last_name" in data:
            self.set_last_name(data["last_name"])
        if "email" in data:
            self.set_email(data["email"])
        if "is_admin" in data:
            self.is_admin = bool(data["is_admin"])

        self.save()
