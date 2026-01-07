# syntax=docker/dockerfile:1.4
FROM python:3.9-alpine AS builder

# Install build dependencies
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    libpq-dev

WORKDIR /app

# Copy only requirements first for better caching
COPY requirments.txt .

# Install Python dependencies
RUN --mount=type=cache,target=/root/.cache \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --no-compile -r requirments.txt && \
    find /usr/local/lib/python3.9 -type d -name "tests" -exec rm -rf {} + 2>/dev/null || true && \
    find /usr/local/lib/python3.9 -type d -name "*.dist-info" -exec rm -rf {}/direct_url.json {} + 2>/dev/null || true && \
    find /usr/local/lib/python3.9 -name "*.so" -exec strip {} + 2>/dev/null || true

# Final stage
FROM python:3.9-alpine

# Install only runtime dependencies
RUN apk add --no-cache libpq

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin


# Copy application code
COPY . .

# Remove unnecessary files
RUN find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true && \
    find . -type f -name "*.pyc" -delete && \
    find . -type f -name "*.pyo" -delete && \
    rm -rf .git .gitignore .dockerignore README.md tests/ *.md 2>/dev/null || true
