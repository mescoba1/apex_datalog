#!/bin/bash
# Start cron in the foreground
crond -f -L /var/log/cron.log &

# Keep the container running indefinitely
tail -f /var/log/cron.log