# /blackteam_insights - Daily Insights Manual Trigger

Run the Pepper Daily Insights Bot manually to generate actionable insights from the BigQuery lakehouse.

## Phase 0: RAG Context Loading (MANDATORY)

**Load relevant context from the RAG system before generating insights.**

Read these files for prior learnings and corrections:
- `~/pitaya/knowledge/feedback_corrections.md` — Data accuracy rules, R-DATA-07 numerical validation

**RAG Query:**
```python
from AS-Virtual_Team_System_v2.rag.rag_client import VTeamRAG
rag = VTeamRAG()
context = rag.query("daily insights revenue FTD analysis", top_k=5)
learnings = rag.query("data accuracy numerical comparison corrections", collection_name="learnings", top_k=3)
```

---

## Usage

```
/blackteam_insights [action]
```

**Actions:**
- `run` - Execute insights for yesterday's data (default)
- `dry-run` - Test with mock data (no BigQuery/Slack)
- `status` - Check bot configuration status

**Arguments provided:** $ARGUMENTS

## Execution

When triggered with `run`:

1. **Navigate to Pepper project:**
```bash
cd /home/andre/BI-AI_Agents_REPO/Pepper/main
```

2. **Set environment variables:**
```bash
export GOOGLE_APPLICATION_CREDENTIALS=~/secrets/bi-chatbot-sa.json
```

3. **Run the insights bot:**
```bash
python3 src/main.py
```

For `dry-run`:
```bash
python3 src/main.py --dry-run
```

## Data Scope

All queries run for **yesterday's data** (SYSDATE-1):
- DATE_ID filter: `YYYYMMDD` format of yesterday
- Comparison: Yesterday vs day before (DoD)
- Lookback: 7 days for trends, 30 days for ROI calculations

## Insight Categories

| Category | Metrics | Tables |
|----------|---------|--------|
| **Conversion Funnel** | Clicks, FTDs, Signups, Commission, EPC | FCT_IGAMING_ARTICLE_PERFORMANCE |
| **SEO** | Rank changes, Traffic, Core Web Vitals | FCT_KEYWORD_STATS, FCT_PAGE_VITALS_STATS |
| **Costs** | ROI, Cost per article | FCT_INVOICE_INFORMATION |
| **Content Production** | Bottlenecks, Publishing velocity | FCT_ARTICLE_DEVELOPMENT |
| **Sales** | Brand, Program, GEO performance | FCT_IGAMING_BRAND_PERFORMANCE, FCT_CLOAKING_TRAFFIC |

## Output

- **Slack:** Rich Block Kit message to configured channel
- **Console:** Plain text summary (dry-run mode)
- **Logs:** `/home/andre/BI-AI_Agents_REPO/Pepper/main/logs/daily_insights.log`

## Configuration

Edit `/home/andre/BI-AI_Agents_REPO/Pepper/main/config/config.json`:
- `slack.channel_id` - Target Slack channel
- `insights.top_n` - Number of top/bottom performers (default: 10)
- `insights.min_clicks_threshold` - Minimum clicks to include (default: 50)

## Project Reference

- **Project ID:** BT-2026-005
- **Bot Name:** Pepper (Tropical Fruit Suite)
- **GitHub:** https://github.com/ParadiseMediaOrg/BI-AI_Agents_REPO/tree/main/Pepper
- **Local Path:** `/home/andre/BI-AI_Agents_REPO/Pepper`

---

## Instructions for Claude

Based on the action argument:

### If action is "run" or empty:
1. Check if BigQuery credentials exist at `~/secrets/bi-chatbot-sa.json`
2. Check if SLACK_BOT_TOKEN is configured
3. If credentials exist, run the full insights:
   ```bash
   cd /home/andre/BI-AI_Agents_REPO/Pepper/main
   export GOOGLE_APPLICATION_CREDENTIALS=~/secrets/bi-chatbot-sa.json
   python3 src/main.py
   ```
4. Report success/failure and key insights summary

### If action is "dry-run":
1. Run with mock data:
   ```bash
   cd /home/andre/BI-AI_Agents_REPO/Pepper/main
   python3 src/main.py --dry-run
   ```
2. Display the output to the user

### If action is "status":
1. Check configuration:
   - BigQuery credentials file exists
   - Slack channel configured in config.json
   - Required Python packages installed
2. Report readiness status

### Error Handling:
- If credentials missing, offer to run in dry-run mode
- If Slack not configured, show instructions to configure
- Log all errors to the log file
