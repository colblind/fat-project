from core.adapters.sqlmodel import SQLModelAdapter
from entity.test import Test
from models.test import TestModel


class TestAdapter(SQLModelAdapter[Test, TestModel]):
    pass
