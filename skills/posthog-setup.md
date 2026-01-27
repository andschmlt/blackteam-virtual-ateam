# /blackteam Setup [domain] - PostHog Analytics Deployment Skill

## Skill Metadata

```yaml
name: posthog-setup
command: /blackteam Setup
version: 1.0.0
author: CodeGuard (Implementation) + Principal (Architecture)
project: PHOG-001
```

---

## Description

Automated PostHog analytics deployment for any owned domain. This skill creates a new PostHog project, generates tracking code, and provides step-by-step implementation instructions.

---

## Usage

```
/blackteam Setup [domain]
```

**Parameters:**
- `domain` (required): Target domain without protocol (e.g., `lover.io`, `example.com`)

**Examples:**
```
/blackteam Setup lover.io
/blackteam Setup mydomain.com
```

---

## Execution Flow

When invoked, the skill executes the following phases:

### Phase 1: Domain Validation

```
1. Parse domain from arguments
2. Verify domain format (valid hostname)
3. Check domain accessibility (HEAD request)
4. Detect tech stack if possible
```

### Phase 2: PostHog Project Setup

```
1. Connect to PostHog API (Paradise Media organization)
2. Create new project named "[domain] Analytics"
3. Configure project settings:
   - Region: EU (eu.posthog.com)
   - Session recording: Enabled (50% sampling)
   - Autocapture: Enabled
4. Generate and retrieve Project API Key
```

### Phase 3: Configuration Generation

```
1. Generate tracking code snippet with domain's API key
2. Create framework-specific implementation guide
3. Generate event taxonomy template (customizable)
4. Create dashboard provisioning script
```

### Phase 4: Dashboard Provisioning

```
1. Create Executive Overview dashboard
2. Create Traffic & Acquisition dashboard
3. Create Content Performance dashboard
4. Create Affiliate Performance dashboard
5. Create Technical Health dashboard
```

### Phase 5: Verification & Handoff

```
1. Test event ingestion endpoint
2. Generate implementation checklist
3. Output complete setup package
```

---

## Skill Implementation

### Input Processing

```python
def parse_arguments(args):
    """Extract domain from skill arguments."""
    if not args or not args.strip():
        raise ValueError("Domain required. Usage: /blackteam Setup [domain]")

    domain = args.strip().lower()

    # Remove protocol if provided
    domain = domain.replace('https://', '').replace('http://', '')

    # Remove trailing slash
    domain = domain.rstrip('/')

    # Validate domain format
    import re
    if not re.match(r'^[a-z0-9]([a-z0-9-]*[a-z0-9])?(\.[a-z0-9]([a-z0-9-]*[a-z0-9])?)+$', domain):
        raise ValueError(f"Invalid domain format: {domain}")

    return domain
```

### PostHog API Integration

```python
import os
import requests

POSTHOG_API_HOST = "https://eu.posthog.com"
POSTHOG_PERSONAL_API_KEY = os.environ.get("POSTHOG_PERSONAL_API_KEY")
ORGANIZATION_ID = "paradise-media"  # Replace with actual org ID

def create_posthog_project(domain):
    """Create a new PostHog project for the domain."""
    headers = {
        "Authorization": f"Bearer {POSTHOG_PERSONAL_API_KEY}",
        "Content-Type": "application/json"
    }

    project_data = {
        "name": f"{domain} Analytics",
        "organization": ORGANIZATION_ID,
        "timezone": "UTC",
        "session_recording_opt_in": True,
        "autocapture_opt_out": False
    }

    response = requests.post(
        f"{POSTHOG_API_HOST}/api/projects/",
        headers=headers,
        json=project_data
    )

    if response.status_code == 201:
        project = response.json()
        return {
            "project_id": project["id"],
            "api_key": project["api_token"],
            "name": project["name"]
        }
    else:
        raise Exception(f"Failed to create project: {response.text}")
```

### Tracking Code Generator

