from typing import Generic

from core.entity.base.types import EntityType, CreateEntityType, UpdateEntityType
from core.repository.abstract import AbstractRepositoryType


class AbstractService(Generic[EntityType, CreateEntityType, UpdateEntityType]):
    def __init__(self, repository: AbstractRepositoryType):
        self._repository = repository

    async def create(self, data: CreateEntityType) -> EntityType:
        return await self._repository.create(data=data)

    async def update(self, data: UpdateEntityType, **kwargs) -> EntityType:
        return await self._repository.update(data=data, **kwargs)

    async def delete(self, **kwargs) -> None:
        await self._repository.delete(**kwargs)

    async def get(self, **kwargs) -> EntityType:
        return await self._repository.get(**kwargs)
