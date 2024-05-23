from config.settings import app_settings

from sqlalchemy import MetaData

DATABASES = {
    'default': {
        'url': f'postgresql+asyncpg://{app_settings.DB_USER}:{app_settings.DB_PASSWORD}@{app_settings.DB_HOST}:{app_settings.DB_PORT}/{app_settings.DB_NAME}',
        'migrations_url': f'postgresql+psycopg://{app_settings.DB_USER}:{app_settings.DB_PASSWORD}@{app_settings.DB_HOST}:{app_settings.DB_PORT}/{app_settings.DB_NAME}',
    }
}


DB_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}


metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)
