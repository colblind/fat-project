from typing import Type

from core.dependencies_injection import inject_service
from core.repository.database import EntityType
from core.entity.auth import UserSignInCredentials
from core.service.abstract import AbstractService
from core.repository.auth import AuthRepository, auth_repository


class AuthService(AbstractService):
    def __init__(self, repository: AuthRepository):
        self._repository = repository
        super().__init__(repository)

    async def sign_in(self, data: UserSignInCredentials) -> tuple[str, str]:
        user = await self._repository.authenticate(**data.model_dump())

        access_token, refresh_token = self._repository.create_token_pair(user)

        return access_token, refresh_token

    async def get_user_by_access_token(self, token: str) -> Type[EntityType]:
        token = self._repository.verify_access_token(token)

        return await self._repository.get_user_by_pk(token.sub)

    async def get_user_by_refresh_token(self, token: str) -> Type[EntityType]:
        token = self._repository.verify_refresh_token(token)

        return await self._repository.get_user_by_pk(token.sub)

    async def exchange_refresh_token(self, token: str) -> tuple[str, str]:
        tokens = await self._repository.exchange_refresh_token(token)

        return tokens


auth_service = AuthService(repository=auth_repository)

auth_service_dependency = inject_service(service=auth_service)
