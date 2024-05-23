from fastapi import APIRouter

from core.pagination.helpers import pagination_params
from entity.test import Test, TestCreate
from services.test import test_service_dependency

from core.pagination.schema import PaginationResponse

test_router = APIRouter()


@test_router.get(path='/', response_model=PaginationResponse[Test])
async def test_list(params: pagination_params, service: test_service_dependency):
    return await service.filter(**params)


@test_router.post(path='/create', response_model=Test)
async def test_create(data: TestCreate, service: test_service_dependency):
    return await service.create(data=data)
