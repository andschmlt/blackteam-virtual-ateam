#!/bin/bash
# BlackTeam Daily Log Generator - Cron Wrapper
# Runs at 17:00 daily via cron

# Set environment variables
export CLICKUP_API_KEY=$(cat /home/andre/.claude/clickup_config.json | python3 -c "import json,sys; print(json.load(sys.stdin)['CLICKUP_API_KEY'])")

# Run the daily log generator
python3 /home/andre/blackteam_daily_logs.py >> /home/andre/.claude/logs/daily_logs_cron.log 2>&1

# Log completion
echo "[$(date)] Daily log generation completed" >> /home/andre/.claude/logs/daily_logs_cron.log
