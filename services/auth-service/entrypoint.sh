#!/bin/sh

echo "Waiting for kafka..."
while ! kcat -b $KAFKA_HOST:$KAFKA_PORT -L; do
    sleep 0.1
done
echo "Kafka started"

echo "Waiting for PostgreSQL..."
while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
    sleep 0.1
done
echo "PostgreSQL is ready."

# Применяем миграции Alembic
echo "Applying Alembic migrations..."
alembic upgrade head

exec "$@"
