FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install system dependencies (optional)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create data directory for SQLite
RUN mkdir -p /app/data

EXPOSE 5000

# Use Gunicorn with the application factory
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()"]