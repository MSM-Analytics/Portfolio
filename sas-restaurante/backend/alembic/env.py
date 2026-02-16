import sys
from pathlib import Path

# backend/
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))


from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.core.database import Base
from app.core.settings import settings
from app.modules.gestao.models import *
from app.modules.gestao.models.product import Product
from app.modules.gestao.models.category import Category

# Alembic Config
config = context.config

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 👉 ESSENCIAL PARA AUTOGENERATE
target_metadata = Base.metadata


def get_database_url():
    return settings.DATABASE_URL


def run_migrations_offline():
    url = settings.database_url
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )


    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
    {
        "sqlalchemy.url": settings.DATABASE_URL
    },
    prefix="sqlalchemy.",
    poolclass=pool.NullPool,
)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
