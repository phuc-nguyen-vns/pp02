# ARG TARGETPLATFORM=linux/arm64

FROM python:3.13-slim

# Environment variables for clean builds
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the official uv binary directly from their published container
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
COPY --from=ghcr.io/astral-sh/uv:latest /uvx /bin/uvx

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies using uv sync (from lock file)
RUN uv sync --locked

# Expose API port
EXPOSE 8001

# Start FastAPI app using uv environment
CMD ["uv", "run", "uvicorn", "server:api_server", "--host", "0.0.0.0", "--port", "8001", "--reload", "--workers", "4"]
