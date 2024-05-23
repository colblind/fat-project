from .base import AbstractException


class InvalidCredentialsException(AbstractException):
    message = "errors.auth.credentials.invalid"
    http_code = 400


class InvalidJWTTokenException(AbstractException):
    message = "errors.auth.token.invalid"
    http_code = 401


class UnAuthorizedException(AbstractException):
    message = "errors.auth.unauthorized"
    http_code = 401
