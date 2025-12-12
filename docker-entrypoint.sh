#!/bin/bash
# 1. Create the log file so 'tail' doesn't fail
touch /var/log/cron.log

# 2. Start cron in the background and pipe its output to the file
#    The '-L' option is removed as we are manually piping the output to the file
crond -f 2>&1 | tee -a /var/log/cron.log &

# 3. Wait a moment for crond to start up before checking logs
sleep 5

# 4. Keep the container running indefinitely by tailing the log
#    This is now safe because the file exists.
echo "Cron daemon started. Tailing /var/log/cron.log..."
tail -f /var/log/cron.log