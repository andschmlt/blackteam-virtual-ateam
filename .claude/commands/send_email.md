# /send_email - Email Reports and Notifications

Send reports, files, or notifications via email using configured SMTP.

## Phase 0: RAG Context Loading

**Load relevant context from the RAG system.**

```python
from AS-Virtual_Team_System_v2.rag.rag_client import VTeamRAG
rag = VTeamRAG()
context = rag.query("email report delivery", top_k=3)
```

---

## Configuration

**Config File:** `/home/andre/.claude/email_config.json`
**Credentials:** `~/.keys/.env` (SMTP_USER, SMTP_PASSWORD)

## Usage

```
/send_email [file_path]              # Send file as attachment
/send_email [file_path] [subject]    # Send with custom subject
/send_email report [domain]          # Send latest PostHog report for domain
```

## Examples

```
/send_email /home/andre/reports/analysis.md
/send_email /home/andre/reports/pokerology_report.pdf "Weekly Analytics Report"
/send_email report pokerology.com
```

## Instructions

When this command is invoked:

### 1. Load Email Configuration

```python
import json
import os

# Load config
with open('/home/andre/.claude/email_config.json') as f:
    config = json.load(f)

# Load credentials from env
from dotenv import load_dotenv
load_dotenv('/home/andre/.keys/.env')

SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
```

### 2. Send Email with Attachment

```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

def send_email_with_attachment(
    to_email: str,
    subject: str,
    body: str,
    attachment_path: str = None
):
    """Send email with optional attachment"""

    msg = MIMEMultipart()
    msg['From'] = f"Virtual ATeam <{SMTP_USER}>"
    msg['To'] = to_email
    msg['Subject'] = subject

    # Add body
    msg.attach(MIMEText(body, 'plain'))

    # Add attachment if provided
    if attachment_path and Path(attachment_path).exists():
        with open(attachment_path, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            filename = Path(attachment_path).name
            part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
            msg.attach(part)

    # Send via SMTP
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)

    return True
```

### 3. For PostHog Reports

If argument is `report [domain]`:
1. Find latest report for domain in `/home/andre/projects/posthog-integration/reports/`
2. Generate subject: `[PostHog Report] {domain} - {date}`
3. Send with report as attachment

### 4. Quick Send Script

Use this script for quick email sending:

```bash
python3 /home/andre/.claude/scripts/send_email.py \\
    --to "andre@paradisemedia.com" \\
    --subject "PostHog Report" \\
    --body "Please find the attached report." \\
    --attachment "/path/to/report.md"
```

## Default Recipients

| Type | Email |
|------|-------|
| Primary | andre@paradisemedia.com |
| BI Updates | andre@paradisemedia.com |

## Related

- `/posthog_analysis` - Generate PostHog reports
- Email config: `/home/andre/.claude/email_config.json`
- SMTP credentials: `~/.keys/.env`
