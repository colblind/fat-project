from datetime import timedelta, datetime
from typing import Type, Callable, AsyncContextManager
from uuid import uuid4

from config.settings import app_settings, JWT_AUDIENCE, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES, \
    JWT_ALGORITHM, JWT_LEEWAY_SECONDS
from core.adapters.sqlmodel import SQLModelAdapter, SQLModelAdapterType
from core.exceptions.auth import InvalidCredentialsException, InvalidJWTTokenException
from core.repository.database import SQLModelRepository, EntityType, CreateEntityType
from dto.auth.token import AccessToken, RefreshToken
from sqlalchemy.ext.asyncio import AsyncSession
from jwt import encode as jwt_encode, decode as jwt_decode

from passlib.context import CryptContext

from helpers.database import default_db_helper
from core.models.user import User


class AuthRepository[User, CreateUserSchema, UpdateUserSchema, UserModel](SQLModelRepository):
    def __init__(self, user_model: Type[EntityType], crypto_context, session_factory: Callable[..., AsyncContextManager[AsyncSession]], adapter: SQLModelAdapterType):
        super().__init__(user_model, session_factory, adapter)
        self._model = user_model
        self._pwd_context = crypto_context

    async def create(self, data: CreateEntityType) -> EntityType:
        data.password = self._get_password_hash(data.password)

        return await super().create(data)

    async def authenticate(self, email: str, password: str) -> Type[EntityType] | None:
        user = await self.get_user_by_email(email=email)

        if not user:
            raise InvalidCredentialsException

        if not self._verify_password(user, password):
            raise InvalidCredentialsException

        return user

    def _verify_password(self, user: Type[EntityType], password: str) -> bool:
        return self._pwd_context.verify(password, user.password)

    def _get_password_hash(self, password: str) -> str:
        return self._pwd_context.hash(password)

    async def get_user_by_email(self, email: str) -> Type[EntityType] | None:
        return await self.get_or_none(email=email)

    async def get_user_by_pk(self, _id: int) -> Type[EntityType] | None:
        return await self.get_or_none(id=_id)

    def _create_token(self, user: Type[EntityType], token_type: str, ttl: timedelta = None, can_expire: bool = True) -> str:
        current_date = datetime.now()

        data_to_encode = {
            'aud': JWT_AUDIENCE,
            'sub': user.id,
            'iat': current_date,
            'jti': uuid4().hex,
            'token_type': token_type,
        }

        if can_expire:
            assert ttl, "if token can expire, ttl must be set"

            data_to_encode.update({
                'exp': current_date + ttl,
            })

        return jwt_encode(payload=data_to_encode, key=app_settings.SECRET_KEY, algorithm=JWT_ALGORITHM)

    def create_access_token(self, user: Type[EntityType], ttl: timedelta = None, can_expire: bool = True) -> str:
        return self._create_token(user=user, token_type="access", ttl=ttl or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES), can_expire=can_expire)

    def create_refresh_token(self, user: Type[EntityType], ttl: timedelta = None, can_expire: bool = True) -> str:
        return self._create_token(user=user, token_type="refresh", ttl=ttl or timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES), can_expire=can_expire)

    def _verify_token(self, token: str, token_type: str, verify_exp: bool = True) -> dict | None:
        try:
            decoded_token = jwt_decode(
                jwt=token,
                key=app_settings.SECRET_KEY,
                algorithms=[JWT_ALGORITHM],
                audience=JWT_AUDIENCE,
                leeway=timedelta(seconds=JWT_LEEWAY_SECONDS),
                options={
                    "require": ["aud", "sub", "iat", "jti", "token_type"],
                    "verify_exp": verify_exp,
                }
            )
        except Exception:
            raise InvalidJWTTokenException

        if not decoded_token.get("token_type") == token_type:
            raise InvalidJWTTokenException

        return decoded_token

    def verify_access_token(self, token: str, verify_exp: bool = True) -> AccessToken:
        token = self._verify_token(token=token, token_type='access', verify_exp=verify_exp)

        if token:
            return AccessToken(**token)

        raise InvalidJWTTokenException

    def verify_refresh_token(self, token: str, verify_exp: bool = True) -> RefreshToken | None:
        token = self._verify_token(token=token, token_type='refresh', verify_exp=verify_exp)

        if token:
            return RefreshToken(**token)

        raise InvalidJWTTokenException

    async def exchange_refresh_token(self, token: str) -> tuple[str, str] | None:
        refresh_token = self.verify_refresh_token(token)

        user = await self.get_user_by_pk(_id=refresh_token.sub)

        return self.create_access_token(user), self.create_refresh_token(user)

    def create_token_pair(self, user: Type[EntityType]) -> tuple[str, str]:
        return self.create_access_token(user), self.create_refresh_token(user)


auth_repository = AuthRepository(user_model=User, crypto_context=CryptContext(schemes=["bcrypt"], deprecated="auto"), session_factory=default_db_helper.session_factory, adapter=SQLModelAdapter(entity=Type[User]))
