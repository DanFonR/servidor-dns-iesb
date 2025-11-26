FROM postgres:latest

RUN apt-get update && rm -rf /var/lib/apt/lists/*

COPY schema.sql /docker-entrypoint-initdb.d/
WORKDIR /docker-entrypoint-initdb.d/
