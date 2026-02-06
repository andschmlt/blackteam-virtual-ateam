# /cloud_jobs - Virtual ATeam Cloud Run Jobs Manager

Manage scheduled jobs running on Google Cloud Run.

## Phase 0: RAG Context Loading

**Load relevant context from the RAG system.**

```python
from AS-Virtual_Team_System_v2.rag.rag_client import VTeamRAG
rag = VTeamRAG()
context = rag.query("cloud jobs cloud run deployment", top_k=3)
learnings = rag.query("cloud deployment corrections", collection_name="learnings", top_k=3)
```

---

## Usage

```
/cloud_jobs [command]
```

**Commands:**
- `status` (default) - Show all jobs and their status
- `list` - List Cloud Run jobs
- `schedulers` - List Cloud Scheduler triggers
- `run <job>` - Manually execute a job
- `logs <job>` - View recent logs
- `deploy` - Deploy/update the Synapse container
- `add` - Interactive job addition

## Execution

### Command: status (default)
```bash
bash /home/andre/synapse/cloud-run/manage_jobs.sh status
```

### Command: list
```bash
bash /home/andre/synapse/cloud-run/manage_jobs.sh list
```

### Command: schedulers
```bash
bash /home/andre/synapse/cloud-run/manage_jobs.sh schedulers
```

### Command: run <job-name>
```bash
bash /home/andre/synapse/cloud-run/manage_jobs.sh run $ARGS
```

### Command: logs <job-name>
```bash
bash /home/andre/synapse/cloud-run/manage_jobs.sh logs $ARGS
```

### Command: deploy
```bash
bash /home/andre/synapse/cloud-run/deploy.sh
```

### Command: add
Prompt for job details and run:
```bash
bash /home/andre/synapse/cloud-run/add_job.sh "$JOB_NAME" "$SCHEDULE" "$COMMAND" "$DESCRIPTION"
```

## Current Jobs

| Job Name | Schedule | Description |
|----------|----------|-------------|
| synapse-weekly-scrape | Sunday 11 PM UTC | Weekly AI news & skills scrape |
| clickup-roi-weekly | Monday 4 PM UTC | Weekly ROI task submission for ClickUp list 901323685943 |

## Adding New Jobs

Use the add_job.sh script:
```bash
/home/andre/synapse/cloud-run/add_job.sh \
    "job-name" \
    "0 6 * * *" \
    "python script.py" \
    "Description"
```

### Schedule Examples
- `0 * * * *` - Every hour
- `0 6 * * *` - Daily at 6 AM UTC
- `0 9,17 * * *` - Twice daily (9 AM, 5 PM UTC)
- `0 23 * * 0` - Weekly Sunday 11 PM UTC
- `*/15 * * * *` - Every 15 minutes

## Project Details

- **GCP Project:** paradisemedia-bi
- **Region:** us-central1
- **Container:** gcr.io/paradisemedia-bi/synapse
- **Service Account:** synapse-scheduler-sa@paradisemedia-bi.iam.gserviceaccount.com
