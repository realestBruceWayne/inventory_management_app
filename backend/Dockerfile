FROM python:3.10-slim

WORKDIR /app
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Install necessary system dependencies for building Postgres packages
RUN apt-get update && apt-get install -y libpq-dev gcc bash && rm -rf /var/lib/apt/lists/*

# Copy uv binary directly
COPY --from=ghcr.io/astral-sh/uv:0.9.2 /uv /bin/

# Use bind mounts to dynamically install packages without needing a manual COPY step first
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --frozen --no-install-project

# Copy your backend project code into the container
COPY . .

ENV PATH="/app/.venv/bin:$PATH"

# Create startup script
RUN echo '#!/bin/bash\n\
echo "Running seed script..."\n\
uv run python seed_data.py\n\
echo "Starting server..."\n\
uv run uvicorn main:app --host 0.0.0.0 --port 8000\n\
' > /app/start.sh && chmod +x /app/start.sh

CMD ["/app/start.sh"]
