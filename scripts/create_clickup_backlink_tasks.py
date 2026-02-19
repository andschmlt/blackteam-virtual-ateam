#!/usr/bin/env python3
"""
Create Paradise Backlink Manager tasks in ClickUp.
Structure: 1 parent epic + 2 doc stories + 2-3 team tasks (BI vs Engineering) + subtasks.
List: 901323608605 (February 26 Scrumban Board)
Marta Szmidt (watcher): 112045921
"""

import requests
import time
import json
import sys

API_KEY = "pk_60332880_BFGB37OGS3728SKRG41AB9EPIKK5O3GY"
LIST_ID = "901323608605"
MARTA_ID = 112045921
BASE_URL = "https://api.clickup.com/api/v2"
HEADERS = {
    "Authorization": API_KEY,
    "Content-Type": "application/json",
}

created_tasks = []
failed_tasks = []


def create_task(list_id, name, description, priority=3, parent=None, tags=None, time_estimate_days=None):
    """Create a ClickUp task and add Marta as watcher."""
    payload = {
        "name": name,
        "description": description,
        "status": "planning",
        "priority": priority,
    }
    if parent:
        payload["parent"] = parent
    if tags:
        payload["tags"] = tags
    if time_estimate_days:
        payload["time_estimate"] = time_estimate_days * 8 * 3600000  # days -> ms (8hr days)

    time.sleep(0.7)

    resp = requests.post(
        f"{BASE_URL}/list/{list_id}/task",
        headers=HEADERS,
        json=payload,
    )

    if resp.status_code in (200, 201):
        task = resp.json()
        task_id = task["id"]
        print(f"  OK: {name} ({task_id})")

        # Add Marta as watcher
        time.sleep(0.5)
        requests.post(
            f"{BASE_URL}/task/{task_id}/watcher",
            headers=HEADERS,
            json={"id": MARTA_ID},
        )
        created_tasks.append({"id": task_id, "name": name})
        return task_id
    else:
        print(f"  FAIL: {name} — {resp.status_code}: {resp.text[:200]}")
        failed_tasks.append({"name": name, "error": resp.text[:200]})
        return None


# ── Read MD files ──
project_plan_md = ""
tech_spec_md = ""
try:
    with open("/home/andre/projects/paradise-backlink-manager/PROJECT_PLAN.md", "r") as f:
        project_plan_md = f.read()
except:
    project_plan_md = "See ~/projects/paradise-backlink-manager/PROJECT_PLAN.md"
try:
    with open("/home/andre/projects/paradise-backlink-manager/TECHNICAL_SPECIFICATION.md", "r") as f:
        tech_spec_md = f.read()
except:
    tech_spec_md = "See ~/projects/paradise-backlink-manager/TECHNICAL_SPECIFICATION.md"

# Truncate to ClickUp desc limit (~50KB)
plan_truncated = project_plan_md[:48000]
spec_truncated = tech_spec_md[:48000]


print("=" * 60)
print("CREATING PARADISE BACKLINK MANAGER TASKS IN CLICKUP")
print("Grouped by team: Engineering vs BI")
print("=" * 60)

# ================================================================
# 1. PARENT TASK (Epic)
# ================================================================
print("\n[1/5] PARENT TASK")
parent_id = create_task(
    LIST_ID,
    "Paradise Backlink Manager — Custom Web App (BT-2026-012)",
    (
        "# Paradise Backlink Manager\n\n"
        "Custom web app to replace Airtable for the backlink team.\n\n"
        "**Problem:** Airtable automation cap hit (100K/month) after 19 days. Team manual for 12+ days.\n"
        "**Cost savings:** $2,426/month → ~$177/month = 93% reduction\n"
        "**Scale:** 500-1,000 backlink requests/month | Team: 5 → 10 people\n\n"
        "**Stack:** Next.js + FastAPI + PostgreSQL (Cloud SQL) + Redis + Cloud Run\n"
        "**Timeline:** 12 weeks dev + 2 weeks parallel run = ~14 weeks total\n"
        "**Team:** 3 developers — 2 Data Engineering + 1 BI\n\n"
        "## Deliverables\n"
        "- Pipeline management (Kanban + Table views)\n"
        "- AI-powered anchor text + publisher matching\n"
        "- Order management with $700 approval workflow\n"
        "- Publisher Hub with automated vetting\n"
        "- Reporting dashboard (domain/geo/month/quarter/team/agency/spend)\n"
        "- Integrations: Ahrefs, BigQuery, ClickUp, Slack, DataForSEO\n"
        "- Centralized encrypted credential storage\n"
        "- Full Airtable data migration\n\n"
        "## Key Documents\n"
        "- **Project Plan:** see subtask 'DOC: Project Plan'\n"
        "- **Technical Spec:** see subtask 'DOC: Technical Specification'\n\n"
        "## Team Split\n"
        "- **Engineering (2 devs):** Backend, DB, Auth, AI, Integrations, Workers, Migration, Security\n"
        "- **BI (1 dev):** Frontend, UI, Reporting Dashboard, Exports\n"
    ),
    priority=1,
    tags=["backlink-manager", "project"],
)

