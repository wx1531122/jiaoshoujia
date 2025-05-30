import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Assuming `prepend_sys_path = .` in alembic.ini adds `backend/` to sys.path.
# So, 'app' should be importable as a package.

# add your model's MetaData object here
# for 'autogenerate' support
# In order for autogenerate to detect changes, it needs to know about all models.
# Import your models here so they are registered with Base.metadata
from app.db.database import Base  # Main Base for metadata
import app.users.models  # Import the module where User model is defined
# If you have other model modules, import them here too, e.g.:
# import app.items.models
# import app.products.models

target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # Use the DATABASE_URL from app.core.config.settings for offline mode too
    from app.core.config import settings
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # import settings here
    from app.core.config import settings # Assuming app is a package

    # Use the DATABASE_URL from settings
    db_url = settings.DATABASE_URL
    
    # Override the sqlalchemy.url from alembic.ini with the one from settings
    config.set_main_option("sqlalchemy.url", db_url) # This ensures alembic uses the correct URL

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
