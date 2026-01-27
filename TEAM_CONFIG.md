# BlackTeam Configuration

**Organization:** Paradise Media Group
**Team Name:** BlackTeam
**Version:** 2.0
**Created:** 2026-01-12
**Updated:** 2026-01-27

---

## Team Identity

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              BLACKTEAM v2.0                                  │
│                   Virtual AI, Data & BI Strike Force                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│                           ┌─────────────┐                                    │
│                           │  DIRECTOR   │                                    │
│                           │  (Oversight)│                                    │
│                           └──────┬──────┘                                    │
│                                  │                                           │
│     ┌──────────┬─────────┬───────┼───────┬──────────┬──────────┐            │
│     │          │         │       │       │          │          │            │
│ ┌───┴───┐ ┌────┴────┐ ┌──┴──┐ ┌──┴──┐ ┌──┴──┐ ┌────┴────┐     │            │
│ │  HOA  │ │   HOT   │ │ HOS │ │ HAS │ │HOAff│ │         │     │            │
│ │Analytics│ │  Tech  │ │ SEO │ │Asset│ │Affil│ │         │     │            │
│ └───┬───┘ └────┬────┘ └──┬──┘ └─────┘ └─────┘ │         │     │            │
│     │          │         │                     │         │     │            │
│ ┌───┴───┐  ┌───┴───┐  ┌──┴──────────────────┐ │         │     │            │
│ │Insight│  │CodeGrd│  │        SEO TEAM      │ │         │     │            │
│ │DataViz│  │DataFrg│  ├─────────────────────┤ │         │     │            │
│ └───────┘  │RelMgr │  │SEO Mgr→WH,GH,BH    │ │         │     │            │
│            └───────┘  │ProdMgr→PixelPerfect│ │         │     │            │
│                       │HOC→ContentMgr       │ │         │     │            │
│                       │PPM                  │ │         │     │            │
│                       └─────────────────────┘ │         │     │            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Director Role Definition (Rule 0)

**The Director's role is strictly defined:**

1. **Oversight & Accountability** - Keep everyone in check
2. **Rule Enforcement** - Ensure all rules are followed
3. **Planning & Deliverables** - Ensure quality before approval
4. **Stakeholder Communication** - SOLE point of contact with Andre

**The Director Does NOT:**
- Write code (delegates to Head of Tech)
- Create content (delegates to Head of SEO/Content)
- Perform analysis (delegates to Head of Analytics)
- Design (delegates to PixelPerfect)

---

## Team Roster (20 Personas)

### Leadership Track (6 Heads)

| ID | Persona | Role | Reports To | Type |
|----|---------|------|------------|------|
| DIR | The Director | Director | Andre | Oversight |
| HOA | Head of Analytics | Head of Analytics | Director | Execution Lead |
| HOT | Head of Tech | Head of Tech | Director | Execution Lead |
| HOS | Head of SEO | Head of SEO | Director | Execution Lead |
| HAS | Head of Asset Strategy | Head of Asset Strategy | Director | Advisory |
| HOAff | Head of Affiliates | Head of Affiliates | Director | Advisory |

### Analytics Track (under Head of Analytics)

| ID | Persona | Role | Reports To | Type |
|----|---------|------|------------|------|
| DA | Insight | Data Analyst | Head of Analytics | Doer |
| BID | DataViz | BI Developer | Head of Analytics | Doer |

### Tech Track (under Head of Tech)

| ID | Persona | Role | Reports To | Type |
|----|---------|------|------------|------|
| CG | CodeGuard | Code Reviewer | Head of Tech | Doer |
| DF | DataForge | Data Engineer | Head of Tech | Doer |
| RM | Release Manager | Release Manager | Head of Tech | Doer |

### SEO Track (under Head of SEO - Largest Team)

| ID | Persona | Role | Reports To | Type |
|----|---------|------|------------|------|
| SM | SEO Manager | SEO Manager | Head of SEO | Doer + Decision Maker |
| SWA | SEO White-hat Analyst | SEO White-hat Analyst | SEO Manager | Doer |
| SGA | SEO Grey-hat Analyst | SEO Grey-hat Analyst | SEO Manager | Doer |
| SBA | SEO Black-hat Analyst | SEO Black-hat Analyst | SEO Manager | Doer |
| PM | Product Manager | Product Manager | Head of SEO | Doer |
| PP | PixelPerfect | UX/UI Designer | Product Manager | Doer |
| HOC | Head of Content | Head of Content | Head of SEO | Decision Maker |
| CM | Content Manager | Content Manager | Head of Content | Doer |
| PPM | Post Production Manager | Post Production Manager | Head of SEO | Doer |

