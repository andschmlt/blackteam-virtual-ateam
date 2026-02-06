# /posthog_update - PostHog Configuration Update

Update existing PostHog configurations with new features, fixes, or enhancements for any domain.

## Phase 0: RAG Context Loading (MANDATORY)

**Load relevant context from the RAG system before PostHog updates.**

Read these files for prior learnings:
- `~/pitaya/knowledge/feedback_corrections.md` — Data accuracy rules
- `~/AS-Virtual_Team_System_v2/blackteam/skills/learnings/` — Latest team learnings

**RAG Query:**
```python
from AS-Virtual_Team_System_v2.rag.rag_client import VTeamRAG
rag = VTeamRAG()
context = rag.query("posthog update configuration", top_k=5)
learnings = rag.query("posthog configuration corrections", collection_name="learnings", top_k=3)
```

---

## MANDATORY: Head of Product Assignment (Director Rule 8)
**Head of Product MUST be involved in ALL PostHog update work.**

When this command is invoked:
1. Head of Product is automatically assigned to the task
2. HoP reviews the update scope and impact
3. Update deliverables require HoP approval before deployment

See: `/mnt/c/Users/andre/Desktop/Virtual ATeam/BlackTeam/DIRECTOR_RULES.md` - Rule 8

---

## HARD RULE: No Remote Push

**NEVER commit or push to main/remote repositories.**

- Save files locally only
- Commit to local repository only (no `git push`)
- Files are prepared for manual deployment by TechOps via ClickUp tasks

This is a safety measure to prevent automated changes to production repositories.

---

## Usage

```
/posthog_update [domain] [update_type]    # Update specific domain
/posthog_update [domain]                  # General update (auto-detect type)
/posthog_update all domains               # Update all domains in registry
```

### Update Types
- `conversion` - Add/update conversion tracking
- `navboost` - Update NavBoost metrics
- `config` - Update PostHog configuration
- `fix` - Bug fixes or corrections

---

## Source of Truth

**ALWAYS use these files as source of truth:**

| File | Path | Purpose |
|------|------|---------|
| **POSTHOG_REGISTRY.md** | `/home/andre/projects/posthog-integration/POSTHOG_REGISTRY.md` | Domain registry, task IDs, GitHub repos, branches |
| **CHANGELOG.md** | `/home/andre/projects/posthog-integration/CHANGELOG.md` | Human-readable changelog |

**Before any update:**
1. Read POSTHOG_REGISTRY.md to get domain info
2. Look up parent task ID
3. Look up GitHub repo and branch
4. Check current version

---

## Quick Reference - Key IDs (DO NOT MODIFY)

| Resource | ID | Purpose |
|----------|-----|---------|
| ClickUp List for Tasks | 901324589525 | All PostHog deployment tasks go here |
| ClickUp Workspace | 8553292 | Paradise Media workspace |
| Andre User ID | 60332880 | ClickUp assignee |
| Malcolm User ID | 82173399 | ClickUp assignee |

---

## Workflow Overview

```
/posthog_update [domain] [type]
        │
        ▼
┌─────────────────────────────────────────┐
│ PHASE 1: Load Registry                  │
│ - Read POSTHOG_REGISTRY.md              │
│ - Get parent task ID for domain         │
│ - Get GitHub repo and branch            │
│ - Determine current version             │
└─────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────┐
│ PHASE 2: Generate Update Files          │
│ - Create/update tracking scripts        │
│ - Generate RELEASE_NOTES.md             │
│ - Generate deployment instructions      │
│ - Save to BlackTeam directory           │
└─────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────┐
│ PHASE 3: ClickUp Sub-Task               │
│ - ALWAYS create sub-task under parent   │
│ - Name: "Update - Deploy Posthog Code"  │
│ - Attach updated files                  │
│ - Assign to Malcolm                     │
└─────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────┐
│ PHASE 4: Local Save & Commit            │
│ - Save files to local directories       │
│ - Update RELEASE_NOTES.md               │
│ - Commit locally (NO remote push)       │
│ - TechOps deploys via ClickUp tasks     │
└─────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────┐
│ PHASE 5: Update Registry                │
│ - Update POSTHOG_REGISTRY.md            │
│   - Add sub-task ID                     │
│   - Add commit hash                     │
│   - Update version                      │
│ - Update CHANGELOG.md                   │
│ - Commit registry changes locally       │
└─────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────┐
│ PHASE 6: Summary                        │
│ - Output task links                     │
│ - List files updated                    │
│ - Git commit hash                       │
│ - Deployment instructions               │
└─────────────────────────────────────────┘
```

---

## Phase 1: Load Registry

### Read Registry for Domain Info

```python
# ALWAYS look up domain in registry first
registry_path = "/home/andre/projects/posthog-integration/POSTHOG_REGISTRY.md"

# Extract for each domain:
# - Parent Task ID (e.g., 86aepf7r3)
# - GitHub Repo (e.g., ParadiseMediaOrg/hudsonreporter.com)
# - Branch (main, master, staging, or migration-staging)
# - Current Version (e.g., 1.1.0)
# - Existing Sub-Tasks
```

