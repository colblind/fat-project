from typing import TypeVar, Generic

from pydantic import ConfigDict, BaseModel

from core.entity.base.entity import BaseEntity

PaginationDataType = TypeVar('PaginationDataType', bound=BaseEntity)


class PaginationResponse(BaseModel, Generic[PaginationDataType]):
    result: list[PaginationDataType]
    count: int

    model_config = ConfigDict(arbitrary_types_allowed=True)
