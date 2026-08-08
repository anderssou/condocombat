"""Pytest fixtures for CondoCombat backend tests."""

import os

# Define SECRET_KEY before any project import to ensure settings picks it up
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-tests-32chars-min!")

from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.database import Base

# Importa os modelos para garantir que todas as tabelas sejam registradas
# em Base.metadata antes do create_all() rodar na fixture abaixo.
import app.models  # noqa: F401


@pytest_asyncio.fixture
async def async_session():
    """AsyncSession real, contra um SQLite em memória.

    Usada nos testes de integração dos modelos (__tests__/test_models.py),
    onde queremos exercitar de verdade constraints, relacionamentos e
    defaults do banco — diferente da `mock_session` abaixo, que é só um
    mock para testes unitários de repository.
    """
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with session_maker() as session:
        yield session

    await engine.dispose()


@pytest.fixture
def mock_session():
    """Mock de AsyncSession para testes unitários de repository.

    Retorna AsyncMock para métodos async (commit, flush, etc.)
    e MagicMock para o Result de execute(), garantindo que métodos
    sync como scalar_one_or_none() e scalars().all() funcionem.
    """
    session = AsyncMock(spec=AsyncSession)
    result = MagicMock()
    result.scalar_one_or_none = MagicMock(return_value=None)
    scalars_mock = MagicMock()
    scalars_mock.all = MagicMock(return_value=[])
    result.scalars = MagicMock(return_value=scalars_mock)
    session.execute = AsyncMock(return_value=result)
    session.add = MagicMock()
    session.add_all = MagicMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.refresh = AsyncMock()
    session.delete = AsyncMock()
    session.close = AsyncMock()
    session.flush = AsyncMock()
    return session