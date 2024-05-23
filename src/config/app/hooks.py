from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from helpers.database import init_databases


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator:
    # Startup
    await init_databases()

    yield

    # Shutdown
