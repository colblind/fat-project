from fastapi import APIRouter

from controllers.routes import get_api_router


def get_app_router():
    router = APIRouter()

    router.add_api_route('/healthcheck', healthcheck, methods=['GET'], include_in_schema=False)
    router.include_router(router=get_api_router(), prefix='/api')

    return router


async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
