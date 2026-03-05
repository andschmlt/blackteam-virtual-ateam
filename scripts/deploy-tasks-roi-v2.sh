#!/bin/bash
# =============================================================================
# TASKS ROI ENGINE v2.0 - Deployment Script
# Master List v1.0 Compliant
# =============================================================================
# Author: W-FLUX (Felix Chang) - WhiteTeam Head of Tech
# Created: 2026-02-03
#
# This script:
# 1. Cleans up old/duplicate Cloud Run jobs and schedulers
# 2. Builds and deploys the v2.0 engine
# 3. Creates a single scheduler for Monday 16:00 UTC
# =============================================================================

set -e

PROJECT_ID="paradisemedia-bi"
REGION="us-central1"
JOB_NAME="tasks-roi-engine-v2"
SCHEDULER_NAME="tasks-roi-weekly-v2"
DAILY_SCHEDULER_NAME="tasks-roi-daily-v2"

echo "============================================================"
echo "TASKS ROI ENGINE v2.0 - DEPLOYMENT"
echo "Master List v1.0 Compliant"
echo "============================================================"
echo ""

# -----------------------------------------------------------------------------
# Step 1: Clean up old Cloud Run jobs
# -----------------------------------------------------------------------------
echo "Step 1: Cleaning up old Cloud Run jobs..."

OLD_JOBS=("clickup-roi-weekly" "tasks-roi-weekly")
for job in "${OLD_JOBS[@]}"; do
    if gcloud run jobs describe "$job" --region="$REGION" --project="$PROJECT_ID" &>/dev/null; then
        echo "  Deleting old job: $job"
        gcloud run jobs delete "$job" --region="$REGION" --project="$PROJECT_ID" --quiet
    else
        echo "  Job not found (already deleted): $job"
    fi
done

echo "  ✓ Old jobs cleaned up"
echo ""

# -----------------------------------------------------------------------------
# Step 2: Clean up old schedulers
# -----------------------------------------------------------------------------
echo "Step 2: Cleaning up old schedulers..."

OLD_SCHEDULERS=("clickup-roi-weekly-trigger" "tasks-roi-monday")
for sched in "${OLD_SCHEDULERS[@]}"; do
    if gcloud scheduler jobs describe "$sched" --location="$REGION" --project="$PROJECT_ID" &>/dev/null; then
        echo "  Deleting old scheduler: $sched"
        gcloud scheduler jobs delete "$sched" --location="$REGION" --project="$PROJECT_ID" --quiet
    else
        echo "  Scheduler not found (already deleted): $sched"
    fi
done

echo "  ✓ Old schedulers cleaned up"
echo ""

# -----------------------------------------------------------------------------
# Step 3: Build and deploy new v2 job
# -----------------------------------------------------------------------------
echo "Step 3: Building and deploying v2.0..."

cd /home/andre/scripts

# Build using Cloud Build
gcloud builds submit \
    --config=cloudbuild-tasks-roi-v2.yaml \
    --project="$PROJECT_ID" \
    .

echo "  ✓ v2.0 deployed"
echo ""

# -----------------------------------------------------------------------------
# Step 4: Create new scheduler (Monday 16:00 UTC)
# -----------------------------------------------------------------------------
echo "Step 4: Creating new scheduler..."

# Get the service account for Cloud Run invocation
SA_EMAIL="synapse-scheduler-sa@${PROJECT_ID}.iam.gserviceaccount.com"

# Create or update the weekly scheduler
if gcloud scheduler jobs describe "$SCHEDULER_NAME" --location="$REGION" --project="$PROJECT_ID" &>/dev/null; then
    echo "  Weekly scheduler already exists, updating..."
    gcloud scheduler jobs update http "$SCHEDULER_NAME" \
        --location="$REGION" \
        --project="$PROJECT_ID" \
        --schedule="0 16 * * 1" \
        --time-zone="UTC" \
        --uri="https://${REGION}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${PROJECT_ID}/jobs/${JOB_NAME}:run" \
        --http-method="POST" \
        --oauth-service-account-email="$SA_EMAIL" \
        --description="Weekly Tasks ROI Analysis - Master List v1.0 Compliant"
