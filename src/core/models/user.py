from enum import Enum

from sqlmodel import SQLModel, Field, Column, Enum as SQLEnum


class UserRolesEnum(str, Enum):
    user = 'user'
    admin = 'admin'
    superuser = 'superuser'


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)

    email: str = Field(max_length=64, regex=r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", unique=True)
    password: str = Field(max_length=256)

    first_name: str = Field(max_length=32)
    last_name: str = Field(max_length=32)

    role: UserRolesEnum = Field(sa_column=Column(SQLEnum(UserRolesEnum)), max_length=32, default=UserRolesEnum.user)

    is_active: bool = Field(default=True)

    @classmethod
    async def create_user(cls, email: str, password: str, first_name: str, last_name: str, role: UserRolesEnum = UserRolesEnum.user, **kwargs):
        return await cls.create(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role=role,
            **kwargs,
        )

    @classmethod
    async def create_admin(cls, email: str, password: str, first_name: str, last_name: str, **kwargs):
        return await cls.create(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role=UserRolesEnum.admin,
            **kwargs,
        )

    @classmethod
    async def create_superuser(cls, email: str, password: str, first_name: str, last_name: str, **kwargs):
        return await cls.create(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role=UserRolesEnum.superuser,
            **kwargs,
        )

    def __str__(self):
        return f'({self.pk}) Пользователь {self.email}'
