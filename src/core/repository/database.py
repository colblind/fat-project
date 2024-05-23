from typing import Optional, Generic, Type, AsyncContextManager, Callable, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, update, delete, or_, desc, asc

from core.adapters.sqlmodel import SQLModelAdapterType
from infra.types import SQLDBModel
from core.entity.base.types import EntityType, CreateEntityType, UpdateEntityType
from core.exceptions.pagination import InvalidOrderingKeyException
from core.repository.abstract import AbstractRepository
from helpers.types import can_cast


class SQLModelRepository(AbstractRepository[EntityType, CreateEntityType, UpdateEntityType], Generic[EntityType, CreateEntityType, UpdateEntityType, SQLDBModel]):
    def __init__(self, model: Type[SQLDBModel], session_factory: Callable[..., AsyncContextManager[AsyncSession]], adapter: SQLModelAdapterType):
        self._model = model
        self._session_factory = session_factory
        self._adapter = adapter

    async def create(self, data: CreateEntityType) -> EntityType:
        async with self._session_factory() as session:
            instance = self._model(**data.model_dump())

            session.add(instance)

            await session.commit()
            await session.refresh(instance)

            return self._adapter.to_entity(instance)

    async def update(self, data: UpdateEntityType, **filters) -> EntityType:
        async with self._session_factory() as session:
            statement = update(self._model).values(**data).filter_by(**filters).returning(self._model)

            res = await session.execute(statement)

            await session.commit()

            return self._adapter.to_entity(res.scalar_one())

    async def delete(self, **filters) -> None:
        async with self._session_factory() as session:
            await session.execute(delete(self._model).filter_by(**filters))

            await session.commit()

    async def get(self, **filters) -> EntityType:
        async with self._session_factory() as session:
            row = await session.execute(select(self._model).filter_by(**filters))

            return self._adapter.to_entity(row.scalar_one())

    async def get_or_none(self, **filters) -> Optional[EntityType] | None:
        async with self._session_factory() as session:
            row = await session.execute(select(self._model).filter_by(**filters))

            result = row.scalar_one_or_none()

            return None if result is None else self._adapter.to_entity(result)

    async def filter(
            self,
            *,
            order: str = "id",
            limit: int = 10,
            offset: int = 0,
            search: str = None,
            **filters,
    ) -> dict[str, list[EntityType] | int]:
        filter_statements = list()

        # warning! should be used with really carefully
        if search:
            for field_name, field_info in self._model.model_fields.items():
                if can_cast(search, field_info.annotation):
                    if search.lower().strip() in ['true', 'false'] and field_info.annotation == bool:
                        casted = False if search.lower().strip() == 'false' else True
                    else:
                        casted = field_info.annotation(search)

                    if isinstance(casted, str):
                        filter_statements.append(getattr(self._model, field_name).icontains(casted))
                    else:
                        filter_statements.append(getattr(self._model, field_name) == casted)

        clean_order_field_name = order.replace('+', '').replace('-', '')
        order_direction = desc if order.startswith('-') else asc

        if clean_order_field_name not in self._model.model_fields.keys():
            raise InvalidOrderingKeyException

        async with self._session_factory() as session:
            statement = select(self._model).order_by(order_direction(clean_order_field_name)).filter_by(**filters)

            if search:
                statement = statement.where(or_(*filter_statements))

            count = len((await session.execute(statement)).all())

            statement = statement.limit(limit).offset(offset)

            row = await session.execute(statement)

            return {
                'result': [self._adapter.to_entity(instance) for instance in row.scalars().all()],
                'count': count,
            }


SQLModelRepositoryType = TypeVar('SQLModelRepositoryType', bound=SQLModelRepository)
