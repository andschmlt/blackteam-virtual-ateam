# /synapse - AI Knowledge Hub Manual Refresh

Manually trigger Synapse AI Knowledge Hub to scrape news and skills.

## Phase 0: RAG Context Loading

**Load relevant context from the RAG system.**

```python
from AS-Virtual_Team_System_v2.rag.rag_client import VTeamRAG
rag = VTeamRAG()
context = rag.query("synapse knowledge hub skills discovery", top_k=3)
```

---

## Usage

```
/synapse [mode]
```

**Modes:**
- `full` (default) - Run full news + skills pipeline
- `news` - News articles only
- `skills` - Skills discovery only
- `dry-run` - Preview without writing files
- `status` - Show last run status and stats

## Execution

Based on the mode argument, execute the appropriate command:

### Mode: full (default)
```bash
cd /home/andre/synapse && python3 scripts/run_weekly_scrape.py --no-email
```

### Mode: news
```bash
cd /home/andre/synapse && python3 scripts/run_weekly_scrape.py --news-only --no-email
```

### Mode: skills
```bash
cd /home/andre/synapse && python3 scripts/run_weekly_scrape.py --skills-only --no-email
```

### Mode: dry-run
```bash
cd /home/andre/synapse && python3 scripts/run_weekly_scrape.py --dry-run --no-email
```

### Mode: status
```bash
echo "=== Synapse Status ===" && \
cat /home/andre/synapse/data/.cache/articles_index.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(f\"Last Run: {data.get('last_updated', 'Never')}\")
print(f\"Total Articles: {data.get('stats', {}).get('total_articles', 0)}\")
print(f\"Total Skills: {data.get('stats', {}).get('total_skills', 0)}\")
print(f\"Duplicates Blocked: {data.get('stats', {}).get('duplicates_blocked', 0)}\")
print()
print('Recent runs:')
for run in data.get('runs', [])[-5:]:
    print(f\"  {run.get('timestamp', 'Unknown')}: {run.get('new_articles', 0)} articles, {run.get('new_skills', 0)} skills\")
"
```

## Output

After execution, display:
1. Summary of articles/skills scraped
2. Location of digest file (if generated)
3. Any errors encountered

## Examples

```
/synapse           # Full pipeline
/synapse news      # News only
/synapse skills    # Skills only
/synapse dry-run   # Preview mode
/synapse status    # Show stats
```

## Cron Schedule

Synapse runs automatically every Sunday at 11:00 PM. Use this command for manual refreshes between scheduled runs.

## Related Files

- **Main Script:** `/home/andre/synapse/scripts/run_weekly_scrape.py`
- **Config:** `/home/andre/synapse/config/sources.yaml`
- **Index:** `/home/andre/synapse/data/.cache/articles_index.json`
- **Digest:** `/home/andre/synapse/data/weekly_digest/`
