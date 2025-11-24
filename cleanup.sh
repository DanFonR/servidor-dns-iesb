#!/usr/bin/env bash
docker rm -f "$(docker ps -aq)"
docker compose -f docker/docker-compose.yml --env-file template.env down --volumes --remove-orphans
docker image prune -a -f
docker volume prune -f
docker container prune -f
docker network prune -f
# docker builder prune -f
