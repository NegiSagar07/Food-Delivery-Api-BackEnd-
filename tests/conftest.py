# File: tests/conftest.py (FINAL, CORRECTED VERSION)

import sys
from pathlib import Path

# Add the project root directory (food-delivery-app/) to the Python path
ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))

import pytest
import pytest_asyncio
from typing import AsyncGenerator
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlmodel import SQLModel
from contextlib import asynccontextmanager  # <-- 1. IMPORT THIS

from app.main import app
from app.database import get_db
from app import models 

# --- Test Database (This is all correct) ---
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestSessionLocal = async_sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=test_engine
)

# --- Test DB Session Fixture (This is all correct) ---
@pytest_asyncio.fixture(scope="session")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    async with TestSessionLocal() as session:
        yield session
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

# --- Dependency Override (This is all correct) ---
async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with TestSessionLocal() as session:
        yield session

# --- 2. THIS IS THE FIX ---
@asynccontextmanager
async def dummy_lifespan(app):
    """
    A dummy lifespan function that does nothing.
    This replaces the app's real lifespan to prevent
    the 'create_all' conflict during tests.
    """
    print("INFO:     Skipping app lifespan for tests.")
    yield  # This makes it a valid async context manager
    print("INFO:     Skipped app lifespan for tests.")
# -------------------------

# --- 3. The Test Client Fixture (Also Fixed) ---
@pytest.fixture(scope="function")
def client(db_session: AsyncSession) -> TestClient: # type: ignore
    """
    Fixture to create a synchronous TestClient.
    """
    # Save the app's original lifespan
    original_lifespan = app.router.lifespan_context
    
    # --- 4. APPLY THE FIX ---
    # Set the lifespan to our dummy function
    app.router.lifespan_context = dummy_lifespan
    # -----------------------
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clean up
    app.dependency_overrides.clear()
    app.router.lifespan_context = original_lifespan