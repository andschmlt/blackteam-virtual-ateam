# /posthog_setup - PostHog + NavBoost Integration Setup

Complete PostHog analytics setup with NavBoost user engagement tracking for any domain or batch of domains.

## Phase 0: RAG Context Loading (MANDATORY)

**Load relevant context from the RAG system before PostHog setup.**

Read these files for prior learnings:
- `~/pitaya/knowledge/feedback_corrections.md` — Data accuracy rules
- `~/AS-Virtual_Team_System_v2/blackteam/skills/learnings/` — Latest team learnings

**RAG Query:**
```python
from AS-Virtual_Team_System_v2.rag.rag_client import VTeamRAG
rag = VTeamRAG()
context = rag.query("posthog setup navboost integration", top_k=5)
learnings = rag.query("posthog setup corrections", collection_name="learnings", top_k=3)
```

---

## MANDATORY: Head of Product Assignment (Director Rule 8)
**Head of Product MUST be involved in ALL PostHog setup work.**

When this command is invoked:
1. Head of Product is automatically assigned to the task
2. HoP must sign off on NavBoost configuration (CTA selectors, engagement weights, pogo targets)
3. HoP reviews experiment design and E-E-A-T implications
4. Setup deliverables require HoP approval before deployment

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
/posthog_setup [domain]              # Single domain setup
/posthog_setup batch                 # Batch setup for all domains from ClickUp folders
/posthog_setup batch [folder_id]     # Batch setup for specific folder
```

---

## Quick Reference - Key IDs (DO NOT MODIFY)

| Resource | ID | Purpose |
|----------|-----|---------|
| ClickUp List for Tasks | 901324589525 | All PostHog deployment tasks go here |
| ClickUp Workspace | 8553292 | Paradise Media workspace |
| iGaming Sites Folder | 90090340968 | Source folder for domain list |
| Lucky7s O&O Folder | 90134211413 | Source folder for domain list |
| PostHog Org ID | 019b2233-57a2-0000-3260-cfa42e906fc4 | For API project creation |
| Andre User ID | 60332880 | ClickUp assignee |
| Malcolm User ID | 82173399 | ClickUp assignee |

---

## Complete Workflow Overview

```
/posthog_setup [domain(s)]
        │
        ▼
┌─────────────────────────────────────────┐
│ PHASE 1: Domain Discovery               │
│ - If batch: Fetch from ClickUp folders  │
│ - If single: Validate domain            │
│ - Check GitHub repo mapping             │
└─────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────┐
│ PHASE 2: PostHog Project Setup          │
│ - Check existing projects via API       │
│ - Create new projects if needed         │
│ - Get API tokens for each domain        │
└─────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────┐
│ PHASE 3: Generate Setup Files           │
│ - navboost-tracker.js (full metrics)    │
│ - posthog-functions.php (WordPress)     │
│ - README.md (installation guide)        │
│ - RELEASE_NOTES.md (deployment docs)    │
└─────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────┐
│ PHASE 4: Local Save & Commit            │
│ - Save files to local setup directory   │
│ - Commit locally (NO remote push)       │
│ - TechOps deploys via ClickUp tasks     │
└─────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────┐
│ PHASE 5: ClickUp Task Creation          │
│ - Create parent task per domain         │
│ - Attach all setup files                │
│ - Create sub-tasks (Release + Deploy)   │
│ - Auto-complete Release Notes sub-task  │
└─────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────┐
│ PHASE 6: Package & Notification         │
│ - Create zip file with all setup files  │
│ - Update deployment tracker             │
│ - Send Slack notification (optional)    │
└─────────────────────────────────────────┘
```

---

## Phase 1: Domain Discovery

### Option A: Batch Mode (All Domains)

Fetch domains from ClickUp folders:

```python
import requests

import os
from dotenv import load_dotenv
load_dotenv(os.path.expanduser("~/.keys/.env"))
CLICKUP_API_KEY = os.environ["CLICKUP_API_KEY"]
FOLDERS = ["90090340968", "90134211413"]  # iGaming + Lucky7s

def fetch_all_domains():
    domains = []
    headers = {"Authorization": CLICKUP_API_KEY}

    for folder_id in FOLDERS:
        response = requests.get(
            f"https://api.clickup.com/api/v2/folder/{folder_id}/list",
            headers=headers
        )
        lists = response.json().get("lists", [])
        for lst in lists:
            domains.append(lst["name"])

    return domains
