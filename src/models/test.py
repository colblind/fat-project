from sqlmodel import SQLModel, Field


class TestModel(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)

    name: str

    active: bool = Field(default=True)
