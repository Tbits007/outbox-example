from typing import AsyncGenerator

from aiokafka import AIOKafkaProducer
from dishka import Provider, Scope, from_context, provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.application.interfaces.email_provider_interface import EmailProvider
from app.application.interfaces.email_sender_interface import EmailSender
from app.application.interfaces.link_creator_interface import LinkCreator
from app.application.interfaces.uow_interface import UnitOfWork
from app.infrastructure.adapters.email_provider import SimpleEmailProvider
from app.infrastructure.adapters.email_sender import SMTPEmailSender
from app.infrastructure.adapters.link_creator import SimpleLinkCreator
from app.infrastructure.adapters.uow import SAUnitOfWork
from app.infrastructure.data_access.database import new_session_maker
from app.main.config import Config


class RootProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config.postgres_)

    @provide(scope=Scope.REQUEST)
    async def get_session(self, session_maker: async_sessionmaker[AsyncSession]) -> AsyncGenerator[AsyncSession, None]:
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    def email_sender(self, config: Config) -> EmailSender:
        return SMTPEmailSender(
            smtp_server=config.smtp_.host,
            smtp_port=config.smtp_.port,
            username=config.smtp_.login,
            password=config.smtp_.password,
        )

    @provide(scope=Scope.APP)
    def get_producer(self, config: Config) -> AIOKafkaProducer:
        return AIOKafkaProducer(bootstrap_servers=config.kafka_.uri)

    email_provider = provide(
        SimpleEmailProvider,
        scope=Scope.REQUEST,
        provides=EmailProvider,
    )

    link_creator = provide(
        SimpleLinkCreator,
        scope=Scope.REQUEST,
        provides=LinkCreator,
    )

    unit_of_work = provide(
        SAUnitOfWork,
        scope=Scope.REQUEST,
        provides=UnitOfWork,
    )