### Example Registry Lookup

| Domain | Parent Task | GitHub Repo | Branch |
|--------|-------------|-------------|--------|
| hudsonreporter.com | 86aepf7r3 | ParadiseMediaOrg/hudsonreporter.com | main |
| culture.org | 86aepf1v4 | ParadiseMediaOrg/culture.org | staging |
| esports.gg | 86aepf24b | ParadiseMediaOrg/esports.gg | migration-staging |

---

## Phase 2: Generate Update Files

### Directory Structure

```
/mnt/c/Users/andre/Desktop/Virtual ATeam/BlackTeam/projects/posthog-integration/
└── posthog-navboost-all-sites/[domain]/
    ├── navboost-tracker.js            # NavBoost tracker
    ├── conversion-tracker.js          # Conversion tracking
    ├── posthog-full-tracking.php      # WordPress integration
    ├── posthog-functions.php          # Helper functions
    ├── DEPLOYMENT_GUIDE.md            # Deployment instructions
    ├── README.md                      # Overview
    └── RELEASE_NOTES.md               # Version history (MANDATORY)
```

### RELEASE_NOTES.md Template (MANDATORY)

```markdown
# Release Notes - [domain]

## Current Version: [X.Y.Z]

### v[X.Y.Z] (YYYY-MM-DD) - [Update Title]
**ClickUp Task:** [parent_task_id](https://app.clickup.com/t/[parent_task_id])
**ClickUp Sub-task:** [subtask_id](https://app.clickup.com/t/[subtask_id])
**Git Commit:** `[hash]`
**Branch:** [branch]

**Changes:**
- [Description of changes]

**Files:**
| File | Size | Description |
|------|------|-------------|
| conversion-tracker.js | 28KB | 5 conversion types |
| posthog-full-tracking.php | 6KB | WordPress integration |
| DEPLOYMENT_GUIDE.md | 7KB | Deployment instructions |

---

### v1.0.0 (YYYY-MM-DD) - Initial Setup
**ClickUp Task:** [parent_task_id](https://app.clickup.com/t/[parent_task_id])

**Features:**
- NavBoost KPI tracking
- Core Web Vitals
- WordPress integration
```

---

## Phase 3: ClickUp Sub-Task (MANDATORY)

### Sub-Task Naming Convention

**ALWAYS use this exact name:**
```
Update - Deploy Posthog Code
```

**NEVER use:**
- ~~"Update: Conversion Tracking - domain.com"~~
- ~~"Bulk Update - 28 Domains"~~
- ~~"Add Conversion Tracking"~~

### Create Sub-Task Under Parent

```python
def create_deploy_subtask(parent_id, domain, branch, description):
    """Create sub-task under existing parent task."""
    url = f"https://api.clickup.com/api/v2/list/{LIST_ID}/task"
    headers = {
        "Authorization": CLICKUP_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "name": "Update - Deploy Posthog Code",  # ALWAYS this exact name
        "description": description,
        "assignees": [MALCOLM_ID],
        "parent": parent_id,  # MUST have parent
        "status": "to do"
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()
```

### Sub-Task Description Template

```markdown
## PostHog Update - v[X.Y.Z]

### GitHub Status
- **Repository:** ParadiseMediaOrg/[domain]
- **Branch:** [branch]
- **Commit:** [commit_hash]

### Files Added to posthog/ folder:
- `conversion-tracker.js` - Enhanced conversion tracking (5 types)
- `posthog-full-tracking.php` - WordPress integration
- `DEPLOYMENT_GUIDE.md` - Deployment instructions
- `navboost-tracker.js` - NavBoost KPI tracking
- `posthog-functions.php` - Helper functions
- `RELEASE_NOTES.md` - Version history

### Changes in This Update:
- [List of changes]

### Deployment Steps:
1. Pull latest from [branch] branch
2. Follow DEPLOYMENT_GUIDE.md instructions
3. Verify in PostHog Live Events
```

---

## Phase 4: Local Save & Commit (NO REMOTE PUSH)

### HARD RULE: Local Only

**DO NOT push to remote repositories.** All files are saved locally and committed to the local repository only. TechOps will deploy manually via ClickUp tasks.

### Save Files Locally

```bash
# 1. Save to BlackTeam directory
BLACKTEAM_DIR="/mnt/c/Users/andre/Desktop/Virtual ATeam/BlackTeam/projects/posthog-integration/posthog-navboost-all-sites"
mkdir -p "$BLACKTEAM_DIR/[domain]"
cp [source_files]/* "$BLACKTEAM_DIR/[domain]/"

# 2. Save to local posthog-integration repo
LOCAL_REPO="/home/andre/projects/posthog-integration"
mkdir -p "$LOCAL_REPO/[domain]"
cp [source_files]/* "$LOCAL_REPO/[domain]/"

# 3. Commit locally only - NO PUSH
cd "$LOCAL_REPO"
git add [domain]/
git commit -m "$(cat <<'EOF'
Add PostHog [update_type] tracking (v[X.Y.Z])

- [Change 1]
- [Change 2]
- WordPress integration via posthog-full-tracking.php

ClickUp Task: [subtask_id]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"

# DO NOT RUN: git push
# Files will be deployed by TechOps via ClickUp tasks
```

