# /news_update_agent - Bedrock Agent News Update System

Multi-project news aggregation system for all bedrock_agent sports verticals with Ralph Loops quality assurance.

## Phase 0: RAG Context Loading (MANDATORY)

**Load relevant context from the RAG system before news updates.**

Read these files for prior learnings:
- `~/AS-Virtual_Team_System_v2/blackteam/skills/learnings/` — Latest team learnings

**RAG Query:**
```python
from AS-Virtual_Team_System_v2.rag.rag_client import VTeamRAG
rag = VTeamRAG()
context = rag.query("news update agent sports content", top_k=5)
learnings = rag.query("news content quality corrections", collection_name="learnings", top_k=3)
```

---

## Usage

```
/news_update_agent                      # Show available projects
/news_update_agent all                  # Update news for ALL projects
/news_update_agent wc2026               # World Cup 2026 only
/news_update_agent premier-league       # Premier League only
/news_update_agent serie-a              # Italian Serie A only
/news_update_agent bundesliga           # Bundesliga only
/news_update_agent ligue1               # French Ligue 1 only
/news_update_agent tennis               # Tennis Grand Slams only
/news_update_agent six-nations          # Six Nations Rugby only
/news_update_agent f1                   # Formula 1 only
/news_update_agent status               # Check status of all projects
/news_update_agent --dry-run [project]  # Test run without saving
```

Arguments: $ARGUMENTS

---

## Supported Projects

| Project ID | Name | Path | News Sources |
|------------|------|------|--------------|
| `wc2026` | World Cup 2026 | `WC_2026_Astro` | FIFA, ESPN, BBC Sport |
| `premier-league` | Premier League 2025-26 | `Premier_League_2025-26_Astro` | Sky Sports, BBC Sport, ESPN |
| `serie-a` | Italian Serie A | `Italian_Serie_A_Astro` | Football Italia, ESPN, Goal |
| `bundesliga` | Bundesliga 2025-26 | `Bundesliga_2025-26_Astro_V2` | Bundesliga.com, Kicker, ESPN |
| `ligue1` | Ligue 1 2025-26 | `Ligue_1_2025-26_Astro` | L'Equipe, ESPN, BBC Sport |
| `tennis` | Tennis Grand Slams | `Tennis_Grand_Slams_Astro` | ATP, WTA, ESPN, Tennis.com |
| `six-nations` | Six Nations 2026 | `Six_Nations_2026_Astro` | Six Nations Rugby, BBC Sport |
| `f1` | Formula 1 2026 | `F1_2026_Astro` | F1.com, Autosport, Motorsport |

**Base Path:** `/home/andre/BI-AI_Agents_REPO/bedrock_agent/`

---

## Quality Assurance: Ralph Loops (4 Cycles)

All news articles MUST pass 4 quality review cycles:

| Cycle | Reviewer | Focus | Threshold |
|-------|----------|-------|-----------|
| 1 | **Director** | Fact-checking, source verification | 80+ |
| 2 | **Head of Content** | Quality, readability, structure | 80+ |
| 3 | **SEO Commander + PPM** | SEO optimization, validation | 80+ |
| 4 | **ALL THREE** | Internal link verification | 0 broken |

---

## CRITICAL RULES

1. **ONLY add REAL news** - Never invent or fabricate articles
2. **Source verification** - All news must come from trusted sources
3. **Fact-checking** - Cross-reference with official sources
4. **No placeholders** - No TBD, TODO, or Lorem ipsum content
5. **Working links** - All internal links must be valid
6. **Valid images** - All images must exist and be properly linked
7. **If no news exists, add nothing** - Zero additions is acceptable
8. **Project-specific sources** - Use only sources relevant to each vertical

---

## Trusted News Sources by Vertical

### Football (WC2026, Premier League, Serie A, Bundesliga)
- FIFA.com (Official - WC only)
- UEFA.com
- ESPN FC
- BBC Sport
- Sky Sports
- Goal.com
- The Guardian Football
- Reuters Sports
- AP News Sports

### Premier League Specific
- premierleague.com (Official)
- Sky Sports Premier League
- BBC Sport Football

### Serie A Specific
- legaseriea.it (Official)
- Football Italia
- Gazzetta dello Sport

### Bundesliga Specific
- bundesliga.com (Official)
- Kicker
- Sport1

### Ligue 1 Specific
- ligue1.com (Official)
- L'Equipe
- RMC Sport
- France Football
- So Foot

### Tennis
- atptour.com (Official ATP)
- wtatennis.com (Official WTA)
- ausopen.com, rolandgarros.com, wimbledon.com, usopen.org (Slams)
- Tennis.com
- ESPN Tennis

### Six Nations Rugby
- sixnationsrugby.com (Official)
- BBC Sport Rugby
- Rugby World
- World Rugby

### Formula 1
- formula1.com (Official)
- Autosport
- Motorsport.com
- RaceFans
- The Race

---

## Execution Process

### Step 1: Parse Arguments

Based on `$ARGUMENTS`:
- No args or empty: Show project list and ask which to update
- `all`: Queue all projects for update
- `[project-id]`: Update specific project
- `status`: Show status of all projects
- `--dry-run [project]`: Test mode

