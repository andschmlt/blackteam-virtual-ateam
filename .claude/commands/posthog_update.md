# /posthog_update - PostHog Configuration Update

Update existing PostHog configurations with new features, fixes, or enhancements for any domain.

## MANDATORY: Head of Product Assignment (Director Rule 8)
**Head of Product MUST be involved in ALL PostHog update work.**

When this command is invoked:
1. Head of Product is automatically assigned to the task
2. HoP reviews the update scope and impact
3. Update deliverables require HoP approval before deployment

See: `/mnt/c/Users/andre/Desktop/Virtual ATeam/BlackTeam/DIRECTOR_RULES.md` - Rule 8

---

## Usage

```
/posthog_update [domain] [update_type]    # Update specific domain
/posthog_update [domain]                  # General update (auto-detect type)
```

### Update Types
- `conversion` - Add/update conversion tracking
- `navboost` - Update NavBoost metrics
- `config` - Update PostHog configuration
- `fix` - Bug fixes or corrections

---

## Quick Reference - Key IDs (DO NOT MODIFY)

| Resource | ID | Purpose |
|----------|-----|---------|
| ClickUp List for Tasks | 901324589525 | All PostHog deployment tasks go here |
| ClickUp Workspace | 8553292 | Paradise Media workspace |
| Andre User ID | 60332880 | ClickUp assignee |
| Joshua User ID | 99970277 | ClickUp assignee |
| Malcolm User ID | 82173399 | ClickUp assignee |

---

## Workflow Overview

```
/posthog_update [domain] [type]
        │
        ▼
┌─────────────────────────────────────────┐
│ PHASE 1: Check Existing Task            │
│ - Search ClickUp for domain task        │
│ - Determine: sub-task or new task       │
└─────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────┐
│ PHASE 2: Generate Update Files          │
│ - Create/update tracking scripts        │
│ - Generate deployment instructions      │
│ - Save to setup directory               │
└─────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────┐
│ PHASE 3: ClickUp Task Management        │
│ IF task exists → Create sub-task        │
│ IF no task → Create "Update PostHog"    │
│ - Attach updated files                  │
│ - Assign to Joshua + Malcolm            │
└─────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────┐
│ PHASE 4: Notification & Summary         │
│ - Output task links                     │
│ - List files updated                    │
│ - Deployment instructions               │
└─────────────────────────────────────────┘
```

---

## Phase 1: Check Existing Task

### Search for Domain Task

```python
import requests

CLICKUP_API_KEY = "pk_60332880_BFGB37OGS3728SKRG41AB9EPIKK5O3GY"
LIST_ID = "901324589525"

def find_existing_task(domain):
    """Search for existing PostHog task for domain."""
    url = f"https://api.clickup.com/api/v2/list/{LIST_ID}/task"
    headers = {"Authorization": CLICKUP_API_KEY}

    response = requests.get(url, headers=headers)
    tasks = response.json().get("tasks", [])

    # Search for domain in task name
    for task in tasks:
        task_name = task.get("name", "").lower()
        if domain.lower() in task_name and "posthog" in task_name.lower():
            return {
                "id": task["id"],
                "name": task["name"],
                "status": task.get("status", {}).get("status"),
                "url": task.get("url")
            }

    return None
```

### Decision Logic

```python
existing_task = find_existing_task(domain)

if existing_task:
    # Task exists → Create sub-task
    action = "create_subtask"
    parent_id = existing_task["id"]
else:
    # No task → Create new "Update PostHog" task
    action = "create_new_task"
    parent_id = None
```

---

## Phase 2: Generate Update Files

### Directory Structure

```
/mnt/c/Users/andre/Desktop/Virtual ATeam/BlackTeam/projects/posthog-integration/
├── setup/[domain]/                    # Original setup files
│   ├── navboost-tracker.js
│   ├── posthog-functions.php
│   └── README.md
│
└── posthog-navboost-all-sites/[domain]/   # All versions including updates
    ├── navboost-tracker.js            # Latest NavBoost tracker
    ├── conversion-tracker.js          # Conversion tracking (if applicable)
    ├── posthog-full-tracking.php      # Complete WordPress integration
    ├── DEPLOYMENT_GUIDE.md            # Deployment instructions
    └── RELEASE_NOTES.md               # Version history
```

### Update File Templates

For conversion tracking updates, include:
1. `conversion-tracker.js` - New conversion events
2. `posthog-full-tracking.php` - Updated WordPress integration
3. `DEPLOYMENT_GUIDE.md` - Updated deployment instructions

