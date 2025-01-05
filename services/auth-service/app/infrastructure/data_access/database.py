from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.main.config import PostgresConfig


def new_session_maker(psql_config: PostgresConfig) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(
        psql_config.DATABASE_URL,
    )

    return async_sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