if not parent_id:
    print("FATAL: Parent task failed. Aborting.")
    sys.exit(1)

# ================================================================
# 2. DOC: Project Plan
# ================================================================
print("\n[2/5] DOC: Project Plan")
doc_plan_id = create_task(
    LIST_ID,
    "DOC: Project Plan & Analysis",
    plan_truncated,
    priority=2,
    parent=parent_id,
    tags=["backlink-manager", "documentation"],
)

# ================================================================
# 3. DOC: Technical Specification
# ================================================================
print("\n[3/5] DOC: Technical Specification")
doc_spec_id = create_task(
    LIST_ID,
    "DOC: Technical Specification v1.0",
    spec_truncated,
    priority=2,
    parent=parent_id,
    tags=["backlink-manager", "documentation"],
)

# ================================================================
# 4. ENGINEERING TEAM TASK (2 devs — Backend, DB, AI, Integrations)
# ================================================================
print("\n[4/5] ENGINEERING TEAM TASK")
eng_id = create_task(
    LIST_ID,
    "ENG: Backend, Integrations, AI & Data Migration",
    (
        "# Engineering Team Workstream\n"
        "**Team:** 2 Data Engineers (Dev 1 = Backend Lead, Dev 2 = Integrations)\n"
        "**Duration:** Weeks 1-14 (~60% of total effort)\n\n"
        "## Scope\n"
        "Everything server-side: FastAPI backend, PostgreSQL schema, Google OAuth, RBAC,\n"
        "all REST API endpoints, AI services (anchor text, publisher matching, gap analysis),\n"
        "all external integrations (Ahrefs, BigQuery, ClickUp, Slack, DataForSEO),\n"
        "background workers (6 cron jobs), data migration from Airtable, credential vault,\n"
        "security audit, performance testing.\n\n"
        "## Dev 1 — Backend Lead (Weeks 1-14)\n"
        "- PostgreSQL schema (13 tables) + Alembic migrations\n"
        "- FastAPI skeleton + project structure\n"
        "- Google OAuth 2.0 + RBAC (5 roles)\n"
        "- Core CRUD APIs (requests, orders, links, publishers, agencies)\n"
        "- Auto-prioritization engine (P0-P5, BigQuery-powered)\n"
        "- Round-robin assignment + GEO detection + duplicate check\n"
        "- Status pipeline with cascading updates + activity log\n"
        "- Anchor text AI engine (Claude via OpenRouter)\n"
        "- Publisher auto-matching (3-layer: geo→niche→LLM)\n"
        "- Competitor gap analysis\n"
        "- Security hardening + performance tuning\n\n"
        "## Dev 2 — Integrations & Data (Weeks 2-14)\n"
        "- GCP infrastructure provisioning (Cloud SQL, Redis, Cloud Run, Secrets)\n"
        "- CI/CD pipeline (Cloud Build → Cloud Run)\n"
        "- Ahrefs API integration + Redis caching (4hr TTL)\n"
        "- DataForSEO integration (spam score, fallback metrics)\n"
        "- BigQuery integration for FTD/revenue data\n"
        "- ClickUp webhook receiver + 5-min poller daemon\n"
        "- Slack integration (notifications, alerts, weekly summary)\n"
        "- Publisher vetting automation (Ahrefs + DataForSEO pipeline)\n"
        "- Encrypted credential storage (AES-256, marketplace logins)\n"
        "- Order approval workflow ($700 threshold)\n"
        "- Bulk CSV import\n"
        "- Airtable data export + migration script + reconciliation\n"
        "- Link health monitoring worker\n"
        "- Pipeline health alerts worker\n\n"
        "## Milestone Gates\n"
        "- Week 3: Auth + CRUD working end-to-end\n"
        "- Week 6: Core pipeline functional (intake → order → track)\n"
        "- Week 9: AI features + all integrations connected\n"
        "- Week 12: All workers running, security audit passed\n"
        "- Week 14: Migration verified, parallel run clean\n\n"
        "## API Endpoints Owned (60+ routes)\n"
        "/auth/*, /requests/*, /orders/*, /links/*, /publishers/*, /agencies/*,\n"
        "/ai/*, /users/*, /webhooks/*, /credentials/*, /reports/* (data layer),\n"
        "/activity/*\n\n"
        "## Reference\n"
        "Full API spec + DB DDL: see 'DOC: Technical Specification' subtask\n"
    ),
    priority=1,
    parent=parent_id,
    tags=["backlink-manager", "engineering"],
    time_estimate_days=50,
)

