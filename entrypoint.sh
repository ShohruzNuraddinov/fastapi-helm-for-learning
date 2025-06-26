#!/bin/sh

if [ "$DATABASE" = "postgres" ]; then
    echo "Waiting for PostgreSQL..."

    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
        echo "PostgreSQL is not ready yet. Waiting..."
        sleep 1
    done

    echo "PostgreSQL started"
fi

echo "Starting the migrations..."
# Run the migrations
alembic upgrade head
echo "Migrations completed"