from pathlib import Path
from typing import Any

from pydantic_settings import BaseSettings

from helpers.constants.config import Environment


class Config(BaseSettings):
    SECRET_KEY: str

    SITE_DOMAIN: str = "myapp.com"

    ENVIRONMENT: Environment = Environment.PRODUCTION

    CORS_ORIGINS: list[str] = ["*"]
    CORS_ORIGINS_REGEX: str | None = None
    CORS_HEADERS: list[str] = {"Accept", "Accept-Language", "Content-Language", "Content-Type"}

    APP_VERSION: str = "1"

    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str


app_settings = Config()

app_configs: dict[str, Any] = {"title": "App API"}
if app_settings.ENVIRONMENT.is_deployed:
    app_configs["root_path"] = f"/v{app_settings.APP_VERSION}"

if not app_settings.ENVIRONMENT.is_debug:
    app_configs["openapi_url"] = None  # hide docs


BASE_PATH = Path(__file__).resolve().parent.parent

# JWT settings
JWT_AUDIENCE = f'app@{app_settings.SITE_DOMAIN}'
ACCESS_TOKEN_EXPIRE_MINUTES = 5
REFRESH_TOKEN_EXPIRE_MINUTES = 30
JWT_ALGORITHM = 'HS256'
JWT_LEEWAY_SECONDS = 10
