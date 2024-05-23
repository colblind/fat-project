from fastapi import APIRouter

from .auth.routes import auth_router
from .test.routes import test_router


def get_v1_router():
    v1_router = APIRouter()

    v1_router.include_router(auth_router, prefix='/auth')
    v1_router.include_router(test_router, prefix='/test')

    return v1_router