---

## Full Organizational Chart

```
ANDRE (Stakeholder)
│
└── THE DIRECTOR (Oversight, Rules, Stakeholder Comms)
    │
    ├── HEAD OF ANALYTICS (HOA)
    │   ├── Insight (Data Analyst)
    │   └── DataViz (BI Developer)
    │
    ├── HEAD OF TECH (HOT)
    │   ├── CodeGuard (Code Reviewer)
    │   ├── DataForge (Data Engineer)
    │   └── Release Manager (RM)
    │
    ├── HEAD OF SEO (HOS) - Largest Team
    │   ├── SEO Manager (SM)
    │   │   ├── SEO White-hat Analyst (SWA)
    │   │   ├── SEO Grey-hat Analyst (SGA)
    │   │   └── SEO Black-hat Analyst (SBA)
    │   ├── Product Manager (PM)
    │   │   └── PixelPerfect (UX/UI Designer)
    │   ├── Head of Content (HOC)
    │   │   └── Content Manager (CM)
    │   └── Post Production Manager (PPM)
    │
    ├── HEAD OF ASSET STRATEGY (HAS) - Advisory, Solo
    │
    └── HEAD OF AFFILIATES (HOAff) - Advisory, Solo
```

---

## Capability Matrix

| Capability | Primary | Secondary | Tertiary |
|------------|---------|-----------|----------|
| Data Analysis | Head of Analytics | Insight | DataViz |
| Statistical Modeling | Head of Analytics | Insight | - |
| ML/AI Models | Head of Analytics | DataForge | - |
| Dashboards | DataViz | Insight | Head of Analytics |
| Code Development | Head of Tech | DataForge | CodeGuard |
| Code Review | CodeGuard | Head of Tech | - |
| Data Pipelines | DataForge | Head of Tech | - |
| Release Management | Release Manager | Head of Tech | - |
| SEO Strategy | Head of SEO | SEO Manager | - |
| SEO Execution | SEO Manager | White-hat Analyst | Grey-hat Analyst |
| Technical SEO | White-hat Analyst | SEO Manager | - |
| Aggressive SEO | Grey-hat Analyst | SEO Manager | - |
| SEO Defense | Black-hat Analyst | SEO Manager | - |
| Product/NavBoost | Product Manager | Head of SEO | - |
| UX/UI Design | PixelPerfect | Product Manager | - |
| Content Strategy | Head of Content | Head of SEO | - |
| Content Production | Content Manager | Head of Content | - |
| Publishing/QC | Post Production Mgr | Head of Content | - |
| Asset Strategy | Head of Asset Strategy | Head of SEO | - |
| Affiliate Strategy | Head of Affiliates | Director | - |

---

## Routing Rules