# ── Engineering subtasks ──
if eng_id:
    print("  [ENG subtasks]")

    create_task(LIST_ID, "ENG-1: Database Schema + FastAPI Skeleton + Auth (Wk 1-3)",
        "**Dev 1 primary, Dev 2 supports infra**\n\n"
        "- Design & implement PostgreSQL schema (13 tables, ENUMs, indexes, views)\n"
        "- Alembic migration files\n"
        "- FastAPI project skeleton with folder structure\n"
        "- Google OAuth 2.0 login flow (JWT + Redis sessions)\n"
        "- RBAC middleware (admin/head/builder/requester/viewer)\n"
        "- Health check endpoint\n"
        "- Standard error response format\n\n"
        "**Dev 2:**\n"
        "- Provision Cloud SQL, Memorystore Redis, Cloud Run, Secret Manager\n"
        "- CI/CD pipeline (Cloud Build → Cloud Run auto-deploy)\n"
        "- VPC connector for private networking\n\n"
        "**Gate:** Auth login working, RBAC enforced, DB migrations applied, CI/CD deploying.\n"
        "**Estimate:** 3 weeks",
        priority=1, parent=eng_id, tags=["backlink-manager", "engineering", "foundation"],
        time_estimate_days=12)

    create_task(LIST_ID, "ENG-2: Core API + Pipeline Logic + Integrations (Wk 4-6)",
        "**Dev 1: Core APIs | Dev 2: Integrations**\n\n"
        "**Dev 1:**\n"
        "- CRUD APIs: backlink_requests (list/create/get/update/delete/kanban/bulk)\n"
        "- CRUD APIs: orders (create/approve/reject), links (create/verify)\n"
        "- CRUD APIs: publishers, agencies\n"
        "- Auto-prioritization engine (BigQuery FTD → P0-P5 scoring)\n"
        "- Round-robin auto-assignment (weighted)\n"
        "- GEO auto-detection from URL/domain\n"
        "- Duplicate URL detection\n"
        "- Status pipeline with cascading updates\n"
        "- Activity log (audit trail)\n"
        "- Order $700 approval workflow\n\n"
        "**Dev 2:**\n"
        "- BigQuery integration + Redis cache (4hr TTL)\n"
        "- Ahrefs API client (DR, traffic, backlinks, gap)\n"
        "- DataForSEO client (spam score, fallback)\n"
        "- Airtable full export script (all 4 tables)\n"
        "- Bulk CSV import endpoint\n\n"
        "**Gate:** Full pipeline API working end-to-end, external data flowing in.\n"
        "**Estimate:** 3 weeks",
        priority=1, parent=eng_id, tags=["backlink-manager", "engineering", "core-api"],
        time_estimate_days=16)

    create_task(LIST_ID, "ENG-3: AI Services + Automation + Workers (Wk 7-9)",
        "**Dev 1: AI engines | Dev 2: Automation + integrations**\n\n"
        "**Dev 1:**\n"
        "- Anchor text AI engine (Claude via OpenRouter, iGaming rules)\n"
        "- Publisher auto-matching (3-layer: geo → niche → LLM verification)\n"
        "- Competitor gap analysis (Ahrefs SERP data)\n\n"
        "**Dev 2:**\n"
        "- ClickUp webhook receiver + 5-min poller daemon\n"
        "- Slack integration (new request, link live, alerts, weekly summary, DMs)\n"
        "- Publisher vetting automation (Ahrefs DR + DataForSEO spam → auto-approve/flag)\n"
        "- Encrypted credential storage (AES-256, marketplace logins)\n"
        "- Background workers framework (Cloud Scheduler → Cloud Run Jobs)\n\n"
        "**Gate:** AI suggestions working, ClickUp flowing in, Slack firing, vetting automated.\n"
        "**Estimate:** 3 weeks",
        priority=1, parent=eng_id, tags=["backlink-manager", "engineering", "ai-automation"],
        time_estimate_days=14)

    create_task(LIST_ID, "ENG-4: Workers + Migration + Security + QA (Wk 10-14)",
        "**Dev 1: Security + performance | Dev 2: Workers + migration**\n\n"
        "**Dev 2:**\n"
        "- Link health monitoring worker (every 6hr — HTTP check all live links)\n"
        "- Pipeline health alerts (every 15min — stuck records, stale orders)\n"
        "- Priority re-calculation worker (hourly)\n"
        "- Ahrefs cache refresh worker (every 4hr)\n"
        "- Weekly report generator (Monday 9 AM → Slack)\n"
        "- Airtable migration script + field mapping + reconciliation\n"
        "- Parallel run monitoring\n\n"
        "**Dev 1:**\n"
        "- Security audit: R-SEC-01 scan, auth test, RBAC test, CORS, CSRF\n"
        "- Performance tuning: indexes, query optimization, EXPLAIN ANALYZE\n"
        "- Load testing: k6/locust (10 concurrent users)\n"
        "- Bug fixes from UAT feedback\n\n"
        "**Gate:** All workers running, migration verified, security passed, performance targets met.\n"
        "**Estimate:** 4-5 weeks (includes 2-week parallel run)",
        priority=1, parent=eng_id, tags=["backlink-manager", "engineering", "launch"],
        time_estimate_days=18)


