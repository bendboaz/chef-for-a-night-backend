from src.model_layer.constants import BusinessObjectTypes
from src.model_layer.types import Task, Recipe, Ingredient

BUSINESS_OBJECT_TYPE_TO_CLASS_MAP = {
    BusinessObjectTypes.TASK: Task,
    BusinessObjectTypes.RECIPE: Recipe,
    BusinessObjectTypes.INGREMENT: Ingredient
}

CLASS_TO_BUSINESS_OBJECT_MAP = {
    cls: object_type for object_type, cls in BUSINESS_OBJECT_TYPE_TO_CLASS_MAP.items()
}
