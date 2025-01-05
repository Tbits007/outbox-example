from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.application.interfaces.outbox_interface import OutboxReader, OutboxSaver, OutboxUpdater
from app.domain.entities.message_entity import Message
from app.infrastructure.data_access.models.message_model import DBMessage


class OutboxGateway(OutboxSaver, OutboxReader, OutboxUpdater):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, message: Message) -> None:
        new_outbox = DBMessage(payload=message.payload, status=message.status)
        self._session.add(new_outbox)

    async def read_all(self) -> list[Message]:
        result = await self._session.execute(select(DBMessage))
        rows = result.scalars().all()
        return [Message(id=row.id, payload=row.payload, status=row.status) for row in rows]

    async def update(self, id: int, update_data: dict) -> Message | None:
        query = select(DBMessage).where(DBMessage.id == id)
        result = await self._session.execute(query)
        db_message = result.scalar_one()
        if not db_message:
            raise Exception("Message not found")

        for field, value in update_data.items():
            if hasattr(db_message, field):
                setattr(db_message, field, value)

        return Message(id=db_message.id, payload=db_message.payload, status=db_message.status)
