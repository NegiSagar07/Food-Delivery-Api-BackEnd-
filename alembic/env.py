# File: alembic/env.py

import asyncio
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool

from alembic import context

# --- 1. ADD THESE IMPORTS ---
# This is the standard way to make your app's modules
# available to Alembic.
import sys, os
from pathlib import Path

# Add the project root directory to the Python path
# This allows Alembic to find your 'app' package
root_dir = Path(__file__).resolve().parents[1]
sys.path.append(str(root_dir))

# Now we can import our app's settings and models
from app.config import settings
from sqlmodel import SQLModel
# We must import all our models here
# so that SQLModel.metadata knows about them
from app import models
# -----------------------------

# This is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# --- 2. TELL ALEMBIC TO USE OUR SETTINGS ---
# We'll get the database URL from our app's settings
# instead of hardcoding it in alembic.ini
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
# ------------------------------------------

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- 3. SET OUR MODELS AS THE "TARGET" ---
# This tells Alembic what the "target" database schema
# should look like. It compares this metadata with the
# actual database to find the differences.
target_metadata = SQLModel.metadata
# ----------------------------------------

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.
    This just generates SQL scripts.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# --- 4. THE ASYNC ONLINE MIGRATION ---
# This is the new, async version of the online migration
def do_run_migrations(connection):
    """
    Helper function to run the actual migrations.
    """
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.
    This runs the migration scripts against the
    live database.
    """
    
    # Create an async engine from our app's settings
    connectable = create_async_engine(
        settings.DATABASE_URL,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        # Run the migrations synchronously
        await connection.run_sync(do_run_migrations)

    # Dispose of the engine
    await connectable.dispose()
# --------------------------------------

# --- 5. THE FINAL SWITCH ---
# This tells Alembic to run the correct function
# (offline or async-online)
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
# ---------------------------