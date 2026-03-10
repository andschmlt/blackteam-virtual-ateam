#!/bin/bash
#
# PostHog 9-Domain Hourly Report Generator
# Director Rule 18 Compliant
# Active: 2026-01-29 ONLY
#

# Configuration
REPORT_DIR="/home/andre/reports"
SCRATCHPAD="/tmp/claude/-home-andre/7fdeec8b-87cf-4ab9-b95f-32fe4632fc7c/scratchpad"
LOG_FILE="/home/andre/reports/posthog_hourly.log"

# Check if still Jan 29
TODAY=$(date +%Y-%m-%d)
if [ "$TODAY" != "2026-01-29" ]; then
    echo "$(date): Hourly reports expired (today is not 2026-01-29)" >> "$LOG_FILE"
    # Remove this cron job
    crontab -l | grep -v "posthog_hourly_report" | crontab -
    exit 0
fi

TIMESTAMP=$(date +%Y%m%d_%H%M)
echo "$(date): Starting hourly PostHog report generation" >> "$LOG_FILE"

# Run analysis
cd "$SCRATCHPAD"
python3 posthog_9domains_analysis.py >> "$LOG_FILE" 2>&1

# Find latest MD file
MD_FILE=$(ls -t "$REPORT_DIR"/posthog_9domains_report_*.md 2>/dev/null | head -1)

if [ -z "$MD_FILE" ]; then
    echo "$(date): ERROR - No markdown report found" >> "$LOG_FILE"
    exit 1
fi

# Convert to PDF
PDF_FILE="${MD_FILE%.md}.pdf"
python3 "$SCRATCHPAD/md_to_pdf_9domains_v2.py" "$MD_FILE" "$PDF_FILE" >> "$LOG_FILE" 2>&1

if [ ! -f "$PDF_FILE" ]; then
    echo "$(date): ERROR - PDF conversion failed" >> "$LOG_FILE"
    exit 1
fi

# Send email
HOUR=$(date +%H:%M)
python3 /home/andre/.keys/send_email.py \
    "andre@paradisemedia.com" \
    "[PostHog 9-Domain Analysis] Hourly Report - $TODAY $HOUR" \
    "PostHog 9-Domain Hourly Report

Generated: $TODAY $HOUR
Report: $(basename $PDF_FILE)

This is an automated hourly report for 2026-01-29.
Product & Tech teams: Please review the attached PDF and flag any issues.

Full analysis attached.

---
BlackTeam Automated Reports" \
    --attachment "$PDF_FILE" >> "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    echo "$(date): Email sent successfully with $PDF_FILE" >> "$LOG_FILE"
else
    echo "$(date): ERROR - Email failed" >> "$LOG_FILE"
fi

echo "$(date): Hourly report complete" >> "$LOG_FILE"
