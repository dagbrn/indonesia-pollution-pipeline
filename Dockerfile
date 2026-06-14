FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# create non-root user for security
RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/*

RUN adduser --disabled-password --no-create-home appuser

# install dependencies first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy only source files needed at runtime
COPY src/ ./src/
COPY settings/ ./settings/
COPY data/ ./data/

USER appuser

CMD ["python", "src/main.py"]