```

### Option B: Single Domain

Validate domain format and check GitHub repo:

```bash
# Check if repo exists in ParadiseMediaOrg
gh repo view ParadiseMediaOrg/[domain] --json name 2>/dev/null && echo "Repo exists"
```

### GitHub Repository Mapping

Load from `/tmp/domain_repos.json` or query GitHub:

```python
DOMAIN_REPOS = {
    "bestdaily.com": "ParadiseMediaOrg/bestdaily.com",
    "betanews.com": "ParadiseMediaOrg/betanews.com",
    "centraljersey.com": "ParadiseMediaOrg/centraljersey.com",
    "countryqueer.com": "ParadiseMediaOrg/countryqueer.com",
    "culture.org": "ParadiseMediaOrg/culture.org",
    "dotesports.com": "ParadiseMediaOrg/dotesports.com",
    "esports.gg": "ParadiseMediaOrg/esports.gg",
    "europeangaming.eu": "ParadiseMediaOrg/europeangaming.eu",
    "godisageek.com": "ParadiseMediaOrg/godisageek.com",
    "hudsonreporter.com": "ParadiseMediaOrg/hudsonreporter.com",
    "iogames.space": "ParadiseMediaOrg/iogames.space",
    "lowerbuckstimes.com": "ParadiseMediaOrg/lowerbuckstimes.com",
    "management.org": "ParadiseMediaOrg/management.org",
    "mrracy.com": "ParadiseMediaOrg/mrracy.com",
    "newgamenetwork.com": "ParadiseMediaOrg/newgamenetwork.com",
    "northeasttimes.com": "ParadiseMediaOrg/northeasttimes.com",
    "ostexperte.de": "ParadiseMediaOrg/ostexperte.de",
    "pokerology.com": "ParadiseMediaOrg/pokerology.com",
    "pokertube.com": "ParadiseMediaOrg/pokertube.com",
    "snjtoday.com": "ParadiseMediaOrg/snjtoday.com",
    "southphillyreview.com": "ParadiseMediaOrg/southphillyreview.com",
    "sport-oesterreich.at": "ParadiseMediaOrg/sport-oesterreich.at",
    "starnewsphilly.com": "ParadiseMediaOrg/starnewsphilly.com",
    "theroanokestar.com": "ParadiseMediaOrg/theroanokestar.com",
    "thesunpapers.com": "ParadiseMediaOrg/thesunpapers.com",
    "topdocumentaryfilms.com": "ParadiseMediaOrg/topdocumentaryfilms.com",
    "warcraftmovies.com": "ParadiseMediaOrg/warcraftmovies.com"
}

# Domains without GitHub repos (setup files only, no push)
NO_GITHUB_REPOS = ["metrotimes.com", "philadelphiaweekly.com", "silvergames.com"]
```

---

## Phase 2: PostHog Project Setup

### Check Existing Projects

```python
import requests

POSTHOG_API_KEY = os.environ.get('POSTHOG_PERSONAL_API_KEY')
POSTHOG_ORG_ID = "019b2233-57a2-0000-3260-cfa42e906fc4"

def get_existing_projects():
    headers = {"Authorization": f"Bearer {POSTHOG_API_KEY}"}
    response = requests.get(
        f"https://us.i.posthog.com/api/organizations/{POSTHOG_ORG_ID}/projects/",
        headers=headers
    )
    return {p["name"].lower(): p for p in response.json().get("results", [])}
