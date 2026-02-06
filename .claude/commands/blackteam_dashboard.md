# /blackteam_dashboard - BlackTeam Monitoring Dashboard

Launch the BlackTeam Monitoring Dashboard for real-time tracking of Virtual ATeam persona utilization, communications, decisions, and KPIs.

## Phase 0: RAG Context Loading

**Load dashboard context from RAG.**

```python
from AS-Virtual_Team_System_v2.rag.rag_client import VTeamRAG
rag = VTeamRAG()
context = rag.query("blackteam dashboard monitoring KPIs", top_k=3)
```

---

## Quick Start

```bash
cd ~/blackteam-dashboard && ./start.sh
```

## Individual Services

**Backend only:**
```bash
cd ~/blackteam-dashboard && ./start-backend.sh
```

**Frontend only:**
```bash
cd ~/blackteam-dashboard && ./start-frontend.sh
```

## Access Points

- **Dashboard UI**: http://localhost:5173
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Features

1. **KPI Grid**: 9 real-time metrics
   - Comments, Decisions, Mistakes, Learnings
   - Issues, Deployments, Merges, Projects, Tasks

2. **Live Activity Feed**: WebSocket-powered updates when new activities are logged

3. **Utilization Chart**: Animated donut showing persona distribution

4. **Team Sidebar**: All 16 personas with active/idle status

5. **Filtering**: Click KPIs or personas to filter the feed

## Data Sources

Reads from `~/virtual-ateam/BlackTeam/logs/`:
- `utilization/UTILIZATION_YYYY-MM-DD.jsonl`
- `learnings/*.md`
- `PROJECT_REGISTRY.json`

## Project Location

`/home/andre/blackteam-dashboard/`
