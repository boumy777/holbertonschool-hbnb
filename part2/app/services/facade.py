from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository
from app.persistence.repository import user_repo, place_repo, review_repo, amenity_repo


class HBnBFacade:
    def __init__(self, user_repo, place_repo, review_repo, amenity_repo):
        self.user_repo = user_repo
        self.place_repo = place_repo
        self.review_repo = review_repo
        self.amenity_repo = amenity_repo

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
        user = self.user_repo.get(user_id)
        if user is None:
            raise ValueError(f"User with ID {user_id} not found.")
        return user

    def get_all_users(self):
        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)


    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found.")
        self.user_repo.update(user_id, user_data)
        return self.user_repo.get(user_id)    

     # ___________ Amenity ___________
    
    def get_all():
        return storage.all(Amenity)

    def get_by_id(amenity_id):
        return storage.get(Amenity, amenity_id)

    def create(data):
        new_amenity = Amenity()
        for key, value in data.items():
            if hasattr(new_amenity, key):
                setattr(new_amenity, key, value)
        storage.save(new_amenity)
        return new_amenity

    def update_amenities(self, amenity_id, data):
        amenity = storage.get(Amenity, amenity_id)
        if amenity:
            amenity.update(data)
            storage.save(amenity)
        return amenity

    def delete(amenity_id):
        return storage.delete(Amenity, amenity_id)


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

        # Validation des IDs user et place
        user = self.user_repo.get(review_data.get("user_id"))
        if not user:
            raise ValueError("User not found")

        place = self.place_repo.get(review_data.get("place_id"))
        if not place:
            raise ValueError("Place not found")

        rating = review_data.get("rating")
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")

        # Création de la review

        required_fields = ['text', 'rating', 'place_id', 'user_id']
        for field in required_fields:
            if field not in review_data:
                raise ValueError(f"Missing required field: {field}")

        review = Review(**review_data)
        self.review_repo.add(review)
        return review.to_dict()

    def get_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")
        return review.to_dict()

    def get_all_reviews(self):
        reviews = self.review_repo.get_all()
        return [review.to_dict() for review in reviews]

    def get_reviews_by_place(self, place_id):
        reviews = self.review_repo.get_by_attribute("place_id", place_id)
        return [review.to_dict() for review in reviews]

        return review.to_dict() if review else None

    def get_all_reviews(self):
        return [r.to_dict() for r in self.review_repo.get_all()]

    def get_reviews_by_place(self, place_id):
        reviews = self.review_repo.get_all()
        return [r.to_dict() for r in reviews if r.place_id == place_id]


    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:

            raise ValueError("Review not found")

        if "rating" in review_data:
            rating = review_data["rating"]
            if not isinstance(rating, int) or not (1 <= rating <= 5):
                raise ValueError("Rating must be an integer between 1 and 5")

        self.review_repo.update(review_id, review_data)
        updated_review = self.review_repo.get(review_id)
        return updated_review.to_dict()

    def delete_review(self, review_id):

        # Placeholder for logic to delete a review
        pass

        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")
        self.review_repo.delete(review_id)
        return {"message": "Review deleted successfully"}

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
facade = HBnBFacade(user_repo, place_repo, review_repo, amenity_repo)
