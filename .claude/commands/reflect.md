# /reflect - Virtual ATeam Learning & Skills Tracker (v2.0)

Capture and consolidate learnings, skills, and insights from this session for the Virtual ATeam personas.

## Phase 0: RAG Context Loading (MANDATORY)

**Load existing learnings from RAG before capturing new ones.**

**RAG Query:**
```python
from AS-Virtual_Team_System_v2.rag.rag_client import VTeamRAG
rag = VTeamRAG()
learnings = rag.query("session learnings corrections", collection_name="learnings", top_k=5)
```

---

## Team Locations

| Team | Local Path | System v2 Path |
|------|------------|----------------|
| **BlackTeam** | `~/virtual-ateam/BlackTeam/` | `~/AS-Virtual_Team_System_v2/blackteam/` |
| **WhiteTeam** | N/A (use v2) | `~/AS-Virtual_Team_System_v2/whiteteam/` |

**Note:** BlackTeam uses local markdown files. WhiteTeam uses v2 system with optional database logging.

---

## BlackTeam Personas (23)

| ID | Persona | Role |
|----|---------|------|
| DIR | The Director | Oversight Only |
| DF | DataForge | Data Engineer |
| CG | CodeGuard | Code Reviewer |
| ET | Elias Thorne | ML Engineer |
| BID | DataViz | BI Developer |
| DA | Insight | Data Analyst |
| SEO | SEO Commander | Head of SEO |
| HOC | Head of Content | Content Leadership |
| HOP | Head of Product | Product & NavBoost |
| HAS | Head of Asset Strategy | Asset Portfolio |
| HPPM | Head of Post Production | QA Leadership |
| PPM | Post Production Manager | Production Ops |
| AM | Affiliate Manager | Partnerships |
| UXD | PixelPerfect | UX/UI Design |
| TL | Tech Lead | Infrastructure |
| RM | Release Manager | Deployment |
| SM | SEO Manager | SEO Operations |
| SWH | SEO White-hat | Ethical SEO |
| SGH | SEO Grey-hat | Aggressive SEO |
| SBH | SEO Black-hat | Defense/Recovery |
| CM | Content Manager | Content Production |
| CA | Content Architect | Schema Design |
| CQA | Content QA | Quality Validation |

## WhiteTeam Personas (24)

| Code | Persona | Role |
|------|---------|------|
| W-WOL | Wol | Director (Strategic) |
| W-NINA | Nina | Head of Analytics |
| W-JACK | Jack | Head of SEO |
| W-HUGO | Hugo | Head of Content |
| W-TESS | Tess | Head of Post Production |
| W-IVAN | Ivan | Head of Tech |
| W-FLUX | Flux | DataForge (Data Engineer) |
| W-SVEN | Sven | CodeGuard (Code Reviewer) |
| W-NOVA | Nova | ML Engineer |
| W-DASH | Dash | BI Developer |
| W-IRIS | Iris | Data Analyst |
| W-GARD | Gabriel | Guardian (Security) |
| W-JADE | Jade | PixelPerfect (UX/UI) |
| W-LUNA | Luna | SEO Commander |
| W-LEXI | Lexi | SEO Manager |
| W-EVAN | Evan | SEO White-hat |
| W-ASH | Ash | SEO Grey-hat |
| W-ROOK | Rook | SEO Black-hat |
| W-MAYA | Maya | Head of Asset Strategy |
| W-MILE | Miles | Content Manager |
| W-VERA | Vera | Content Architect |
| W-FINN | Finn | Affiliate Manager |
| W-COLE | Cole | Post Production Manager |
| W-KYLE | Kyle | Release Manager |

---

## Your Task

Analyze this conversation session and perform the following reflection:

### 1. Identify Active Persona(s) and Team

Determine which Virtual ATeam persona(s) were engaged in this session:
- **Team:** BlackTeam, WhiteTeam, or Cross-Team
- **Persona(s):** Based on work type, terminology, and methodologies

**Routing Rules:**
| Keywords | BlackTeam | WhiteTeam |
|----------|-----------|-----------|
| Director orchestration | DIR | W-WOL |
| Data pipeline, ETL | DF | W-FLUX |
| Code review, PR | CG | W-SVEN |
| ML, prediction | ET | W-NOVA |
| SEO, keywords | SEO | W-LUNA |
| Content strategy | HOC | W-HUGO |
| Security, incidents | - | W-GARD |

### 2. Capture Session Intelligence

For EACH active persona, extract and categorize:

**SKILLS DEMONSTRATED**
- New techniques or capabilities shown
- Tools or methods applied effectively
- Domain expertise exhibited

**LEARNINGS & INSIGHTS**
- New knowledge gained about the codebase/project
- Process improvements discovered
- Domain-specific insights acquired
- Patterns or anti-patterns identified

**MISTAKES & CORRECTIONS**
- Errors made during the session
- How they were identified and resolved
- Prevention strategies for the future

**TEAM INTERACTIONS** (if applicable)
- Cross-persona collaboration that occurred
- Cross-team collaboration (BlackTeam ↔ WhiteTeam)
- Handoffs or reviews between team members
- Shared learnings applicable to multiple personas

### 3. Update Files (Team-Specific)

#### BlackTeam Files

**Canonical Locations:**
- **Skills:** `~/virtual-ateam/BlackTeam/skills/`
- **Learnings:** `~/virtual-ateam/BlackTeam/learnings/`

