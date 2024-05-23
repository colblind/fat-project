from fastapi import APIRouter

from .v1.routes import get_v1_router


def get_api_router():
    api_router = APIRouter()

    api_router.include_router(get_v1_router(), prefix='/v1')

    return api_router
