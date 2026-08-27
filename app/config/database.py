from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from app.core.customException import CustomException
from fastapi import status
from app.config.secretes import secretes
from sqlalchemy.exc import SQLAlchemyError

if not secretes.DB_URL:
    raise RuntimeError("DB_URL environment variable is not set")

class Base(DeclarativeBase):
    pass

engine = create_async_engine(
    secretes.DB_URL,
    pool_pre_ping=True,
    echo=True
)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False,
)

async def get_db():
    try:
      async with SessionLocal() as db:
        yield db
    except SQLAlchemyError:
        raise CustomException(status.HTTP_503_SERVICE_UNAVAILABLE, "Database service is temporarily unavailable")

"""
| Option                   | Definition                                                                                      |
| ------------------------ | ----------------------------------------------------------------------------------------------- |
| `bind=engine`            | Connects the session factory to the SQLAlchemy engine.                                          |
| `class_=AsyncSession`    | Tells the factory to create asynchronous database sessions.                                     |
| `autoflush=False`        | Prevents SQLAlchemy from automatically flushing pending changes before queries.                 |
| `expire_on_commit=False` | Keeps ORM object's loaded attributes available after `commit()`.                                |
| `pool_pre_ping=True`     | Checks whether a pooled DB connection is alive before using it; this belongs to the **engine**. |
"""