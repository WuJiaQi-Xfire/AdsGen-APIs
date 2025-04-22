# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app/backend

# ─── 系统依赖 ───────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# ─── Python 依赖 ───────────────────────────────────────────
COPY requirements.txt .
RUN python -m pip install --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements.txt

# ─── 应用代码 ──────────────────────────────────────────────
COPY . .

# 使用环境变量设置端口
ARG BACKEND_PORT=8000
ENV BACKEND_PORT=${BACKEND_PORT}

EXPOSE ${BACKEND_PORT}
CMD uvicorn src.main:app --host 0.0.0.0 --port ${BACKEND_PORT}