---

## Phase 3: ClickUp Task Management

### Option A: Create Sub-Task (Task Exists)

```python
def create_update_subtask(parent_id, domain, update_type, description):
    """Create sub-task under existing parent task."""
    url = f"https://api.clickup.com/api/v2/list/{LIST_ID}/task"
    headers = {
        "Authorization": CLICKUP_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "name": f"Update: {update_type.title()} Tracking - {domain}",
        "description": description,
        "assignees": [JOSHUA_ID, MALCOLM_ID],
        "parent": parent_id,
        "status": "to do"
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()
```

### Option B: Create New Task (No Existing Task)

```python
def create_update_task(domain, update_type, description):
    """Create new Update PostHog task."""
    url = f"https://api.clickup.com/api/v2/list/{LIST_ID}/task"
    headers = {
        "Authorization": CLICKUP_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "name": f"Update PostHog - {domain}",
        "description": f"""Update of existing PostHog configuration for {domain}

## Update Type
{update_type.title()}

## Description
{description}

## Update Details
- This is an update to an existing PostHog configuration
- Review attached files for changes
- Follow DEPLOYMENT_GUIDE.md for installation

## Files
See attachments for updated tracking scripts.
""",
        "assignees": [JOSHUA_ID, MALCOLM_ID],
        "status": "to do"
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()
```

### Add Attachments

```python
def add_attachment(task_id, file_path, filename):
    """Add file attachment to task."""
    url = f"https://api.clickup.com/api/v2/task/{task_id}/attachment"
    headers = {"Authorization": CLICKUP_API_KEY}

    with open(file_path, 'rb') as f:
        files = {'attachment': (filename, f, 'text/plain')}
        response = requests.post(url, headers=headers, files=files)

    return response.status_code == 200
```

---

## Phase 4: Notification & Summary

### Output Format

```
## PostHog Update Complete

### Domain: [domain.com]
### Update Type: [type]

### Task Action:
- [Created sub-task under existing parent / Created new Update PostHog task]
- Task ID: [id]
- Task URL: [url]

### Files Updated:
| File | Description |
|------|-------------|
| conversion-tracker.js | 5 conversion types |
| posthog-full-tracking.php | WordPress integration |
| DEPLOYMENT_GUIDE.md | Installation instructions |

### Deployment Steps:
1. Download attached files from ClickUp task
2. Follow DEPLOYMENT_GUIDE.md
3. Verify events in PostHog dashboard

### ClickUp Task:
https://app.clickup.com/t/[task_id]
```

---

## Complete Implementation

