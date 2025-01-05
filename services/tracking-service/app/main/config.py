from os import environ as env

from pydantic import BaseModel, Field


class MongoDBConfig(BaseModel):
    uri: str = Field(alias="MONGODB_URI")
    db_name: str = Field(alias="MONGODB_DB_NAME")
    collection_name: str = Field(alias="MONGODB_COLLECTION_NAME")


class KafkaConfig(BaseModel):
    host: str = Field(alias="KAFKA_HOST")
    port: int = Field(alias="KAFKA_PORT")

    def uri(self):
        return f"{self.host}:{self.port}"


class Config(BaseModel):
    mongodb: MongoDBConfig = Field(default_factory=lambda: MongoDBConfig(**env))
    kafka: KafkaConfig = Field(default_factory=lambda: KafkaConfig(**env))
