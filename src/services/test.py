from core.dependencies_injection import inject_service
from core.service.database import SQLModelService
from entity.test import Test, TestCreate, TestUpdate
from repositories.test import test_repository


class TestService(SQLModelService[Test, TestCreate, TestUpdate]):
    pass


test_service = TestService(repository=test_repository)

test_service_dependency = inject_service(test_service)
