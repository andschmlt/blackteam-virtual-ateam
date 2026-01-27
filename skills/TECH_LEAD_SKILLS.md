# Tech Lead - Skills Inventory

**Persona:** Tech Lead
**Role:** Technical Lead - DevOps, Infrastructure, Access Management
**Last Updated:** 2026-01-26

---

## Core Competencies

### GitHub Administration
- Repository access management via `gh` CLI
- Collaborator invitation workflows
- Permission level configuration (read, write, admin)
- GitHub API usage for automation

### DevOps & Tooling
- CLI command design and implementation
- Automation script creation
- Access control workflows
- Session history analysis and auditing

### Infrastructure Management
- Repository organization
- Team access patterns
- Permission auditing

### Technical Stack

| Technology | Level | Application |
|------------|-------|-------------|
| Python 3.x | Advanced | Automation scripts, CLI tools, API integrations |
| Bash/Shell | Expert | DevOps scripts, CI/CD pipelines |
| Git/GitHub | Expert | Version control, workflows, actions |
| GitHub Actions | Advanced | CI/CD pipelines, automation |
| Terraform | Intermediate | Infrastructure as Code |
| Docker | Advanced | Containerization, local development |
| GCP | Advanced | Cloud infrastructure, IAM, Secret Manager |
| AWS | Intermediate | S3, IAM, basic services |

---

## Coding Standards & Best Practices

### Python Standards (Automation Scripts)

**PEP 8 Compliance:**
| Rule | Standard | Example |
|------|----------|---------|
| Indentation | 4 spaces, no tabs | All Python files |
| Line length | ≤120 characters | Paradise Media standard |
| Naming | snake_case for functions/variables | `get_user_access()` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRIES = 3` |
| Classes | PascalCase | `GitHubClient` |

**Import Organization:**
```python
# 1. Standard library
import os
import sys
import json
from pathlib import Path

# 2. Third-party
import requests
from github import Github

# 3. Local application
from utils.config import load_config
```

**Type Annotations (Required for all functions):**
```python
from typing import Optional, List, Dict

def add_collaborator(
    repo: str,
    username: str,
    permission: str = "push"
) -> bool:
    """Add collaborator to GitHub repository."""
    ...
```

**Error Handling Pattern:**
```python
# GOOD: Specific, contextual, actionable
try:
    response = gh_api.add_collaborator(repo, user)
except GithubException as e:
    if e.status == 404:
        logger.error(f"Repository not found: {repo}")
        raise RepoNotFoundError(repo) from e
    elif e.status == 403:
        logger.error(f"Permission denied for {repo}")
        raise PermissionError(f"No admin access to {repo}") from e
    raise

# BAD: Silent failure
try:
    response = gh_api.add_collaborator(repo, user)
except:
    pass  # Never do this!
```

### Shell/Bash Standards

**Script Header (Required):**
```bash
#!/bin/bash
# Script: deploy.sh
# Purpose: Deploy application to production
# Author: Tech Lead
# Last Updated: 2026-01-26
#
# Usage: ./deploy.sh <environment> [--dry-run]
#
# Dependencies:
#   - gcloud CLI authenticated
#   - kubectl configured
#   - jq installed

set -euo pipefail  # Exit on error, undefined vars, pipe failures
```

**Variable Naming:**
| Type | Convention | Example |
|------|------------|---------|
| Local variables | lowercase_snake | `local file_path="/tmp/data"` |
| Environment variables | UPPER_SNAKE | `export API_KEY="xxx"` |
| Constants | UPPER_SNAKE | `readonly MAX_RETRIES=3` |
| Function names | lowercase_snake | `validate_input()` |

**Best Practices:**
```bash
# GOOD: Quote variables to prevent word splitting
cp "$source_file" "$dest_dir/"

# BAD: Unquoted variables
cp $source_file $dest_dir/

# GOOD: Use [[ ]] for conditionals
if [[ -f "$config_file" ]]; then
    source "$config_file"
fi

