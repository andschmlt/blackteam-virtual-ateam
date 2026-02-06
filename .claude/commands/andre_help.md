# /andre_help - Workspace Overview

## Phase 0: RAG Context Loading

**Load workspace context from RAG.**

```python
from AS-Virtual_Team_System_v2.rag.rag_client import VTeamRAG
rag = VTeamRAG()
context = rag.query("workspace projects status overview", top_k=3)
```

---

Display this banner exactly:

```
── ANDRE WORKSPACE ──

PROJECTS
  • BI-01 | BI-AI_Agents_REPO  | [GH]
  • EG-02 | europeangaming.eu  | [GH]
  • LV-03 | lover.io           | [GH]
  • NT-04 | northeasttimes.com | [GH]
  • PB-05 | paradise_brain     | [Local]
  • BA-06 | bedrock_agent      | [GH]

CRON (Local)
  • 09:00 lover.io PostHog
  • 09:05 northeasttimes PostHog
  • 17:00 Daily Logs

CLOUD RUN JOBS (GCP - paradisemedia-bi)
  • news-updater       | Daily 12:00 UTC | 8 sports verticals
  • tasks-roi-weekly   | Monday 16:00 UTC | ClickUp ROI comments

  Manual: gcloud run jobs execute <job> --region=us-central1

ANALYSIS (~/analysis/)
  • adhoc/      - Ad-hoc analysis
  • tasks_roi/  - /tasks_ROI output
  • posthog/    - PostHog archives
  • seo/        - SEO analysis
  • custom/     - Other analysis

SESSIONS (~/Desktop/Virtual ATeam/BlackTeam/sessions/)
  • Use /resume_blackteam to view/resume

VIRTUAL ATEAM
  • /blackteam         - Execute with 16 BlackTeam specialists
  • /whiteteam         - Execute OR validate with 25 specialists
  • /A_Virtual_Team    - Full 41+ persona orchestration
  • /persona           - Load single specialist
  • /director          - Direct request to Director
  • /create_persona    - Generate new persona
  • /resume_blackteam  - Resume interrupted session
  • /blackteam_help    - Team roster & routing
  • /reflect           - Capture learnings

ANALYTICS & DATA
  • /posthog_analysis  - PostHog analytics reports
  • /BI-Chatbot        - Query BI data lake (BigQuery)
  • /tasks_ROI         - ClickUp task ROI analysis
  • /ml_predict        - ML predictions (XGBoost/Linear)
  • /dataguard         - Data terminology standards

SKILLS (~/.claude/context/skills/)
  • DOMAIN_DAILY_ANALYTICS   - Unified domain performance view
  • ML_COMPETITIVE_ANALYSIS  - Domain/article prediction

CONTENT & DEVOPS
  • /bedrock_agent     - Content vertical generator
  • /news_update_agent - Sports news updates
  • /synapse           - AI Knowledge Hub refresh
  • /codeguard         - Code quality monitoring
  • /cloud_jobs        - Cloud Run jobs manager
  • /githubaccess      - Add GitHub collaborator

WORKSPACE
  • /andre_help        - This overview
  • /assess            - Workspace assessment
```

Output only the banner above, nothing else.
