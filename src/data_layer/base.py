from abc import ABC, abstractmethod
from typing import List, NoReturn
from uuid import UUID


class DataLayer(ABC):
    @abstractmethod
    def get_collection(self, business_object_type: str) -> List[UUID]:
        pass

    @abstractmethod
    def get_object_data(self, business_object_id: UUID, business_object_type: str) -> dict:
        pass

    @abstractmethod
    def delete_object(self, business_object_type: str, business_object_id: UUID) -> NoReturn:
        pass

    @abstractmethod
    def write_object_data(self, business_object_id: UUID, business_object_type: str, business_object_data: dict) \
            -> NoReturn:
        pass
