from typing import Optional


class AbstractException(Exception):
    message: str
    http_code: Optional[int]


class DataValidationException(Exception):
    errors: dict[str, list[str]]
    http_code: Optional[int]
