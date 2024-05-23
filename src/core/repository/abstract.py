from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Type

from core.entity.base.types import EntityType, CreateEntityType, UpdateEntityType


class AbstractRepository(ABC, Generic[EntityType, CreateEntityType, UpdateEntityType]):
    @abstractmethod
    async def create(self, data: CreateEntityType) -> EntityType:
        raise NotImplementedError

    @abstractmethod
    async def update(self, data: UpdateEntityType, **kwargs) -> EntityType:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self, **kwargs) -> EntityType:
        raise NotImplementedError


AbstractRepositoryType = TypeVar('AbstractRepositoryType', bound=AbstractRepository)
