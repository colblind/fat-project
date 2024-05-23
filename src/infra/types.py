from typing import TypeVar

from sqlmodel import SQLModel

SQLDBModel = TypeVar('SQLDBModel', bound=SQLModel)
