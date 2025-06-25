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
    
    # ___________ User ___________

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

    def update(amenity_id, data):
        amenity = storage.get(Amenity, amenity_id)
        if amenity:
            amenity.update(data)
            storage.save(amenity)
        return amenity

    def delete(amenity_id):
        return storage.delete(Amenity, amenity_id)


    # ___________ Place ___________

    def create_place(self, place_data):
    # Placeholder for logic to create a place, including validation for price, latitude, and longitude
        pass

    def get_place(self, place_id):
        # Placeholder for logic to retrieve a place by ID, including associated owner and amenities
        pass

    def get_all_places(self):
        # Placeholder for logic to retrieve all places
        pass

    def update_place(self, place_id, place_data):
        # Placeholder for logic to update a place
        pass
    
    # ___________ Review ___________

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
