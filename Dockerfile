FROM python:3.14.7-slim-trixie 

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/


RUN pip install -r requirements.txt \
    && chmod +x start.sh

ENTRYPOINT [ "/bin/sh", "/app/start.sh" ]  