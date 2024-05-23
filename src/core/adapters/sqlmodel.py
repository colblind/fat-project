from typing import Generic, Type, TypeVar

from infra.types import SQLDBModel
from .abstract import AbstractAdapter, EntityType


class SQLModelAdapter(AbstractAdapter[EntityType], Generic[EntityType, SQLDBModel]):
    def __init__(self, entity: Type[EntityType]):
        super(SQLModelAdapter, self).__init__(entity)

    def from_dict(self, data: dict) -> SQLDBModel:
        return self._entity.parse_obj(data)

    def to_dict(self, data: SQLDBModel) -> dict:
        return data.model_dump()

    def to_entity(self, data: SQLDBModel) -> EntityType:
        return self._entity.parse_obj(data.model_dump())


SQLModelAdapterType = TypeVar('SQLModelAdapterType', bound=SQLModelAdapter)
