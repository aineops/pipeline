#!/bin/bash
MAX_WAIT=120  # Maximum wait time in seconds
WAIT_INTERVAL=10  # Interval to wait between checks in seconds
while [ $MAX_WAIT -gt 0 ]; do
    if docker-compose ps | grep -q '(healthy)'; then
        echo 'Tous les conteneurs sont en état healthy.'
        break
    fi
    echo "En attente des conteneurs... Reste $MAX_WAIT secondes."
    sleep $WAIT_INTERVAL
    MAX_WAIT=$(($MAX_WAIT-$WAIT_INTERVAL))
done
if [ $MAX_WAIT -le 0 ]; then
    echo 'Timeout atteint. Tous les conteneurs ne sont pas up and running.'
    exit 1
fi
