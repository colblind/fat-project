from abc import ABC, abstractmethod

from core.entity.base.types import EntityType
from core.service.auth import AuthService


class BasePermission(ABC):
    auth_service: AuthService

    @abstractmethod
    async def __call__(self, *args, **kwargs) -> EntityType:
        raise NotImplementedError
