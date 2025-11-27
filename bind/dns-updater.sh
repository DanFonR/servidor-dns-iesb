#!/bin/bash

ZONE_FILE=${ZONE_FILE:-/zones/db.aredanvisa.local}
FRONTENDS=$(echo $FRONTENDS | tr ',' ' ')
INTERVAL=5

function bump_serial() {
    sed -i 's/^\(\s*[0-9]\{10\}\)\s*;/echo $(date +%Y%m%d%H)/e' "$ZONE_FILE"
}

while true; do
    echo "[DNS-UPDATER] Checking frontend containers..."

    TMP=$(mktemp)

    # Copy everything except old frontend entries
    awk '!/www.*A 10\.11\.0\./' "$ZONE_FILE" > "$TMP"

    # Detect running frontends
    for name in $FRONTENDS; do
        RUNNING=$(docker inspect -f '{{.State.Running}}' "$name" 2>/dev/null)

        if [[ "$RUNNING" == "true" ]]; then
            IP=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "$name")
            echo "www IN A $IP" >> "$TMP"
            echo "[DNS-UPDATER] $name is UP → adding $IP"
        else
            echo "[DNS-UPDATER] $name is DOWN → removing from DNS"
        fi
    done

    mv "$TMP" "$ZONE_FILE"

    bump_serial
    rndc reload

    sleep $INTERVAL
done
