# R-SEC-03: CORS Security Rules

**Priority:** P1 High
**Owner:** W-GARD (Guardian) + W-IVAN (Architecture)
**Created:** 2026-03-03
**Status:** ACTIVE

---

## Purpose

Standardize Cross-Origin Resource Sharing (CORS) policies for all web services, APIs, and Cloud Run deployments. Prevents unauthorized cross-origin requests and data exfiltration.

## Rules

### Rule 1: No Wildcard Origins in Production

```python
# BAD — allows any origin
CORS(app, origins="*")

# GOOD — explicit allowed origins
CORS(app, origins=[
    "https://australiafootball.com",
    "https://www.australiafootball.com",
    "https://admin.paradisemedia.com",
])
```

### Rule 2: Origin Allowlist by Service Type

| Service Type | Allowed Origins | Credentials |
|---|---|---|
| Public website (Astro) | N/A (static, no CORS needed) | N/A |
| Internal API (Cloud Run) | `domain:paradisemedia.com` only | Yes |
| Health endpoints | Same-origin only | No |
| PostHog proxy | PostHog CDN + site domain | No |
| MCP Server | localhost + Cloud Run service accounts | Yes |
| Webhook receivers | Specific sender domains only | Verify HMAC |

### Rule 3: Credential Handling

```python
# When credentials=True, origins MUST be explicit (not wildcard)
CORS(app,
    origins=["https://admin.paradisemedia.com"],
    supports_credentials=True,
    allow_headers=["Authorization", "Content-Type"],
    methods=["GET", "POST"],
    max_age=3600  # Cache preflight for 1 hour
)
```

### Rule 4: Cloud Run CORS Headers

For Cloud Run services that serve API responses:

```yaml
# In Cloud Run service config or application code
Access-Control-Allow-Origin: https://specific-domain.com
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Authorization, Content-Type
Access-Control-Max-Age: 3600
```

**NEVER** set `Access-Control-Allow-Origin: *` on authenticated endpoints.

### Rule 5: Webhook CORS + HMAC

For incoming webhooks (Slack, GitHub, ClickUp):

```python
import hmac
import hashlib

def verify_webhook_signature(payload: bytes, signature: str, secret: str) -> bool:
    """Verify HMAC signature on incoming webhooks."""
    expected = hmac.new(
        secret.encode(), payload, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)
```

## Enforcement

- **W-FLUX:** Reviews CORS config in all PRs touching API endpoints
- **W-GARD:** Approves CORS policy changes for production services
- **W-IVAN:** Validates architecture doesn't require wildcard CORS

---

*R-SEC-03 | Virtual ATeam Security Standards | Paradise Media Group*
