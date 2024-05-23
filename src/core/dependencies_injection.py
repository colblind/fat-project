from core.repository.abstract import AbstractRepository
from core.service.abstract import AbstractService

from typing import Annotated, Type, TypeVar

from fastapi import Depends


RepositoryType = TypeVar('RepositoryType', bound=AbstractRepository)
ServiceType = TypeVar('ServiceType', bound=AbstractService)


def inject_repository(repository: AbstractRepository) -> Type[RepositoryType]:
    def inner():
        return repository

    return Annotated[Type[repository], Depends(inner)]


def inject_service(service: ServiceType) -> Type[ServiceType]:
    def inner() -> ServiceType:
        return service

    return Annotated[Type[service], Depends(inner)]
