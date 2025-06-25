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

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        user.update(user_data)
        return user
    # ___________ Amenity ___________
    
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
    # ___________ Place ___________

    def create_place(self, place_data):
        # Vérifie que l'owner_id est bien lié à un utilisateur existant
        owner_id = place_data.get("owner_id")
        if not owner_id or not self.user_repo.get(owner_id):
            raise ValueError(f"Owner with ID {owner_id} does not exist")

        try:
            place = Place(**place_data)
        except ValueError as e:
            raise ValueError(f"Invalid place data: {e}")

        self.place_repo.add(place)
        return place.to_dict()

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

    # Create a review with the given data and return it as a dictionary
    def create_review(self, review_data):
        # Validate required fields for review creation
        required_fields = ['text', 'rating', 'place_id', 'user_id']

        # Ensure all required fields are present in review_data
        for field in required_fields:
            if field not in review_data:
                raise ValueError(f"Missing required field: {field}")

        # Create the Review object and save it
        review = Review(**review_data)
        self.review_repo.add(review)
        storage.save(review)

        # Return the created review as a dictionary
        return review.to_dict()

    # Retrieve a review by its ID, including associated user and place
    def get_review(self, review_id):
        all_reviews = storage.all(Review)
        for review in all_reviews.values():
            if review.id == review_id:
                return review.to_dict()

    # Retrieve all reviews, including associated users and places
    def get_all_reviews(self):
        reviews_storage = storage.all(Review).values()  # Retrieve all reviews from storage without filtering
        if not reviews_storage:
            return [] # return an empty list
        return [review.to_dict() for review in reviews_storage]

    # Retrieve all reviews for a specific place by its ID
    def get_reviews_by_place(self, place_id):
        all_reviews = storage.all(Review)
        similar_reviews = [] # Retrieve all reviews from storage
        for review in all_reviews.values():
            if review.place_id == place_id:
                similar_reviews.append(review.to_dict()) # append == ajouter the review to the list if it matches the place_id
        return similar_reviews

    # Update a review by its ID and return the updated review as a dictionary
    def update_review(self, review_id, review_data):
        all_reviews = storage.all(Review) # Retrieve all reviews from storage
        for review in all_reviews.values():
            if review.id == review_id:
                review.text = review_data.get('text', review.text)
                review.rating = review_data.get('rating', review.rating)

                # Validate the review data before saving
                if not isinstance(review.text, str) or review.text == "":
                    raise ValueError("Text must be a non-empty string")
                if not isinstance(review.rating, int):
                    raise ValueError("Rating must be an integer")
                if review.rating < 1 or review.rating > 5:
                    raise ValueError("Rating must be between 1 and 5")
                
        # Save the updated review
        storage.save()
        # Return the updated review as a dictionary if it exists else return None
        return review.to_dict() if review else None

    # Delete a review by its ID
    def delete_review(self, review_id):

        all_reviews = storage.all(Review) # Retrieve all reviews from storage

        for review in all_reviews.values():
            if review.id == review_id:
                storage.delete(review) # Delete the review from storage
                storage.save()  # Save changes to storage
                return review.to_dict() # Convert the review to a dictionary and return it
        return None  # Return None if the review was not found

facade = HBnBFacade()
