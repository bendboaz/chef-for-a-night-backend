from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class Metadata(BaseModel):
    tags: List[str]


class BusinessObject(BaseModel):
    _id: UUID
    _meta: Metadata


class Constraint(BaseModel):
    constraint_type: str
    constraint_details: dict


class Picture(BaseModel):
    url: str


class Ingredient(BusinessObject):
    name: str


class RecipeStep(BaseModel):
    text: str


class RecipeInstructions(BaseModel):
    steps: List[RecipeStep]


class TaskMetadata(Metadata):
    ingredients: List[Ingredient]


class RecipeMetadata(Metadata):
    ingredients: List[Ingredient]


class Task(BusinessObject):
    description: str
    constraints: List[Constraint]
    _meta: TaskMetadata


class Recipe(BusinessObject):
    name: str
    picture: Optional[Picture]
    ingredients: List[Ingredient]
    instructions: List[RecipeInstructions]
    _meta: RecipeMetadata