```python
def generate_tracking_code(api_key, domain):
    """Generate the PostHog tracking code snippet."""
    return f'''<!-- PostHog Analytics - {domain} -->
<script>
    !function(t,e){{var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){{function g(t,e){{var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){{t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}}}(p=t.createElement("script")).type="text/javascript",p.async=!0,p.src=s.api_host.replace('.i.posthog.com','-assets.i.posthog.com')+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){{var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e}},u.people.toString=function(){{return u.toString(1)+".people (stub)"}},o="capture identify alias people.set people.set_once set_config register register_once unregister opt_out_capturing has_opted_out_capturing opt_in_capturing reset isFeatureEnabled onFeatureFlags getFeatureFlag getFeatureFlagPayload reloadFeatureFlags group updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures getActiveMatchingSurveys getSurveys onSessionId setPersonProperties".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])}},e.__SV=1)}}(document,window.posthog||[]);

    posthog.init('{api_key}', {{
        api_host: 'https://eu.i.posthog.com',
        person_profiles: 'identified_only',
        capture_pageview: true,
        capture_pageleave: true,
        autocapture: true,
        session_recording: {{
            maskAllInputs: true,
            maskTextSelector: '.ph-no-capture'
        }}
    }});
</script>'''
```

---

## Output Template

When the skill completes, it outputs:

```markdown
# PostHog Setup Complete: [domain]

## Project Details

| Property | Value |
|----------|-------|
| Project Name | [domain] Analytics |
| Project ID | [project_id] |
| API Key | [api_key] |
| Region | EU (Frankfurt) |
| Dashboard URL | https://eu.posthog.com/project/[project_id] |

## Tracking Code

Add this to your site's `<head>`:

\`\`\`html
[generated_tracking_code]
\`\`\`

## Implementation Checklist

- [ ] Add tracking code to site layout/template
- [ ] Deploy to staging environment
- [ ] Verify events in PostHog Live Events
- [ ] Check session replay is working
- [ ] Deploy to production
- [ ] Verify production data flow

## Dashboards Created

1. Executive Overview
2. Traffic & Acquisition
3. Content Performance
4. Affiliate Performance
5. Technical Health

## Next Steps

1. Review the Implementation Guide: `deliverables/IMPLEMENTATION_GUIDE.md`
2. Customize event tracking per Event Taxonomy: `deliverables/EVENT_TAXONOMY.md`
3. Run QA validation checklist

## Resources

- [PostHog Dashboard](https://eu.posthog.com/project/[project_id])
- [PostHog Docs](https://posthog.com/docs)
- [Event Taxonomy](./EVENT_TAXONOMY.md)
- [Implementation Guide](./IMPLEMENTATION_GUIDE.md)

---
*Generated by /blackteam Setup | PHOG-001*
```

---

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `Invalid domain format` | Malformed domain input | Check domain syntax |
| `Domain not accessible` | DNS or server issue | Verify domain is live |
| `API authentication failed` | Invalid/missing API key | Check POSTHOG_PERSONAL_API_KEY |
| `Project creation failed` | API error or limits | Check PostHog account status |
| `Dashboard creation failed` | API error | Retry or create manually |

---

## Configuration Requirements

### Environment Variables

```bash
# Required for skill execution
POSTHOG_PERSONAL_API_KEY=phx_xxxxxxxxxxxxxxxxxxxx

# Organization ID (from PostHog settings)
POSTHOG_ORG_ID=xxxxx
```

### File Dependencies

```
/mnt/c/Users/andre/Desktop/Virtual ATeam/BlackTeam/
├── skills/
│   └── posthog-setup.md          # This file
├── templates/
│   └── posthog/
│       ├── tracking-snippet.js    # Base tracking code
│       ├── dashboard-config.json  # Dashboard definitions
│       └── event-handlers.js      # Custom event script
└── projects/
    └── posthog-integration/
        └── deliverables/          # Reference documentation
```

---

## Testing

### Manual Test

```bash
# Simulate skill execution
/blackteam Setup testdomain.com
```

### Expected Output

1. Domain validation passes
2. Project created in PostHog
3. Tracking code generated
4. Dashboards provisioned
5. Implementation checklist provided

### Verification

1. Log into PostHog
2. Verify new project exists
3. Check dashboards are created
4. Test tracking code on target domain

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-14 | Initial release |

---

*Skill Definition v1.0 | CodeGuard + Principal | PHOG-001*
