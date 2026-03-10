# R-SEC-06: Secrets Rotation Schedule

**Priority:** P1 High
**Owner:** W-GARD (Guardian)
**Created:** 2026-03-03
**Status:** ACTIVE

---

## Purpose

Define rotation cadence, ownership, and procedures for all API keys, tokens, and credentials used across the workspace. Prevents stale credentials and limits blast radius of any single key compromise.

## Active Credentials Inventory

| Credential | Provider | Location | Rotation | Owner | Used By |
|---|---|---|---|---|---|
| `GITHUB_TOKEN` | GitHub PAT | Secret Manager `github-token` | 90 days | Andre | news_updater, editorial_generator, git push |
| `ANTHROPIC_API_KEY` | Anthropic Console | Secret Manager `anthropic-api-key` | 180 days | Andre | editorial_generator, /content_palm |
| `POSTHOG_PERSONAL_API_KEY` | PostHog | `~/.keys/.env` | 180 days | Andre | PostHog reports, /posthog_analysis |
| `POSTHOG_PROJECT_API_KEY` | PostHog | Client-side (public) | 365 days | Andre | conversion-tracker.js (R-SEC-01 exception) |
| `CLICKUP_API_KEY` | ClickUp | `~/.keys/.env` | 180 days | Andre | /tasks_ROI, task creation scripts |
| `GOOGLE_APPLICATION_CREDENTIALS` | GCP Service Account | `~/.keys/service-account.json` | 365 days | Andre | BigQuery, GCS, Cloud Run |
| `NOTION_API_KEY` | Notion Integration | `~/.keys/.env` | 180 days | Andre | MCP Notion server |
| `SLACK_BOT_TOKEN` | Slack App | `~/.keys/.env` | 365 days | Andre | MCP Slack server |

## Rotation Procedures

### GitHub Personal Access Token (90-day rotation)

```bash
# 1. Generate new token
# GitHub.com > Settings > Developer settings > Personal access tokens > Fine-grained tokens
# Scopes: repo (contents, metadata), workflow

# 2. Update Secret Manager
echo -n "ghp_NEW_TOKEN_HERE" | gcloud secrets versions add github-token --data-file=- --project=paradisemedia-bi

# 3. Update local dev environment
# Edit ~/.keys/.env — update GITHUB_TOKEN=ghp_NEW_TOKEN_HERE

# 4. Verify Cloud Run jobs can still push
gcloud run jobs execute news-updater-australiafootball --region=us-central1
# Check logs for successful git push

# 5. Revoke old token
# GitHub.com > Settings > Developer settings > Delete old token

# 6. Log rotation
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) GITHUB_TOKEN rotated" >> ~/.keys/rotation.log
```

### Anthropic API Key (180-day rotation)

```bash
# 1. Generate new key at console.anthropic.com > API Keys
# 2. Update Secret Manager
echo -n "sk-ant-NEW_KEY" | gcloud secrets versions add anthropic-api-key --data-file=- --project=paradisemedia-bi
# 3. Update ~/.keys/.env
# 4. Test: EDITORIAL_DRY_RUN=true python3 scripts/editorial_generator.py
# 5. Revoke old key at Anthropic Console
# 6. Log rotation
```

### PostHog Personal API Key (180-day rotation)

```bash
# 1. Generate at PostHog > Settings > Personal API keys
# 2. Update ~/.keys/.env — POSTHOG_PERSONAL_API_KEY=phx_NEW_KEY
# 3. Test: python3 scripts/posthog_hourly_report.sh (verify data returns)
# 4. Revoke old key at PostHog
# 5. Log rotation
```

## Rotation Calendar

| Month | Keys Due | Action |
|---|---|---|
| Every 3 months | GITHUB_TOKEN | Rotate PAT, update Secret Manager |
| Every 6 months | ANTHROPIC_API_KEY, POSTHOG_PERSONAL, CLICKUP, NOTION | Rotate all API keys |
| Every 12 months | GCP Service Account, SLACK_BOT_TOKEN, POSTHOG_PROJECT | Rotate long-lived credentials |

## Emergency Rotation (Credential Compromise)

If a key is suspected compromised:

1. **Immediately revoke** at the provider (GitHub, Anthropic, PostHog, etc.)
2. **Generate new key** at provider
3. **Update Secret Manager** + `~/.keys/.env`
4. **Redeploy** all affected Cloud Run services
5. **Verify** services operational
6. **Log incident** per R-SEC-05 (Incident Response Playbook)

## Rotation Log

Maintained at `~/.keys/rotation.log`:

```
# Format: ISO_DATE CREDENTIAL_NAME ACTION
2026-03-03T18:00:00Z GITHUB_TOKEN initial_setup
2026-03-03T18:00:00Z ANTHROPIC_API_KEY initial_setup
```

## Pre-Rotation Checklist

- [ ] New key generated and tested locally
- [ ] Secret Manager updated with new version
- [ ] Local `~/.keys/.env` updated
- [ ] Cloud Run jobs tested (dry-run)
- [ ] Old key revoked at provider
- [ ] Rotation logged to `~/.keys/rotation.log`
- [ ] No services returning 401/403 errors

---

*R-SEC-06 | Virtual ATeam Security Standards | Paradise Media Group*
