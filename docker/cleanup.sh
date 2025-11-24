#!/usr/bin/env bash
docker compose -f ./docker-compose.yml --env-file ../.env down --volumes --remove-orphans
docker image prune -f
docker volume prune -f
docker network prune -f
