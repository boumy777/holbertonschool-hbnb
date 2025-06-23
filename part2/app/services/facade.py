from app.models import user, place, review, amenity
from app.persistence.repository import storage


class Facade:
    def __init__(self):
        self.storage = storage
        self.model_map = {
            "User": user.User,
            "Place": place.Place,
            "Review": review.Review,
	    "Amenity": amenity.Amenity,

        }

    def create(self, model_name, data):
        model_cls = self.model_map.get(model_name)
        if not model_cls:
            raise ValueError("Invalid model name")

        obj = model_cls(**data)
        self.storage.save(obj)
        return obj.to_dict()

    def get_all(self, model_name):
        model_cls = self.model_map.get(model_name)
        if not model_cls:
            raise ValueError("Invalid model name")

        return [obj.to_dict() for obj in self.storage.all(model_cls).values()]

    def get_by_id(self, model_name, obj_id):
        model_cls = self.model_map.get(model_name)
        if not model_cls:
            raise ValueError("Invalid model name")

        obj = self.storage.get(model_cls, obj_id)
        return obj.to_dict() if obj else None

    def delete(self, model_name, obj_id):
        model_cls = self.model_map.get(model_name)
        if not model_cls:
            raise ValueError("Invalid model name")

        obj = self.storage.get(model_cls, obj_id)
        if obj:
            self.storage.delete(obj)
            return True
        return False

    # Méthodes spécifiques à Review (exploitées dans reviews.py)
    def create_review(self, data):
        return self.create("Review", data)

    def get_all_reviews(self):
        return self.get_all("Review")

    def get_review_by_id(self, review_id):
        return self.get_by_id("Review", review_id)

    def delete_review(self, review_id):
        return self.delete("Review", review_id)


# Instance globale
facade = Facade()
