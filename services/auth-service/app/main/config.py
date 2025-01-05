from os import environ as env

from pydantic import BaseModel, Field


class PostgresConfig(BaseModel):
    host: str = Field(alias="POSTGRES_HOST")
    port: int = Field(alias="POSTGRES_PORT")
    login: str = Field(alias="POSTGRES_USER")
    password: str = Field(alias="POSTGRES_PASSWORD")
    database: str = Field(alias="POSTGRES_DB")

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.login}:{self.password}@{self.host}:{self.port}/{self.database}"


class JwtConfig(BaseModel):
    SECRET_KEY: str = Field(alias="SECRET_KEY")
    ALGORITHM: str = Field(alias="ALGORITHM")
    ACCESS_TOKEN_EXPIRES_MINUTES: int = Field(alias="ACCESS_TOKEN_EXPIRES_MINUTES")
    REFRESH_TOKEN_EXPIRES_MINUTES: int = Field(alias="REFRESH_TOKEN_EXPIRES_MINUTES")


class SmtpConfig(BaseModel):
    host: str = Field(alias="SMTP_HOST")
    port: int = Field(alias="SMTP_PORT")
    login: str = Field(alias="SMTP_USER")
    password: str = Field(alias="SMTP_PASSWORD")


class KafkaConfig(BaseModel):
    host: str = Field(alias="KAFKA_HOST")
    port: int = Field(alias="KAFKA_PORT")

    def uri(self):
        return f"{self.host}:{self.port}"


class Config(BaseModel):
    postgres_: PostgresConfig = Field(default_factory=lambda: PostgresConfig(**env))
    smtp_: SmtpConfig = Field(default_factory=lambda: SmtpConfig(**env))
    jwt_: JwtConfig = Field(default_factory=lambda: JwtConfig(**env))
    kafka_: KafkaConfig = Field(default_factory=lambda: KafkaConfig(**env))
