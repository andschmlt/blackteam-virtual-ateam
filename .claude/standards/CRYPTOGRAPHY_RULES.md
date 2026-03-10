# R-SEC-04: Cryptography & Transport Security Rules

**Priority:** P2 Medium
**Owner:** W-GARD (Guardian)
**Created:** 2026-03-03
**Status:** ACTIVE

---

## Purpose

Standardize cryptographic choices across the workspace — TLS, hashing, token signing, and data at rest. Prevents weak encryption, deprecated algorithms, and insecure defaults.

## Rules

### Rule 1: TLS Requirements

| Context | Minimum TLS | Notes |
|---|---|---|
| Cloud Run services | TLS 1.2 (GCP default) | GCP handles termination |
| External API calls | TLS 1.2 | `verify=True` in requests (default) |
| GitHub API | TLS 1.2 | Enforced by GitHub |
| Database connections | TLS 1.2 | BigQuery enforces by default |

**NEVER** set `verify=False` in production:
```python
# BAD — disables certificate verification
requests.get(url, verify=False)

# GOOD — default behavior, verifies certificates
requests.get(url)
```

### Rule 2: Password/Token Hashing

| Purpose | Algorithm | Notes |
|---|---|---|
| User passwords | bcrypt (cost 12+) or argon2id | NEVER MD5 or SHA-1 |
| API token comparison | `hmac.compare_digest()` | Constant-time comparison |
| Content fingerprinting | SHA-256 | For dedup, caching |
| File integrity | SHA-256 | For deployment verification |

```python
import hmac

# BAD — timing attack vulnerable
if token == expected_token:
    pass

# GOOD — constant-time comparison
if hmac.compare_digest(token, expected_token):
    pass
```

### Rule 3: Secret Generation

```python
import secrets

# Generate secure tokens
api_token = secrets.token_urlsafe(32)     # 32 bytes = 256 bits
session_id = secrets.token_hex(16)         # 16 bytes = 128 bits

# NEVER use random module for security
import random
bad_token = random.randint(0, 999999)  # PREDICTABLE — never use for auth
```

### Rule 4: Data at Rest

| Data Type | Protection | Location |
|---|---|---|
| API keys | GCP Secret Manager | Referenced via `secretKeyRef` |
| Local dev keys | `~/.keys/.env` (chmod 600) | Never in git |
| Database credentials | Secret Manager | Service account access only |
| User PII | Not stored | N/A for current projects |

### Rule 5: JWT/Token Standards (if applicable)

- Signing algorithm: RS256 or ES256 (NEVER HS256 with shared secret in production)
- Token expiry: 1 hour for access tokens, 30 days for refresh tokens
- Claims: Include `iss`, `exp`, `sub`, `aud` minimum

## Enforcement

- **W-GARD:** Reviews all crypto choices in PRs
- **B-TECH:** Implements approved crypto patterns
- Scan for deprecated patterns: `grep -rn 'md5\|sha1\|verify=False\|random.randint.*token' scripts/`

---

*R-SEC-04 | Virtual ATeam Security Standards | Paradise Media Group*
