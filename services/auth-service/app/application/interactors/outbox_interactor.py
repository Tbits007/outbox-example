import asyncio

from aiokafka import AIOKafkaProducer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.application.interfaces.outbox_interface import OutboxUpdater
from app.application.interfaces.uow_interface import UnitOfWork
from app.domain.entities.message_entity import MessageStatus
from app.infrastructure.data_access.models.message_model import DBMessage


class OutboxRelayInteractor:
    def __init__(
        self, session: AsyncSession, producer: AIOKafkaProducer, outbox_gateway: OutboxUpdater, uow: UnitOfWork
    ) -> None:
        self._session = session
        self._producer = producer
        self._outbox_gateway = outbox_gateway
        self._uow = uow

    async def __call__(self) -> None:
        while True:
            events_query = select(DBMessage).where(DBMessage.status == MessageStatus.PENDING.value)
            events = (await self._session.execute(events_query)).scalars().all()

            for event in events:
                async with self._uow:
                    await self._producer.send_and_wait(topic="user-actions", value=event.payload.encode("utf-8"))
                    await self._outbox_gateway.update(event.id, {"status": MessageStatus.SENT.value})
                    await self._uow.commit()
            await asyncio.sleep(5)