# ================================================================
# 5. BI TEAM TASK (1 dev — Frontend, UI, Reporting)
# ================================================================
print("\n[5/5] BI TEAM TASK")
bi_id = create_task(
    LIST_ID,
    "BI: Frontend, UI, Reporting Dashboard & Exports",
    (
        "# BI Team Workstream\n"
        "**Team:** 1 BI Developer (Dev 3 = Frontend & Reporting)\n"
        "**Duration:** Weeks 2-14 (~35% of total effort)\n\n"
        "## Scope\n"
        "Entire Next.js frontend: all pages, components, views, reporting dashboard,\n"
        "CSV/PDF exports, responsive design, UX polish.\n\n"
        "## Dev 3 — Frontend & Reporting (Weeks 2-14)\n"
        "- Next.js 15 setup with App Router + Tailwind + shadcn/ui\n"
        "- Google OAuth login page\n"
        "- Navigation layout (Pipeline | Links | Publishers | Agencies | Reports | Settings)\n"
        "- Request intake form (auto-domain, duplicate warning, validation)\n"
        "- Pipeline table view (sortable, filterable, paginated, bulk actions)\n"
        "- Pipeline Kanban board (drag-drop, status changes, priority colors)\n"
        "- Request detail slide-over (AI suggestions, order history, activity)\n"
        "- Publisher Hub UI (list, search, filter, add, vet status, performance)\n"
        "- Agency management UI (list, detail, order history, caution flags)\n"
        "- Order management UI (place order, approval flow, status tracking)\n"
        "- Reporting: overview dashboard with trend charts\n"
        "- Reporting: by-domain, by-geo breakdowns\n"
        "- Reporting: by-month/quarter (historical — key stakeholder request)\n"
        "- Reporting: by-team (velocity, completion rate)\n"
        "- Reporting: by-agency (delivery, price, quality comparison)\n"
        "- Spend tracking dashboard (budget, by domain/market/agency)\n"
        "- CSV/PDF export for all report views\n"
        "- Settings pages (users, credentials, notifications, integrations)\n"
        "- UAT session facilitation + training docs\n\n"
        "## Pages Owned\n"
        "/login, /pipeline, /pipeline/:id, /links, /links/:id,\n"
        "/publishers, /publishers/:id, /publishers/new,\n"
        "/agencies, /agencies/:id,\n"
        "/reports, /reports/domains, /reports/geo, /reports/team,\n"
        "/reports/agencies, /reports/spend,\n"
        "/settings, /settings/users, /settings/credentials,\n"
        "/settings/notifications, /settings/integrations\n\n"
        "## Milestone Gates\n"
        "- Week 4: Login + intake form + basic table view live\n"
        "- Week 7: Kanban board + request detail panel working\n"
        "- Week 9: Publisher Hub + Agency + Order UIs complete\n"
        "- Week 12: All reporting dashboards + exports live\n"
        "- Week 14: UAT fixes, polish, training docs delivered\n\n"
        "## Key Dependencies (from Engineering)\n"
        "- Week 3: Auth API ready → build login page\n"
        "- Week 4: Requests API → build intake form + table\n"
        "- Week 5: Orders/Links API → build order flow\n"
        "- Week 6: Priority API → build Kanban with priority colors\n"
        "- Week 10: Reports API → build dashboards\n\n"
        "## Tech Stack\n"
        "- Next.js 15 (App Router, SSR)\n"
        "- shadcn/ui + Tailwind CSS\n"
        "- TanStack Query v5 (server state, optimistic updates)\n"
        "- @dnd-kit/core (Kanban drag-drop)\n"
        "- Recharts or Chart.js (dashboard charts)\n"
        "- TypeScript throughout\n\n"
        "## Reference\n"
        "Full page specs + component design: see 'DOC: Technical Specification' subtask (Section 7)\n"
    ),
    priority=1,
    parent=parent_id,
    tags=["backlink-manager", "bi-team"],
    time_estimate_days=35,
)

