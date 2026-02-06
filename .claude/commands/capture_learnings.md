# /capture_learnings - Automatic RAG Update Rule

## Phase 0: RAG Context Loading (MANDATORY)

**Load existing learnings from RAG before capturing new ones (avoid duplicates).**

**RAG Query:**
```python
from AS-Virtual_Team_System_v2.rag.rag_client import VTeamRAG
rag = VTeamRAG()
existing = rag.query("recent learnings corrections", collection_name="learnings", top_k=5)
```

---

## MANDATORY RULE: ALWAYS CAPTURE LEARNINGS

**This rule applies to ALL sessions involving Virtual ATeam, BlackTeam, or WhiteTeam.**

After ANY significant interaction, correction, or learning, Claude MUST:

### 1. Update Pitaya RAG (if Pitaya-related)
```
File: ~/pitaya/knowledge/feedback_corrections.md
```
Add to the Correction Log table:
| Date | Issue | Correction |

### 2. Update Virtual Team v2 Knowledge Base
```
BlackTeam: ~/AS-Virtual_Team_System_v2/blackteam/skills/learnings/
WhiteTeam: ~/AS-Virtual_Team_System_v2/whiteteam/skills/learnings/
```

### 3. What to Capture

| Type | Example | Where to Store |
|------|---------|----------------|
| Data rules | "Use reporting schema only" | MASTER_LIST, team rules |
| Query patterns | "Default to 6 months" | Pitaya RAG, BigQuery client |
| Output format | "Business-friendly language" | System prompts, team configs |
| User preferences | "50% on WHY analysis" | Feedback corrections |
| Technical fixes | "Mode detection regex" | Code comments, RAG |
| Process improvements | "Plan before results" | System prompts |

### 4. Format for Learnings

```markdown
## Learning: [Brief Title]
**Date:** YYYY-MM-DD
**Source:** [User feedback / Bug fix / Enhancement]
**Teams Affected:** [BlackTeam / WhiteTeam / Both]

### Issue
[What was wrong or missing]

### Solution
[What was changed or added]

### Files Updated
- [file1]
- [file2]

### Rule (if applicable)
[New rule to follow going forward]
```

### 5. Trigger Conditions

ALWAYS capture learnings when:
- User provides correction or feedback
- A bug is fixed
- A new pattern is discovered
- User preferences are expressed
- Data rules are clarified
- Output format is adjusted

### 6. Never Forget

- **ALWAYS** run this at end of significant sessions
- **ALWAYS** update both Pitaya RAG and Team configs
- **NEVER** lose learnings between sessions
- **NEVER** repeat the same mistakes

---

## MANDATORY: RAG Index Update (v2.0)

**After writing learnings to markdown files, ALWAYS update the RAG index:**

### Step 1: Write Learnings to Files

Write to appropriate locations:
- `~/AS-Virtual_Team_System_v2/blackteam/skills/learnings/YYYY-MM-DD_topic.md`
- `~/AS-Virtual_Team_System_v2/whiteteam/skills/learnings/YYYY-MM-DD_topic.md`

### Step 2: Run RAG Indexer (MANDATORY)

```bash
# Re-index all collections to update RAG with new learnings
python3 ~/AS-Virtual_Team_System_v2/rag/scripts/index_all.py
```

### Step 3: Verify Indexing

```bash
# Verify new document count
python3 -c "
from rag.rag_client import VTeamRAG
rag = VTeamRAG()
stats = rag.get_stats()
total = sum(c.get('document_count', 0) for c in stats.get('collections', {}).values())
print(f'Provider: {rag.get_provider_name()}')
print(f'Total documents indexed: {total}')
print(f'Learnings collection: {stats.get(\"collections\", {}).get(\"learnings\", {}).get(\"document_count\", 0)} docs')
"
```

### Step 4: Commit Changes (if significant)

```bash
# Commit learnings files to git
cd ~/AS-Virtual_Team_System_v2
git add blackteam/skills/learnings/ whiteteam/skills/learnings/
git commit -m "Capture session learnings - [brief description]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
git push origin main
```

---

## GCS RAG Sync (MANDATORY)

**CRITICAL:** GCS sync MUST succeed every time. Use the correct credentials.

### Required Environment Variables

```bash
# MUST be set for GCS sync to work
export GOOGLE_APPLICATION_CREDENTIALS=/home/andre/secrets/bi-chatbot-sa.json
export GCS_BUCKET=virtual-ateam-rag
```

### Service Account Reference

| Service Account | File | GCS Access |
|-----------------|------|------------|
| `andre-claude@paradisemedia-bi.iam.gserviceaccount.com` | `bi-chatbot-sa.json` | ✅ YES |
| `papaya-drive-uploader@` | DELETED | ❌ NO |

**NEVER use papaya-drive-uploader - it was deleted and has no GCS access.**

### Run RAG Indexer with GCS Sync

```bash
# ALWAYS use this command to ensure GCS sync works
GOOGLE_APPLICATION_CREDENTIALS=/home/andre/secrets/bi-chatbot-sa.json \
GCS_BUCKET=virtual-ateam-rag \
python3 ~/AS-Virtual_Team_System_v2/rag/scripts/index_all.py
```

### Verify GCS Sync Success

The output MUST show:
```
============================================================
Cloud Sync
============================================================
Syncing to GCS bucket: virtual-ateam-rag
GCS sync: SUCCESS
Last sync: [timestamp]
============================================================
```

**If GCS sync shows FAILED:**
1. Check `GOOGLE_APPLICATION_CREDENTIALS` is set to `bi-chatbot-sa.json`
2. Check `GCS_BUCKET` is set to `virtual-ateam-rag`
3. Verify service account has `storage.objectAdmin` on bucket

---

## Execution Checklist

When `/capture_learnings` is invoked:

- [ ] Identify learnings from the session
- [ ] Write to appropriate markdown files (BlackTeam/WhiteTeam)
- [ ] **Run RAG indexer** (`python3 rag/scripts/index_all.py`)
- [ ] Verify document count increased
- [ ] Commit and push changes to git
- [ ] Report completion with document counts

---

## Auto-Invoke Rules

This skill is **automatically invoked** at the end of:

| Skill | When Invoked |
|-------|--------------|
| `/blackteam` | Phase 5 completion |
| `/whiteteam` | Execution/Validation completion |
| `/A_Virtual_Team` | Joint sign-off |
| `/reflect` | After reflection captured |

**Rule G4:** All learnings must be captured to BOTH files AND RAG for semantic retrieval.

---

*This rule ensures continuous improvement and knowledge retention for the Virtual ATeam system.*
*Version 2.0 - Now with automatic RAG indexing*
