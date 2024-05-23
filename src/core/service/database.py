from typing import Generic

from core.repository.database import SQLModelRepositoryType
from core.service.abstract import AbstractService
from core.entity.base.types import EntityType, CreateEntityType, UpdateEntityType


class SQLModelService(AbstractService[EntityType, CreateEntityType, UpdateEntityType], Generic[EntityType, CreateEntityType, UpdateEntityType]):
    def __init__(self, repository: SQLModelRepositoryType):
        super(SQLModelService, self).__init__(repository)
        self._repository = repository

    async def filter(self,
                     *,
                     order: str = "id",
                     limit: int = 10,
                     offset: int = 0,
                     search: str = None,
                     **filters,
                     ) -> dict[str, list[EntityType] | int]:
        return await self._repository.filter(order=order, limit=limit, offset=offset, search=search, **filters)
