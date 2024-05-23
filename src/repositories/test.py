from adapters.test import TestAdapter
from core.repository.database import SQLModelRepository
from helpers.database import default_db_helper
from models.test import TestModel
from entity.test import Test, TestCreate, TestUpdate


class TestRepository(SQLModelRepository[Test, TestCreate, TestUpdate, TestModel]):
    pass


test_repository = TestRepository(model=TestModel, session_factory=default_db_helper.session_factory, adapter=TestAdapter(entity=Test))
