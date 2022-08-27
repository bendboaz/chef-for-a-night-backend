import json
import warnings
from pathlib import Path
from typing import List, Union, NoReturn
from uuid import UUID

from src.data_layer.base import DataLayer
from src.data_layer.exceptions import CollectionDoesNotExistException, ObjectDoesNotExistException


class FilesystemDataLayer(DataLayer):
    """
    An implementation of ModelLayer for local systems - The different collections are different
    directories in the filesystem.
    """
    def __init__(self, root: Union[str, Path]):
        super(FilesystemDataLayer, self).__init__()

        self.root = Path(root)
        self._collections = None

    def get_collection(self, business_object_type: str) -> List[UUID]:
        if business_object_type in self._collections:
            return self._collections[business_object_type]

        self._collections[business_object_type] = self._load_collection(business_object_type)
        return self._collections[business_object_type]

    def get_object_data(self, business_object_id: UUID, business_object_type: str) -> dict:
        object_data_path = self._get_collection_path(business_object_type) / self._get_filename(business_object_id)
        with open(object_data_path) as business_object_file:
            object_data = json.load(business_object_file)
        return object_data

    def delete_object(self, business_object_type: str, business_object_id: UUID) -> NoReturn:
        self._assert_collection_exists(business_object_type)
        self._assert_object_exists(business_object_id, business_object_type)

        object_path = self._get_object_path(business_object_type, business_object_id)
        object_path.unlink()

    def write_object_data(self, business_object_id: UUID, business_object_type: str,
                          business_object_data: dict) -> NoReturn:
        self._assert_collection_exists(business_object_type)

        object_path = self._get_object_path(business_object_type, business_object_id)
        if object_path.exists():
            warnings.warn("Overriding object {} in collection {}".format(business_object_id, business_object_type))

        with open(object_path, 'w+') as object_file:
            json.dump(business_object_data, object_file)

    def _load_collection(self, business_object_type: str) -> List[UUID]:
        self._assert_collection_exists(business_object_type)
        return [UUID(uuid) for uuid in self._get_collection_uuids(business_object_type)]

    def _assert_collection_exists(self, business_object_type):
        if not (self._get_collection_path(business_object_type)).exists():
            raise CollectionDoesNotExistException(business_object_type)

    @staticmethod
    def _get_filename(business_object_id: UUID) -> str:
        return f'{str(business_object_id)}.json'

    def _get_collection_uuids(self, business_object_type: str) -> List[str]:
        return [document.name.split('.')[0] for document in (
            self._get_collection_path(business_object_type)).glob('*.json')]

    def _get_collection_path(self, business_object_type) -> Path:
        return self.root / business_object_type

    def _get_object_path(self, business_object_type: str, business_object_id: UUID) -> Path:
        return self._get_collection_path(business_object_type) / self._get_filename(business_object_id)

    def _assert_object_exists(self, business_object_id, business_object_type):
        collection = self.get_collection(business_object_type)
        if business_object_id not in collection:
            raise ObjectDoesNotExistException(business_object_type, business_object_id)
