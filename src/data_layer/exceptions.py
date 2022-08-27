from uuid import UUID


class CollectionDoesNotExistException(Exception):
    def __init__(self, collection: str):
        super(CollectionDoesNotExistException, self).__init__('Collection {} does not exist'.format(collection))
        self.collection = collection


class ObjectDoesNotExistException(Exception):
    def __init__(self, collection: str, object_id: UUID):
        super(ObjectDoesNotExistException, self).__init__(
            'Object {} does not exist in collection {}'.format(object_id, collection)
        )
        self.collection = collection
        self.object_id = object_id

