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
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

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
    # Placeholder for logic to create a review, including validation for user_id, place_id, and rating
        pass

    def get_review(self, review_id):
        # Placeholder for logic to retrieve a review by ID
        pass

    def get_all_reviews(self):
        # Placeholder for logic to retrieve all reviews
        pass

    def get_reviews_by_place(self, place_id):
        # Placeholder for logic to retrieve all reviews for a specific place
        pass

    def update_review(self, review_id, review_data):
        # Placeholder for logic to update a review
        pass

    def delete_review(self, review_id):
        # Placeholder for logic to delete a review
        pass
