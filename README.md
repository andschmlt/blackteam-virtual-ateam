# BlackTeam v2.0 - Virtual ATeam Distribution

**Organization:** Paradise Media Group
**Version:** 2.0
**Release Date:** 2026-01-27

---

## Overview

BlackTeam is a Virtual ATeam of 20 AI personas designed to work with Claude (or other LLMs) to execute projects with defined roles, responsibilities, and standards.

---

## Quick Start

### 1. Copy to Your Machine

Copy this folder to your working directory:
```bash
cp -r BlackTeam-v2.0-release ~/virtual-ateam/BlackTeam
```

### 2. Load Context in Claude

Add this to your Claude project or session:

```
Load the BlackTeam context from:
- ~/virtual-ateam/BlackTeam/TEAM_CONFIG.md (team structure)
- ~/virtual-ateam/BlackTeam/DIRECTOR_RULES.md (operational rules)
- ~/virtual-ateam/BlackTeam/skills/prompts/ (persona prompts)
```

### 3. Activate a Persona

Use trigger keywords or activation phrases:

```
"Director, let's start a project..."
"Head of Analytics, analyze this data..."
"Head of SEO, review our strategy..."
```

---

## Team Structure (20 Personas)

### Leadership (6 Heads)
| Persona | Role | Focus |
|---------|------|-------|
| Director | Oversight | Rules, planning, stakeholder comms |
| Head of Analytics | Data Leadership | Statistics, ML, datasets |
| Head of Tech | Tech Leadership | Code, infrastructure, releases |
| Head of SEO | SEO Leadership | Strategy, approvals, guidance |
| Head of Asset Strategy | Advisory | Portfolio, publishers |
| Head of Affiliates | Advisory | Partnerships, commissions |

### Analytics Track
| Persona | Role |
|---------|------|
| Insight | Data Analyst |
| DataViz | BI Developer |

### Tech Track
| Persona | Role |
|---------|------|
| CodeGuard | Code Reviewer |
| DataForge | Data Engineer |
| Release Manager | Deployment Coordinator |

### SEO Track (Largest)
| Persona | Role |
|---------|------|
| SEO Manager | Operations |
| SEO White-hat Analyst | Ethical SEO |
| SEO Grey-hat Analyst | Aggressive SEO |
| SEO Black-hat Analyst | Defense & Recovery |
| Product Manager | NavBoost, Experiments |
| PixelPerfect | UX/UI Design |
| Head of Content | Content Strategy |
| Content Manager | Content Production |
| Post Production Mgr | QC, Publishing |

---

## Folder Structure

```
BlackTeam-v2.0-release/
├── README.md                   # This file
├── TEAM_CONFIG.md              # Full team structure and routing
├── DIRECTOR_RULES.md           # 25 operational rules
├── CONTENT_STANDARDS.md        # Content quality standards
├── personas/                   # Persona files and job descriptions
│   ├── *_JOB_DESCRIPTION.md    # Role charters
│   └── *.md                    # Persona operating instructions
└── skills/                     # Skills and prompts
    ├── *_SKILLS.md             # Skills inventory per persona
    └── prompts/                # Role Lock Prompts + Character Sheets
        ├── *_PROMPT.md         # System prompts for activation
        └── *_SHEET.md          # Character sheets with stats
```

---

## How to Use Personas

### Method 1: Direct Activation
Copy the system prompt from `skills/prompts/[PERSONA]_PROMPT.md` into your conversation.

### Method 2: Keyword Routing
Use routing keywords from `TEAM_CONFIG.md` - Claude will identify the appropriate persona.

### Method 3: Full Context Load
Load all files at session start for the Director to orchestrate the full team.

---

## Key Files

| File | Purpose |
|------|---------|
| `TEAM_CONFIG.md` | Master team configuration, org chart, routing rules |
| `DIRECTOR_RULES.md` | 25 operational rules all personas must follow |
| `personas/*.md` | Detailed persona operating instructions |
| `skills/*_SKILLS.md` | Skills inventory and capabilities |
| `skills/prompts/*_PROMPT.md` | System prompts for persona activation |
| `skills/prompts/*_SHEET.md` | Character sheets with stats and templates |

---

## Director Role (Rule 0)

The Director's role is strictly defined:

1. **Oversight & Accountability** - Keep everyone in check
2. **Rule Enforcement** - Ensure all rules are followed
3. **Planning & Deliverables** - Ensure quality before approval
4. **Stakeholder Communication** - SOLE point of contact

**The Director Does NOT:**
- Write code (delegates to Head of Tech)
- Create content (delegates to Head of SEO/Content)
- Perform analysis (delegates to Head of Analytics)
- Design (delegates to PixelPerfect)

---

## Example Usage

### Start a Project
```
Director, I need to analyze our SEO performance and create a dashboard.

[Director will]:
1. Assess the request
2. Assign Head of Analytics for data analysis
3. Assign DataViz for dashboard creation
4. Assign Head of SEO for SEO insights
5. Coordinate deliverables
6. Report back to stakeholder
```

### Activate Specific Persona
```
Head of Analytics, perform a deep dive analysis on our conversion funnel data.

[Head of Analytics will]:
1. Define methodology
2. Analyze data
3. Surface insights
4. Provide action items
```

---

## License

Internal use only - Paradise Media Group

---

*BlackTeam v2.0 | Paradise Media Group | 2026-01-27*
