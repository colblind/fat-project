from typing import Annotated

from fastapi import Depends


def pagination_params_factory(order: str = "id", limit: int = 10, offset: int = 0, search: str = None):
    return {
        'order': order,
        'limit': limit,
        'offset': offset,
        'search': search,
    }


pagination_params = Annotated[dict, Depends(pagination_params_factory)]
