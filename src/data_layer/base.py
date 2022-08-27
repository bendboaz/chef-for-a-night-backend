from abc import ABC, abstractmethod
from typing import List, NoReturn
from uuid import UUID

from src.data_layer.types import BusinessObject


class DataLayer(ABC):
    """
    Abstract class for data layers.
    """

    @abstractmethod
    def get_business_object_by_id(self, business_object_id: UUID) -> BusinessObject:
        pass

    @abstractmethod
    def list_business_objects(self, business_object_type: str) -> List[BusinessObject]:
        pass

    @abstractmethod
    def update_business_object(self, business_object_id: UUID, business_object: BusinessObject) -> NoReturn:
        pass

    @abstractmethod
    def create_business_object(self, business_object: BusinessObject) -> NoReturn:
        pass

    @abstractmethod
    def delete_business_object(self, business_object_id: UUID) -> NoReturn:
        pass
