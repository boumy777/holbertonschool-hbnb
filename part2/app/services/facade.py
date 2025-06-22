# business/facade.py

from repository import storage
from app.models.user import User
from app.models.amenity import Amenity
from app.models.review import Review
from app.models.base_model import to_dict


class HBNBFacade:
    # ───────────── USER ─────────────

    def get_all_users(self):
        users = storage.all(User).values()
        return [user.to_dict(strip_password=True) for user in users]

    def get_user(self, user_id):
        user = storage.get(User, user_id)
        return user.to_dict(strip_password=True) if user else None

    def create_user(self, data):
        if not data.get("email") or not data.get("password"):
            raise ValueError("Missing email or password")
        user = User(**data)
        user.save()
        return user.to_dict(strip_password=True)

    def update_user(self, user_id, data):
        user = storage.get(User, user_id)
        if not user:
            return None
        for field in ["email", "first_name", "last_name"]:
            if field in data:
                setattr(user, field, data[field])
        user.save()
        return user.to_dict(strip_password=True)

    # ──────────── AMENITY ────────────

    def get_all_amenities(self):
        amenities = storage.all(Amenity).values()
        return [a.to_dict() for a in amenities]

    def get_amenity(self, amenity_id):
        amenity = storage.get(Amenity, amenity_id)
        return amenity.to_dict() if amenity else None

    def create_amenity(self, data):
        if not data.get("name"):
            raise ValueError("Missing name")
        amenity = Amenity(**data)
        amenity.save()
        return amenity.to_dict()

    def update_amenity(self, amenity_id, data):
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            return None
        if "name" in data:
            amenity.name = data["name"]
            amenity.save()
        return amenity.to_dict()

    # ──────────── PLACE ────────────

    def create_place(self, place_data):
        pass

    def get_place(self, place_id):

        pass

    def get_all_places(self):

        pass

    def update_place(self, place_id, place_data):

        pass

    def delete_place(self, place_id):

        pass

    # ──────────── REVIEW ────────────

    #Create a new review, ensuring all required fields are present and valid.
    def create_review(self, review_data):

        # Fields required for a review
        required_fields = ['text','rating','place_id','user_id']

        # Check if all required fields are present and valid
        for field in required_fields:
            if field not in review_data:
                raise ValueError("Missing required field: {}".format(field))
            
        # Verify the types and values of the fields
        if not isinstance(review_data['text'], str) or review_data['text'] == "":
            raise ValueError("Text must be a non-empty string")
        
        # Check if rating is an integer between 1 and 5
        if not isinstance(review_data['rating'], int):
            raise ValueError("Rating must be an integer")
        if review_data['rating'] < 1 or review_data['rating'] > 5:
            raise ValueError("Rating must be between 1 and 5")
        
        # Check if place_id and user_id are non-empty strings
        # List of fields that should be non-empty strings
        id_fields = ['place_id', 'user_id']

        # Ensure place_id and user_id are non-empty strings
        for field in id_fields:
            if not isinstance(review_data[field], str) or review_data[field] == "":
                raise ValueError("{} must be a non-empty string".format(field))
            
        # Verify that place_id and user_id exist in the database
        place = storage.get('Place', review_data['place_id'])
        if not place:
            raise ValueError("Place with ID {} does not exist".format(review_data['place_id']))
        user = storage.get('User', review_data['user_id'])
        if not user:
            raise ValueError("User with ID {} does not exist".format(review_data['user_id']))

    # Create a new review and return it as a dictionary.
    def get_review(self, review_id):
        all_reviews = storage.all(Review) # Retrieve all reviews from storage
        for rev in all_reviews.values():
            if rev.id == review_id:
                return rev.to_dict()
        return None

    # Create a new review who takes all review_data and returns the review as a dictionary.
    def get_all_reviews(self):
        reviews_storage = storage.all(Review).values()  # Retrieve all reviews from storage without filtering
        if not reviews_storage:
            return [] # return an empty list
        return [review.to_dict() for review in reviews_storage]

    def get_reviews_by_place(self, place_id):
        all_reviews = storage.all(Review)
        similar_reviews = [] # Retrieve all reviews from storage
        for review in all_reviews.values():
            if review.place_id == place_id:
                similar_reviews.append(review.to_dict()) # append == ajouter the review to the list if it matches the place_id
        return similar_reviews

    # Update an existing review by its ID, ensuring the review exists and the data is valid.
    def update_review(self, review_id, review_data):
        all_reviews = storage.all(Review)
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
    
    # Delete a review by its ID, ensuring the review exists before deletion.
    def delete_review(self, review_id):
        all_reviews = storage.all(Review)
        for review in all_reviews.values():
            if review.id == review_id:
                storage.delete(review) # Delete the review from storage
                storage.save()  # Save changes to storage
                return review.to_dict()
        return None  # Return None if the review was not found