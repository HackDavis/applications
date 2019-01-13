from enum import Enum
from sqlalchemy.inspection import inspect


class Serializer:
    def serialize(self):
        """Serialize a SQLAlchemy model"""
        model_dict = self.__dict__
        model_dict.pop('_sa_instance_state', None)
        return self.serialize_value(model_dict)

    @staticmethod
    def serialize_value(value):
        """Serialize values depending on their types"""
        if isinstance(value, list):
            return [Serializer.serialize_value(element) for element in value]
        elif isinstance(value, dict):
            return {key: Serializer.serialize_value(value) for key, value in value.items()}
        elif isinstance(value, tuple):
            return [Serializer.serialize_value(element) for element in value]
        elif isinstance(value, Enum):
            return Serializer.serialize_value(value.name)
        elif isinstance(value, Serializer):
            return value.serialize()

        return value
