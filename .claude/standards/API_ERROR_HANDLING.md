# API Error Handling Standards

**Version:** 1.0
**Updated:** 2026-02-03
**Purpose:** Define error handling procedures for all external API integrations

---

## General Principles

1. **Fail gracefully** - Never crash, always provide useful feedback
2. **Log everything** - All errors must be logged for debugging
3. **Retry intelligently** - Use exponential backoff, not infinite loops
4. **Inform the user** - Don't silently swallow errors

---

## Standard Error Response Format

When an API error occurs, report it consistently:

```markdown
## API Error Occurred

**Service:** [Service Name]
**Endpoint:** [Endpoint/Operation]
**Error Type:** [Timeout/Auth/Rate Limit/Server Error/etc.]
**Error Code:** [HTTP status or error code]
**Message:** [Error message]

### Impact
[What this means for the current task]

### Fallback Action
[What alternative action is being taken]

### User Options
1. [Option 1 - e.g., retry later]
2. [Option 2 - e.g., use cached data]
3. [Option 3 - e.g., skip this step]
```

---

## Service-Specific Handling

### MCP Server (localhost:8000)

**Health Check:**
```bash
curl -s http://localhost:8000/health
```

| Error | Cause | Action |
|-------|-------|--------|
| Connection refused | Server not running | Log activities locally, notify user |
| Timeout | Server overloaded | Retry once after 5s, then proceed without logging |
| 500 error | Server error | Log locally, continue execution |

**Fallback:** If MCP server unavailable, logging is NON-BLOCKING. Continue execution and log to local file instead.

```markdown
**MCP Server Unavailable**
- Logging redirected to: ~/.claude/logs/fallback_YYYY-MM-DD.log
- Execution continues normally
- Sync to MCP when server returns
```

---

### ClickUp API

**Health Check:**
```python
# Test with a simple list query
mcp__claude_ai_ClickUp__clickup_get_lists(folder_id="known_folder")
```

| Error | Cause | Action |
|-------|-------|--------|
| 401 Unauthorized | Invalid API key | Stop, request new key from user |
| 429 Rate Limited | Too many requests | Wait 60s, retry with backoff |
| 500/502/503 | ClickUp down | Retry 3x with backoff, then skip ClickUp updates |
| Timeout | Network issue | Retry once, then proceed without ClickUp |

**Fallback:** If ClickUp unavailable for task updates:
```markdown
**ClickUp Update Deferred**
- Task ID: [ID]
- Intended Update: [Description]
- Stored for retry at: ~/.claude/pending_clickup_updates.json
- Manual update may be required
```

---

### PostHog API

**Health Check:**
```bash
curl -s "https://app.posthog.com/api/projects/?personal_api_key=$POSTHOG_KEY"
```

| Error | Cause | Action |
|-------|-------|--------|
| 401 Unauthorized | Invalid key | Stop PostHog operations, notify user |
| 429 Rate Limited | Quota exceeded | Wait, use cached data if available |
| Timeout | Network/server | Retry 2x, then report partial results |

**Fallback:** Use cached data when available:
```markdown
**PostHog API Unavailable**
- Using cached data from: [timestamp]
- Data may be up to [X hours] old
- For real-time data, retry when API available
```

---

### BigQuery

**Health Check:**
```python
from google.cloud import bigquery
client = bigquery.Client()
client.query("SELECT 1").result()
```

| Error | Cause | Action |
|-------|-------|--------|
| Auth error | SA key invalid | Stop, check credentials path |
| Quota exceeded | Too many queries | Wait 60s, batch queries |
| Timeout | Query too complex | Simplify query, add LIMIT |
| 404 Table not found | Wrong table name | Check schema, report to user |

**Fallback:**
```markdown
**BigQuery Error**
- Query: [simplified query description]
- Error: [error type]
- Attempting: [fallback action]
- If issue persists, manual query may be required
```

---

### Slack (MCP Tool)

| Error | Cause | Action |
|-------|-------|--------|
| Auth error | Token expired | Notify user to re-auth |
| Channel not found | Wrong channel ID | List channels, ask user to select |
| Rate limited | Too many messages | Queue messages, send with delay |

**Fallback:**
```markdown
**Slack Notification Deferred**
- Intended message saved
- Will retry on next opportunity
- Alternative: Email notification available
```

---

## Retry Logic Standards

### Exponential Backoff

```
Attempt 1: Immediate
Attempt 2: Wait 1 second
Attempt 3: Wait 2 seconds
Attempt 4: Wait 4 seconds
(Max 3 retries for most services)
```

### Retry Decision Matrix

| Error Type | Retry? | Max Attempts | Backoff |
|------------|--------|--------------|---------|
| Timeout | Yes | 3 | Exponential |
| 429 Rate Limit | Yes | 3 | Fixed 60s |
| 500 Server Error | Yes | 2 | Exponential |
| 401 Auth Error | No | 0 | N/A |
| 404 Not Found | No | 0 | N/A |
| 400 Bad Request | No | 0 | N/A |

---

## Error Logging Format

All errors should be logged with:

```json
{
  "timestamp": "2026-02-03T10:30:00Z",
  "service": "ClickUp",
  "operation": "create_task",
  "error_type": "rate_limit",
  "error_code": 429,
  "error_message": "Rate limit exceeded",
  "retry_count": 2,
  "fallback_action": "deferred_update",
  "context": {
    "task_name": "Example task",
    "list_id": "12345"
  }
}
```

---

## User Communication Templates

### Temporary Error (Will Retry)
```
Encountered a temporary issue with [Service]. Retrying...
```

### Persistent Error (Fallback Active)
```
[Service] is currently unavailable. Using fallback: [description].
Your work will continue without interruption.
```

### Blocking Error (User Action Required)
```
Cannot proceed without [Service]. Error: [brief description]
Please:
1. [Action 1]
2. [Action 2]
```

---

## Service Dependencies

| Service | Critical? | Fallback Available? |
|---------|-----------|---------------------|
| MCP Server | No | Yes (local logging) |
| ClickUp | No | Yes (deferred updates) |
| PostHog | No | Yes (cached data) |
| BigQuery | Yes* | Partial (cached results) |
| Slack | No | Yes (email alternative) |
| Email (SMTP) | No | Yes (local save) |

*BigQuery is critical for data queries but non-critical for other operations.

---

## Pre-Execution Health Checks

Before starting work that depends on external services:

```markdown
## SERVICE HEALTH CHECK

| Service | Status | Action |
|---------|--------|--------|
| MCP Server | [OK/DOWN] | [Continue/Use fallback] |
| ClickUp | [OK/DOWN] | [Continue/Defer updates] |
| BigQuery | [OK/DOWN] | [Continue/Report limitation] |
```

Only perform health checks when the service will actually be used.

---

## Related Files

- **VALIDATION_STANDARDS.md** - Data validation requirements
- **PATH_MAPPINGS.md** - Credential locations
- **TEAM_CONFIG.md** - Integration points