### Step 2: For Each Selected Project

```bash
# Set project path
BASE_PATH="/home/andre/BI-AI_Agents_REPO/bedrock_agent"
PROJECT_PATH="$BASE_PATH/[PROJECT_FOLDER]"

# Check if news script exists
if [ -f "$PROJECT_PATH/scripts/news_update.py" ]; then
    python3 "$PROJECT_PATH/scripts/news_update.py" --manual
else
    # Use generic news fetcher
    python3 "$BASE_PATH/scripts/generic_news_fetcher.py" --project [project-id]
fi
```

### Step 3: Ralph Loops QA (Per Article)

#### Cycle 1: Director Review
```
Checks:
- [ ] Has valid source citation with URL
- [ ] Source is from trusted news outlet for this vertical
- [ ] Has proper publication date (within 7 days)
- [ ] No placeholder text (TBD, TODO, etc.)
- [ ] Title is specific and meaningful
- [ ] Content is factually accurate
```

#### Cycle 2: Content Review
```
Checks:
- [ ] Adequate content length (500+ characters)
- [ ] Proper markdown structure with headers
- [ ] All internal links are valid
- [ ] Valid markdown syntax
- [ ] Has summary section
- [ ] Appropriate tone for sports journalism
```

#### Cycle 3: SEO/QA Review
```
Checks:
- [ ] Summary is SEO meta-ready (under 300 chars)
- [ ] Has category/sport tag
- [ ] All images exist and are linked
- [ ] Title contains relevant keywords
- [ ] Filename is URL-friendly
- [ ] No duplicate content across projects
```

#### Cycle 4: Internal Link Gate
```
Checks:
- [ ] ALL internal links return 200
- [ ] No broken image links
- [ ] Cross-links to related content work
- HARD GATE: Must pass with 0 broken links
```

### Step 4: Report Results

```markdown
## News Update Agent Report

**Date:** [Date]
**Time:** [Time]
**Trigger:** Manual via /news_update_agent

### Projects Updated

| Project | Fetched | Passed QA | Added | Rejected |
|---------|---------|-----------|-------|----------|
| WC 2026 | X | X | X | X |
| Premier League | X | X | X | X |
| Serie A | X | X | X | X |
| ... | ... | ... | ... | ... |
| **TOTAL** | **X** | **X** | **X** | **X** |

### Ralph Loops Summary
- Cycle 1 (Director): X/X passed
- Cycle 2 (Content): X/X passed
- Cycle 3 (SEO/QA): X/X passed
- Cycle 4 (Links): X/X passed (0 broken)

### Rejected Articles
[List by project with rejection reasons]

### Git Status
- Branch: main
- Commits: [list]
- Pushed: Yes/No

---
News Update Agent v1.0 | Bedrock Agent System
```

---

## Project Paths Reference

| Project | News Output | Images | QA Reports |
|---------|-------------|--------|------------|
| WC 2026 | `WC_2026_Astro/src/content/news/` | `WC_2026_Astro/public/images/news/` | - |
| Premier League | `Premier_League_2025-26_Astro/src/content/news/` | `Premier_League_2025-26_Astro/public/images/news/` | - |
| Serie A | `Italian_Serie_A_Astro/src/content/news/` | `Italian_Serie_A_Astro/public/images/news/` | - |
| Bundesliga | `Bundesliga_2025-26_Astro_V2/src/content/news/` | `Bundesliga_2025-26_Astro_V2/public/images/news/` | - |
| Ligue 1 | `Ligue_1_2025-26_Astro/src/content/news/` | `Ligue_1_2025-26_Astro/public/images/news/` | - |
| Tennis | `Tennis_Grand_Slams_Astro/src/content/news/` | `Tennis_Grand_Slams_Astro/public/images/news/` | - |
| Six Nations | `Six_Nations_2026_Astro/src/content/news/` | `Six_Nations_2026_Astro/public/images/news/` | - |
| F1 | `F1_2026_Astro/src/content/news/` | `F1_2026_Astro/public/images/news/` | - |

---

## Status Command

When `status` is passed, show:

```bash
# For each project, show:
# 1. Total news articles
# 2. Last update date
# 3. News from last 7 days

for project in wc2026 premier-league serie-a bundesliga ligue1 tennis six-nations f1; do
    echo "=== $project ==="
    # Count files, show last modified, etc.
done
```

---

## Cron Integration

This agent can be scheduled:

```bash
# Daily at 12:00 PM - Update all projects
0 12 * * * /home/andre/BI-AI_Agents_REPO/bedrock_agent/scripts/news_update_all.sh

# Individual project schedules (if needed)
0 8 * * * /path/to/news_update.sh wc2026
0 9 * * * /path/to/news_update.sh premier-league
```

---

## Notes

- Always confirm with user before pushing to main
- Each project may have different news frequencies
- Some projects may have no news on certain days - this is OK
- Cross-check for duplicate stories across verticals
- Email report sent to: andre@paradisemedia.com
- Part of the Bedrock Agent ecosystem

---

*News Update Agent v1.1 | Bedrock Agent System | Paradise Media Group*
*Updated: 2026-02-02 - Added Ligue 1 support*
