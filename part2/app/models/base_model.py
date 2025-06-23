import uuid
from datetime import datetime

class BaseModel:
    def __init__(self, **kwargs):
        self.id = kwargs.get("id", str(uuid.uuid4()))

        # Parse created_at de manière sûre
        self.created_at = self._parse_datetime(kwargs.get("created_at")) or datetime.utcnow()
        self.updated_at = self._parse_datetime(kwargs.get("updated_at")) or self.created_at

    def _parse_datetime(self, value):
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                return None
        return None

    def to_dict(self):
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
