from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.application.interfaces.uow_interface import UnitOfWork


class SAUnitOfWork(UnitOfWork):
    """Sqlalchemy unit of work"""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def __aenter__(self) -> "UnitOfWork":
        return self

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        await self.rollback()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