```

### Create New PostHog Project

```python
def create_posthog_project(domain):
    headers = {
        "Authorization": f"Bearer {POSTHOG_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {"name": domain}

    response = requests.post(
        f"https://us.i.posthog.com/api/organizations/{POSTHOG_ORG_ID}/projects/",
        headers=headers,
        json=payload
    )

    if response.status_code in [200, 201]:
        project = response.json()
        return {
            "id": project["id"],
            "api_token": project["api_token"],
            "name": project["name"]
        }
    else:
        raise Exception(f"Failed to create project: {response.text}")
```

---

## Phase 3: Generate Setup Files

### Directory Structure

```
/mnt/c/Users/andre/Desktop/Virtual ATeam/BlackTeam/projects/posthog-integration/setup/
└── [domain.com]/
    ├── navboost-tracker.js     # Full NavBoost KPI Framework tracking
    ├── posthog-functions.php   # WordPress integration
    ├── README.md               # Installation guide
    └── RELEASE_NOTES.md        # Deployment documentation
```

### navboost-tracker.js Template

**CRITICAL:** This file MUST include ALL of the following metrics:

1. **Core Web Vitals** (via PostHog autocapture)
   - LCP (Largest Contentful Paint)
   - CLS (Cumulative Layout Shift)
   - INP (Interaction to Next Paint)

2. **NavBoost KPI Framework**
   - Pogo rate detection (< 8 seconds = pogo)
   - Dwell time tracking with ratings (very_bad, weak, normal, strong)
   - Scroll depth milestones (25%, 50%, 75%, 100%)
   - CTA visibility and click tracking
   - Good abandonment (affiliate clicks from Google users)

3. **Conversions**
   - Toplist row visibility (for affiliate sites)
   - CTA engagement
   - Outbound click tracking

4. **Session Recording & Heatmaps** (via PostHog config)

```javascript
/**
 * NavBoost Tracking Module for PostHog
 * Full NavBoost KPI Framework Implementation
 *
 * @site [DOMAIN]
 * @project_id [PROJECT_ID]
 * @version 2.0.0
 */

(function() {
    'use strict';

    const CONFIG = {
        SITE_DOMAIN: '[DOMAIN]',
        POGO_THRESHOLD_MS: 8000,
        SCROLL_MILESTONES: [25, 50, 75, 100],
        SCROLL_ZONES: {
            25: 'above_fold',
            50: 'cta_zone',
            75: 'content',
            100: 'footer'
        },
        GOOGLE_DOMAINS: [
            'google.com', 'google.co.uk', 'google.de', 'google.fr', 'google.es',
            'google.it', 'google.nl', 'google.com.au', 'google.ca', 'google.co.in'
        ],
        DWELL_BENCHMARKS: {
            VERY_BAD: 10000,
            WEAK: 30000,
            NORMAL: 90000
        },
        TARGETS: {
            POGO_RATE: 20,
            DWELL_TIME: 60,
            CTA_CTR: 3,
            ENGAGEMENT_SCORE: 65,
            GOOD_ABANDONMENT: 10
        },
        CTA_SELECTORS: [
            '[data-cta]', '.cta-button', '.affiliate-link', 'a[rel="sponsored"]',
            '.toplist-item a', 'a[href*="/go/"]', 'a[href*="/redirect/"]',
            '.bonus-btn', '.signup-btn', '.read-more'
        ],
        TOPLIST_SELECTORS: [
            '.toplist-row', '.casino-item', '.operator-card',
            '[data-toplist-position]', '.ranking-item'
        ]
    };

    // [Full implementation as generated in the session]
    // See: /mnt/c/Users/andre/Desktop/Virtual ATeam/BlackTeam/projects/posthog-integration/setup/pokerology.com/navboost-tracker.js
    // for complete reference implementation
})();
```

### posthog-functions.php Template

```php
<?php
/**
 * PostHog Analytics Integration for [DOMAIN]
 *
 * @package PostHog_NavBoost
 * @version 2.0.0
 */

if (!defined('ABSPATH')) exit;

/**
 * Initialize PostHog with full configuration
 */
function [DOMAIN_SLUG]_posthog_init() {
    ?>
    <script>
        !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.crossOrigin="anonymous",p.async=!0,p.src=s.api_host.replace(".i.posthog.com","-assets.i.posthog.com")+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="init capture register register_once register_for_session unregister unregister_for_session getFeatureFlag getFeatureFlagPayload isFeatureEnabled reloadFeatureFlags updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures on onFeatureFlags onSessionId getSurveys getActiveMatchingSurveys renderSurvey canRenderSurvey getNextSurveyStep identify setPersonProperties group resetGroups setPersonPropertiesForFlags resetPersonPropertiesForFlags setGroupPropertiesForFlags resetGroupPropertiesForFlags reset get_distinct_id getGroups get_session_id get_session_replay_url alias set_config startSessionRecording stopSessionRecording sessionRecordingStarted captureException loadToolbar get_property getSessionProperty createPersonProfile opt_in_capturing opt_out_capturing has_opted_in_capturing has_opted_out_capturing clear_opt_in_out_capturing debug".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);

        posthog.init('[API_TOKEN]', {
            api_host: 'https://us.i.posthog.com',
            person_profiles: 'identified_only',
            capture_pageview: true,
            capture_pageleave: true,
            autocapture: true,
            autocapture_web_vitals_opt_in: true,
            capture_performance_opt_in: true,
            session_recording: {
                maskAllInputs: true,
                maskTextContent: false
            },
            enable_heatmaps: true,
            property_denylist: ['$ip']
        });

        // Track page metadata
        posthog.capture('$pageview', {
            page_template: document.body.className,
            page_url: window.location.href,
            page_title: document.title
        });
    </script>
    <?php
}
add_action('wp_head', '[DOMAIN_SLUG]_posthog_init', 1);

