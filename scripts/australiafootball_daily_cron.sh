#!/bin/bash
# australiafootball.com Daily Report — Cron wrapper
# Runs the Python report script and logs output
#
# Cron entry (08:00 AEST = 22:00 UTC previous day):
#   0 22 * * * /home/andre/scripts/australiafootball_daily_cron.sh >> /home/andre/reports/australiafootball/cron.log 2>&1
#
# Or for 08:00 AEST if system is in UTC:
#   0 22 * * * /home/andre/scripts/australiafootball_daily_cron.sh

LOG_DIR="/home/andre/reports/australiafootball"
mkdir -p "$LOG_DIR"

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
echo "[$TIMESTAMP] Starting daily report..."

# Run the report
python3 /home/andre/scripts/australiafootball_daily_report.py >> "$LOG_DIR/cron.log" 2>&1
EXIT_CODE=$?

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
if [ $EXIT_CODE -eq 0 ]; then
    echo "[$TIMESTAMP] Report completed successfully (exit $EXIT_CODE)"
else
    echo "[$TIMESTAMP] Report failed (exit $EXIT_CODE)"
fi
