from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.settings import app_settings


def apply_app_middlewares(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_settings.CORS_ORIGINS,
        allow_headers=app_settings.CORS_HEADERS,
        allow_credentials=True,
    )