else
    gcloud scheduler jobs create http "$SCHEDULER_NAME" \
        --location="$REGION" \
        --project="$PROJECT_ID" \
        --schedule="0 16 * * 1" \
        --time-zone="UTC" \
        --uri="https://${REGION}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${PROJECT_ID}/jobs/${JOB_NAME}:run" \
        --http-method="POST" \
        --oauth-service-account-email="$SA_EMAIL" \
        --description="Weekly Tasks ROI Analysis - Master List v1.0 Compliant"
fi

echo "  ✓ Scheduler created: $SCHEDULER_NAME (Monday 16:00 UTC)"
echo ""

# -----------------------------------------------------------------------------
# Step 4b: Create daily delta scheduler (10pm Malta time)
# -----------------------------------------------------------------------------
echo "Step 4b: Creating daily delta scheduler..."

# The daily job uses the same Cloud Run Job but with --daily-delta flag.
# Cloud Scheduler triggers Cloud Run Jobs via HTTP POST. To pass different args
# we override the container args in the job execution request body.
DAILY_BODY='{"overrides":{"containerOverrides":[{"args":["--list-id","901323685943","--date-range","ytd","--display","both","--daily-delta"]}]}}'

if gcloud scheduler jobs describe "$DAILY_SCHEDULER_NAME" --location="$REGION" --project="$PROJECT_ID" &>/dev/null; then
    echo "  Daily scheduler already exists, updating..."
    gcloud scheduler jobs update http "$DAILY_SCHEDULER_NAME" \
        --location="$REGION" \
        --project="$PROJECT_ID" \
        --schedule="0 22 * * *" \
        --time-zone="Europe/Malta" \
        --uri="https://${REGION}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${PROJECT_ID}/jobs/${JOB_NAME}:run" \
        --http-method="POST" \
        --message-body="$DAILY_BODY" \
        --headers="Content-Type=application/json" \
        --oauth-service-account-email="$SA_EMAIL" \
        --description="Daily Tasks ROI Delta Check - 10pm Malta time"
else
    gcloud scheduler jobs create http "$DAILY_SCHEDULER_NAME" \
        --location="$REGION" \
        --project="$PROJECT_ID" \
        --schedule="0 22 * * *" \
        --time-zone="Europe/Malta" \
        --uri="https://${REGION}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${PROJECT_ID}/jobs/${JOB_NAME}:run" \
        --http-method="POST" \
        --message-body="$DAILY_BODY" \
        --headers="Content-Type=application/json" \
        --oauth-service-account-email="$SA_EMAIL" \
        --description="Daily Tasks ROI Delta Check - 10pm Malta time"
fi

echo "  ✓ Scheduler created: $DAILY_SCHEDULER_NAME (daily 22:00 Europe/Malta)"
echo ""

# -----------------------------------------------------------------------------
# Step 5: Verification
# -----------------------------------------------------------------------------
echo "Step 5: Verification..."
echo ""

echo "Cloud Run Jobs:"
gcloud run jobs list --region="$REGION" --project="$PROJECT_ID" --filter="name:tasks-roi"
echo ""

echo "Schedulers:"
gcloud scheduler jobs list --location="$REGION" --project="$PROJECT_ID" --filter="name:tasks-roi"
echo ""

echo "============================================================"
echo "DEPLOYMENT COMPLETE"
echo "============================================================"
echo ""
echo "New job: $JOB_NAME"
echo "Weekly scheduler: $SCHEDULER_NAME (Monday 16:00 UTC)"
echo "Daily scheduler:  $DAILY_SCHEDULER_NAME (daily 22:00 Europe/Malta)"
echo ""
echo "To test manually:"
echo "  Monday run:  gcloud run jobs execute $JOB_NAME --region=$REGION"
echo "  Daily delta: gcloud run jobs execute $JOB_NAME --region=$REGION --args='--list-id,901323685943,--date-range,ytd,--display,both,--daily-delta'"
echo ""
echo "============================================================"
