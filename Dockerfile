# syntax=docker/dockerfile:1
FROM python:3.12-slim AS base
WORKDIR /app
COPY pyproject.toml /app/
RUN pip install --no-cache-dir uv pip && pip install --no-cache-dir -e .
COPY app /app/app
EXPOSE 8080
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8080"]
