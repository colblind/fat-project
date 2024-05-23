from controllers.v1.auth.schemas import UserOut, UserSignInOut
from core.permissions.generic import is_authenticated
from core.entity.auth import UserSignInCredentials, TokenPairStr, RefreshAccessTokenIn
from core.service.auth import auth_service_dependency

from fastapi import APIRouter

auth_router = APIRouter()


@auth_router.post(path='/sign-in', response_model=UserSignInOut)
async def sign_in(auth_service: auth_service_dependency, data: UserSignInCredentials):
    access_token, refresh_token = await auth_service.sign_in(data=data)

    return UserSignInOut(access=access_token, refresh=refresh_token)


@auth_router.get(path='/profile', response_model=UserOut)
async def profile(current_user: is_authenticated):
    return current_user.model_dump()


@auth_router.post(path="/token/refresh", response_model=TokenPairStr)
async def refresh_access_token(auth_service: auth_service_dependency, data: RefreshAccessTokenIn):
    access_token, refresh_token = await auth_service.exchange_refresh_token(data.refresh)

    return TokenPairStr(
        access=access_token,
        refresh=refresh_token,
    )
