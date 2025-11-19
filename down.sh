#!/usr/bin/env bash
docker compose -f docker/docker-compose.yml --env-file template.env down -v