# GOOD: Use arrays for multiple items
declare -a domains=("site1.com" "site2.com" "site3.com")
for domain in "${domains[@]}"; do
    echo "Processing: $domain"
done

# GOOD: Use functions for reusable logic
log_info() {
    echo "[INFO] $(date '+%Y-%m-%d %H:%M:%S') $*"
}

log_error() {
    echo "[ERROR] $(date '+%Y-%m-%d %H:%M:%S') $*" >&2
}
```

**Error Handling:**
```bash
# Trap for cleanup on exit
cleanup() {
    rm -f "$temp_file"
    log_info "Cleanup complete"
}
trap cleanup EXIT

# Check command success
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" > /dev/null 2>&1; then
    log_error "Not authenticated to GCP"
    exit 1
fi
```

### Git Workflow Standards

**Branch Naming:**
| Type | Pattern | Example |
|------|---------|---------|
| Feature | `feature/<ticket>-<description>` | `feature/BT-123-add-posthog` |
| Bugfix | `fix/<ticket>-<description>` | `fix/BT-456-null-handling` |
| Hotfix | `hotfix/<ticket>-<description>` | `hotfix/BT-789-prod-crash` |
| Release | `release/v<version>` | `release/v1.2.0` |

**Commit Message Format:**
```
<type>(<scope>): <subject>

<body>

<footer>

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Commit Types:**
| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Code restructuring |
| `test` | Adding/updating tests |
| `chore` | Maintenance tasks |
| `ci` | CI/CD changes |

**Protected Branch Rules:**
- `main`: Require PR, 1+ approval, passing CI, no force push
- `develop`: Require PR, passing CI
- Feature branches: No restrictions

**Git Safety Rules (HARD RULES):**
| Rule | Severity |
|------|----------|
| Never `git push --force` to main/master | BLOCKING |
| Never commit credentials/secrets | BLOCKING |
| Never skip pre-commit hooks (--no-verify) | BLOCKING |
| Always create PR for main branch changes | BLOCKING |
| Never use `git reset --hard` on shared branches | BLOCKING |

### CI/CD Pipeline Standards

**GitHub Actions Structure:**
```yaml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  PYTHON_VERSION: '3.11'

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      - name: Install dependencies
        run: pip install flake8 black isort mypy
      - name: Run linters
        run: |
          flake8 --max-line-length=120 src/
          black --check --line-length 120 src/
          isort --check --profile black src/

  test:
    needs: lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: pytest --cov=src --cov-report=xml

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Security scan
        run: |
          pip install bandit
          bandit -r src/ -ll
```

**Pipeline Requirements:**
| Stage | Tools | Failure Action |
|-------|-------|----------------|
| Lint | flake8, black, isort | Block merge |
| Type Check | mypy | Warn (log issue) |
| Security | bandit, gitleaks | Block merge |
| Test | pytest | Block merge |
| Build | docker build | Block merge |

### Security Standards

**Credential Management:**
| Do | Don't |
|----|-------|
| Use Secret Manager (GCP/AWS) | Hardcode in code |
| Use environment variables | Commit to git |
| Use `.env.example` templates | Share `.env` files |
| Rotate keys regularly | Use same key everywhere |

