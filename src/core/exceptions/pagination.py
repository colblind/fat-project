from core.exceptions.base import AbstractException


class InvalidOrderingKeyException(AbstractException):
    message = "errors.pagination.ordering.invalid"
    http_code = 400