# ── BI subtasks ──
if bi_id:
    print("  [BI subtasks]")

    create_task(LIST_ID, "BI-1: Frontend Setup + Intake Form + Pipeline Table (Wk 2-5)",
        "**Dev 3**\n\n"
        "- Next.js 15 setup: App Router, Tailwind CSS, shadcn/ui, TypeScript\n"
        "- TanStack Query v5 config + API client wrapper\n"
        "- Navigation layout with sidebar\n"
        "- Google OAuth login page + auth redirect\n"
        "- Request intake form:\n"
        "  - Fields: target URL, keyword, GEO, tier, page status, links needed, notes\n"
        "  - Auto-extract domain from URL on blur\n"
        "  - Duplicate URL warning\n"
        "  - Form validation + success confirmation\n"
        "- Pipeline table view:\n"
        "  - Columns: Priority | Domain | Keyword | GEO | Assigned | Status | Age | Actions\n"
        "  - Sortable headers\n"
        "  - Filter bar: Status, GEO, Priority, Domain, Assigned To, Date Range\n"
        "  - Priority color coding (P0=red, P1=orange, P2=yellow)\n"
        "  - Pagination (50/page)\n"
        "  - Quick actions: Assign, Change Status, View Details\n"
        "  - Bulk select checkboxes\n"
        "  - Auto-refresh every 60s\n\n"
        "**Gate:** PM can log in, submit a request, see it in the table.\n"
        "**Estimate:** 4 weeks",
        priority=1, parent=bi_id, tags=["backlink-manager", "bi-team", "frontend"],
        time_estimate_days=12)

    create_task(LIST_ID, "BI-2: Kanban Board + Detail Panel + Publisher/Agency/Order UI (Wk 6-9)",
        "**Dev 3**\n\n"
        "- Pipeline Kanban board:\n"
        "  - Columns by status (8 columns)\n"
        "  - Drag-drop cards between columns (dnd-kit)\n"
        "  - Optimistic UI updates\n"
        "  - Card: priority color, domain chip, keyword, assigned avatar\n"
        "  - Column count badges\n"
        "  - Toggle: Kanban ↔ Table (same filters apply)\n"
        "- Request detail slide-over panel:\n"
        "  - Header: URL, domain, keyword\n"
        "  - Status badge + dropdown\n"
        "  - AI anchor suggestions (clickable to select)\n"
        "  - AI publisher matches (clickable to select)\n"
        "  - Order history\n"
        "  - Activity timeline\n"
        "  - Actions: Assign, Place Order, Verify\n"
        "- Publisher Hub UI:\n"
        "  - Table: Domain, DR, Traffic, Niches, GEOs, Vetting Status, Avg Price\n"
        "  - Filter bar + search\n"
        "  - Add publisher form\n"
        "  - Publisher profile page (performance, notes, contact, history)\n"
        "- Agency management UI:\n"
        "  - List with NDA status, avg price, delivery, quality, caution flags\n"
        "  - Agency detail page with order history\n"
        "- Order management UI:\n"
        "  - Place order flow (select publisher/agency, enter price)\n"
        "  - Approval queue for orders >$700\n"
        "  - Order status tracking\n\n"
        "**Gate:** Full pipeline workflow usable in UI. Publishers and agencies manageable.\n"
        "**Estimate:** 4 weeks",
        priority=1, parent=bi_id, tags=["backlink-manager", "bi-team", "frontend"],
        time_estimate_days=14)

    create_task(LIST_ID, "BI-3: Reporting Dashboard + Exports + Settings + UAT (Wk 10-14)",
        "**Dev 3**\n\n"
        "- Reporting overview dashboard:\n"
        "  - Total links ordered/live/verified/pending with trend charts\n"
        "  - Period selector: 7d, 30d, 90d, 1y, custom\n"
        "  - Pipeline funnel visualization\n"
        "- By-domain report: links + spend per domain, drill-down\n"
        "- By-geo report: links + spend per market, pie/bar charts\n"
        "- By-month/quarter: historical view (KEY stakeholder request)\n"
        "- By-team: velocity, completion rate, active workload per builder\n"
        "- By-agency: delivery time, avg price, quality score, order volume\n"
        "- Spend tracking: total budget, by domain/market/agency, monthly trend\n"
        "- CSV/PDF export button on every report page\n"
        "- Settings pages:\n"
        "  - User management (admin only)\n"
        "  - Marketplace credentials (admin/head only)\n"
        "  - Notification preferences\n"
        "  - Integration health status\n"
        "- UAT facilitation with Marta + 2 builders\n"
        "- User guides (per role) + quick-start doc\n"
        "- Bug fixes + UX polish + responsive design + loading states\n\n"
        "**Charts:** Recharts or Chart.js\n\n"
        "**Gate:** All dashboards live, exports working, UAT passed, team trained.\n"
        "**Estimate:** 5 weeks (including UAT + polish)",
        priority=1, parent=bi_id, tags=["backlink-manager", "bi-team", "reporting"],
        time_estimate_days=16)


