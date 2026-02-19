FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    gettext \
    netcat-openbsd \
    gosu \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN addgroup --system app && adduser --system --ingroup app app && \
    mkdir -p /app/staticfiles /app/media /app/logs && \
    chmod +x /app/entrypoint.sh && \
    chown -R app:app /app

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
