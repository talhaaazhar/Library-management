# alembic/env.py

import sys
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# ------------------ PYTHON PATH FIX ------------------
# Add backend folder to Python path so 'app' can be imported
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# ------------------ APP IMPORTS ------------------
from app.core.config import settings
from app.core.database import Base
from app.models import *  # Import all models so Alembic sees them

# this is the Alembic Config object
config = context.config

# Setup logging
fileConfig(config.config_file_name)

# Override sqlalchemy.url in alembic.ini with your app's settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Metadata for autogenerate
target_metadata = Base.metadata

# ------------------ RUN MIGRATIONS ------------------
def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
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
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
