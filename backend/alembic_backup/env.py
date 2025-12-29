# alembic/env.py

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Import your app's settings and models
from app.core.config import settings
from app.core.database import Base
from app.models import *  # Import all models so Alembic sees them

# Alembic Config object, provides access to .ini values
config = context.config

# Setup Python logging from the config file
fileConfig(config.config_file_name)

# Override sqlalchemy.url in alembic.ini with your app's settings
config.set_main_option("sqlalchemy.url", settings.SQLALCHEMY_DATABASE_URL)

# Reference to your metadata for autogenerate support
target_metadata = Base.metadata

# -------------------- OFFLINE MIGRATIONS --------------------
def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# -------------------- ONLINE MIGRATIONS --------------------
def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


# -------------------- EXECUTE --------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
