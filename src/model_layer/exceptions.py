class InvalidBusinessObjectTypeException(TypeError):
    def __init__(self, business_object_type: str):
        super().__init__('Business object type {} does not exist'.format(business_object_type))
        self.business_object_type = business_object_type


class BusinessObjectDoesNotExistException(ValueError):
    def __init__(self, business_object_type, business_object_id):
        super().__init__(
            'Business object of type {} with id {} does not exist'.format(
                business_object_type, business_object_id
            )
        )
