# /rag_health - RAG System Health Check & Monitoring

Monitor the Virtual Team v2 RAG system health, verify learnings capture, and check vector database status.

## Phase 0: RAG Bootstrap

**Initialize RAG connection before health check.**

```python
from AS-Virtual_Team_System_v2.rag.rag_client import VTeamRAG
rag = VTeamRAG()
# Verify connection before running diagnostics
```

---

## Usage

```
/rag_health              # Full health check report
/rag_health quick        # Quick status only
/rag_health json         # JSON output for automation
```

Arguments: $ARGUMENTS

---

## What This Command Checks

### 1. Vector Database (ChromaDB / ChromaDB-GCS)
- Total documents stored
- Collection statistics (personas, rules, learnings, skills, projects)
- Database path and health status
- **GCS-backed mode (Cloud Run):** Bucket, prefix, sync status

### 2. Cloud RAG Providers (if configured)
- ChromaDB-GCS (auto-detected via GCS_BUCKET env var)
- Qdrant Cloud status
- Pinecone status
- Connection health

### 3. Learnings Files
- BlackTeam learnings (`~/AS-Virtual_Team_System_v2/blackteam/skills/learnings/`)
- WhiteTeam learnings (`~/AS-Virtual_Team_System_v2/whiteteam/skills/learnings/`)
- Recent files (last 7 days)
- Today's capture status

### 4. Pitaya Feedback
- Feedback corrections file status
- Correction count
- Last modified date

### 5. Capture History
- Recent `/capture_learnings` invocations
- Auto-capture events
- Pitaya feedback loops

---

## Execution

When `/rag_health` is invoked:

```bash
# Run the health check script
cd ~/AS-Virtual_Team_System_v2
python3 rag/scripts/rag_health_check.py
```

For quick check:
```bash
python3 rag/scripts/rag_health_check.py --quick
```

For JSON output:
```bash
python3 rag/scripts/rag_health_check.py --json
```

---

## Expected Output

### Local Mode (Development)
```
======================================================================
RAG HEALTH CHECK REPORT
Timestamp: 2026-02-04T15:30:00
Status: HEALTHY
======================================================================

📊 VECTOR DATABASE (ChromaDB)
----------------------------------------
  Path: /home/andre/.claude/rag/virtual_team_v2
  Status: healthy
  Total Documents: 2,180
  Collections:
    - vteam_skills: 903 docs
    - vteam_learnings: 50 docs
    - vteam_projects: 448 docs
    - vteam_rules: 222 docs
    - vteam_personas: 557 docs

☁️  CLOUD RAG PROVIDERS
----------------------------------------
  ⚪ Qdrant: not_configured
  ⚪ Pinecone: not_configured
```

### Cloud Run Mode (GCS_BUCKET set)
```
======================================================================
RAG HEALTH CHECK REPORT
Timestamp: 2026-02-04T15:30:00
Status: HEALTHY
======================================================================

📊 VECTOR DATABASE (ChromaDB-GCS)
----------------------------------------
  GCS Bucket: gs://virtual-ateam-rag/chromadb/virtual_team_v2/
  Local Cache: /tmp/chroma/virtual_team_v2
  GCS Status: ✅ Connected
  Status: healthy
  Total Documents: 2,180
  Collections:
    - vteam_skills: 903 docs
    - vteam_learnings: 50 docs
    - vteam_projects: 448 docs
    - vteam_rules: 222 docs
    - vteam_personas: 557 docs

☁️  CLOUD RAG PROVIDERS
----------------------------------------
  ⚪ Qdrant: not_configured
  ⚪ Pinecone: not_configured

📚 LEARNINGS FILES
----------------------------------------
  BlackTeam: ~/AS-Virtual_Team_System_v2/blackteam/skills/learnings/
    Total files: 12
    Recent (7 days): 3
    Captured today: ✅ Yes
  WhiteTeam: ~/AS-Virtual_Team_System_v2/whiteteam/skills/learnings/
    Total files: 8
    Recent (7 days): 2
    Captured today: ✅ Yes

📅 RECENT LEARNINGS FILES
----------------------------------------
  - 2026-02-04_cloud_validation.md (2026-02-04)
  - 2026-02-03_session_learnings.md (2026-02-03)

🍈 PITAYA FEEDBACK
----------------------------------------
  Path: ~/pitaya/knowledge/feedback_corrections.md
  Corrections: 15
  Last modified: 2026-02-03

📈 SUMMARY
----------------------------------------
  Total Vector Documents: 2,180
  Total Learnings Files: 20
  Pitaya Corrections: 15

======================================================================
```

---

## Health Status Indicators

| Status | Meaning |
|--------|---------|
| ✅ HEALTHY | All systems operational |
| ⚠️ DEGRADED | Some issues detected |
| ❌ ERROR | Critical issues found |

---

## Daily Scheduled Check

A cron job runs this check daily at 09:00:

```cron
0 9 * * * cd ~/AS-Virtual_Team_System_v2 && python3 rag/scripts/rag_health_check.py >> ~/AS-Virtual_Team_System_v2/rag/logs/daily_health.log 2>&1
```

---

## Log Locations

| Log | Path | Purpose |
|-----|------|---------|
| Health Check | `~/AS-Virtual_Team_System_v2/rag/logs/health_check.jsonl` | Historical health data |
| Capture Events | `~/AS-Virtual_Team_System_v2/rag/logs/capture_learnings.jsonl` | /capture_learnings invocations |
| Daily Report | `~/AS-Virtual_Team_System_v2/rag/logs/daily_health.log` | Daily cron output |

---

## Cloud Run Configuration

For Cloud Run deployments, set these environment variables:

```bash
# Enable GCS-backed ChromaDB
GCS_BUCKET=virtual-ateam-rag     # GCS bucket for RAG persistence
GCS_RAG_DB_ID=virtual_team_v2    # Database identifier (optional)
VECTOR_DB_PROVIDER=chromadb_gcs  # Explicit provider (auto-detected if GCS_BUCKET set)
```

The system will:
1. On startup: Download data from GCS to `/tmp/chroma/{db_id}/`
2. During runtime: ChromaDB writes to local `/tmp` directory
3. Background thread: Syncs local changes to GCS every 5 minutes
4. On shutdown: Final sync to GCS

---

## Troubleshooting

### No documents in vector database
```bash
# Re-run indexer
python3 ~/AS-Virtual_Team_System_v2/rag/scripts/index_all.py
```

### Learnings not being captured
```bash
# Manually invoke capture
/capture_learnings
```

### Cloud provider connection issues
```bash
# Check environment variables
echo $QDRANT_URL
echo $QDRANT_API_KEY
echo $PINECONE_API_KEY
```

### GCS-backed ChromaDB issues
```bash
# Check GCS bucket configuration
echo $GCS_BUCKET
echo $GCS_RAG_DB_ID

# Check GCS authentication
gcloud auth list

# Verify bucket access
gsutil ls gs://$GCS_BUCKET/chromadb/

# Force sync to GCS
python3 -c "from cloud.chromadb_gcs import get_gcs_chromadb; db = get_gcs_chromadb(); db.sync_to_gcs()"
```

---

## Integration with Team Skills

This health check is automatically referenced by:
- `/capture_learnings` - Verifies RAG update success
- `/blackteam` - Phase 5 completion check
- `/whiteteam` - Validation completion check
- `/A_Virtual_Team` - Joint sign-off verification

---

**Rule G4:** All learnings must be captured to BOTH files AND RAG for semantic retrieval.

*RAG Health Check v1.0 - Virtual Team v2*
