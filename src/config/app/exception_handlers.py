from typing import TypedDict

from pydantic import ValidationError
from pydantic_core.core_schema import ErrorType
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from core.exceptions.base import AbstractException, DataValidationException

PydanticExceptionToErrorCodeMap = TypedDict('PydanticExceptionToErrorCodeMap', {key: str for key in ErrorType})

pydantic_exception_to_error_code_map: PydanticExceptionToErrorCodeMap = {
    'no_such_attribute': {
        'type': 'errors.validation.invalid_argument',
        'http_code': 400,
    },
    'json_invalid': {
        'type': 'errors.validation.invalid_json',
        'http_code': 400,
    },
    'json_type': {
        'type': 'errors.validation.invalid_json',
        'http_code': 400,
    },
    'recursion_loop': {
        'type': 'errors.server.internal_server_error',
        'http_code': 500,
    },
    'missing': {
        'type': 'errors.validation.missing_value',
        'http_code': 400,
    },
    'frozen_field': {
        'type': 'errors.server.internal_server_error',
        'http_code': 500,
    },
    'frozen_instance': {
        'type': 'errors.server.internal_server_error',
        'http_code': 500,
    },
    'extra_forbidden': {
        'type': 'errors.validation.invalid_argument',
        'http_code': 400,
    },
    'invalid_key': {
        'type': 'errors.validation.invalid_argument',
        'http_code': 400,
    },
    'get_attribute_error': {
        'type': 'errors.server.internal_server_error',
        'http_code': 500,
    },
    'model_type': {
        'type': 'errors.server.internal_server_error',
        'http_code': 500,
    },
    'model_attributes_type': {
        'type': 'errors.server.internal_server_error',
        'http_code': 500,
    },
    'dataclass_type': {
        'type': 'errors.validation.invalid_argument',
        'http_code': 400,
    },
    'dataclass_exact_type': {
        'type': 'errors.validation.invalid_argument',
        'http_code': 400,
    },
    'none_required': {
        'type': 'errors.validation.invalid_argument',
        'http_code': 400,
    },
    'greater_than': {
        'type': 'errors.validation.greater_than',
        'http_code': 400,
    },
    'greater_than_equal': {
        'type': 'errors.validation.greater_than_equal',
        'http_code': 400,
    },
    'less_than': {
        'type': 'errors.validation.less_than',
        'http_code': 400,
    },
    'less_than_equal': {
        'type': 'errors.validation.less_than_equal',
        'http_code': 400,
    },
    'multiple_of': {
        'type': 'errors.validation.multiple_of',
        'http_code': 400,
    },
    'finite_number': {
        'type': 'errors.validation.finite_number',
        'http_code': 400,
    },
    'too_short': {
        'type': 'errors.validation.too_short',
        'http_code': 400,
    },
    'too_long': {
        'type': 'errors.validation.too_long',
        'http_code': 400,
    },
    'iterable_type': {
        'type': 'errors.validation.iterable_type',
        'http_code': 400,
    },
    'iteration_error': {
        'type': 'errors.server.internal_server_error',
        'http_code': 500,
    },
    'string_type': {
        'type': 'errors.validation.invalid_argument_for_string',
        'http_code': 400,
    },
    'string_sub_type': {
        'type': 'errors.validation.invalid_argument_for_string',
        'http_code': 400,
    },
    'string_unicode': {
        'type': 'errors.validation.invalid_argument_for_unicode_string',
        'http_code': 400,
    },
    'string_too_short': {
        'type': 'errors.validation.string_too_short',
        'http_code': 400,
    },
    'string_too_long': {
        'type': 'errors.validation.string_too_long',
        'http_code': 400,
    },
    'string_pattern_mismatch': {
        'type': 'errors.validation.string_pattern_mismatch',
        'http_code': 400,
    },
    'enum': {
        'type': 'errors.validation.invalid_argument_for_enum',
        'http_code': 400,
    },
    'dict_type': {
        'type': 'errors.validation.invalid_argument_for_dict',
        'http_code': 400,
    },
    'mapping_type': {
        'type': 'errors.validation.invalid_argument_for_mapping',
        'http_code': 400,
    },
    'list_type': {
        'type': 'errors.validation.invalid_argument_for_list',
        'http_code': 400,
    },
    'tuple_type': {
        'type': 'errors.validation.invalid_argument_for_tuple',
        'http_code': 400,
    },
    'set_type': {
        'type': 'errors.validation.invalid_argument_for_set',
        'http_code': 400,
    },
    'bool_type': {
        'type': 'errors.validation.invalid_argument_for_bool',
        'http_code': 400,
    },
    'bool_parsing': {
        'type': 'errors.validation.invalid_argument_for_bool',
        'http_code': 400,
    },
    'int_type': {
        'type': 'errors.validation.invalid_argument_for_int',
        'http_code': 400,
    },
    'int_parsing': {
        'type': 'errors.validation.invalid_argument_for_int',
        'http_code': 400,
    },
    'int_parsing_size': {
        'type': 'errors.validation.int_too_long',
        'http_code': 400,
    },
    'int_from_float': {
        'type': 'errors.validation.invalid_argument_for_int',
        'http_code': 400,
    },  # TODO: think `bout more verbose error name
    'float_type': {
        'type': 'errors.validation.invalid_argument_for_float',
        'http_code': 400,
    },
    'float_parsing': {
        'type': 'errors.validation.invalid_argument_for_float',
        'http_code': 400,
    },
    'bytes_type': {
        'type': 'errors.validation.invalid_argument_for_bytes',
        'http_code': 400,
    },
    'bytes_too_short': {
        'type': 'errors.validation.bytes_too_short',
        'http_code': 400,
    },
    'bytes_too_long': {
        'type': 'errors.validation.bytes_too_long',
        'http_code': 400,
    },
    'value_error': {
        'type': 'errors.validation.invalid_argument',
        'http_code': 400,
    },
    'assertion_error': {
        'type': 'errors.server.internal_server_error',
        'http_code': 500,
    },
    'literal_error': {
        'type': 'errors.server.internal_server_error',
        'http_code': 500,
    },
    'date_type': {
        'type': 'errors.validation.invalid_argument_for_date',
        'http_code': 400,
    },
    'date_parsing': {
        'type': 'errors.validation.invalid_argument_for_date',
        'http_code': 400,
    },
    'date_from_datetime_parsing': {
        'type': 'errors.validation.invalid_argument_for_date',
        'http_code': 400,
    },
    'date_from_datetime_inexact': {
        'type': 'errors.validation.invalid_argument_for_date',
        'http_code': 400,
    },
    'date_past': {
        'type': 'errors.validation.date_past',
        'http_code': 400,
    },
    'date_future': {
        'type': 'errors.validation.date_future',
        'http_code': 400,
    },
    'time_type': {
        'type': 'errors.validation.invalid_argument_for_time',
        'http_code': 400,
    },
    'time_parsing': {
        'type': 'errors.validation.invalid_argument_for_time',
        'http_code': 400,
    },
    'datetime_type': {
        'type': 'errors.validation.invalid_argument_for_datetime',
        'http_code': 400,
    },
    'datetime_parsing': {
        'type': 'errors.validation.invalid_argument_for_datetime',
        'http_code': 400,
    },
    'datetime_object_invalid': {
        'type': 'errors.validation.invalid_argument_for_datetime',
        'http_code': 400,
    },
    'datetime_from_date_parsing': {
        'type': 'errors.validation.invalid_argument_for_datetime',
        'http_code': 400,
    },
    'datetime_past': {
        'type': 'errors.validation.datetime_past',
        'http_code': 400,
    },
    'datetime_future': {
        'type': 'errors.validation.datetime_future',
        'http_code': 400,
    },
    'timezone_naive': {
        'type': 'errors.validation.datetime_naive',
        'http_code': 400,
    },
    'timezone_aware': {
        'type': 'errors.validation.datetime_aware',
        'http_code': 400,
    },
    'time_delta_type': {
        'type': 'errors.validation.invalid_argument_for_timedelta',
        'http_code': 400,
    },
    'time_delta_parsing': {
        'type': 'errors.validation.invalid_argument_for_timedelta',
        'http_code': 400,
    },
    'frozen_set_type': {
        'type': 'errors.server.internal_server_error',
        'http_code': 500,
    },
    'is_instance_of': {
        'type': 'errors.server.internal_server_error',
        'http_code': 500,
    },
    'is_subclass_of': {
        'type': 'errors.server.internal_server_error',
        'http_code': 500,
    },
    'callable_type': {
        'type': 'errors.server.internal_server_error',
        'http_code': 500,
    },
    'union_tag_invalid': {
        'type': 'errors.server.internal_server_error',
        'http_code': 500,
    },
    'union_tag_not_found': {
        'type': 'errors.server.internal_server_error',
        'http_code': 500,
    },
    'arguments_type': {
        'type': 'errors.server.internal_server_error',
        'http_code': 500,
    },
    'missing_argument': {
        'type': 'errors.server.internal_server_error',
        'http_code': 500,
    },
    'unexpected_keyword_argument': {
        'type': 'errors.server.internal_server_error',
        'http_code': 500,
    },
    'missing_keyword_only_argument': {
        'type': 'errors.server.internal_server_error',
        'http_code': 500,
    },
    'unexpected_positional_argument': {
        'type': 'errors.server.internal_server_error',
        'http_code': 500,
    },
    'missing_positional_only_argument': {
        'type': 'errors.server.internal_server_error',
        'http_code': 500,
    },
    'multiple_argument_values': {
        'type': 'errors.server.internal_server_error',
        'http_code': 500,
    },
    'url_type': {
        'type': 'errors.validation.invalid_argument_for_url',
        'http_code': 400,
    },
    'url_parsing': {
        'type': 'errors.validation.invalid_argument_for_url',
        'http_code': 400,
    },
    'url_syntax_violation': {
        'type': 'errors.validation.invalid_argument_for_url',
        'http_code': 400,
    },
    'url_too_long': {
        'type': 'errors.validation.url_too_long',
        'http_code': 400,
    },
    'url_scheme': {
        'type': 'errors.validation.invalid_url_scheme',
        'http_code': 400,
    },
    'uuid_type': {
        'type': 'errors.validation.invalid_argument_for_uuid',
        'http_code': 400,
    },
    'uuid_parsing': {
        'type': 'errors.validation.invalid_argument_for_uuid',
        'http_code': 400,
    },
    'uuid_version': {
        'type': 'errors.validation.invalid_argument_for_uuid',
        'http_code': 400,
    },
    'decimal_type': {
        'type': 'errors.validation.invalid_argument_for_decimal',
        'http_code': 400,
    },
    'decimal_parsing': {
        'type': 'errors.validation.invalid_argument_for_decimal',
        'http_code': 400,
    },
    'decimal_max_digits': {
        'type': 'errors.validation.decimal_too_long',
        'http_code': 400,
    },
    'decimal_max_places': {
        'type': 'errors.validation.decimal_too_long',
        'http_code': 400,
    },
    'decimal_whole_digits': {
        'type': 'errors.validation.decimal_too_long',
        'http_code': 400,
    },
}


async def abstract_exception_handler(request: Request, exception: AbstractException):
    return JSONResponse(status_code=exception.http_code, content={
        'message': exception.message,
    })


async def data_validation_exception_handler(request: Request, exception: DataValidationException):
    return JSONResponse(status_code=exception.http_code, content={
        'errors': exception.errors,
    })


async def request_validation_error_handler(request: Request, exception: RequestValidationError):
    errors_dict = dict()

    for errors in exception.args:
        for field_error in errors:
            error_location = '.'.join(field_error.get('loc')[1:])

            if error_location not in errors_dict.keys():
                errors_dict[error_location] = list()

            error_type = field_error.get('type')

            error_mapped_type = pydantic_exception_to_error_code_map.get(error_type, None)

            if not error_mapped_type:
                continue

            errors_dict[error_location].append(error_mapped_type.get('type'))

    return JSONResponse(status_code=400, content=errors_dict)