**Secret Detection (Pre-commit):**
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks
```

**Patterns to Block:**
```regex
# API Keys
(?i)(api[_-]?key|apikey)['\"]?\s*[:=]\s*['\"]?[a-zA-Z0-9]{20,}

# AWS Keys
AKIA[0-9A-Z]{16}

# GCP Service Account
"type"\s*:\s*"service_account"

# Generic Secrets
(?i)(password|secret|token)['\"]?\s*[:=]\s*['\"]?[^\s'"]{8,}
```

### Infrastructure as Code Standards

**Terraform Naming:**
```hcl
# Resources: <provider>_<resource>_<name>
resource "google_storage_bucket" "data_lake_bronze" {
  name     = "${var.project}-bronze-${var.environment}"
  location = var.region
}

# Variables: descriptive, snake_case
variable "environment" {
  description = "Deployment environment (dev, staging, prod)"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}
```

**Terraform Best Practices:**
| Rule | Rationale |
|------|-----------|
| Use remote state (GCS/S3) | Team collaboration, locking |
| Separate environments | Prevent accidental prod changes |
| Use modules for reuse | DRY principle |
| Tag all resources | Cost tracking, ownership |
| Use `terraform fmt` | Consistent formatting |
| Use `terraform validate` | Catch errors early |

### Docker Standards

**Dockerfile Best Practices:**
```dockerfile
# Use specific version, not :latest
FROM python:3.11-slim

# Set labels for metadata
LABEL maintainer="tech-lead@paradisemedia.com"
LABEL version="1.0.0"

# Set working directory
WORKDIR /app

# Copy requirements first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/

# Use non-root user
RUN useradd --create-home appuser
USER appuser

# Set entrypoint
ENTRYPOINT ["python", "-m", "src.main"]
```

**Docker Rules:**
| Rule | Severity |
|------|----------|
| Never use `:latest` tag | WARNING |
| Always use non-root user | BLOCKING |
| Use multi-stage builds for production | SUGGESTION |
| Use `.dockerignore` | WARNING |
| Pin dependency versions | WARNING |

---

## Code Quality Tools

### Required Tools

| Tool | Purpose | Command |
|------|---------|---------|
| **flake8** | Python linting | `flake8 --max-line-length=120` |
| **black** | Python formatting | `black --line-length 120` |
| **isort** | Import sorting | `isort --profile black` |
| **mypy** | Type checking | `mypy --strict` |
| **bandit** | Security scanning | `bandit -r src/` |
| **gitleaks** | Secret detection | `gitleaks detect` |
| **shellcheck** | Bash linting | `shellcheck script.sh` |
| **hadolint** | Dockerfile linting | `hadolint Dockerfile` |
| **tflint** | Terraform linting | `tflint` |

### Pre-commit Configuration

```yaml
# .pre-commit-config.yaml
repos:
  # Python
  - repo: https://github.com/psf/black
    rev: 24.1.0
    hooks:
      - id: black
        args: ['--line-length=120']
  - repo: https://github.com/pycqa/isort
    rev: 5.13.0
    hooks:
      - id: isort
        args: ['--profile=black']
  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        args: ['--max-line-length=120']

  # Security
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.7
    hooks:
      - id: bandit
        args: ['-r', 'src/']
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks

  # Shell
  - repo: https://github.com/koalaman/shellcheck-precommit
    rev: v0.9.0
    hooks:
      - id: shellcheck

  # Docker
  - repo: https://github.com/hadolint/hadolint
    rev: v2.12.0
    hooks:
      - id: hadolint

  # General
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-merge-conflict
      - id: detect-private-key
```

---

## Skills Demonstrated

### 2026-01-15 - GitHub Access Management
- **Skill:** `gh api` for programmatic collaborator management
- **Command:** `gh api repos/{owner}/{repo}/collaborators/{username} -X PUT -f permission=push`
- **Context:** Adding team members to repositories efficiently
- **Reusable:** Yes - standardized in `/githubaccess` command

### 2026-01-15 - Session History Analysis
- **Skill:** Grep-based history mining from Claude session logs
- **Pattern:** Search `.claude/history.jsonl` for command usage patterns
- **Use Case:** Auditing who was given access to which repositories
- **Reusable:** Yes - applicable for any command usage audit

### 2026-01-15 - Docsify Static Site Path Resolution
- **Skill:** Debugging and fixing path resolution in Docsify static sites
- **Pattern:** Calculate relative path prefix based on file depth in directory tree
- **Use Case:** Fixing broken images/links when markdown files are in nested folders
- **Code Pattern:**
  ```python
  depth = len(filepath.relative_to(base).parts) - 1
  prefix = "../" * depth if depth > 0 else "./"
  ```
- **Key Insight:** Docsify resolves paths relative to current page location, not document root
- **Reusable:** Yes - applicable to any Docsify or similar static site generator

### 2026-01-15 - Server Log Analysis for Path Debugging
- **Skill:** Using Python http.server access logs to diagnose browser path resolution
- **Pattern:** Watch server logs for actual GET requests to identify path issues
- **Use Case:** When QA tests pass but browser shows broken images
- **Example Log:** `GET /world-cups/images/worldcups/wc_1966.svg HTTP/1.1" 404` reveals path prepending
- **Reusable:** Yes - server logs are ground truth for any path/routing issues

### 2026-01-15 - Ralph Loop QA Methodology
- **Skill:** 3-iteration validation ensuring consistency across test runs
- **Pattern:** Run each test 3 times (Ralph 1, 2, 3), only pass if all 3 succeed
- **Use Case:** Validating all pages, images, and links in a static site
- **Final Results:** 855 checks × 3 loops = comprehensive validation
- **Reusable:** Yes - applicable to any QA process requiring high confidence

### 2026-01-21 - PostHog Update Command Design
- **Skill:** Multi-phase CLI command design with workflow automation
- **Pattern:** 5-phase workflow (Check Task → Generate Files → ClickUp → Git → Summary)
- **Use Case:** Standardized PostHog configuration updates across domains
- **Reusable:** Yes - `/posthog_update` command for any domain

### 2026-01-21 - ClickUp Sub-Task Creation via API
- **Skill:** Creating child tasks linked to existing parent tasks
- **Command:** POST to `/api/v2/list/{list_id}/task` with `parent` field
- **Context:** Enables hierarchical task organization for updates
- **Reusable:** Yes - pattern applicable to any ClickUp sub-task workflow

### 2026-01-21 - Project-Wide CHANGELOG Management
- **Skill:** Centralized changelog for multi-domain projects
- **Pattern:** Domain Status Summary table + per-domain version history + Commit Log table
- **Use Case:** Tracking PostHog configuration versions across 28+ domains
- **Reusable:** Yes - CHANGELOG.md structure reusable for any multi-project setup

### 2026-01-22 - Hard Rule Implementation in Workflow Commands
- **Skill:** Adding safety rules to workflow automation commands
- **Pattern:** "HARD RULE" section at top of command file with explicit prohibitions
- **Use Case:** Preventing automated `git push` to production repositories
- **Implementation:**
  ```markdown
  ## HARD RULE: No Remote Push
  **NEVER commit or push to main/remote repositories.**
  - Save files locally only
  - Commit to local repository only (no `git push`)
  ```
- **Reusable:** Yes - pattern applicable to any command needing safety guardrails

### 2026-01-22 - Assignee Management in Workflow Commands
- **Skill:** Updating ClickUp assignee configuration across workflow files
- **Pattern:** Search and replace assignee IDs/names in command files
- **Use Case:** Changing task assignment from Joshua+Malcolm to Malcolm only
- **Tools:** `replace_all` edit parameter for bulk replacements
- **Reusable:** Yes - pattern for any assignee/config changes across multiple files

### 2026-01-26 - BlackTeam Dashboard v1.1 Release (Full-Stack Application)
- **Skill:** Full-stack dashboard deployment with FastAPI + React
- **Stack:**
  - Backend: FastAPI, uvicorn, WebSocket, Python 3.11+
  - Frontend: React 18, Vite, TailwindCSS, Zustand
  - Real-time: WebSocket for live activity updates
- **Components Built:**
  - `/api/persona-prompts` - REST endpoint for Role Lock Prompts & Character Sheets
  - `prompts_parser.py` - Service to parse 31 persona prompt files
  - `GovernanceDrawer.tsx` - 8-tab drawer with copy-to-clipboard functionality
- **Deployment Pattern:**
  ```bash
  # Backend (port 8000)
  cd backend && python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
  # Frontend (port 5173/5175)
  cd frontend && npm run dev
  ```
- **Git Workflow:**
  - Initialized repo with `.gitignore` (excludes __pycache__, node_modules, .env)
  - 2 commits: feature commit → full project commit
- **Result:** Dashboard accessible at http://localhost:5175 with Governance → Prompts tab
- **Reusable:** Yes - FastAPI + React + TailwindCSS template for internal tools