# ================================================================
# SUMMARY
# ================================================================
print("\n" + "=" * 60)
print("DONE")
print("=" * 60)
print(f"Tasks created:  {len(created_tasks)}")
print(f"Tasks failed:   {len(failed_tasks)}")

if failed_tasks:
    print("\nFailed:")
    for ft in failed_tasks:
        print(f"  - {ft['name']}: {ft['error']}")

print(f"\nStructure:")
print(f"  Parent: {parent_id}")
print(f"  ├── DOC: Project Plan: {doc_plan_id}")
print(f"  ├── DOC: Tech Spec: {doc_spec_id}")
print(f"  ├── ENG: {eng_id}")
print(f"  │   ├── ENG-1: Foundation (Wk 1-3)")
print(f"  │   ├── ENG-2: Core API (Wk 4-6)")
print(f"  │   ├── ENG-3: AI + Automation (Wk 7-9)")
print(f"  │   └── ENG-4: Workers + Migration + QA (Wk 10-14)")
print(f"  └── BI: {bi_id}")
print(f"      ├── BI-1: Setup + Intake + Table (Wk 2-5)")
print(f"      ├── BI-2: Kanban + Detail + Publisher/Agency (Wk 6-9)")
print(f"      └── BI-3: Reporting + Exports + UAT (Wk 10-14)")

# Save IDs
with open("/home/andre/projects/paradise-backlink-manager/clickup_task_ids.json", "w") as f:
    json.dump({
        "parent_id": parent_id,
        "doc_plan_id": doc_plan_id,
        "doc_spec_id": doc_spec_id,
        "eng_id": eng_id,
        "bi_id": bi_id,
        "all_tasks": created_tasks,
        "failed": failed_tasks,
    }, f, indent=2)

print(f"\nIDs saved: ~/projects/paradise-backlink-manager/clickup_task_ids.json")
