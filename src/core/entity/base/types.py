from typing import TypeVar

from .entity import BaseEntity
from core.dto import BaseDTO

EntityType = TypeVar("EntityType", bound=BaseEntity)
CreateEntityType = TypeVar("CreateEntityType", bound=BaseDTO)
UpdateEntityType = TypeVar("UpdateEntityType", bound=BaseDTO)
