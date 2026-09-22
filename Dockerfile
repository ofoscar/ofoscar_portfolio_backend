FROM python:3.12-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY . .

RUN uv sync --locked --no-dev

ENV PATH="/app/.venv/bin:$PATH"

CMD ["fastapi", "run", "src/ofoscar_backend/main.py", "--host", "0.0.0.0", "--port", "8000"]