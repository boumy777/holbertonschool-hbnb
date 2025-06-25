from app.models.base_model import BaseModel

class Review(BaseModel):
    def __init__(self, text, place_id, user_id, rating=0):
        super().__init__()
        # Validate text, must be a non-empty string
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Text must be a non-empty string")
        
        # Validate place_id, must be a non-empty string
        if not isinstance(place_id, str) or not place_id.strip():
            raise ValueError("Place ID must be a non-empty string")

        # Validate user_id, must be a non-empty string
        if not isinstance(user_id, str) or not user_id.strip():
            raise ValueError("User ID must be a non-empty string")
        
        # Validate rating, must be an integer and between 1 and 5
        if not isinstance(rating, int):
            raise TypeError("Rating must be an integer")
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        
        # Initialize attributes
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id