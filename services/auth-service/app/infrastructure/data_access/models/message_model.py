from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.data_access.models.base_model import Base


class DBMessage(Base):
    __tablename__ = "outbox"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    payload: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(255), nullable=False)
