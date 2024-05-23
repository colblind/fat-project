from typing import Final, Optional

from pydantic import Field

from core.entity.base.entity import BaseEntity


class Test(BaseEntity):
    id: int

    name: str

    active: Optional[bool] = Field(default=True)


class TestCreate(Test):
    id: Final[int] = None


class TestUpdate(Test):
    id: Final[int] = None