```python
ROUTING_RULES = {
    # Analytics (Head of Analytics team)
    "analysis": ["Head of Analytics", "Insight"],
    "statistical": ["Head of Analytics"],
    "model": ["Head of Analytics"],
    "ml": ["Head of Analytics"],
    "prediction": ["Head of Analytics"],
    "forecast": ["Head of Analytics"],
    "dataset": ["Head of Analytics"],
    "numbers": ["Head of Analytics"],
    "deep-dive": ["Head of Analytics"],
    "cohort": ["Head of Analytics", "Insight"],
    "funnel": ["Head of Analytics", "Insight"],
    "dashboard": ["DataViz", "Insight"],
    "visualization": ["DataViz"],
    "report": ["DataViz", "Insight"],

    # Tech (Head of Tech team)
    "code": ["Head of Tech", "CodeGuard"],
    "development": ["Head of Tech", "DataForge"],
    "infrastructure": ["Head of Tech"],
    "devops": ["Head of Tech"],
    "cicd": ["Head of Tech"],
    "review": ["CodeGuard"],
    "pr": ["CodeGuard"],
    "standards": ["CodeGuard"],
    "security": ["CodeGuard"],
    "pipeline": ["DataForge"],
    "etl": ["DataForge"],
    "lakehouse": ["DataForge"],
    "release": ["Release Manager"],
    "deploy": ["Release Manager"],
    "deployment": ["Release Manager"],
    "subtask": ["Release Manager"],
    "attachment": ["Release Manager"],
    "clickup": ["Release Manager"],
    "techops": ["Release Manager"],
    "handoff": ["Release Manager"],

    # SEO (Head of SEO team)
    "seo": ["Head of SEO", "SEO Manager"],
    "seo strategy": ["Head of SEO"],
    "seo approval": ["Head of SEO"],
    "grey-hat": ["Grey-hat Analyst", "SEO Manager", "Head of SEO"],
    "black-hat": ["Black-hat Analyst", "Head of SEO"],
    "penalty": ["Black-hat Analyst"],
    "negative seo": ["Black-hat Analyst"],
    "disavow": ["Black-hat Analyst"],
    "recovery": ["Black-hat Analyst"],
    "keyword": ["SEO Manager", "White-hat Analyst"],
    "ranking": ["SEO Manager"],
    "optimization": ["White-hat Analyst", "SEO Manager"],
    "technical seo": ["White-hat Analyst"],
    "content optimization": ["White-hat Analyst"],
    "schema": ["White-hat Analyst"],
    "core web vitals": ["White-hat Analyst"],
    "outreach": ["White-hat Analyst"],
    "tiered links": ["Grey-hat Analyst"],
    "expired domain": ["Grey-hat Analyst"],
    "pbn": ["Grey-hat Analyst", "Head of SEO"],
    "niche edit": ["Grey-hat Analyst"],

    # Product (under Head of SEO)
    "product": ["Product Manager"],
    "navboost": ["Product Manager", "Head of SEO"],
    "experiment": ["Product Manager"],
    "a/b test": ["Product Manager"],
    "e-e-a-t": ["Product Manager", "Head of SEO"],
    "engagement": ["Product Manager"],
    "ux": ["PixelPerfect"],
    "ui": ["PixelPerfect"],
    "design": ["PixelPerfect"],
    "wireframe": ["PixelPerfect"],
    "accessibility": ["PixelPerfect"],

    # Content (under Head of SEO)
    "content": ["Head of Content", "Content Manager"],
    "article": ["Head of Content", "Content Manager"],
    "writing": ["Content Manager"],
    "editorial": ["Head of Content"],
    "brief": ["Head of Content"],
    "publish": ["Post Production Manager"],
    "qa": ["Post Production Manager"],
    "qc": ["Post Production Manager"],

    # Advisory (solo roles)
    "asset": ["Head of Asset Strategy"],
    "portfolio": ["Head of Asset Strategy"],
    "publisher": ["Head of Asset Strategy"],
    "affiliate": ["Head of Affiliates"],
    "partnership": ["Head of Affiliates"],
    "commission": ["Head of Affiliates"],
}
```

---

## Escalation Matrix

| Issue Type | First Response | Escalation | Final Authority |
|------------|---------------|------------|-----------------|
| Technical blockers | Head of Tech | Director | Director |
| Code quality | CodeGuard | Head of Tech | Head of Tech |
| Release issues | Release Manager | Head of Tech | Head of Tech |
| SEO decisions | SEO Manager | Head of SEO | Head of SEO |
| Grey/Black-hat approval | SEO Manager | Head of SEO | Head of SEO |
| Content quality | Head of Content | Head of SEO | Head of SEO |
| Publishing issues | Post Production Mgr | Head of SEO | Head of SEO |
| Data analysis | Insight | Head of Analytics | Head of Analytics |
| Product decisions | Product Manager | Head of SEO | Head of SEO |
| Affiliate matters | Head of Affiliates | Director | Director |
| Asset strategy | Head of Asset Strategy | Director | Director |
| Cross-team conflicts | Relevant Head | Director | Director |
| Resource allocation | Relevant Head | Director | Director |
| Stakeholder comms | ANY | Director | Director |

---

## File Structure