**Per-Persona Files:**
- `[PERSONA]_SKILLS.md` - Cumulative skills inventory
- `[PERSONA]_LEARNINGS.md` - Session-by-session log

**Team File:**
- `TEAM_LEARNINGS.md` - WINS, LOSSES, CROSS-TEAM INSIGHTS

#### WhiteTeam Files

**Canonical Locations:**
- **Skills:** `~/AS-Virtual_Team_System_v2/whiteteam/skills/`
- **Learnings:** `~/AS-Virtual_Team_System_v2/whiteteam/learnings/`

**Per-Persona Files:**
- `[PERSONA]_SKILLS.md` - Cumulative skills inventory
- `[PERSONA]_LEARNINGS.md` - Session-by-session log (create if needed)

**Team File:**
- `TEAM_LEARNINGS.md` - WINS, LOSSES, CROSS-TEAM INSIGHTS

### 4. Log to Virtual ATeam System v2 API (Optional)

When the ATeam API is available, also log learnings to the database:

```bash
# Source config
source ~/.config/ateam/config.env

# Log a learning
curl -X POST "$ATEAM_API_URL/tool/log_learning" \
  -H "X-API-Key: $ATEAM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "persona_code": "W-WOL",
    "learning_type": "win",
    "title": "Session Learning Title",
    "description": "Detailed description of the learning",
    "tags": ["security", "deployment"]
  }'
```

**Learning Types:**
- `skill` - New capability demonstrated
- `win` - Successful outcome
- `loss` - Mistake or failure
- `insight` - Process improvement
- `cross_team` - Multi-team learning

### 5. Deduplication (MANDATORY)

Before appending ANY skill or learning:

```bash
# Check BlackTeam skills
grep -i "skill_name" ~/virtual-ateam/BlackTeam/skills/[PERSONA]_SKILLS.md

# Check WhiteTeam skills
grep -i "skill_name" ~/AS-Virtual_Team_System_v2/whiteteam/skills/[PERSONA]_SKILLS.md
```

**Rules:**
1. READ existing file FIRST before appending
2. Normalize skill names (lowercase) for comparison
3. If skill exists with similar wording, DO NOT add duplicate
4. If skill exists but session adds nuance, UPDATE existing entry
5. For learnings, always append (dated entries) but avoid duplicate insights

### 6. Output Format

```
## Reflection Complete

### Team(s) Active: [BlackTeam/WhiteTeam/Cross-Team]
### Persona(s) Active: [List with codes]

### Skills Captured:
- [Skill 1]
- [Skill 2]

### Key Learnings:
- [Learning 1]
- [Learning 2]

### Corrections Logged:
- [If any]

### Files Updated:
- [List of files modified]

### API Logged:
- [If v2 API used: Yes/No]
- [Learnings logged: Count]
```

---

## File Structure Reference

### BlackTeam (Local Markdown)

```
~/virtual-ateam/BlackTeam/
├── skills/                         # 18 skill files
│   ├── TECH_LEAD_SKILLS.md
│   ├── CODEGUARD_SKILLS.md
│   ├── DATAFORGE_SKILLS.md
│   └── ...
└── learnings/                      # 17 learning files
    ├── TECH_LEAD_LEARNINGS.md
    ├── TEAM_LEARNINGS.md
    └── ...
```

### WhiteTeam (v2 System)

```
~/AS-Virtual_Team_System_v2/whiteteam/
├── skills/                         # 25 skill files + 57 prompts
│   ├── SKILLS_INDEX.md
│   ├── TECH_LEAD_SKILLS.md
│   └── prompts/
│       ├── DIRECTOR_PROMPT.md
│       └── ...
└── learnings/                      # 2 files (24 planned)
    ├── LEARNINGS_INDEX.md
    └── TEAM_LEARNINGS.md
```

### Database Schema (v2)

```sql
-- learnings table
CREATE TABLE learnings (
    id UUID PRIMARY KEY,
    team_id UUID REFERENCES teams(id),
    persona_id UUID REFERENCES personas(id),
    learning_type VARCHAR(30), -- 'skill', 'win', 'loss', 'insight', 'cross_team'
    title VARCHAR(200),
    description TEXT,
    tags TEXT[],
    created_at TIMESTAMP
);
```

---

## Cross-Team Reflection

When a session involves both BlackTeam and WhiteTeam personas:

1. **Identify primary team** - Which team led the work?
2. **Log to both** - Update files for both teams
3. **Mark as cross-team** - Use `cross_team` learning type
4. **Link entries** - Reference the other team's entry

Example cross-team entry:
```markdown
#### 2026-01-30 - ATeam System v2 Integration (Cross-Team)
**Persona(s):** Head of Tech (BlackTeam), W-WOL (WhiteTeam)
**Cross-Team:** Yes - First documented BlackTeam ↔ WhiteTeam collaboration
**Win:** [Description]
```

---

## Important Notes

- Always READ existing files before appending to avoid duplicates
- Use ISO date format (YYYY-MM-DD) for all timestamps
- Keep entries concise but actionable
- Cross-reference related learnings across personas and teams
- Flag any learnings that should update persona definition files
- For WhiteTeam, create per-persona learning files as needed (only INDEX and TEAM exist initially)
- **v2 API logging is optional** - markdown files are primary storage
