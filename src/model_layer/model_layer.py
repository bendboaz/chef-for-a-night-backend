import itertools
from contextlib import contextmanager
from typing import List, NoReturn
from uuid import UUID

from src.data_layer.exceptions import CollectionDoesNotExistException, ObjectDoesNotExistException
from src.model_layer.exceptions import BusinessObjectDoesNotExistException, InvalidBusinessObjectTypeException
from src.data_layer.base import DataLayer
from src.model_layer.mapper import BUSINESS_OBJECT_TYPE_TO_CLASS_MAP, CLASS_TO_BUSINESS_OBJECT_MAP
from src.model_layer.types import BusinessObject


class ModelLayer:
    """
    Abstract class for model layers. Translates business object operations into data layer ones.
    """
    def __init__(self, data_layer: DataLayer):
        super().__init__()

        self.data_layer = data_layer

    def get_business_object_by_id(self, business_object_type: str, business_object_id: UUID) -> BusinessObject:
        with self._wrap_data_layer_exceptions():
            object_data = self.data_layer.get_object_data(business_object_id, business_object_type)

        return BUSINESS_OBJECT_TYPE_TO_CLASS_MAP[business_object_type](object_data)

    def list_business_objects(self, business_object_type: str) -> List[BusinessObject]:
        with self._wrap_data_layer_exceptions():
            all_ids = self.data_layer.get_collection(business_object_type)
            loaded_objects = list(map(
                self.get_business_object_by_id,
                itertools.repeat(business_object_type, len(all_ids)),
                all_ids
            ))
        return loaded_objects

    def update_business_object(self, business_object: BusinessObject) -> NoReturn:
        business_object_type = CLASS_TO_BUSINESS_OBJECT_MAP[type(business_object)]
        with self._wrap_data_layer_exceptions():
            self.data_layer.write_object_data(business_object.id, business_object_type, business_object.dict())

    def create_business_object(self, business_object: BusinessObject) -> NoReturn:
        business_object_type = CLASS_TO_BUSINESS_OBJECT_MAP[type(business_object)]
        with self._wrap_data_layer_exceptions():
            self.data_layer.write_object_data(business_object._id, business_object_type, business_object.dict())

    def delete_business_object(self, business_object: BusinessObject) -> NoReturn:
        business_object_type = CLASS_TO_BUSINESS_OBJECT_MAP[type(business_object)]
        with self._wrap_data_layer_exceptions():
            self.data_layer.delete_object(business_object_type, business_object._id)

    @contextmanager
    def _wrap_data_layer_exceptions(self):
        try:
            yield
        except CollectionDoesNotExistException as e:
            raise InvalidBusinessObjectTypeException(e.collection)
        except ObjectDoesNotExistException as e:
            raise BusinessObjectDoesNotExistException(e.collection, e.object_id)
