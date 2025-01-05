import asyncio

from dishka import make_async_container

from app.application.interactors.outbox_interactor import OutboxRelayInteractor
from app.main.config import Config
from app.main.ioc.providers.auth import AuthProvider
from app.main.ioc.providers.outbox import OutboxProvider
from app.main.ioc.providers.root import RootProvider
from app.main.ioc.providers.user import UserProvider


async def main():
    config = Config()
    container = make_async_container(
        RootProvider(),
        AuthProvider(),
        UserProvider(),
        OutboxProvider(),
        context={Config: config},
    )
    async with container() as nested_container:
        interactor = await nested_container.get(OutboxRelayInteractor)
        await interactor()


if __name__ == "__main__":
    asyncio.run(main())
