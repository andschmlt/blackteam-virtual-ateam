#!/bin/bash
# Hudson Reporter PostHog Monitor - Runs every 30 minutes
# Started: $(date)

LOG_FILE="/home/andre/scripts/hudson_monitor.log"

echo "Starting Hudson Reporter PostHog Monitor at $(date)" >> "$LOG_FILE"
echo "Will run every 30 minutes until stopped" >> "$LOG_FILE"

while true; do
    echo "" >> "$LOG_FILE"
    echo "========================================" >> "$LOG_FILE"
    echo "Running report at $(date)" >> "$LOG_FILE"
    echo "========================================" >> "$LOG_FILE"
    
    python3 /home/andre/scripts/hudson_posthog_monitor.py >> "$LOG_FILE" 2>&1
    
    echo "Sleeping for 30 minutes..." >> "$LOG_FILE"
    sleep 1800
done
