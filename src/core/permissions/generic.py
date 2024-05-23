from typing import Annotated

from core.entity.base.types import EntityType
from core.exceptions.auth import UnAuthorizedException
from core.permissions.base import BasePermission

from fastapi import Security, Depends
from fastapi.security import APIKeyHeader

from core.models.user import User

from core.service.auth import auth_service


class IsAuthenticated(BasePermission):
    auth_service = auth_service

    async def __call__(self, authorization_header: str = Security(APIKeyHeader(name='Authorization', auto_error=False))) -> EntityType:

        if authorization_header is None:
            raise UnAuthorizedException

        if 'Bearer ' not in authorization_header:
            raise UnAuthorizedException

        clear_token = authorization_header.replace('Bearer ', '')

        return await self.auth_service.get_user_by_access_token(clear_token)


is_authenticated = Annotated[User, Depends(IsAuthenticated())]