/**
 * Enqueue NavBoost tracker script
 */
function [DOMAIN_SLUG]_navboost_tracker() {
    wp_enqueue_script(
        'navboost-tracker',
        get_stylesheet_directory_uri() . '/assets/js/navboost-tracker.js',
        array(),
        '2.0.0',
        true
    );
}
add_action('wp_enqueue_scripts', '[DOMAIN_SLUG]_navboost_tracker', 20);
```

---

## Phase 4: Local Save & Commit (NO REMOTE PUSH)

### HARD RULE: Local Only

**DO NOT push to remote repositories.** All files are saved locally and committed to the local repository only. TechOps will deploy manually via ClickUp tasks.

### Save Files Locally

```python
import os
import shutil

SETUP_DIR = "/mnt/c/Users/andre/Desktop/Virtual ATeam/BlackTeam/projects/posthog-integration/setup"
LOCAL_REPO = "/home/andre/projects/posthog-integration"

def save_locally(domain, repo_path):
    """Save setup files locally - NO REMOTE PUSH."""

    # Create domain directory in setup folder
    domain_dir = os.path.join(SETUP_DIR, domain)
    os.makedirs(domain_dir, exist_ok=True)

    # Files are already generated in Phase 3
    # They are saved in: SETUP_DIR/[domain]/

    # Also copy to local posthog-integration repo
    local_domain_dir = os.path.join(LOCAL_REPO, domain)
    os.makedirs(local_domain_dir, exist_ok=True)

    for filename in ["navboost-tracker.js", "posthog-functions.php", "README.md", "RELEASE_NOTES.md"]:
        src = os.path.join(domain_dir, filename)
        dst = os.path.join(local_domain_dir, filename)
        if os.path.exists(src):
            shutil.copy2(src, dst)

    return domain_dir

def commit_locally(domain):
    """Commit changes to local repository only - NO PUSH."""
    os.chdir(LOCAL_REPO)

    # Stage files
    subprocess.run(["git", "add", f"{domain}/"], check=True)

    # Commit locally only - NO PUSH
    subprocess.run([
        "git", "commit", "-m",
        f"Add PostHog NavBoost setup for {domain}\n\nIncludes:\n- Full NavBoost KPI Framework tracking\n- Core Web Vitals\n- Conversions tracking\n- Session recording & heatmaps\n\nCo-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
    ], check=True)

    # DO NOT RUN: git push
    # Files will be deployed by TechOps via ClickUp tasks

    return "Committed locally (no remote push)"
```

### Why No Remote Push?

1. **Safety**: Prevents automated changes to production repositories
2. **Review**: TechOps can review files before deployment
3. **Control**: Manual deployment ensures proper testing
4. **Audit**: ClickUp tasks provide deployment tracking

---

## Phase 5: ClickUp Task Creation (CRITICAL)

### Configuration

**ALL PostHog deployment tasks go to list 901324589525**

```python
CLICKUP_CONFIG = {
    "API_KEY": os.environ["CLICKUP_API_KEY"],  # Loaded from ~/.keys/.env
    "LIST_ID": "901324589525",  # Centralized PostHog deployment list
    "ASSIGNEES": {
        "andre": 60332880,
        "malcolm": 82173399
    }
}
```

### Task Structure (Per Domain)

```
PostHog Configuration - [domain.com]  (Parent Task)
├── Assignee: Malcolm
├── Status: To Do
├── Attachments:
│   ├── navboost-tracker.js
│   ├── posthog-functions.php
│   ├── RELEASE_NOTES.md
│   └── README.md
│
├── Sub-task 1: "Add Release Notes"
│   ├── Assignee: Andre
│   └── Status: Complete (auto-marked)
│
└── Sub-task 2: "Deploy PostHog Code"
    ├── Assignee: Malcolm
    └── Status: To Do
