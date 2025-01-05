from aiokafka import AIOKafkaConsumer
import asyncio

from dishka import make_async_container

from app.application.dtos.action_dtos import CreateActionDTO
from app.application.interactors.action_interactors import CreateActionInteractor
from app.main.config import Config
from app.main.ioc.providers.action import ActionProvider
from app.main.ioc.providers.root import RootProvider


async def consume(config: Config, interactor: CreateActionInteractor):
    consumer = AIOKafkaConsumer(
        'user-actions',
        bootstrap_servers=config.kafka.uri(),
    )
    await consumer.start()
    try:
        async for msg in consumer:
            result = msg.value.decode("utf-8")
            dto = CreateActionDTO(
                email=result["email"],
                action_type=result["action_type"],
                details=result["details"],
            )
            await interactor(dto)
    finally:
        await consumer.stop()


async def main():
    config = Config()
    container = make_async_container(
        RootProvider(),
        ActionProvider(),
        context={Config: config},
    )
    async with container() as nested_container:
        interactor = await nested_container.get(CreateActionInteractor)
        await consume(config, interactor)    
    

if __name__ == "__main__":
    asyncio.run(main())