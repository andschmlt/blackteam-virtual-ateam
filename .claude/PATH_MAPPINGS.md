# Path Mappings Reference

**Version:** 1.0
**Updated:** 2026-02-03
**Purpose:** Canonical path reference for all Virtual ATeam files

---

## Primary Directories

| Purpose | Canonical Path |
|---------|----------------|
| Virtual ATeam v2 Root | `/home/andre/AS-Virtual_Team_System_v2/` |
| BlackTeam | `/home/andre/AS-Virtual_Team_System_v2/blackteam/` |
| WhiteTeam | `/home/andre/AS-Virtual_Team_System_v2/whiteteam/` |
| Claude Commands | `/home/andre/.claude/commands/` |
| Claude Standards | `/home/andre/.claude/standards/` |
| Claude Projects | `/home/andre/.claude/projects/` |
| Secrets/Keys | `/home/andre/.keys/` and `/home/andre/secrets/` |

---

## BlackTeam File Locations

```
/home/andre/AS-Virtual_Team_System_v2/blackteam/
├── personas/                    # Persona definitions
│   ├── DIRECTOR.md
│   ├── DATAFORGE.md
│   ├── CODEGUARD.md
│   └── ...
├── rules/                       # Rule files
│   ├── DIRECTOR_RULES.md        # All 33+ rules
│   └── CONTENT_STANDARDS.md     # Content QA standards
├── skills/                      # Skill definitions
│   └── prompts/                 # Persona prompts
│       ├── DIRECTOR_PROMPT.md
│       ├── DIRECTOR_SHEET.md
│       ├── DATAFORGE_PROMPT.md
│       └── ...
├── templates/                   # Output templates
│   └── content-team/            # Content team templates
├── frameworks/                  # Rule frameworks
│   └── RULE_34_IMAGE_UNIQUENESS_FRAMEWORK.md
└── tools/                       # Utility scripts
    ├── log_activity.sh
    └── generate_utilization_report.sh
```

---

## WhiteTeam File Locations

```
/home/andre/AS-Virtual_Team_System_v2/whiteteam/
├── personas/                    # Validator definitions
│   ├── GUARDIAN.md              # Security (W-GARD)
│   └── ...
├── rules/                       # Validation rules
│   └── WHITETEAM_RULES.md       # All 50 rules
├── skills/                      # Validation skills
│   └── prompts/                 # Validator prompts
└── templates/                   # Validation templates
```

---

## Shared Configuration Files

| File | Location |
|------|----------|
| TEAM_CONFIG.md | `/home/andre/AS-Virtual_Team_System_v2/TEAM_CONFIG.md` |
| RALPH_LOOPS_SPECIFICATION.md | `/home/andre/AS-Virtual_Team_System_v2/RALPH_LOOPS_SPECIFICATION.md` |
| PROJECT_REGISTRY.json | `/home/andre/AS-Virtual_Team_System_v2/PROJECT_REGISTRY.json` |

---

## Claude Configuration

```
/home/andre/.claude/
├── commands/                    # Skill/command definitions
│   ├── blackteam.md
│   ├── whiteteam.md
│   ├── director.md
│   ├── A_Virtual_Team.md
│   └── ...
├── standards/                   # Standards documentation
│   ├── VALIDATION_STANDARDS.md
│   ├── API_ERROR_HANDLING.md
│   └── DOCUMENTATION_STYLE_GUIDE.md
├── projects/                    # Project tracking
│   └── workspace-accuracy-improvement/
├── ROUTING_DECISION_TREE.md     # Command selection guide
├── PATH_MAPPINGS.md             # This file
├── settings.json                # Claude settings
└── clickup_config.json          # ClickUp integration
```

---

## Agent Projects

| Agent | Path |
|-------|------|
| BI-Chatbot | `/home/andre/BI-Chatbot/` |
| Pitaya | `/home/andre/pitaya/` |
| BI-CARLOS | `/home/andre/BI-CARLOS/` |
| Paradise Brain | `/home/andre/paradise_brain/` |
| Bedrock Agent | `/home/andre/AS-Virtual_Team_System_v2/projects/bedrock_agent/` |

---

## Credentials & Secrets

| Purpose | Location |
|---------|----------|
| Email Utility | `/home/andre/.keys/send_email.py` |
| Environment Variables | `/home/andre/.keys/.env` |
| BigQuery Service Account | `/home/andre/secrets/bi-chatbot-sa.json` |
| ClickUp Config | `/home/andre/.claude/clickup_config.json` |

---

## Analysis & Reports Output

| Type | Location |
|------|----------|
| Analysis PDFs | `/home/andre/analysis/` |
| Reports | `/home/andre/reports/` |

---

## Deprecated Paths (DO NOT USE)

The following paths are **deprecated** and should NOT be used:

| Deprecated Path | Replacement |
|-----------------|-------------|
| `/mnt/c/Users/andre/Desktop/Virtual ATeam/BlackTeam/` | `/home/andre/AS-Virtual_Team_System_v2/blackteam/` |
| `/mnt/c/Users/andre/Desktop/Virtual ATeam/BlackTeam/skills/prompts/` | `/home/andre/AS-Virtual_Team_System_v2/blackteam/skills/prompts/` |
| `~/virtual-ateam/BlackTeam/` | `/home/andre/AS-Virtual_Team_System_v2/blackteam/` |
| `C:\Users\andre\Desktop\Virtual ATeam\` | `/home/andre/AS-Virtual_Team_System_v2/` |
| `C:\Users\andre\Desktop\Claude Widgets\` | `/home/andre/.claude/widgets/` (if needed) |
| `/home/andre/BI-AI_Agents_REPO/` | `/home/andre/AS-Virtual_Team_System_v2/` |
| `/home/andre/BI-AI_Agents_REPO/bedrock_agent/` | `/home/andre/AS-Virtual_Team_System_v2/projects/bedrock_agent/` |
| `~/BI-AI_Agents_REPO/` | `~/AS-Virtual_Team_System_v2/` |

---

## Path Resolution Rules

1. **Always use absolute Linux paths** starting with `/home/andre/`
2. **Never use Windows paths** (`C:\`, `/mnt/c/`)
3. **Avoid relative paths** except within project directories
4. **Use tilde expansion** (`~`) only when necessary, prefer absolute paths

---

## Quick Lookup

```bash
# BlackTeam rules
/home/andre/AS-Virtual_Team_System_v2/blackteam/rules/DIRECTOR_RULES.md

# WhiteTeam rules
/home/andre/AS-Virtual_Team_System_v2/whiteteam/rules/WHITETEAM_RULES.md

# Team config
/home/andre/AS-Virtual_Team_System_v2/TEAM_CONFIG.md

# Command routing
/home/andre/.claude/ROUTING_DECISION_TREE.md

# Send email
/home/andre/.keys/send_email.py
```

