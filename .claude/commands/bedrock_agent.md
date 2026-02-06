# /bedrock_agent - Content Vertical Generator

Create and manage content verticals using The_Agent framework.

---

## Phase 0: RAG Context Loading (MANDATORY)

**Load relevant context from the RAG system before content generation.**

Read these files for prior learnings and corrections:
- `~/pitaya/knowledge/feedback_corrections.md` — Data accuracy rules, R-DATA-07 numerical validation
- `~/AS-Virtual_Team_System_v2/blackteam/skills/learnings/` — Latest team learnings

**RAG Query:**
```python
from AS-Virtual_Team_System_v2.rag.rag_client import VTeamRAG
rag = VTeamRAG()
context = rag.query("bedrock agent content vertical", top_k=5)
learnings = rag.query("content generation corrections", collection_name="learnings", top_k=3)
rules = rag.query("content standards quality gates", collection_name="rules", top_k=3)
```

---

## ⛔ MANDATORY WORKFLOW ENFORCEMENT ⛔

**STOP. READ THIS FIRST. NO EXCEPTIONS.**

Before executing ANY bedrock_agent command, you MUST follow this workflow. Skipping steps is NOT allowed.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    BEDROCK AGENT EXECUTION PROTOCOL                         │
│                         (NON-NEGOTIABLE)                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  STEP 1: BLACKTEAM BRIEF (MANDATORY)                                        │
│  ────────────────────────────────────                                       │
│  • Generate Project Tracking ID: BT-YYYY-NNN                                │
│  • Create Project Brief with scope, assignments, quality gates              │
│  • Assign ALL team personas to work streams                                 │
│  • Present brief to user for approval                                       │
│                                                                             │
│  STEP 2: TEAM EXECUTION (MANDATORY)                                         │
│  ──────────────────────────────────                                         │
│  • Head of Content → Editorial standards, voice, accuracy                   │
│  • SEO Commander → H1/H2 structure, keywords, meta tags                     │
│  • PixelPerfect → Visual QA, accessibility, design system                   │
│  • DataForge → Data pipelines, JSON files, scraping                         │
│  • Post Production → Links, images, functional testing                      │
│  • Elias Thorne → ML models, ratings, algorithms                            │
│  • Insight → Data quality, coverage gaps                                    │
│                                                                             │
│  STEP 3: 5 RALPH LOOPS QA (MANDATORY)                                       │
│  ────────────────────────────────────                                       │
│  • Loop 1: Content Quality (Head of Content) - 85+ to pass                  │
│  • Loop 2: SEO Optimization (SEO Commander) - 85+ to pass                   │
│  • Loop 3: Technical QA (Post Production) - 90+ to pass                     │
│  • Loop 4: UX/UI Review (PixelPerfect) - 85+ to pass                        │
│  • Loop 5: Data Validation (Elias + Insight) - 85+ to pass                  │
│                                                                             │
│  STEP 4: RELEASE APPROVAL (MANDATORY)                                       │
│  ────────────────────────────────────                                       │
│  • Generate Release Notes with all changes                                  │
│  • Post Production Manager reviews                                          │
│  • Director final approval                                                  │
│  • Add ClickUp comment to task                                              │
│                                                                             │
│  STEP 5: GIT + DEPLOY (MANDATORY)                                           │
│  ────────────────────────────────                                           │
│  • Git commit with proper message                                           │
│  • Push to GitHub                                                           │
│  • Create Astro version for production                                      │
│  • Deploy to Vercel                                                         │
│  • Update hub/index.html                                                    │
│                                                                             │
│  STEP 6: REFLECT (MANDATORY)                                                │
│  ──────────────────────────                                                 │
│  • Invoke /reflect to capture learnings                                     │
│  • Update skills and learnings files                                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Workflow Checklist (MUST complete ALL)

```
PRE-EXECUTION CHECKLIST
═══════════════════════════════════════════════════════════════════════════════
☐ BlackTeam Brief created with Project ID
☐ All team personas assigned to work streams
☐ User approved the brief before execution
☐ Content generated following team standards
☐ Loop 1 passed: Content Quality (85+)
☐ Loop 2 passed: SEO Optimization (85+)
☐ Loop 3 passed: Technical QA (90+)
☐ Loop 4 passed: UX/UI Review (85+)
☐ Loop 5 passed: Data Validation (85+)
☐ Release Notes generated and approved
☐ Director final approval obtained
☐ Git committed and pushed to GitHub
☐ Astro version created
☐ Deployed to Vercel
☐ /reflect invoked to capture learnings
═══════════════════════════════════════════════════════════════════════════════

⚠️  IF ANY CHECKBOX IS UNCHECKED, DO NOT PROCEED TO NEXT STEP
⚠️  IF USER REQUESTS TO SKIP STEPS, EXPLAIN WHY THIS IS NOT ALLOWED
⚠️  QUALITY OVER SPEED - ALWAYS
```

### Why This Matters

1. **Consistency** - Every project follows the same standards
2. **Quality** - 5 QA loops catch issues before production
3. **Team Knowledge** - Personas bring specialized expertise
4. **Traceability** - Project IDs link to ClickUp and learnings
5. **Deployment** - Vercel deployment is automatic, not optional
6. **Learning** - /reflect captures improvements for future projects

---

## Project Reference