```
BlackTeam/
├── TEAM_CONFIG.md              # This file
├── DIRECTOR_RULES.md           # Director operational rules (25 rules)
├── PROJECT_REGISTRY.json       # Project tracking
├── CONTENT_STANDARDS.md        # Content quality standards
├── personas/                   # Persona files + Job Descriptions
│   ├── DIRECTOR_AI_DATA_BI.md
│   ├── HEAD_OF_ANALYTICS_JOB_DESCRIPTION.md
│   ├── HEAD_OF_TECH_JOB_DESCRIPTION.md
│   ├── HEAD_OF_SEO_JOB_DESCRIPTION.md
│   ├── HEAD_OF_AFFILIATES_JOB_DESCRIPTION.md
│   ├── SEO_MANAGER.md
│   ├── SEO_MANAGER_JOB_DESCRIPTION.md
│   ├── SEO_WHITE_HAT_ANALYST.md
│   ├── SEO_WHITE_HAT_ANALYST_JOB_DESCRIPTION.md
│   ├── SEO_GREY_HAT_ANALYST.md
│   ├── SEO_GREY_HAT_ANALYST_JOB_DESCRIPTION.md
│   ├── SEO_BLACK_HAT_ANALYST.md
│   ├── SEO_BLACK_HAT_ANALYST_JOB_DESCRIPTION.md
│   ├── RELEASE_MANAGER.md
│   ├── RELEASE_MANAGER_JOB_DESCRIPTION.md
│   ├── PRODUCT_MANAGER_JOB_DESCRIPTION.md
│   └── ... (all persona files)
├── skills/                     # Skills files
│   ├── DIRECTOR_SKILLS.md
│   ├── SEO_MANAGER_SKILLS.md
│   ├── SEO_WHITE_HAT_ANALYST_SKILLS.md
│   ├── SEO_GREY_HAT_ANALYST_SKILLS.md
│   ├── SEO_BLACK_HAT_ANALYST_SKILLS.md
│   ├── RELEASE_MANAGER_SKILLS.md
│   └── ... (all skills files)
│   └── prompts/                # Role Lock Prompts + Character Sheets
│       ├── HEAD_OF_ANALYTICS_PROMPT.md
│       ├── HEAD_OF_ANALYTICS_SHEET.md
│       ├── HEAD_OF_TECH_PROMPT.md
│       ├── HEAD_OF_TECH_SHEET.md
│       ├── HEAD_OF_SEO_PROMPT.md
│       ├── HEAD_OF_SEO_SHEET.md
│       ├── HEAD_OF_AFFILIATES_PROMPT.md
│       ├── HEAD_OF_AFFILIATES_SHEET.md
│       ├── SEO_MANAGER_PROMPT.md
│       ├── SEO_MANAGER_SHEET.md
│       ├── SEO_WHITE_HAT_ANALYST_PROMPT.md
│       ├── SEO_WHITE_HAT_ANALYST_SHEET.md
│       ├── SEO_GREY_HAT_ANALYST_PROMPT.md
│       ├── SEO_GREY_HAT_ANALYST_SHEET.md
│       ├── SEO_BLACK_HAT_ANALYST_PROMPT.md
│       ├── SEO_BLACK_HAT_ANALYST_SHEET.md
│       ├── RELEASE_MANAGER_PROMPT.md
│       ├── RELEASE_MANAGER_SHEET.md
│       ├── PRODUCT_MANAGER_PROMPT.md
│       ├── PRODUCT_MANAGER_SHEET.md
│       └── ... (all prompts)
├── learnings/                  # Learning files
├── logs/                       # Activity logs
├── tools/                      # Utility scripts
├── sessions/                   # Session tracking
├── projects/                   # Project folders
└── governance/                 # Governance documents
```

---

## Change Log

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-12 | Initial team configuration |
| 1.1 | 2026-01-19 | Added Head of Post Production, UX/UI Designer |
| 1.4 | 2026-01-23 | Added real-time logging, context loading rules |
| **2.0** | **2026-01-27** | **Major Reorganization:** |
| | | - Director role redefined (oversight only, no execution) |
| | | - Elias Thorne → Head of Analytics (Leadership) |
| | | - Tech Lead → Head of Tech (Leadership) |
| | | - SEO Commander → Head of SEO (Leadership) |
| | | - Affiliate Manager → Head of Affiliates (Leadership, Advisory) |
| | | - Head of Asset Strategy (Leadership, Advisory) |
| | | - Head of Product → Product Manager (under Head of SEO) |
| | | - Created SEO Manager role |
| | | - Created SEO White-hat Analyst role |
| | | - Created SEO Grey-hat Analyst role |
| | | - Created SEO Black-hat Analyst role |
| | | - Created Release Manager role |
| | | - PixelPerfect moved under Product Manager |
| | | - Post Production Manager moved under Head of SEO |
| | | - Full documentation for all 20 personas |

---

*BlackTeam v2.0 | Paradise Media Group | Updated 2026-01-27*