### Why No Remote Push?

1. **Safety**: Prevents automated changes to production repositories
2. **Review**: TechOps can review files before deployment
3. **Control**: Manual deployment ensures proper testing
4. **Audit**: ClickUp tasks provide deployment tracking

### Branch Reference (for TechOps deployment)

| Branch Type | Domains |
|-------------|---------|
| main | bestdaily.com, betanews.com, countryqueer.com, etc. |
| master | centraljersey.com, iogames.space |
| staging | culture.org, dotesports.com, newgamenetwork.com, etc. |
| migration-staging | esports.gg |

---

## Phase 5: Update Registry (MANDATORY)

### Update POSTHOG_REGISTRY.md

After each update, add/update in registry:

1. **Domain Registry Table** - Update version
2. **Commit Log** - Add new commit entry
3. **Sub-Tasks Table** - Add new sub-task ID

### Update CHANGELOG.md

After each update:

1. **Domain Status Summary** - Update status/version
2. **Changelog by Domain** - Add new entry

### Commit Registry Changes (LOCAL ONLY)

```bash
cd /home/andre/projects/posthog-integration
git add POSTHOG_REGISTRY.md CHANGELOG.md
git commit -m "Update registry: [domain] v[X.Y.Z]

- Sub-task: [subtask_id]
- Commit: [hash]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"

# DO NOT RUN: git push
# Registry is local-only
```

---

## Phase 6: Summary Output

### Output Format

```
## PostHog Update Complete

### Domain: [domain.com]
### Version: [X.Y.Z]
### Update Type: [type]

### ClickUp:
- Parent Task: https://app.clickup.com/t/[parent_id]
- Sub-task: https://app.clickup.com/t/[subtask_id]

### Git Status: LOCAL ONLY (no remote push)
- Local Commit: [hash]
- Target Repo: ParadiseMediaOrg/[domain]
- Target Branch: [branch] (for TechOps deployment)

### Files Updated:
| File | Description |
|------|-------------|
| conversion-tracker.js | 5 conversion types |
| posthog-full-tracking.php | WordPress integration |
| DEPLOYMENT_GUIDE.md | Installation instructions |
| RELEASE_NOTES.md | Version history |

### Registry Updated:
- POSTHOG_REGISTRY.md ✓
- CHANGELOG.md ✓

### Deployment Steps:
1. TechOps: Pull from [branch] branch
2. Follow DEPLOYMENT_GUIDE.md
3. Verify events in PostHog dashboard
```

---

## Checklist

Before completing `/posthog_update`:

- [ ] Registry loaded (POSTHOG_REGISTRY.md)
- [ ] Files generated in BlackTeam directory
- [ ] RELEASE_NOTES.md created/updated
- [ ] ClickUp sub-task created as "Update - Deploy Posthog Code"
- [ ] Sub-task attached to correct parent task
- [ ] Files saved locally (NO remote push)
- [ ] Committed to local repo only
- [ ] POSTHOG_REGISTRY.md updated with sub-task ID and commit
- [ ] CHANGELOG.md updated
- [ ] Summary output provided to user

**HARD RULE**: Never push to remote - TechOps deploys via ClickUp tasks

---

## Files & Locations

| Location | Path | Purpose |
|----------|------|---------|
| **Registry** | `/home/andre/projects/posthog-integration/POSTHOG_REGISTRY.md` | Source of truth |
| **Changelog** | `/home/andre/projects/posthog-integration/CHANGELOG.md` | Human-readable log |
| **Local Archive** | `/home/andre/projects/posthog-integration/[domain]/` | Local copies |
| **BlackTeam Archive** | `/mnt/c/Users/andre/Desktop/Virtual ATeam/BlackTeam/projects/posthog-integration/posthog-navboost-all-sites/` | Working files |
| **API Keys** | `/home/andre/.keys/.env` | Credentials |

---

## Version Numbering

| Change Type | Version Bump | Example |
|-------------|--------------|---------|
| Initial setup | 1.0.0 | New domain |
| New feature (conversion tracking) | 1.X.0 | 1.0.0 → 1.1.0 |
| Bug fix / minor update | 1.0.X | 1.1.0 → 1.1.1 |
| Breaking change | X.0.0 | 1.1.0 → 2.0.0 |

---

## Related Commands

- `/posthog_setup` - Initial PostHog setup for new domains
- `/posthog_analysis` - Generate analytics reports
- `/blackteam` - Full project execution with Director

---

*Last Updated: 2026-01-21*
