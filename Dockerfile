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

# Run with gunicorn + uvicorn workers for production resilience:
#   --max-requests: recycle workers after N requests (prevents memory leaks)
#   --max-requests-jitter: stagger recycling so workers don't all restart at once
#   --timeout: kill workers that hang for >60s
#   --graceful-timeout: give workers 10s to finish after SIGTERM
CMD ["sh", "-c", "uv run gunicorn kjvstudy_org.server:app --worker-class uvicorn.workers.UvicornWorker --bind ${HOST:-0.0.0.0}:${PORT:-8000} --workers ${WORKERS:-2} --max-requests 2000 --max-requests-jitter 500 --timeout 60 --graceful-timeout 10 --proxy-protocol --forwarded-allow-ips='*' --access-logfile -"]
