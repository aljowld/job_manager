from collections.abc import Generator

from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

# Bounds how long a connection attempt can take so an unreachable database
# fails fast (e.g. for the readiness check) instead of hanging indefinitely.
_CONNECT_TIMEOUT_SECONDS = 5

engine: Engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    connect_args={"connect_timeout": _CONNECT_TIMEOUT_SECONDS},
)
SessionLocal: sessionmaker[Session] = sessionmaker(
    bind=engine, autoflush=False, autocommit=False, expire_on_commit=False
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
