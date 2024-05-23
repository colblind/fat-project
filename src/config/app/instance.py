from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from config.app.controller import get_app_router
from config.app.exception_handlers import abstract_exception_handler, data_validation_exception_handler, \
    request_validation_error_handler
from config.app.hooks import lifespan
from config.app.middlewares import apply_app_middlewares
from config.settings import app_configs
from core.exceptions.base import AbstractException, DataValidationException


def get_app_instance() -> FastAPI:
    app = FastAPI(lifespan=lifespan, **app_configs)

    apply_app_middlewares(app=app)

    app.include_router(router=get_app_router())
    app.add_exception_handler(AbstractException, abstract_exception_handler)
    app.add_exception_handler(DataValidationException, data_validation_exception_handler)
    app.add_exception_handler(RequestValidationError, request_validation_error_handler)

    return app
