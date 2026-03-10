# R-SEC-02: Input Validation Rules

**Priority:** P1 High
**Owner:** W-GARD (Guardian) + W-FLUX (Code Auditor)
**Created:** 2026-03-03
**Status:** ACTIVE

---

## Purpose

Standardize input validation patterns across all Python, JavaScript/TypeScript, and shell scripts in the workspace. Prevents injection attacks, data corruption, and unexpected behavior.

## Rules

### Rule 1: Never Trust External Input

ALL data from these sources MUST be validated before use:
- RSS feed content (titles, descriptions, URLs)
- Web scrape results (HTML content, extracted text)
- API responses (JSON payloads, headers)
- User input (CLI arguments, form fields)
- Environment variables (when used in queries/commands)
- File content (uploaded files, parsed configs)

### Rule 2: URL Validation

```python
# REQUIRED pattern for any URL used in requests or stored in content
from urllib.parse import urlparse

def validate_url(url: str, allowed_schemes=("https",), allowed_domains=None) -> bool:
    """Validate URL before use. Reject invalid or dangerous URLs."""
    try:
        parsed = urlparse(url)
    except Exception:
        return False
    if parsed.scheme not in allowed_schemes:
        return False
    if not parsed.netloc:
        return False
    if allowed_domains and not any(d in parsed.netloc for d in allowed_domains):
        return False
    # Block private/internal IPs (SSRF prevention)
    if any(parsed.netloc.startswith(p) for p in ("127.", "10.", "192.168.", "172.16.", "localhost")):
        return False
    return True
```

### Rule 3: String Sanitization

```python
import re

def sanitize_title(text: str, max_length: int = 200) -> str:
    """Sanitize text for use in filenames, frontmatter, or display."""
    text = re.sub(r"[\x00-\x1f\x7f]", "", text)  # Remove control chars
    text = text.replace('"', '\\"')                 # Escape quotes for YAML
    return text[:max_length].strip()

def sanitize_html(text: str) -> str:
    """Strip HTML tags — never render untrusted HTML."""
    return re.sub(r"<[^>]+>", "", text).strip()
```

### Rule 4: SQL / Query Parameterization

**NEVER** use string interpolation in queries:

```python
# BAD — SQL injection risk
query = f"SELECT * FROM table WHERE name = '{user_input}'"

# GOOD — parameterized
query = "SELECT * FROM table WHERE name = %s"
cursor.execute(query, (user_input,))

# GOOD — BigQuery
query = "SELECT * FROM table WHERE name = @name"
job_config = bigquery.QueryJobConfig(query_parameters=[
    bigquery.ScalarQueryParameter("name", "STRING", user_input)
])
```

### Rule 5: File Path Validation

```python
import os

def safe_filepath(base_dir: str, filename: str) -> str:
    """Prevent path traversal attacks."""
    # Resolve to absolute and verify it's under base_dir
    full_path = os.path.realpath(os.path.join(base_dir, filename))
    if not full_path.startswith(os.path.realpath(base_dir)):
        raise ValueError(f"Path traversal blocked: {filename}")
    return full_path
```

### Rule 6: Integer/Type Validation

```python
def safe_int(value: str, default: int = 0, min_val: int = 0, max_val: int = 10000) -> int:
    """Safely convert string to bounded integer."""
    try:
        n = int(value)
        return max(min_val, min(n, max_val))
    except (ValueError, TypeError):
        return default
```

### Rule 7: RSS/XML Input Safety

- Always use `xml.etree.ElementTree` (stdlib) — it disables external entity loading by default
- NEVER use `xml.sax` or `lxml.etree.parse()` with untrusted XML without disabling external entities
- Limit parsed content size: `text[:500]` for descriptions, `text[:200]` for titles
- Strip HTML from RSS description fields before storing

## Enforcement

| Command | Enforcement Point |
|---|---|
| `/news_update_agent` | RSS parsing, URL validation, Reddit content extraction |
| `/launch_site` | Script generation, API integration code |
| `/bedrock_agent` | Content generation, data pipeline code |
| `/content_palm` | Palm API response validation |
| `/blackteam` | Any code generation task |

**Validation:** W-FLUX reviews all generated code for input validation compliance. W-GARD approves for security-sensitive paths.

---

*R-SEC-02 | Virtual ATeam Security Standards | Paradise Media Group*
