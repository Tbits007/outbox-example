import motor.motor_asyncio
from dishka import Provider, Scope, from_context, provide
from faststream.kafka import KafkaBroker


from app.main.config import Config


class RootProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)
    broker = from_context(provides=KafkaBroker, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_client(
        self,
        config: Config
    ) -> motor.motor_asyncio.AsyncIOMotorClient:
        return motor.motor_asyncio.AsyncIOMotorClient(config.mongodb.uri)

    @provide(scope=Scope.APP)
    def get_collection(
        self,
        config: Config,
        client: motor.motor_asyncio.AsyncIOMotorClient,
    ) -> motor.motor_asyncio.AsyncIOMotorCollection:
        db = client[config.mongodb.db_name]
        collection = db[config.mongodb.collection_name]
        return collection