- **Project ID:** BT-2026-004
- **Base Path:** `/home/andre/BI-AI_Agents_REPO/bedrock_agent/`
- **Framework:** `bedrock_agent/The_Agent/`
- **Docs:** `bedrock_agent/The_Agent/docs/`
- **Reference:** WC_2026_Project (3,523 files)
- **GitHub:** [ParadiseMediaOrg/BI-AI_Agents_REPO](https://github.com/ParadiseMediaOrg/BI-AI_Agents_REPO/tree/main/bedrock_agent)

---

## What is a Vertical?

A **Vertical** is a content category - the broad topic area your project covers.

```
VERTICAL HIERARCHY
==================
Vertical (Category)     → Sports, Politics, Gaming, Entertainment
    └── Sub-category    → Football, Rugby, Tennis, Golf, Darts...
        └── Scope       → Local, National, International
            └── Title   → Serie A, Bundesliga, World Cup 2026...
```

**Examples:**
| Vertical | Sub-category | Scope | Title |
|----------|--------------|-------|-------|
| Sports | Football | International | FIFA World Cup 2026 |
| Sports | Football | Local | Serie A (Italy) |
| Sports | Football | Local | Bundesliga (Germany) |
| Sports | Tennis | International | Grand Slams |
| Gaming | Esports | International | League of Legends Worlds |

---

## Commands

```
/bedrock_agent new                      # Create new project (interactive wizard)
/bedrock_agent configure [project]      # Edit existing project config
/bedrock_agent generate [project]       # Generate content & HTML website
/bedrock_agent status [project]         # Check progress & file counts
/bedrock_agent qa [project]             # Run quality checks
/bedrock_agent version [project]        # Create archived version
/bedrock_agent list                     # List all projects
```

**Arguments:** $ARGUMENTS

---

## Interactive Wizard

When running `/bedrock_agent new`, guide the user through these questions using `AskUserQuestion`. Make each question clear with examples.

### Question 1: Vertical Category

```
What vertical (content category) is this project for?

┌───────────────┬─────────────────────────────────────────┐
│ Vertical      │ Examples                                │
├───────────────┼─────────────────────────────────────────┤
│ Sports        │ Football leagues, Tennis, Golf, MMA     │
│ Politics      │ Elections, Parliament, Local councils   │
│ Gaming        │ Esports, Casino, Video games            │
│ Entertainment │ Film, Music, Celebrity news             │
│ Business      │ Finance, Markets, Industry news         │
│ Travel        │ Destinations, Hotels, Reviews           │
│ Other         │ Custom category                         │
└───────────────┴─────────────────────────────────────────┘
```

### Question 2: Sub-category (Based on Vertical)

**If Sports:**
```
What sport does this cover?

┌─────────────┬──────────────────────────────────────────┐
│ Sport       │ Popular competitions                     │
├─────────────┼──────────────────────────────────────────┤
│ Football    │ World Cup, Serie A, Premier League       │
│ Rugby       │ Six Nations, World Cup, Super Rugby      │
│ Tennis      │ Grand Slams, ATP/WTA Tours               │
│ Golf        │ PGA Tour, Majors, Ryder Cup              │
│ Darts       │ PDC World Championship, Premier League   │
│ Basketball  │ NBA, EuroLeague, FIBA                    │
│ Formula 1   │ F1 World Championship                    │
│ MMA         │ UFC, Bellator, ONE Championship          │
│ Cricket     │ World Cup, IPL, The Ashes                │
│ Other       │ Specify your sport                       │
└─────────────┴──────────────────────────────────────────┘
```

**If Gaming:**
```
What type of gaming content?

┌─────────────┬──────────────────────────────────────────┐
│ Type        │ Examples                                 │
├─────────────┼──────────────────────────────────────────┤
│ Esports     │ LoL Worlds, CS2 Majors, Dota TI          │
│ Casino      │ Online casinos, Poker tournaments        │
│ Video Games │ Game reviews, News, Guides               │
│ Other       │ Specify your type                        │
└─────────────┴──────────────────────────────────────────┘
```

**If Politics:**
```
What level of political coverage?

┌─────────────┬──────────────────────────────────────────┐
│ Level       │ Examples                                 │
├─────────────┼──────────────────────────────────────────┤
│ Local       │ City councils, Regional elections        │
│ National    │ Parliament, Federal elections            │
│ International│ EU, UN, Geopolitics                     │
│ Other       │ Specify your focus                       │
└─────────────┴──────────────────────────────────────────┘
```

### Question 3: Geographic Scope

```
What is the geographic scope?

┌───────────────┬────────────────────────────────────────┐
│ Scope         │ Examples                               │
├───────────────┼────────────────────────────────────────┤
│ Local         │ Serie A (Italy), Bundesliga (Germany)  │
│               │ English Premier League, La Liga        │
│               │ Single country/region focus            │
├───────────────┼────────────────────────────────────────┤
│ National      │ US Open (Tennis), FA Cup               │
│               │ Country-wide but not single league     │
├───────────────┼────────────────────────────────────────┤
│ International │ FIFA World Cup, Olympics               │
│               │ Champions League, Grand Slams          │
│               │ Multiple countries participating       │
└───────────────┴────────────────────────────────────────┘
```

### Question 4: Tournament/League Title

```
What is the official title of this tournament or league?

Examples:
• "FIFA World Cup 2026"
• "Serie A 2025-26"
• "Bundesliga 2025-26"
• "English Premier League"
• "ATP Tour 2026"
• "PDC World Championship"

Enter the title:
```

### Question 5: Country (If Local/National Scope)

*Only asked if scope is Local or National*

```
Which country is this based in?

┌─────────────┬──────────────────────────────────────────┐
│ Country     │ Popular leagues/tournaments              │
├─────────────┼──────────────────────────────────────────┤
│ Italy       │ Serie A, Coppa Italia                    │
│ Germany     │ Bundesliga, DFB-Pokal                    │
│ England     │ Premier League, FA Cup                   │
│ Spain       │ La Liga, Copa del Rey                    │
│ France      │ Ligue 1, Coupe de France                 │
│ USA         │ MLS, US Open (Tennis)                    │
│ Other       │ Specify country                          │
└─────────────┴──────────────────────────────────────────┘
```

### Question 6: Content Style

```
What content style do you want?

┌──────────────────┬───────────────────────────────────────┐
│ Style            │ Description                           │
├──────────────────┼───────────────────────────────────────┤
│ Sports Journalism│ Match reports, player interviews,     │
│                  │ transfer news, expert analysis        │
├──────────────────┼───────────────────────────────────────┤
│ Statistical      │ Data-driven, stats tables, rankings,  │
│                  │ comparison tools, analytics           │
├──────────────────┼───────────────────────────────────────┤
│ Travel & Venue   │ Stadium guides, city info, fan        │
│                  │ travel tips, hospitality              │
├──────────────────┼───────────────────────────────────────┤
│ Encyclopedia     │ Wikipedia-style factual pages,        │
│                  │ historical records, profiles          │
├──────────────────┼───────────────────────────────────────┤
│ Mixed            │ Combination of above styles           │
│                  │ (like WC 2026 project)                │
└──────────────────┴───────────────────────────────────────┘
```

### Question 7: News Section

```
Do you want an automated News Section?

┌─────────┬─────────────────────────────────────────────────┐
│ Option  │ What happens                                    │
├─────────┼─────────────────────────────────────────────────┤
│ Yes     │ • News scraping pipeline configured             │
│         │ • Cron job for daily updates                    │
│         │ • Sources: Google News, RSS feeds, APIs         │
│         │ • Auto-generated news articles                  │
│         │ • Example: WC 2026, Serie A projects            │
├─────────┼─────────────────────────────────────────────────┤
│ No      │ • Static content only                           │
│         │ • Manual updates when needed                    │
│         │ • Lower maintenance                             │
└─────────┴─────────────────────────────────────────────────┘
```

### Question 8: Content Scope

```
How much content do you want to create?

┌─────────────┬─────────┬─────────┬──────────────────────────┐
│ Size        │ Players │ Teams   │ Best for                 │
├─────────────┼─────────┼─────────┼──────────────────────────┤
│ Starter     │ 20      │ 10      │ Quick MVP, testing       │
│ Standard    │ 50      │ 20      │ Single tournament/league │
│ Complete    │ 100     │ 32      │ Full coverage            │
│ Enterprise  │ 150+    │ 48+     │ WC 2026 scale            │
│ Custom      │ ?       │ ?       │ You specify              │
└─────────────┴─────────┴─────────┴──────────────────────────┘
```

---

## Wizard Summary

After all questions, display confirmation:

```
PROJECT CONFIGURATION SUMMARY
═════════════════════════════════════════════════════════════

Vertical:       Sports
Sub-category:   Football
Scope:          Local
Title:          Serie A 2025-26
Country:        Italy
Content Style:  Sports Journalism + Statistical
News Section:   Yes (auto-scraping enabled)
Content Scope:  Standard (50 players, 20 teams)

Project folder: /home/andre/BI-AI_Agents_REPO/bedrock_agent/Serie_A_2025-26/

═════════════════════════════════════════════════════════════

Proceed with this configuration? (Yes / Edit / Cancel)
```

---

## Generated Output

After wizard completion, create:

```
/home/andre/BI-AI_Agents_REPO/bedrock_agent/{Project_Name}/
├── main/                           # Working directory
│   ├── config/
│   │   └── vertical.json           # Master config
│   ├── data/
│   ├── output/
│   │   ├── index.html              # Docsify website
│   │   ├── _sidebar.md             # Navigation
│   │   ├── README.md               # Homepage
│   │   ├── latest_news.md          # News feed (if enabled)
│   │   ├── players/
│   │   │   ├── current/            # Active players
│   │   │   └── legends/            # Historic greats
│   │   ├── teams/
│   │   ├── tournaments/
│   │   ├── venues/
│   │   ├── news/                   # News articles (if enabled)
│   │   └── comparison/dynamic/     # Comparison tool
│   ├── scripts/
│   │   └── news_scraper.py         # News pipeline (if enabled)
│   └── qa/
├── Version_1.0/                    # First release
│   └── RELEASE_NOTES.md
├── docs/
└── VERSION.md
```

---

## vertical.json Configuration

Generated config file structure:

```json
{
  "project": {
    "name": "Serie A 2025-26",
    "slug": "Serie_A_2025-26",
    "created": "2026-01-20",
    "version": "1.0"
  },
  "vertical": {
    "category": "Sports",
    "subcategory": "Football",
    "scope": "Local",
    "country": "Italy"
  },
  "content": {
    "style": ["sports_journalism", "statistical"],
    "players_target": 50,
    "teams_target": 20,
    "include_legends": true,
    "include_venues": true
  },
  "news": {
    "enabled": true,
    "sources": ["google_news", "rss_feeds"],
    "cron_schedule": "0 12 * * *",
    "keywords": ["Serie A", "Italian football", "Calcio"]
  },
  "entities": {
    "primary": "players",
    "group": "teams",
    "event": "matches",
    "venue": "stadiums"
  },
  "theme": {
    "primary_color": "#1a472a",
    "secondary_color": "#ffffff"
  }
}
```

---

## Command Details

### `/bedrock_agent new`

Starts interactive wizard with all questions above.

### `/bedrock_agent configure [project]`

Load and edit existing configuration:
```
/bedrock_agent configure Serie_A_2025-26

Current configuration:
• Vertical: Sports > Football
• Scope: Local (Italy)
• Title: Serie A 2025-26
• Style: Sports Journalism + Statistical
• News: Enabled (daily at 12:00)
• Content: 50 players, 20 teams

What would you like to change?
```

### `/bedrock_agent generate [project]`

Generate content and HTML:
```
/bedrock_agent generate Serie_A_2025-26

Options:
• html       → Generate Docsify website files only
• comparison → Generate comparison tool data only
• templates  → Generate content templates only
• news       → Run news scraper now
• all        → Generate everything (default)
```

### `/bedrock_agent status [project]`

Check progress:
```
/bedrock_agent status WC_2026_Project

FIFA World Cup 2026 - Status
═══════════════════════════════════════
Vertical: Sports > Football > International
Version: 10.9 | Progress: 87%

Content Counts:
  Players (current)  │ 120/150  │ ████████░░ 80%
  Players (legends)  │  20/20   │ ██████████ 100%
  Teams              │  48/48   │ ██████████ 100%
  Tournaments        │  22/22   │ ██████████ 100%
  News articles      │  85/100  │ ████████░░ 85%
  Venues             │  12/16   │ ███████░░░ 75%

News Pipeline: ✓ Active (last run: 2h ago)
Quality: ✓ All gates passed
Website: ✓ HTML generated
```

### `/bedrock_agent qa [project]`

Run quality assurance:
```
/bedrock_agent qa Serie_A_2025-26

Quality Gates:
  ✓ No Placeholders     │ 0 files with TBD/TODO
  ✓ Section Presence    │ All files have proper headers
  ✓ Minimum Files       │ 37/30 minimum met
  ✓ Source Citations    │ All content has sources
  ⚠ Image References    │ 5 files missing images (warning)

Ralph Loops:
  Cycle 1 (Director)  │ 88/100 │ PASSED
  Cycle 2 (Content)   │ 92/100 │ PASSED
  Cycle 3 (SEO/QA)    │ 85/100 │ PASSED
  Overall             │ 88/100 │ PASSED ✓
```

### `/bedrock_agent version [project]`

Create archived version:
```
/bedrock_agent version Serie_A_2025-26

Current version: 1.0

Create new version?
• 1.1 (minor update)
• 2.0 (major release)
• Custom version number
```

### `/bedrock_agent list`

List all projects:
```
/bedrock_agent list

Bedrock Agent Projects
═══════════════════════════════════════════════════════════════════════════
│ Project             │ Vertical         │ Scope         │ News │ Files │
├─────────────────────┼──────────────────┼───────────────┼──────┼───────┤
│ WC_2026_Project     │ Sports/Football  │ International │ ✓    │ 3,523 │
│ Serie_A_2025-26     │ Sports/Football  │ Local (IT)    │ ✓    │ 352   │
│ Italian_Serie_A     │ Sports/Football  │ Local (IT)    │ ✓    │ 348   │
│ Tennis_Grand_Slams  │ Sports/Tennis    │ International │ ✗    │ 37    │
═══════════════════════════════════════════════════════════════════════════

Framework: The_Agent (14 Python modules)
Docs: bedrock_agent/The_Agent/docs/
```

---

## Your Task

Based on the command provided in `$ARGUMENTS`:

### If `new`:
1. Run full interactive wizard with all questions
2. Use `AskUserQuestion` with clear examples as shown above
3. Show configuration summary for confirmation
4. Generate directory structure and config
5. If News Section enabled, configure news pipeline
6. Show next steps

### If `configure [project]`:
1. Load existing `vertical.json`
2. Display current settings in a readable format
3. Ask what to change
4. Save updated config

### If `generate [project]`:
1. Load config
2. Generate HTML website (Docsify)
3. Generate comparison data (if enabled)
4. Run news scraper (if enabled and requested)
5. Report files created

### If `status [project]`:
1. Count files in each category
2. Calculate progress percentages
3. Check news pipeline status
4. Check if HTML exists
5. Display formatted status report

### If `qa [project]`:
1. Run quality gates
2. Run Ralph Loops if requested
3. Display results with pass/fail indicators

### If `version [project]`:
1. Show current version
2. Ask for new version number
3. Copy main/ to Version_X.Y/
4. Generate RELEASE_NOTES.md
5. Update VERSION.md

### If `list`:
1. Scan bedrock_agent directory
2. Load each project's config
3. Count files
4. Display formatted table

---

## News Pipeline (When Enabled)

When user selects "Yes" for News Section:

1. **Configure sources** based on vertical/subcategory:
   - Google News API with relevant keywords
   - Sport-specific RSS feeds
   - Official league/tournament feeds

2. **Create cron job** for daily updates:
   ```bash
   # Added to crontab
   0 12 * * * /path/to/scripts/news_scraper.py
   ```

3. **Generate keywords** from project config:
   - Title + Country + Key terms
   - Example: "Serie A", "Italian football", "Calcio", team names

---

## Example Wizard Flow

```
User: /bedrock_agent new

Agent: Let's create a new content project!

Q1: What vertical (content category)?
User: Sports

Q2: What sport?
User: Football

Q3: Geographic scope?
User: Local

Q4: Tournament/League title?
User: Bundesliga 2025-26

Q5: Which country?
User: Germany

Q6: Content style?
User: Sports Journalism

Q7: Automated News Section?
User: Yes

Q8: Content scope?
User: Standard

Agent:
PROJECT CONFIGURATION SUMMARY
═════════════════════════════════════════════════════════════
Vertical:       Sports > Football
Scope:          Local (Germany)
Title:          Bundesliga 2025-26
Content Style:  Sports Journalism
News Section:   Yes (auto-scraping enabled)
Content Scope:  Standard (50 players, 20 teams)
═════════════════════════════════════════════════════════════

User: Yes

Agent:
✓ Created: /home/andre/BI-AI_Agents_REPO/bedrock_agent/Bundesliga_2025-26/
✓ Config: main/config/vertical.json
✓ Structure: main/, Version_1.0/, docs/
✓ News pipeline: Configured (daily at 12:00)

Next steps:
1. Review config: /bedrock_agent configure Bundesliga_2025-26
2. Generate site: /bedrock_agent generate Bundesliga_2025-26
3. Check status: /bedrock_agent status Bundesliga_2025-26
```

---

## BLACKTEAM INTEGRATION (AUTOMATIC)

**CRITICAL:** After project creation via `/bedrock_agent new`, BlackTeam is AUTOMATICALLY invoked with full team assignments and 5 Ralph Loops for quality assurance.

### Team Roster & Assignments

When a project is generated, assign ALL team members with specific responsibilities:

```
BLACKTEAM PROJECT EXECUTION
═══════════════════════════════════════════════════════════════════════════════

Project: {Project_Name}
Internal ID: BT-2026-XXX
Director: The Director (Strategy, Coordination, Final Approval)

WORK STREAMS
─────────────────────────────────────────────────────────────────────────────
│ Role                │ Persona              │ Responsibilities              │
├─────────────────────┼──────────────────────┼───────────────────────────────┤
│ Content Quality     │ Head of Content      │ Editorial standards, voice,   │
│                     │                      │ accuracy, storytelling        │
├─────────────────────┼──────────────────────┼───────────────────────────────┤
│ SEO Strategy        │ SEO Commander        │ H1/H2 structure, keywords,    │
│                     │                      │ meta tags, competitor research│
├─────────────────────┼──────────────────────┼───────────────────────────────┤
│ Data Engineering    │ DataForge            │ Data pipelines, JSON files,   │
│                     │                      │ news scraping infrastructure  │
├─────────────────────┼──────────────────────┼───────────────────────────────┤
│ ML/Data Science     │ Elias Thorne         │ Player rating models,         │
│                     │                      │ comparison algorithms, stats  │
├─────────────────────┼──────────────────────┼───────────────────────────────┤
│ UX/UI Design        │ PixelPerfect         │ Visual design, fonts, colors, │
│                     │                      │ logo placement, responsive    │
├─────────────────────┼──────────────────────┼───────────────────────────────┤
│ BI Development      │ DataViz              │ Stats dashboards, charts,     │
│                     │                      │ data visualizations           │
├─────────────────────┼──────────────────────┼───────────────────────────────┤
│ QA Testing          │ Post Production Mgr  │ Link testing, content QA,     │
│                     │                      │ broken images, final checks   │
├─────────────────────┼──────────────────────┼───────────────────────────────┤
│ Code Quality        │ CodeGuard            │ Code standards, security,     │
│                     │                      │ performance, best practices   │
├─────────────────────┼──────────────────────┼───────────────────────────────┤
│ Data Analysis       │ Insight              │ Content insights, gaps,       │
│                     │                      │ recommendations               │
└─────────────────────┴──────────────────────┴───────────────────────────────┘
```

---

## 5 RALPH LOOPS (MANDATORY)

Every task goes through 5 Ralph Loops with different focus areas. Each loop MUST pass before release.

### Loop 1: Content Quality (Head of Content)
```
RALPH LOOP 1: CONTENT QUALITY
═════════════════════════════════════════════════════════════
Reviewer: Head of Content
Focus: Editorial Excellence

CHECKLIST:
☐ No placeholder text (TBD, TODO, Lorem ipsum, [INSERT])
☐ Factual accuracy verified with sources
☐ Consistent voice and tone across all content
☐ Player/team names spelled correctly
☐ Dates and statistics accurate
☐ Proper grammar and punctuation
☐ Engaging headlines and subheadings
☐ Story arc and narrative flow
☐ Quotes properly attributed
☐ No duplicate content

SCORE: ___/100 | PASS: 85+ required
COMMENTS: [Head of Content provides detailed feedback]
```

### Loop 2: SEO Optimization (SEO Commander)
```
RALPH LOOP 2: SEO OPTIMIZATION
═════════════════════════════════════════════════════════════
Reviewer: SEO Commander
Focus: Search Engine Excellence

CHECKLIST:
☐ H1 tags: One per page, includes primary keyword
☐ H2 tags: Logical hierarchy, secondary keywords
☐ H3-H6 tags: Proper nesting, no skipping levels
☐ Meta titles: 50-60 chars, keyword-optimized
☐ Meta descriptions: 150-160 chars, compelling CTAs
☐ URL slugs: Clean, keyword-rich, no special chars
☐ Image alt text: Descriptive, includes keywords
☐ Internal linking: 3-5 relevant links per page
☐ External links: Authoritative sources, open in new tab
☐ Keyword density: 1-2% for primary, natural placement
☐ Schema markup: Proper structured data for sport entities

KEYWORD RESEARCH REQUIREMENTS:
- Research competitors (similar sports sites)
- Identify high-volume, low-competition keywords
- Map keywords to specific pages
- Include long-tail variations
- Monitor trending topics for news content

SCORE: ___/100 | PASS: 85+ required
COMMENTS: [SEO Commander provides detailed feedback]
```

### Loop 3: Technical QA (Post Production Manager)
```
RALPH LOOP 3: TECHNICAL QA
═════════════════════════════════════════════════════════════
Reviewer: Post Production Manager
Focus: Links, Images, Functionality

CHECKLIST - LINKS:
☐ All internal links working (no 404s)
☐ All external links working
☐ External links have rel="noopener noreferrer"
☐ Anchor text is descriptive (no "click here")
☐ Navigation links consistent across pages
☐ Sidebar links all functional
☐ Comparison tool links working
☐ News article links valid

CHECKLIST - IMAGES:
☐ All images load correctly
☐ No broken image references
☐ Images have appropriate dimensions
☐ Images compressed for web
☐ Placeholder images replaced with real content
☐ Logo displays correctly in header/footer

CHECKLIST - CONTENT:
☐ All sections have content (no empty pages)
☐ Tables render correctly
☐ Code blocks formatted properly
☐ Special characters display correctly
☐ Mobile responsive layout works

SCORE: ___/100 | PASS: 90+ required
COMMENTS: [Post Production Manager provides detailed feedback]
```

### Loop 4: UX/UI Review (PixelPerfect)
```
RALPH LOOP 4: UX/UI DESIGN REVIEW
═════════════════════════════════════════════════════════════
Reviewer: PixelPerfect (Senior UX/UI Designer)
Focus: Visual Excellence & Accessibility

CHECKLIST - TYPOGRAPHY:
☐ Font sizes readable (16px+ body, 24px+ H1)
☐ Font family consistent across site
☐ Line height appropriate (1.5-1.7 for body)
☐ Text color contrast WCAG AA compliant (4.5:1)
☐ Heading hierarchy visually distinct

CHECKLIST - COLORS:
☐ Primary/secondary colors applied consistently
☐ Background colors don't clash with text
☐ Links visually distinct from body text
☐ Hover states clearly visible
☐ Dark mode works correctly (if enabled)
☐ No white text on light backgrounds

CHECKLIST - LAYOUT:
☐ Logo positioned correctly (header)
☐ Navigation intuitive and accessible
☐ Content width appropriate (max 800px for reading)
☐ Spacing consistent (margins, padding)
☐ Cards/tables aligned properly
☐ Footer contains required information

CHECKLIST - RESPONSIVENESS:
☐ Mobile layout works (320px+)
☐ Tablet layout works (768px+)
☐ Desktop layout works (1024px+)
☐ Images scale correctly
☐ Tables scroll horizontally on mobile
☐ Touch targets 44px+ for mobile

CHECKLIST - COMPARISON TOOL:
☐ Player cards display correctly
☐ Stats tables readable
☐ Selection dropdowns work
☐ Side-by-side comparison renders properly
☐ Charts/graphs display correctly

SCORE: ___/100 | PASS: 85+ required
COMMENTS: [PixelPerfect provides detailed feedback]
```

### Loop 5: Data & ML Validation (Elias Thorne + Insight)
```
RALPH LOOP 5: DATA & ML VALIDATION
═════════════════════════════════════════════════════════════
Reviewers: Elias Thorne (ML/Data Science) + Insight (Analysis)
Focus: Data Accuracy & Model Quality

CHECKLIST - PLAYER RATINGS (Elias Thorne):
☐ Rating algorithm produces sensible results
☐ All player stats within valid ranges
☐ Comparison tool calculations correct
☐ Historical data properly weighted
☐ No outliers causing skewed ratings
☐ Model explanations documented
☐ JSON data structures valid
☐ All required fields populated

CHECKLIST - DATA QUALITY (Insight):
☐ Team rosters complete and accurate
☐ Tournament brackets/schedules correct
☐ Historical records verified
☐ Statistics match official sources
☐ News content relevant and timely
☐ Data freshness appropriate
☐ Coverage gaps identified and addressed

CHECKLIST - NEWS PIPELINE (if enabled):
☐ News sources configured correctly
☐ Keywords generating relevant results
☐ Article deduplication working
☐ Content formatting correct
☐ Attribution and sources included

SCORE: ___/100 | PASS: 85+ required
COMMENTS: [Elias Thorne + Insight provide detailed feedback]
```

---

## BLACKTEAM EXECUTION FLOW

After `/bedrock_agent generate` completes:

```
1. INVOKE BLACKTEAM
   └── /blackteam "QA review for {Project_Name} content generation"

2. ASSIGN ALL ROLES
   └── Each specialist receives their work stream

3. PARALLEL EXECUTION
   ├── Head of Content → Reviews all markdown files
   ├── SEO Commander → Audits SEO structure
   ├── PixelPerfect → Reviews UI/UX
   ├── Elias Thorne → Validates ML models
   ├── Post Production → Tests all links
   └── Insight → Checks data quality

4. RUN RALPH LOOPS (PARALLEL EXECUTION)
   ┌─────────────────────────────────────────────────────────────┐
   │ Loop 1: Content Quality (Head of Content) - SEQUENTIAL     │
   │         Must pass FIRST (85+ score)                        │
   └────────────────────────┬────────────────────────────────────┘
                            │ PASS
          ┌─────────────────┼─────────────────┐
          │                 │                 │
   ┌──────┴──────┐   ┌──────┴──────┐   ┌──────┴──────┐
   │   Loop 2    │   │   Loop 3    │   │   Loop 4    │
   │    SEO      │   │  Technical  │   │   UX/UI     │
   │  (85+)      │   │   (90+)     │   │   (85+)     │
   │ IN PARALLEL │   │ IN PARALLEL │   │ IN PARALLEL │
   └──────┬──────┘   └──────┬──────┘   └──────┬──────┘
          │                 │                 │
          └─────────────────┼─────────────────┘
                            │ ALL PASS
   ┌────────────────────────┴────────────────────────────────────┐
   │ Loop 5: Data & ML Validation (Elias + Insight) - SEQUENTIAL │
   │         Final validation (85+ score)                        │
   └─────────────────────────────────────────────────────────────┘

5. COLLECT FEEDBACK
   └── Each specialist comments in their track (Loops 2-4 submit simultaneously)

6. FIX ISSUES
   └── Address feedback from failed loops ONLY (passed loops not re-run)

7. RE-RUN FAILED LOOPS
   └── Only re-run loops that failed (not all 5)

8. DIRECTOR APPROVAL
   └── Final sign-off from The Director

9. VERSION RELEASE
   └── Create Version_X.0 with release notes
```

---

## PARALLEL LOOP EXECUTION PROTOCOL

**CRITICAL:** Loops 2-4 execute simultaneously after Loop 1 passes. This reduces QA time by ~50%.

### Execution Rules

1. **Loop 1 (Director/Content) runs FIRST:**
   - Validates source/facts integrity
   - Must score 85+ to proceed
   - If fails, fix and re-run before continuing

2. **After Loop 1 passes, launch Loops 2, 3, 4 IN PARALLEL:**
   ```
   PARALLEL LAUNCH:
   ├── Loop 2 (SEO Commander) - Starts immediately
   ├── Loop 3 (Post Production) - Starts immediately
   └── Loop 4 (PixelPerfect) - Starts immediately
   ```
   - Each reviewer works independently
   - No reviewer waits for another
   - Each produces their own score and feedback

3. **Aggregation Gate:**
   - Wait for ALL three parallel loops to complete
   - ALL must pass their threshold:
     - Loop 2: 85+
     - Loop 3: 90+ (highest standard)
     - Loop 4: 85+
   - If ANY fails, proceed to fix phase

4. **Re-run Efficiency:**
   - If Loop 2 fails but Loops 3 and 4 pass:
     - Fix Loop 2 issues
     - Re-run ONLY Loop 2
     - Do NOT re-run Loops 3 and 4
   - Passed loops retain their scores

5. **Proceed to Loop 5:**
   - Only when ALL of Loops 2, 3, 4 pass
   - Loop 5 (Elias + Insight) validates final data quality
   - Must score 85+ for approval

### Benefits

| Metric | Sequential | Parallel | Improvement |
|--------|------------|----------|-------------|
| QA Time | 5 loops × T | 1 + 3 parallel + 1 | ~50% faster |
| Re-runs | All 5 loops | Only failed loops | Fewer cycles |
| Feedback | Delayed | Simultaneous | Faster fixes |

### Example Timeline

```
SEQUENTIAL (OLD):
Loop 1 ──► Loop 2 ──► Loop 3 ──► Loop 4 ──► Loop 5
[10 min]  [10 min]  [10 min]  [10 min]  [10 min]  = 50 min total

PARALLEL (NEW):
Loop 1 ──► ┌─ Loop 2 ─┐
           ├─ Loop 3 ─┼──► Loop 5
           └─ Loop 4 ─┘
[10 min]    [10 min]        [10 min]  = 30 min total
```

---

## TEAM COMMENTARY REQUIREMENTS

**MANDATORY:** Each team member MUST provide commentary and advice in their work track:

```
TEAM FEEDBACK FORMAT
═════════════════════════════════════════════════════════════

[Persona Name] - [Role]
Loop: [1-5] | Score: [XX/100] | Status: [PASS/NEEDS WORK]

OBSERVATIONS:
• [What was done well]
• [What needs improvement]

ISSUES FOUND:
1. [Issue] - [File/Location] - [Severity: Critical/High/Medium/Low]
2. [Issue] - [File/Location] - [Severity]

RECOMMENDATIONS:
• [Specific actionable advice]
• [Best practice suggestion]

FILES REVIEWED:
• [file1.md] - [Status]
• [file2.md] - [Status]

─────────────────────────────────────────────────────────────
```

---

## SEO BEST PRACTICES (MANDATORY)

SEO Commander must enforce these standards:

### H1/H2 Structure
```
CORRECT:
<h1>FIFA World Cup 2026 - Complete Guide</h1>
  <h2>Tournament Overview</h2>
  <h2>Teams & Groups</h2>
    <h3>Group A</h3>
    <h3>Group B</h3>
  <h2>Top Players to Watch</h2>

WRONG:
<h2>FIFA World Cup 2026</h2>  ← Missing H1
<h1>Overview</h1>             ← Multiple H1s
<h4>Teams</h4>                ← Skipped H2, H3
```

### Keyword Research Workflow
```
1. IDENTIFY primary keyword for page
   Example: "World Cup 2026 players"

2. RESEARCH using:
   - Google Keyword Planner
   - Ahrefs/SEMrush (competitor analysis)
   - Google Trends (trending topics)
   - "People also ask" boxes

3. MAP keywords to content:
   - H1: Primary keyword
   - H2s: Secondary keywords
   - Body: Long-tail variations
   - Images: Alt text with keywords

4. MONITOR rankings after publish
```

### Content Quality Checklist
```
☐ Unique content (no copy-paste from other sites)
☐ 1500+ words for pillar pages
☐ 500+ words for player/team profiles
☐ 300+ words for news articles
☐ Sources cited for all statistics
☐ Updated within last 30 days (for news)
```

---

## QUALITY GATES SUMMARY

Before any release, ALL gates must pass:

```
QUALITY GATES STATUS
═════════════════════════════════════════════════════════════
│ Gate                    │ Owner            │ Threshold │ Status │
├─────────────────────────┼──────────────────┼───────────┼────────┤
│ Content Quality         │ Head of Content  │ 85/100    │ ☐      │
│ SEO Optimization        │ SEO Commander    │ 85/100    │ ☐      │
│ Technical QA            │ Post Production  │ 90/100    │ ☐      │
│ UX/UI Review            │ PixelPerfect     │ 85/100    │ ☐      │
│ Data/ML Validation      │ Elias + Insight  │ 85/100    │ ☐      │
├─────────────────────────┼──────────────────┼───────────┼────────┤
│ ALL GATES PASSED        │ Director         │ 5/5       │ ☐      │
└─────────────────────────┴──────────────────┴───────────┴────────┘

Release blocked until all gates show ✓
```

---

## AUTOMATIC INVOCATION

When `/bedrock_agent generate` completes, automatically run:

```
/blackteam Execute 5 Ralph Loops QA for {Project_Name}:
- Content Quality review by Head of Content
- SEO audit by SEO Commander
- Technical QA by Post Production Manager
- UX/UI review by PixelPerfect
- Data validation by Elias Thorne + Insight
All team members must comment with findings and recommendations.
```

---

## ASTRO DEPLOYMENT (MANDATORY)

**CRITICAL:** After QA passes and content is committed to GitHub, ALWAYS create an Astro version for production deployment.

### Astro Project Generation

When all QA gates pass, create an Astro version:

```
PROJECT STRUCTURE
═════════════════════════════════════════════════════════════
{Project_Name}_Astro/
├── package.json
├── astro.config.mjs
├── tsconfig.json
├── vercel.json
├── VERSION.md
├── .gitignore
└── src/
    ├── content/
    │   ├── config.ts          # Content Collections schema
    │   ├── players/           # Player markdown with frontmatter
    │   ├── teams/             # Team markdown with frontmatter
    │   └── venues/            # Venue markdown with frontmatter
    ├── components/
    │   └── Search.astro       # Pagefind search
    ├── layouts/
    │   └── BaseLayout.astro   # Base layout with nav/footer
    ├── pages/
    │   ├── index.astro        # Homepage
    │   ├── players/
    │   │   ├── index.astro
    │   │   └── [...slug].astro
    │   ├── teams/
    │   │   ├── index.astro
    │   │   └── [...slug].astro
    │   └── venues/
    │       ├── index.astro
    │       └── [...slug].astro
    └── styles/
        └── global.css         # Theme CSS variables
```

### Content Conversion

Convert Docsify markdown to Astro content with frontmatter:

```markdown
# Docsify format:
# Cole Palmer
> Chelsea - #20 - Attacking Midfielder

# Astro format (with frontmatter):
---
name: "Cole Palmer"
club: "Chelsea"
position: "Attacking Midfielder"
nationality: "England"
age: 23
overall: 88
pace: 76
shooting: 88
---
# Cole Palmer
```

### Build Commands

```bash
# Install dependencies
cd {Project_Name}_Astro && npm install

# Build static site
npm run build

# Add search index (post-build)
npx pagefind --site dist

# Preview locally
npm run preview

# Deploy to Vercel
vercel deploy --prod
```

### Deployment Workflow

After GitHub commit, execute:

1. **Create Astro project** - Copy base structure
2. **Convert content** - Add frontmatter to all markdown files
3. **Build site** - `npm run build`
4. **Deploy to Vercel** - `vercel deploy --prod`
5. **Add to hub** - Update `start_all_servers.sh` and `hub/index.html`

### Vercel Integration

Each project deploys to: `{project-slug}.vercel.app`

Examples:
- `premier-league-2025-26.vercel.app`
- `italian-serie-a.vercel.app`
- `wc-2026.vercel.app`

---

*BlackTeam BT-2026-004 - Content Vertical Generator with Full QA Integration*

---

## ⚡ COMPREHENSIVE PERSONA CHECKLISTS ⚡

**MANDATORY:** Each persona MUST complete their checklist BEFORE signing off. No exceptions.

---

### 📋 HEAD OF CONTENT - Editorial Excellence Checklist

```
HEAD OF CONTENT - MANDATORY REVIEW CHECKLIST
═══════════════════════════════════════════════════════════════════════════════

SECTION A: HISTORICAL CONTENT VERIFICATION (CRITICAL)
────────────────────────────────────────────────────────────────────────────────
☐ A1. Team History Accuracy
   • Founded year verified against official sources
   • Championship/trophy counts verified (WCC, WDC, league titles)
   • Historical milestones included (first win, record seasons)
   • Notable past managers/principals mentioned
   • Team name changes documented (if applicable)
   • Previous ownership history accurate

☐ A2. Tournament/League History Accuracy
   • First edition year verified
   • All past champions listed correctly
   • Record holders verified (most wins, fastest laps, etc.)
   • Format changes documented (if applicable)
   • Historical venues/circuits included
   • Major rule changes noted with correct years

☐ A3. Player/Driver History Accuracy
   • Career statistics verified from official sources
   • Championship wins correct (years, teams)
   • Career start date verified
   • Previous team history accurate
   • Award history complete (ROTY, POTY, etc.)
   • Record achievements verified

☐ A4. Venue/Circuit History Accuracy
   • Opening year verified
   • Previous names documented
   • Capacity figures current
   • Notable events held historically
   • Renovations/changes noted with dates
   • Track layout changes documented (for circuits)

SECTION B: EDITORIAL QUALITY STANDARDS
────────────────────────────────────────────────────────────────────────────────
☐ B1. No Placeholder Content
   • No "TBD", "TODO", "PLACEHOLDER" text
   • No "[INSERT X]" markers
   • No "Lorem ipsum" filler
   • No "Coming soon" sections
   • No empty sections with just headers

☐ B2. Factual Accuracy
   • All statistics sourced from official data
   • Dates formatted consistently (Month DD, YYYY)
   • Names spelled correctly (verify special characters)
   • Numbers match official records
   • Rankings/standings current

☐ B3. Voice & Tone Consistency
   • Professional sports journalism tone throughout
   • Consistent tense (present for current, past for history)
   • No informal language (slang, colloquialisms)
   • Active voice preferred
   • Engaging but not sensationalist

☐ B4. Content Completeness
   • All entities have full profiles (not stub pages)
   • Bio sections 150+ words minimum
   • Stats sections include all relevant metrics
   • Career highlights substantive (5+ bullet points)
   • News articles 300+ words

☐ B5. Cross-References & Links
   • Team pages link to all drivers/players
   • Driver pages link back to teams
   • Circuit pages link to races held there
   • News articles link to relevant entities
   • Related content sections populated

SECTION C: SOURCE VERIFICATION
────────────────────────────────────────────────────────────────────────────────
☐ C1. Primary Sources Used
   • Official league/federation websites
   • Official team websites
   • Verified news outlets
   • Press releases when applicable

☐ C2. Citation Standards
   • Statistics attributed to source
   • Quotes properly attributed
   • Historical facts verifiable
   • No unsourced claims

═══════════════════════════════════════════════════════════════════════════════
SIGN-OFF: Head of Content | Score: ___/100 | Date: ____________
Notes: __________________________________________________________________
═══════════════════════════════════════════════════════════════════════════════
```

---

### 🔍 SEO COMMANDER - Search Optimization Checklist

```
SEO COMMANDER - MANDATORY REVIEW CHECKLIST
═══════════════════════════════════════════════════════════════════════════════

SECTION A: ON-PAGE SEO STRUCTURE
────────────────────────────────────────────────────────────────────────────────
☐ A1. Heading Hierarchy
   • Exactly ONE H1 per page (no more, no less)
   • H1 contains primary keyword
   • H2s follow H1 logically (no skipping to H3)
   • H3s nest under H2s properly
   • No heading level skipping (H1 → H3 is WRONG)

☐ A2. Meta Tags
   • Title tag: 50-60 characters, keyword at start
   • Meta description: 150-160 characters, includes CTA
   • OG:title set for social sharing
   • OG:description set
   • OG:image specified (1200x630px recommended)
   • Twitter card meta tags present

☐ A3. URL Structure
   • Clean slugs (no underscores, use hyphens)
   • Keywords in URL path
   • No special characters in URLs
   • Consistent casing (lowercase)
   • Logical hierarchy (/teams/ferrari/, not /t/f/)

SECTION B: KEYWORD OPTIMIZATION
────────────────────────────────────────────────────────────────────────────────
☐ B1. Keyword Research Completed
   • Primary keyword identified per page
   • Secondary keywords (3-5) identified
   • Long-tail variations documented
   • Competitor keywords analyzed
   • Search volume data recorded

☐ B2. Keyword Placement
   • Primary keyword in H1
   • Primary keyword in first 100 words
   • Secondary keywords in H2s
   • Keywords in image alt text
   • Keywords in meta description
   • Natural keyword density (1-2%)

☐ B3. Entity-Specific SEO
   • Player names include team/position
   • Team names include sport/league
   • Circuit names include country
   • Race names include year
   • News titles include relevant keywords

SECTION C: TECHNICAL SEO
────────────────────────────────────────────────────────────────────────────────
☐ C1. Internal Linking
   • 3-5 internal links per page minimum
   • Descriptive anchor text (not "click here")
   • Links to related content
   • Breadcrumb navigation present
   • Sidebar navigation functional

☐ C2. Image SEO
   • All images have alt text
   • Alt text includes keywords naturally
   • Image filenames descriptive
   • Images compressed for web
   • Lazy loading implemented

☐ C3. Schema Markup
   • SportsOrganization schema for teams
   • Person schema for players/drivers
   • SportsEvent schema for races/matches
   • Article schema for news
   • BreadcrumbList schema present

☐ C4. Indexability
   • No noindex tags on public pages
   • Sitemap.xml generated
   • Robots.txt properly configured
   • Canonical URLs set
   • No duplicate content issues

═══════════════════════════════════════════════════════════════════════════════
SIGN-OFF: SEO Commander | Score: ___/100 | Date: ____________
Notes: __________________________________________________________________
═══════════════════════════════════════════════════════════════════════════════
```

---

### 🎨 PIXELPERFECT - UX/UI Design Checklist

```
PIXELPERFECT (SENIOR UX/UI DESIGNER) - MANDATORY REVIEW CHECKLIST
═══════════════════════════════════════════════════════════════════════════════

SECTION A: TEXT VISIBILITY & READABILITY (CRITICAL)
────────────────────────────────────────────────────────────────────────────────
☐ A1. Text Color Contrast - WCAG 2.1 AA Compliance
   • Body text: 4.5:1 contrast ratio minimum
   • Large text (18px+): 3:1 contrast ratio minimum
   • NO white text on light backgrounds
   • NO light gray text on white backgrounds
   • NO red text on dark red backgrounds
   • Use contrast checker tool to verify

☐ A2. Problematic Color Combinations - NEVER USE
   • ❌ White (#FFFFFF) on Yellow
   • ❌ Light gray (#CCCCCC) on White
   • ❌ Red (#E10600) on Black (#15151E) for body text
   • ❌ Any text with contrast ratio below 4.5:1

☐ A3. Typography Standards
   • Body text: 16px minimum (1rem)
   • H1: 2rem minimum (32px)
   • H2: 1.5rem minimum (24px)
   • H3: 1.25rem minimum (20px)
   • Line height: 1.5-1.7 for body text
   • Font weight: 400 for body, 600-700 for headings

☐ A4. Font Family Consistency
   • Primary font applied site-wide
   • Fallback fonts specified (system fonts)
   • No mixing of incompatible font families
   • Headings and body can differ but must complement

SECTION B: COLOR SYSTEM & THEME ALIGNMENT
────────────────────────────────────────────────────────────────────────────────
☐ B1. Brand Colors Applied Correctly
   • Primary color used for headers/CTAs
   • Secondary color used for accents
   • Background colors consistent
   • Card backgrounds have proper contrast
   • Link colors distinct from body text

☐ B2. Hover & Focus States
   • All interactive elements have hover states
   • Hover states visually distinct
   • Focus states visible for keyboard nav
   • No color-only state changes (add underline/border)

☐ B3. Dark Mode (If Applicable)
   • All text readable in dark mode
   • Images don't clash with dark background
   • Cards have visible borders/shadows
   • Form inputs visible and usable

SECTION C: ASTRO TEMPLATE COMPLIANCE
────────────────────────────────────────────────────────────────────────────────
☐ C1. Component Consistency
   • Cards match established component patterns
   • Headers consistent across all pages
   • Footers identical site-wide
   • Navigation matches template standard

☐ C2. Layout Grid Compliance
   • Container max-width consistent
   • Grid columns match template (3-col, 4-col)
   • Spacing uses CSS variables
   • Responsive breakpoints match template

☐ C3. Design Token Usage
   • CSS variables for all colors
   • CSS variables for spacing
   • CSS variables for fonts
   • No hard-coded magic numbers

SECTION D: RESPONSIVE DESIGN
────────────────────────────────────────────────────────────────────────────────
☐ D1. Mobile (320px - 767px)
   • Single column layout
   • Touch targets 44px minimum
   • Font sizes scale appropriately
   • Images don't overflow
   • Tables scroll horizontally
   • Navigation collapses to menu

☐ D2. Tablet (768px - 1023px)
   • Two column layout where appropriate
   • Cards reflow properly
   • Images scale correctly

☐ D3. Desktop (1024px+)
   • Full layout displays
   • Sidebar visible (if applicable)
   • Maximum content width enforced
   • No horizontal scrolling

SECTION E: ACCESSIBILITY (WCAG 2.1)
────────────────────────────────────────────────────────────────────────────────
☐ E1. Keyboard Navigation
   • All interactive elements focusable
   • Tab order logical
   • No keyboard traps
   • Skip links present

☐ E2. Screen Reader Support
   • Semantic HTML used (nav, main, article, aside)
   • ARIA labels where needed
   • Images have alt text
   • Form labels associated correctly

☐ E3. Motion & Animation
   • Respects prefers-reduced-motion
   • No flashing content (3 Hz limit)
   • Animations can be paused

SECTION F: VISUAL POLISH - FINAL DELIVERY
────────────────────────────────────────────────────────────────────────────────
☐ F1. Alignment & Spacing
   • All elements properly aligned
   • Consistent padding/margins
   • No overlapping elements
   • Grid alignment maintained

☐ F2. Images & Media
   • All images load correctly
   • Placeholder images replaced
   • Correct aspect ratios
   • No stretched/distorted images
   • Alt text present

☐ F3. Card Components
   • All cards same height in rows
   • Card content doesn't overflow
   • Card hover states work
   • Championship badges display correctly

☐ F4. Navigation
   • Logo displays correctly
   • Active state shows current page
   • All links work
   • Mobile menu functions

═══════════════════════════════════════════════════════════════════════════════
SIGN-OFF: PixelPerfect | Score: ___/100 | Date: ____________
Notes: __________________________________________________________________
═══════════════════════════════════════════════════════════════════════════════
```

---

### 🔧 POST PRODUCTION MANAGER - Technical QA Checklist

```
POST PRODUCTION MANAGER - MANDATORY REVIEW CHECKLIST
═══════════════════════════════════════════════════════════════════════════════

SECTION A: LINK VALIDATION (ZERO TOLERANCE FOR 404s)
────────────────────────────────────────────────────────────────────────────────
☐ A1. Internal Links
   • All navigation links work
   • All content links work
   • All card links work
   • All sidebar links work
   • No broken anchor links
   • No circular redirects

☐ A2. External Links
   • All external links work
   • rel="noopener noreferrer" on external links
   • target="_blank" for external links
   • No links to defunct websites

☐ A3. Asset Links
   • All image src paths valid
   • All CSS files load
   • All JS files load
   • Favicon loads correctly
   • Font files load

SECTION B: BUILD & DEPLOYMENT VERIFICATION
────────────────────────────────────────────────────────────────────────────────
☐ B1. Astro Build Success
   • npm run build completes without errors
   • No TypeScript errors
   • No missing imports
   • All content collections valid
   • Static pages generated correctly

☐ B2. Asset Generation
   • dist/ folder contains all pages
   • CSS bundled and minified
   • Images copied to dist
   • No missing static files

☐ B3. Vercel Deployment
   • Deployment successful
   • No build errors in Vercel logs
   • Preview URL works
   • Production URL works
   • Environment variables set (if any)

SECTION C: CONTENT INTEGRITY
────────────────────────────────────────────────────────────────────────────────
☐ C1. Data Rendering
   • All frontmatter fields render
   • No "undefined" or "null" displayed
   • Numbers format correctly
   • Dates format correctly
   • Lists render as lists

☐ C2. Content Display
   • No truncated content
   • No HTML showing as text
   • Special characters render correctly
   • Emoji display correctly (if used)
   • Code blocks formatted (if any)

☐ C3. Dynamic Content
   • Filters work correctly
   • Sort functions work
   • Search works (if implemented)
   • Pagination works (if implemented)

SECTION D: PERFORMANCE
────────────────────────────────────────────────────────────────────────────────
☐ D1. Page Load
   • Homepage loads under 3 seconds
   • No render-blocking resources
   • Images lazy loaded
   • Fonts preloaded

☐ D2. Asset Optimization
   • Images compressed
   • CSS minified
   • JS minified
   • No unused CSS

SECTION E: BROWSER TESTING
────────────────────────────────────────────────────────────────────────────────
☐ E1. Desktop Browsers
   • Chrome (latest) - Works
   • Firefox (latest) - Works
   • Safari (latest) - Works
   • Edge (latest) - Works

☐ E2. Mobile Browsers
   • iOS Safari - Works
   • Chrome Mobile - Works
   • Samsung Internet - Works

SECTION F: FINAL CHECKS
────────────────────────────────────────────────────────────────────────────────
☐ F1. Console Errors
   • No JavaScript errors in console
   • No 404 errors in network tab
   • No CORS errors
   • No deprecation warnings

☐ F2. Sitemap & SEO Files
   • sitemap.xml exists and valid
   • robots.txt exists
   • No pages blocked accidentally
   • All important pages in sitemap

═══════════════════════════════════════════════════════════════════════════════
SIGN-OFF: Post Production Manager | Score: ___/100 | Date: ____________
Notes: __________________________________________________________________
═══════════════════════════════════════════════════════════════════════════════
```

---

### 📊 ELIAS THORNE + INSIGHT - Data Validation Checklist

```
ELIAS THORNE + INSIGHT - MANDATORY DATA REVIEW CHECKLIST
═══════════════════════════════════════════════════════════════════════════════

SECTION A: DATA ACCURACY (Elias Thorne)
────────────────────────────────────────────────────────────────────────────────
☐ A1. Numeric Data Ranges
   • All ratings within valid ranges (0-100)
   • Ages realistic (16-50 for players)
   • Speeds/times physically possible
   • Percentages sum correctly where applicable
   • No negative values where impossible

☐ A2. Statistical Consistency
   • Win + Loss + Draw = Total matches
   • Points calculations correct
   • Goal difference matches goals scored - conceded
   • Lap times format correct (mm:ss.xxx)
   • Championship points accurate

☐ A3. Ranking Algorithm Validation
   • Top-ranked entities have best stats
   • No obvious outliers
   • Historical weighting applied correctly
   • Recent form weighted appropriately
   • Algorithm documented

SECTION B: DATA COMPLETENESS (Insight)
────────────────────────────────────────────────────────────────────────────────
☐ B1. Entity Coverage
   • All teams have content (no missing teams)
   • All drivers/players have profiles
   • All circuits/venues have pages
   • Full calendar/schedule present
   • No orphan pages (linked but don't exist)

☐ B2. Field Completeness
   • No empty required fields
   • Image paths specified (even if placeholder)
   • All stats populated
   • Bio sections filled
   • Contact/social links present (where applicable)

☐ B3. Relationship Integrity
   • All team references valid
   • All driver-team relationships correct
   • Circuit-race links accurate
   • News category tags valid

SECTION C: HISTORICAL DATA VERIFICATION
────────────────────────────────────────────────────────────────────────────────
☐ C1. Championship Records
   • Total championship counts accurate
   • Championship years listed correctly
   • No claimed championships that didn't happen
   • Multiple championships for same year handled

☐ C2. Career Statistics
   • Career start dates accurate
   • Total races/matches correct
   • Win counts verified
   • Podium/top finishes accurate
   • Record achievements verified

☐ C3. Timeline Consistency
   • Events in chronological order
   • No future events listed as past
   • Date formats consistent
   • Season years accurate (2025-26 vs 2026)

SECTION D: JSON/DATA FILE VALIDATION
────────────────────────────────────────────────────────────────────────────────
☐ D1. File Structure
   • Valid JSON syntax
   • Required fields present
   • Data types correct (string/number/array)
   • No trailing commas
   • UTF-8 encoding

☐ D2. Content Schema
   • Frontmatter matches Zod schema
   • All defined fields populated
   • Optional fields handled correctly
   • Enum values valid

SECTION E: NEWS PIPELINE (If Enabled)
────────────────────────────────────────────────────────────────────────────────
☐ E1. Source Validation
   • News sources configured correctly
   • Keywords generating relevant results
   • No spam/irrelevant articles
   • Deduplication working

☐ E2. Content Quality
   • Articles properly formatted
   • Attribution/sources included
   • Dates accurate
   • Categories correct

═══════════════════════════════════════════════════════════════════════════════
SIGN-OFF: Elias Thorne | Score: ___/100 | Date: ____________
SIGN-OFF: Insight | Score: ___/100 | Date: ____________
Notes: __________________________________________________________________
═══════════════════════════════════════════════════════════════════════════════
```

---

## 🏗️ ASTRO TEMPLATE COMPLIANCE RULES

**MANDATORY:** All generated Astro projects must follow these standards.

```
ASTRO TEMPLATE COMPLIANCE MATRIX
═══════════════════════════════════════════════════════════════════════════════

REFERENCE TEMPLATES
────────────────────────────────────────────────────────────────────────────────
├── WC_2026_Astro_V2/       # World Cup 2026 (Reference Standard)
├── Italian_Serie_A_Astro/  # Serie A (Football League)
└── F1_2026_Astro/          # Formula 1 (Racing)

REQUIRED FILE STRUCTURE
────────────────────────────────────────────────────────────────────────────────
{Project}_Astro/
├── package.json            # MUST have: astro, @astrojs/mdx
├── astro.config.mjs        # MUST have: mdx integration
├── tsconfig.json           # MUST extend @astro/tsconfig/strict
├── vercel.json             # MUST have: buildCommand, outputDirectory
├── src/
│   ├── content/
│   │   └── config.ts       # MUST define Zod schemas for ALL entities
│   ├── components/
│   │   ├── Header.astro    # MUST have consistent navigation
│   │   ├── Footer.astro    # MUST have consistent footer
│   │   └── *Card.astro     # One card component per entity type
│   ├── layouts/
│   │   └── Layout.astro    # MUST have SEO meta tags
│   ├── pages/
│   │   ├── index.astro     # Homepage
│   │   └── {entity}/
│   │       ├── index.astro # Listing page with filters
│   │       └── [slug].astro # Detail page with getStaticPaths
│   └── styles/
│       └── globals.css     # MUST define CSS variables

CSS VARIABLE REQUIREMENTS
────────────────────────────────────────────────────────────────────────────────
:root {
  /* Brand Colors - REQUIRED */
  --{sport}-primary: #XXXXXX;    /* Main brand color */
  --{sport}-secondary: #XXXXXX;  /* Accent color */
  --{sport}-black: #XXXXXX;      /* Dark background */
  --{sport}-white: #XXXXXX;      /* Light background */
  --{sport}-gray: #XXXXXX;       /* Muted elements */

  /* Typography - REQUIRED */
  --font-primary: 'Font Name', sans-serif;
  --font-heading: 'Font Name', sans-serif;

  /* Spacing - RECOMMENDED */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;
}

CONTENT COLLECTION SCHEMA REQUIREMENTS
────────────────────────────────────────────────────────────────────────────────
// Example for any entity (drivers, teams, players, etc.)
const entityCollection = defineCollection({
  type: 'content',
  schema: z.object({
    // REQUIRED FIELDS
    name: z.string(),               // Entity name
    slug: z.string().optional(),    // URL slug (auto from filename if omitted)
    image: z.string().optional(),   // Image path

    // ENTITY-SPECIFIC FIELDS
    // ... define based on entity type

    // SEO FIELDS - RECOMMENDED
    metaTitle: z.string().optional(),
    metaDescription: z.string().optional(),
  }),
});

PAGE DIRECTOR REQUIREMENTS
────────────────────────────────────────────────────────────────────────────────
// Listing Page (index.astro) MUST have:
☐ getCollection() call to fetch all entities
☐ Sort by relevant field (name, date, etc.)
☐ Filter UI (by category, year, country, etc.)
☐ Grid/list display using card components
☐ Client-side filter JavaScript

// Detail Page ([slug].astro) MUST have:
☐ getStaticPaths() with all entity slugs
☐ getCollection() filtered by slug
☐ Full entity details
☐ Related content section
☐ Back to listing link

CARD COMPONENT REQUIREMENTS
────────────────────────────────────────────────────────────────────────────────
// Every *Card.astro MUST:
☐ Accept entity props from content collection
☐ Link to detail page
☐ Display image with fallback
☐ Show key info (name, category, etc.)
☐ Have hover state
☐ Be responsive

LAYOUT REQUIREMENTS
────────────────────────────────────────────────────────────────────────────────
// Layout.astro MUST include:
☐ <!DOCTYPE html> declaration
☐ <html lang="en">
☐ <head> with:
   - <meta charset="UTF-8">
   - <meta name="viewport">
   - <meta name="description"> from props
   - <meta property="og:*"> tags
   - <meta name="twitter:card">
   - <link rel="icon">
   - <title> with site name suffix
☐ <body> with:
   - <Header />
   - <slot /> for page content
   - <Footer />
☐ Global styles imported

BUILD & DEPLOY REQUIREMENTS
────────────────────────────────────────────────────────────────────────────────
☐ npm run build succeeds without errors
☐ npm run preview shows working site
☐ vercel deploy --prod succeeds
☐ All pages accessible at production URL
☐ hub/index.html updated with new project link

═══════════════════════════════════════════════════════════════════════════════
```

---

## 📚 PERSONA STANDARDS & LEARNINGS ENFORCEMENT

**CRITICAL:** These standards are derived from previous projects and MUST be enforced on every execution.

```
MANDATORY PERSONA STANDARDS (From BLACKTEAM_LEARNINGS.md)
═══════════════════════════════════════════════════════════════════════════════

LEARNED STANDARD 1: Research Before Execution
────────────────────────────────────────────────────────────────────────────────
"When creating sports content, verify all player/team data against official
sources BEFORE writing. Do not rely on general knowledge alone."

ENFORCEMENT:
☐ Head of Content must cite official sources
☐ Elias Thorne must verify stats against APIs/official data
☐ All numerical data must be cross-referenced

LEARNED STANDARD 2: Design Accessibility First
────────────────────────────────────────────────────────────────────────────────
"All UX decisions must meet WCAG 2.1 AA standards. Check contrast ratios
before approving any color combination."

ENFORCEMENT:
☐ PixelPerfect must run contrast checker on ALL text
☐ No design approval without accessibility verification
☐ Document any exceptions with justification

LEARNED STANDARD 3: Test All Links Before Release
────────────────────────────────────────────────────────────────────────────────
"Every link in the project must be tested. A single 404 error in production
is unacceptable."

ENFORCEMENT:
☐ Post Production Manager must test EVERY link
☐ Automated link checker run on build
☐ Release blocked if any 404s found

LEARNED STANDARD 4: Historical Data Requires Verification
────────────────────────────────────────────────────────────────────────────────
"Championship counts, career statistics, and historical records must be
verified against official federation/league websites."

ENFORCEMENT:
☐ Head of Content verifies all historical claims
☐ Insight cross-references with multiple sources
☐ No "estimated" or "approximately" for verifiable facts

LEARNED STANDARD 5: Mobile-First Always
────────────────────────────────────────────────────────────────────────────────
"Design and test for mobile FIRST. If it doesn't work on a 320px screen,
it doesn't ship."

ENFORCEMENT:
☐ PixelPerfect tests all pages at 320px
☐ No horizontal scrolling on mobile
☐ Touch targets 44px minimum

LEARNED STANDARD 6: Content Completeness Over Speed
────────────────────────────────────────────────────────────────────────────────
"A complete profile for 20 entities is better than stub pages for 100
entities. Never ship placeholder content."

ENFORCEMENT:
☐ Head of Content rejects any stub/placeholder content
☐ Better to have fewer complete pages than many incomplete ones
☐ "Coming soon" sections are NOT acceptable

LEARNED STANDARD 7: SEO is Not Optional
────────────────────────────────────────────────────────────────────────────────
"Every page must have proper SEO metadata. Missing meta descriptions or
duplicate titles are release-blocking issues."

ENFORCEMENT:
☐ SEO Commander audits every page
☐ Build fails if meta tags missing
☐ Sitemap generated automatically

LEARNED STANDARD 8: Team Communication Documented
────────────────────────────────────────────────────────────────────────────────
"All QA feedback must be documented with specific file references and
actionable recommendations."

ENFORCEMENT:
☐ Each loop produces written feedback
☐ Issues list file paths and line numbers
☐ Recommendations are specific, not vague

═══════════════════════════════════════════════════════════════════════════════
```

---

## ✅ MASTER EXECUTION CHECKLIST

**Use this checklist for EVERY `/bedrock_agent` execution:**

```
BEDROCK AGENT MASTER EXECUTION CHECKLIST
═══════════════════════════════════════════════════════════════════════════════

PRE-EXECUTION
────────────────────────────────────────────────────────────────────────────────
☐ BlackTeam Brief created with Project ID (BT-YYYY-NNN)
☐ All team personas assigned
☐ User approved brief before execution
☐ Reference templates identified (WC_2026_Astro_V2, etc.)

CONTENT GENERATION
────────────────────────────────────────────────────────────────────────────────
☐ All entities created (players, teams, circuits, etc.)
☐ Historical data verified by Head of Content
☐ Statistics verified by Elias Thorne + Insight
☐ No placeholder text (TBD, TODO, Lorem ipsum)

5 RALPH LOOPS QA
────────────────────────────────────────────────────────────────────────────────
☐ Loop 1: Content Quality (Head of Content) - 85+ PASS
   └── Historical verification checklist completed
☐ Loop 2: SEO Optimization (SEO Commander) - 85+ PASS
   └── All meta tags present, keywords optimized
☐ Loop 3: Technical QA (Post Production) - 90+ PASS
   └── Zero 404 errors, all assets load
☐ Loop 4: UX/UI Review (PixelPerfect) - 85+ PASS
   └── WCAG 2.1 AA compliant, text visible
☐ Loop 5: Data Validation (Elias + Insight) - 85+ PASS
   └── All data within valid ranges

ASTRO TEMPLATE COMPLIANCE
────────────────────────────────────────────────────────────────────────────────
☐ File structure matches template standard
☐ CSS variables defined correctly
☐ Content collection schemas valid
☐ Page directors have filters and detail pages
☐ Card components consistent

RELEASE & DEPLOY
────────────────────────────────────────────────────────────────────────────────
☐ RELEASE_NOTES.md generated
☐ Director final approval
☐ Git commit with descriptive message
☐ Pushed to GitHub
☐ Deployed to Vercel
☐ Production URL tested
☐ hub/index.html updated

POST-RELEASE
────────────────────────────────────────────────────────────────────────────────
☐ /reflect invoked to capture learnings
☐ ClickUp task updated
☐ Team notified of release

═══════════════════════════════════════════════════════════════════════════════
FINAL SIGN-OFF

Project: _____________________ | Project ID: BT-_______-_______
Overall Score: _____/100 | Status: ☐ APPROVED | ☐ NEEDS REVISION

Director Signature: _________________________________
Date: _________________

═══════════════════════════════════════════════════════════════════════════════
```

---

*End of Comprehensive Persona Checklists - All personas MUST complete their assigned checklists before release approval.*