```

### Implementation

```python
import requests
import os
import time

CLICKUP_API_KEY = os.environ["CLICKUP_API_KEY"]  # Loaded from ~/.keys/.env
LIST_ID = "901324589525"
SETUP_DIR = "/mnt/c/Users/andre/Desktop/Virtual ATeam/BlackTeam/projects/posthog-integration/setup"

ANDRE_ID = 60332880
MALCOLM_ID = 82173399

HEADERS = {
    "Authorization": CLICKUP_API_KEY,
    "Content-Type": "application/json"
}

def create_task(name, description, assignees, parent_id=None):
    """Create a ClickUp task."""
    url = f"https://api.clickup.com/api/v2/list/{LIST_ID}/task"

    payload = {
        "name": name,
        "description": description,
        "assignees": assignees,
        "status": "to do"
    }

    if parent_id:
        payload["parent"] = parent_id

    response = requests.post(url, headers=HEADERS, json=payload)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def add_attachment(task_id, file_path, filename):
    """Add file attachment to a ClickUp task."""
    url = f"https://api.clickup.com/api/v2/task/{task_id}/attachment"

    headers = {"Authorization": CLICKUP_API_KEY}

    if not os.path.exists(file_path):
        return False

    with open(file_path, 'rb') as f:
        files = {'attachment': (filename, f, 'text/plain')}
        response = requests.post(url, headers=headers, files=files)

    return response.status_code == 200

def mark_complete(task_id):
    """Mark a task as complete."""
    url = f"https://api.clickup.com/api/v2/task/{task_id}"
    payload = {"status": "complete"}
    response = requests.put(url, headers=HEADERS, json=payload)
    return response.status_code == 200

def process_domain(domain, has_github_repo=True):
    """Create ClickUp tasks for a domain with attachments."""

    domain_dir = os.path.join(SETUP_DIR, domain)
    github_note = f"https://github.com/ParadiseMediaOrg/{domain}" if has_github_repo else "No GitHub repository"

    # Create parent task
    parent_desc = f"""PostHog NavBoost Configuration for {domain}

## Files Included
- navboost-tracker.js - Frontend tracking script with full NavBoost KPI Framework
- posthog-functions.php - WordPress integration code
- RELEASE_NOTES.md - Deployment instructions

## Metrics Tracked
- Core Web Vitals (LCP, CLS, INP)
- NavBoost KPIs (pogo rate, dwell time, scroll depth, CTA CTR)
- Conversions
- Session Recording
- Heatmaps

## GitHub Repository
{github_note}
"""

    parent_task = create_task(
        f"PostHog Configuration - {domain}",
        parent_desc,
        [MALCOLM_ID]
    )

    if not parent_task:
        return None

    parent_id = parent_task["id"]

    # Add attachments to parent task
    for filename in ["navboost-tracker.js", "posthog-functions.php", "RELEASE_NOTES.md", "README.md"]:
        file_path = os.path.join(domain_dir, filename)
        add_attachment(parent_id, file_path, filename)

    time.sleep(0.3)  # Rate limiting

    # Create sub-task 1: Release Notes (auto-complete)
    subtask1 = create_task(
        "Add Release Notes",
        f"Release notes created for {domain}. See attached RELEASE_NOTES.md.",
        [ANDRE_ID],
        parent_id
    )

    if subtask1:
        mark_complete(subtask1["id"])

    time.sleep(0.3)

    # Create sub-task 2: Deploy
    subtask2_desc = f"""Deploy PostHog tracking code to {domain}

## Deployment Steps:

1. **Add posthog-functions.php to theme:**
   - Copy to: wp-content/themes/theme-starter-developer/inc/posthog-functions.php
   - Add include in functions.php: require_once get_template_directory() . '/inc/posthog-functions.php';

2. **Add navboost-tracker.js:**
   - Copy to: wp-content/themes/theme-starter-developer/assets/js/navboost-tracker.js
   - Enqueue in posthog-functions.php (already configured)

3. **Verify Installation:**
   - Check browser console for PostHog initialization
   - Verify events in PostHog dashboard
   - Test Core Web Vitals tracking
   - Verify NavBoost metrics (pogo detection, dwell time)

## GitHub Repository
{github_note}
"""

    subtask2 = create_task(
        "Deploy PostHog Code",
        subtask2_desc,
        [MALCOLM_ID],
        parent_id
    )

    return {
        "domain": domain,
        "parent_id": parent_id,
        "subtask1_id": subtask1["id"] if subtask1 else None,
        "subtask2_id": subtask2["id"] if subtask2 else None
    }
