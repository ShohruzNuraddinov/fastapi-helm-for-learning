# syntax=docker/dockerfile:1.4

FROM python:3.9-alpine

RUN apk add libpq-dev gcc

WORKDIR /app

COPY requirments.txt .

RUN --mount=type=cache,target=/root/.cache \
    pip install --upgrade pip && \
    pip install -r requirments.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8082"]
