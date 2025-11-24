FROM postgres:latest

RUN apt-get update && apt-get install -y postgresql-${PG_MAJOR}-cron && rm -rf /var/lib/apt/lists/*

COPY schema.sql /docker-entrypoint-initdb.d/
WORKDIR /docker-entrypoint-initdb.d/