```

---

## Phase 6: Package & Notification

### Create Zip Package

```bash
cd "/mnt/c/Users/andre/Desktop/Virtual ATeam/BlackTeam/projects/posthog-integration/setup"
zip -r ../posthog-navboost-all-sites.zip . -x "*.DS_Store"
```

### Update Deployment Tracker

Update `/mnt/c/Users/andre/Desktop/Virtual ATeam/BlackTeam/projects/posthog-integration/POSTHOG_DEPLOYMENT_TRACKER.md`

### Slack Notification (Optional)

```bash
# Using Slack webhook
curl -X POST -H 'Content-type: application/json' \
  --data '{
    "text": "🚀 *PostHog NavBoost Setup Complete*\n\nDomains: [COUNT]\nClickUp Tasks: Created in list 901324589525\n\n— Virtual ATeam"
  }' \
  $SLACK_WEBHOOK_URL
```

---

## Execution Summary Format

After running `/posthog_setup`, output:

```
## PostHog Setup Complete

### Domains Processed: [COUNT]

| Domain | PostHog ID | Local Files | ClickUp Task |
|--------|------------|-------------|--------------|
| domain1.com | 12345 | ✓ Saved | 86abc123 |
| domain2.com | 12346 | ✓ Saved | 86abc124 |
| domain3.com | 12347 | ✓ Saved | 86abc125 |

### Git Status: LOCAL ONLY (no remote push)

### Task Structure (per domain):
- Parent Task: "PostHog Configuration - {domain}"
  - Assignee: Malcolm
  - Attachments: navboost-tracker.js, posthog-functions.php, RELEASE_NOTES.md, README.md
- Sub-task 1: "Add Release Notes" (Andre) - Auto-completed
- Sub-task 2: "Deploy PostHog Code" (Malcolm) - To Do

### ClickUp List
https://app.clickup.com/8553292/v/l/li/901324589525

### Setup Files
/mnt/c/Users/andre/Desktop/Virtual ATeam/BlackTeam/projects/posthog-integration/setup/

### Zip Package
/mnt/c/Users/andre/Desktop/Virtual ATeam/BlackTeam/projects/posthog-integration/posthog-navboost-all-sites.zip
```

---

## Reference: NavBoost Targets

| Metric | Target | Critical |
|--------|--------|----------|
| Pogo Rate | < 20% | > 25% |
| Dwell Time | > 60s | < 30s |
| CTA CTR | > 3% | < 1% |
| Engagement Score | > 65 | < 50 |
| Good Abandonment | > 10% | < 5% |

## Reference: Core Web Vitals Thresholds

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP | ≤1200ms | ≤2500ms | >2500ms |
| CLS | ≤0.1 | ≤0.25 | >0.25 |
| INP | ≤200ms | ≤500ms | >500ms |

---

## Related Commands

- `/posthog_analysis` - Generate analytics reports
- `/blackteam` - Full project execution with Director
- `/codeguard` - Code quality monitoring

## Files

- API Keys: `/home/andre/.keys/.env`
- ClickUp Config: `/home/andre/.claude/clickup_config.json`
- Setup Files: `/mnt/c/Users/andre/Desktop/Virtual ATeam/BlackTeam/projects/posthog-integration/setup/[domain]/`
- Deployment Tracker: `/mnt/c/Users/andre/Desktop/Virtual ATeam/BlackTeam/projects/posthog-integration/POSTHOG_DEPLOYMENT_TRACKER.md`
- Domain Repos Map: `/tmp/domain_repos.json`
