#!/bin/sh
set -e

# Default to 1600 if not provided
PUID="${PUID:-1600}"
PGID="${PGID:-1600}"
USER="${USER:-apiusr}"
GROUP="${USER:-apiusr}"
CHOWNPATH="/netflowParser"

# Create group if missing
if ! getent group "$GROUP" >/dev/null 2>&1; then
    addgroup -g "$PGID" "$GROUP"
fi

# Create user if missing
if ! id -u "$USER" >/dev/null 2>&1; then
    adduser -D -u "$PUID" -G "$GROUP" "$USER"
fi

# Download IP2Location database
if [[ -n "$IP2LOC_TOKEN" ]]; then
    wget -O "$CHOWNPATH"/IP2LOCATION-LITE-DB9.BIN "https://www.ip2location.com/download/?token="$IP2LOC_TOKEN"&file=DB9LITEBIN"
fi

# Fix permissions (only do this on /app/API)
chown -R "$PUID:$PGID" "$CHOWNPATH"

# Create an updater process
(
while true; do
    sleep 12h
    su-exec "$PUID:$PGID" "/bin/sh" "$CHOWNPATH"/updateIP2Lbin.sh || true
done
) &

# Drop privileges & run command
exec su-exec "$PUID:$PGID" "$@"
