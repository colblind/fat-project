from abc import ABC, abstractmethod
from typing import Generic, Type

from core.entity.base.types import EntityType
from helpers.singleton import Singleton


class AbstractAdapter(ABC, Generic[EntityType]):
    __metaclass__ = Singleton

    def __init__(self, entity: Type[EntityType]):
        self._entity = entity

    @abstractmethod
    def to_dict(self, entity: EntityType) -> dict:
        raise NotImplemented

    @abstractmethod
    def from_dict(self, data: dict) -> EntityType:
        raise NotImplemented