```python
#!/usr/bin/env python3
"""
PostHog Update Command Implementation
/posthog_update [domain] [update_type]
"""

import requests
import os
import time

# Configuration
CLICKUP_API_KEY = "pk_60332880_BFGB37OGS3728SKRG41AB9EPIKK5O3GY"
LIST_ID = "901324589525"
ANDRE_ID = 60332880
JOSHUA_ID = 99970277
MALCOLM_ID = 82173399

HEADERS = {
    "Authorization": CLICKUP_API_KEY,
    "Content-Type": "application/json"
}

SETUP_DIR = "/mnt/c/Users/andre/Desktop/Virtual ATeam/BlackTeam/projects/posthog-integration/posthog-navboost-all-sites"


def find_existing_task(domain):
    """Search for existing PostHog task for domain."""
    url = f"https://api.clickup.com/api/v2/list/{LIST_ID}/task"
    headers = {"Authorization": CLICKUP_API_KEY}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None

    tasks = response.json().get("tasks", [])

    for task in tasks:
        task_name = task.get("name", "").lower()
        if domain.lower() in task_name and "posthog" in task_name.lower():
            return {
                "id": task["id"],
                "name": task["name"],
                "status": task.get("status", {}).get("status"),
                "url": task.get("url")
            }

    return None


def create_subtask(parent_id, domain, update_type, description):
    """Create sub-task under existing parent task."""
    url = f"https://api.clickup.com/api/v2/list/{LIST_ID}/task"

    payload = {
        "name": f"Update: {update_type.title()} Tracking - {domain}",
        "description": description,
        "assignees": [JOSHUA_ID, MALCOLM_ID],
        "parent": parent_id,
        "status": "to do"
    }

    response = requests.post(url, headers=HEADERS, json=payload)
    return response.json() if response.status_code == 200 else None


def create_new_task(domain, update_type, description):
    """Create new Update PostHog task."""
    url = f"https://api.clickup.com/api/v2/list/{LIST_ID}/task"

    full_desc = f"""Update of existing PostHog configuration for {domain}

## Update Type
{update_type.title()}

## Description
{description}

## Update Details
- This is an update to an existing PostHog configuration
- Review attached files for changes
- Follow DEPLOYMENT_GUIDE.md for installation

## Files
See attachments for updated tracking scripts.
"""

    payload = {
        "name": f"Update PostHog - {domain}",
        "description": full_desc,
        "assignees": [JOSHUA_ID, MALCOLM_ID],
        "status": "to do"
    }

    response = requests.post(url, headers=HEADERS, json=payload)
    return response.json() if response.status_code == 200 else None


def add_attachment(task_id, file_path, filename):
    """Add file attachment to task."""
    url = f"https://api.clickup.com/api/v2/task/{task_id}/attachment"
    headers = {"Authorization": CLICKUP_API_KEY}

    if not os.path.exists(file_path):
        return False

    with open(file_path, 'rb') as f:
        files = {'attachment': (filename, f, 'application/octet-stream')}
        response = requests.post(url, headers=headers, files=files)

    return response.status_code == 200


def posthog_update(domain, update_type="conversion"):
    """Main update function."""

    # Phase 1: Check existing task
    existing_task = find_existing_task(domain)

    # Phase 2: Prepare description
    description = f"""PostHog Update for {domain}

## Update Type: {update_type.title()}

## Changes Included:
- Enhanced conversion tracking
- Updated deployment guide
- WordPress integration file

## Deployment Instructions:
1. Download attached files
2. Follow DEPLOYMENT_GUIDE.md for step-by-step installation
3. Verify events in PostHog Live Events dashboard
4. Confirm conversion events are firing

## Files Attached:
- conversion-tracker.js - Enhanced conversion tracking (5 types)
- posthog-full-tracking.php - Complete WordPress integration
- DEPLOYMENT_GUIDE.md - Detailed deployment instructions
"""

    # Phase 3: Create task or subtask
    if existing_task:
        print(f"Found existing task: {existing_task['name']}")
        task = create_subtask(existing_task["id"], domain, update_type, description)
        action = "Created sub-task"
        parent_url = existing_task.get("url", "")
    else:
        print(f"No existing task found. Creating new Update PostHog task.")
        task = create_new_task(domain, update_type, description)
        action = "Created new task"
        parent_url = ""

    if not task:
        print("Failed to create task")
        return None

    task_id = task["id"]

    # Phase 4: Add attachments
    domain_dir = os.path.join(SETUP_DIR, domain)
    files_to_attach = [
        ("conversion-tracker.js", "conversion-tracker.js"),
        ("posthog-full-tracking.php", "posthog-full-tracking.php"),
        ("DEPLOYMENT_GUIDE.md", "DEPLOYMENT_GUIDE.md"),
        ("navboost-tracker.js", "navboost-tracker.js"),
    ]

    attached = []
    for filename, display_name in files_to_attach:
        file_path = os.path.join(domain_dir, filename)
        if os.path.exists(file_path):
            if add_attachment(task_id, file_path, display_name):
                attached.append(display_name)
                time.sleep(0.3)  # Rate limiting

    return {
        "domain": domain,
        "task_id": task_id,
        "task_name": task.get("name"),
        "action": action,
        "parent_url": parent_url,
        "files_attached": attached
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python posthog_update.py [domain] [update_type]")
        sys.exit(1)

    domain = sys.argv[1]
    update_type = sys.argv[2] if len(sys.argv) > 2 else "conversion"

    result = posthog_update(domain, update_type)

    if result:
        print(f"\n## PostHog Update Complete\n")
        print(f"### Domain: {result['domain']}")
        print(f"### Action: {result['action']}")
        print(f"### Task: {result['task_name']}")
        print(f"### Task ID: {result['task_id']}")
        print(f"### Files Attached: {', '.join(result['files_attached'])}")
        print(f"\n### ClickUp Task: https://app.clickup.com/t/{result['task_id']}")
```

---

## Related Commands

- `/posthog_setup` - Initial PostHog setup for new domains
- `/posthog_analysis` - Generate analytics reports
- `/blackteam` - Full project execution with Director

---

## Files

- API Keys: `/home/andre/.keys/.env`
- ClickUp Config: `/home/andre/.claude/clickup_config.json`
- Setup Files: `/mnt/c/Users/andre/Desktop/Virtual ATeam/BlackTeam/projects/posthog-integration/posthog-navboost-all-sites/[domain]/`
