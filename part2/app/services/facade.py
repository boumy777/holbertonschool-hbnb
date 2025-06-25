from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ========== Génériques ==========

    def get(self, model_name, obj_id):
        repo_map = {
            "User": self.user_repo,
            "Place": self.place_repo,
            "Review": self.review_repo,
            "Amenity": self.amenity_repo
        }
        repo = repo_map.get(model_name)
        if not repo:
            raise ValueError(f"Unknown model: {model_name}")
        obj = repo.get(obj_id)
        return obj.to_dict() if obj else None

    def update(self, model_name, obj_id, data):
        repo_map = {
            "User": self.user_repo,
            "Place": self.place_repo,
            "Review": self.review_repo,
            "Amenity": self.amenity_repo
        }
        repo = repo_map.get(model_name)
        if not repo:
            raise ValueError(f"Unknown model: {model_name}")

        obj = repo.get(obj_id)
        if not obj:
            return None
        for key, value in data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        return obj.to_dict()

    # ========== Users ==========

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        user.update(user_data)
        return user

    # ========== Amenities ==========

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        amenity.update(amenity_data)
        return amenity

    # ========== Places ==========

    def create_place(self, place_data):
        owner_id = place_data.get("owner_id")
        if not owner_id or not self.user_repo.get(owner_id):
            raise ValueError(f"Owner with ID {owner_id} does not exist")

        place = Place(**place_data)
        self.place_repo.add(place)
        return place.to_dict()

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        return place.to_dict() if place else None

    def get_all_places(self):
        return [p.to_dict() for p in self.place_repo.get_all()]

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        for key, value in place_data.items():
            if hasattr(place, key):
                setattr(place, key, value)
        return place.to_dict()

    # ========== Reviews ==========

    def create_review(self, review_data):
        required_fields = ['text', 'rating', 'place_id', 'user_id']
        for field in required_fields:
            if field not in review_data:
                raise ValueError(f"Missing required field: {field}")

        review = Review(**review_data)
        self.review_repo.add(review)
        return review.to_dict()

    def get_review(self, review_id):
        review = self.review_repo.get(review_id)
        return review.to_dict() if review else None

    def get_all_reviews(self):
        return [r.to_dict() for r in self.review_repo.get_all()]

    def get_reviews_by_place(self, place_id):
        reviews = self.review_repo.get_all()
        return [r.to_dict() for r in reviews if r.place_id == place_id]

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        review.text = review_data.get('text', review.text)
        review.rating = review_data.get('rating', review.rating)

        # Validations
        if not isinstance(review.text, str) or review.text == "":
            raise ValueError("Text must be a non-empty string")
        if not isinstance(review.rating, int) or not (1 <= review.rating <= 5):
            raise ValueError("Rating must be between 1 and 5")

        return review.to_dict()

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if review:
            self.review_repo.delete(review_id)
            return review.to_dict()
        return None

# Facade globale
facade = HBnBFacade()
