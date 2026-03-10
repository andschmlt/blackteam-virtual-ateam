# R-SEC-05: Incident Response Playbook

**Priority:** P1 High
**Owner:** W-GARD (Guardian) + B-BOB (Director)
**Created:** 2026-03-03
**Status:** ACTIVE

---

## Purpose

Define procedures for detecting, containing, and recovering from security incidents. Ensures consistent, fast, and documented response to any security event.

## Severity Classification

| Severity | Definition | Response Time | Examples |
|---|---|---|---|
| **CRITICAL** | Active exploit, data breach, credential leak in public | < 15 min | Hardcoded API key pushed to public repo, database exposed |
| **HIGH** | Vulnerability found, unauthorized access detected | < 1 hour | Cloud Run IAM misconfigured, API key 401 errors |
| **MEDIUM** | Policy violation, expired credentials, anomaly | < 4 hours | Key > 90 days old, unusual API usage pattern |
| **LOW** | Best practice gap, documentation issue | < 24 hours | Missing CORS headers, weak error handling |

## Phase 1: Detection

### Automated Detection
```bash
# 1. Secret exposure scan (run before every git push)
grep -rn 'phx_\|phc_\|pk_\|sk-\|ntn_\|AIzaSy\|xoxb-\|ghp_\|ghs_' .

# 2. Cloud Run log monitoring (check for auth failures)
gcloud logging read "resource.type=cloud_run_job AND severity>=WARNING" \
  --limit=50 --project=paradisemedia-bi

# 3. API key health check
python3 -c "
import os, urllib.request
key = os.environ.get('POSTHOG_PERSONAL_API_KEY', '')
if key:
    req = urllib.request.Request('https://app.posthog.com/api/projects/',
        headers={'Authorization': f'Bearer {key}'})
    try:
        urllib.request.urlopen(req, timeout=10)
        print('PostHog key: VALID')
    except Exception as e:
        print(f'PostHog key: INVALID — {e}')
"
```

### Manual Detection Triggers
- User reports unexpected behavior
- Cloud Run job fails with auth errors
- GitHub security alert notification
- Unusual billing spike on GCP

## Phase 2: Containment

### CRITICAL — Credential Leak
```bash
# 1. Immediately revoke the exposed key
# GitHub: Settings > Developer settings > Personal access tokens > Revoke
# PostHog: Project settings > API keys > Delete
# Anthropic: Console > API keys > Delete

# 2. Rotate to new key
# Generate new key at provider
# Update Secret Manager
gcloud secrets versions add SECRET_NAME --data-file=-

# 3. Redeploy affected services
gcloud run jobs update JOB_NAME --region=REGION \
  --set-secrets="ENV_VAR=SECRET_NAME:latest"

# 4. Check git history for exposure
git log --all --oneline -20
# If key was committed, force-push to remove (after user approval)
```

### HIGH — Unauthorized Access
```bash
# 1. Check IAM bindings
gcloud run services get-iam-policy SERVICE --region=REGION

# 2. Remove unauthorized bindings
gcloud run services remove-iam-policy-binding SERVICE \
  --member="UNAUTHORIZED_MEMBER" --role="ROLE" --region=REGION

# 3. Check access logs
gcloud logging read "resource.type=cloud_run_revision AND httpRequest.status>=400" \
  --limit=100 --project=paradisemedia-bi
```

## Phase 3: Recovery

1. **Verify containment** — confirm compromised credential no longer works
2. **Deploy new credentials** — rotate all potentially affected keys
3. **Test services** — run dry-run on all affected Cloud Run jobs
4. **Monitor** — watch logs for 24 hours for continued suspicious activity

## Phase 4: Post-Incident

### Incident Report Template
```markdown
## Incident Report: [TITLE]

**Date:** [DATE]
**Severity:** [CRITICAL/HIGH/MEDIUM/LOW]
**Reported By:** [PERSONA/USER]
**Time to Detect:** [DURATION]
**Time to Contain:** [DURATION]
**Time to Resolve:** [DURATION]

### What Happened
[Description of the incident]

### Root Cause
[Why it happened]

### Impact
- Services affected: [LIST]
- Data exposed: [SCOPE]
- Duration of exposure: [TIME]

### Actions Taken
1. [Action 1]
2. [Action 2]

### Prevention
- [ ] Rule added/updated: [RULE ID]
- [ ] Automation added: [DESCRIPTION]
- [ ] Training conducted: [TOPIC]

### Lessons Learned
[Key takeaways for the team]
```

### Save to Learnings
```bash
# After every incident, capture to RAG
# File: ~/AS-Virtual_Team_System_v2/whiteteam/skills/learnings/YYYY-MM-DD_incident_TITLE.md
```

## Known Incident History

| Date | Severity | Incident | Resolution | Rule Created |
|---|---|---|---|---|
| 2026-02-06 | HIGH | 9 files with hardcoded API keys | Moved to ~/.keys/.env | R-SEC-01 |
| 2026-02-06 | CRITICAL | SQL injection in 7 handlers | Parameterized queries | R-SEC-02 |
| 2026-02-08 | MEDIUM | Cloud Run IAM overly permissive | Restricted to domain | R-DEPLOY-01 |
| 2026-02-11 | HIGH | 4 blind deploys without debugging | Local test mandate | R-DEBUG-01 |
| 2026-02-06 | MEDIUM | PostHog API key returning 401 | Key regenerated | API_ERROR_HANDLING |

## Escalation Path

```
Persona Detects Issue
        ↓
W-GARD (Guardian) — Assess severity
        ↓
CRITICAL/HIGH → B-BOB + W-WOL immediately
        ↓
MEDIUM → Next standup / async notification
        ↓
LOW → Document and queue for next session
```

---

*R-SEC-05 | Virtual ATeam Security Standards | Paradise Media Group*
