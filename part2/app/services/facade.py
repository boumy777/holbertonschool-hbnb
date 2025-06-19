# business/facade.py

from repository import storage
from business.models.user import User
from business.models.amenity import Amenity

# ───────────── USER ─────────────

def get_all_users():
    users = storage.all(User).values()
    return [user.to_dict(strip_password=True) for user in users]

def get_user(user_id):
    user = storage.get(User, user_id)
    return user.to_dict(strip_password=True) if user else None

def create_user(data):
    if not data.get("email") or not data.get("password"):
        raise ValueError("Missing email or password")
    user = User(**data)
    user.save()
    return user.to_dict(strip_password=True)

def update_user(user_id, data):
    user = storage.get(User, user_id)
    if not user:
        return None
    for field in ["email", "first_name", "last_name"]:
        if field in data:
            setattr(user, field, data[field])
    user.save()
    return user.to_dict(strip_password=True)

# ──────────── AMENITY ────────────

def get_all_amenities():
    amenities = storage.all(Amenity).values()
    return [a.to_dict() for a in amenities]

def get_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    return amenity.to_dict() if amenity else None

def create_amenity(data):
    if not data.get("name"):
        raise ValueError("Missing name")
    amenity = Amenity(**data)
    amenity.save()
    return amenity.to_dict()

def update_amenity(amenity_id, data):
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        return None
    if "name" in data:
        amenity.name = data["name"]
        amenity.save()
    return amenity.to_dict()
