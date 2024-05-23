import asyncio

from pydantic import BaseModel, Field


class Data(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    role: str
    is_active: bool


class GeneralData(BaseModel):
    id: int
    field: str


class GeneralAnonData(GeneralData):
    id: int = Field(exclude=True)


async def main():
    gd = GeneralData(id=1, field='test')
    gad = GeneralAnonData(id=2, field='text')

    print(gd.model_dump())
    print(gad.model_dump())

    # await default_db_helper.init_tables()
    #
    # await auth_service.create(Data(email='user@mail.com', password='1234', first_name='Test', last_name='Test', role='user', is_active=True))


if __name__ == '__main__':
    asyncio.run(main())
