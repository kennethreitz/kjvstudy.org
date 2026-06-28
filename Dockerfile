FROM python:3.13 AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies into the system
RUN uv sync --frozen --no-install-project --no-dev

FROM python:3.13-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Install runtime dependencies (healthcheck + WeasyPrint system deps)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libpango-1.0-0 \
    libharfbuzz0b \
    libpangoft2-1.0-0 \
    libffi8 \
    libgdk-pixbuf-2.0-0 \
    shared-mime-info \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH="/app" \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY . .

# Build search index at image build time for fast searches
RUN python3 -c "from kjvstudy_org.utils.search_index import init_search_index; init_search_index()"

# Run with granian for production:
#   Rust-based ASGI server — static files served directly from Rust layer
CMD ["sh", "-c", "uv run granian kjvstudy_org.server:api --interface asgi --host ${HOST:-0.0.0.0} --port ${PORT:-8000} --workers ${WORKERS:-2} --runtime-threads ${RUNTIME_THREADS:-2} --respawn-failed-workers --access-log --static-path-route /static --static-path-mount /app/kjvstudy_org/static --static-path-expires 86400"]
