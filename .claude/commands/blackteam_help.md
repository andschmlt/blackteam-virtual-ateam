# BlackTeam Help Command

Display comprehensive information about the BlackTeam virtual workforce, team structure, and routing rules.

## Phase 0: RAG Context Loading

**Load team roster and rules from RAG.**

```python
from AS-Virtual_Team_System_v2.rag.rag_client import VTeamRAG
rag = VTeamRAG()
roster = rag.query("blackteam roster personas routing", collection_name="personas", top_k=5)
rules = rag.query("blackteam rules governance", collection_name="rules", top_k=3)
```

---

## Output Format

When this command is invoked, display the following information:

```
================================================================================
                            BLACKTEAM HELP
                    Virtual AI, Data & BI Strike Force
                         Paradise Media Group
================================================================================

TEAM STRUCTURE
================================================================================

                          ┌─────────────┐
                          │  DIRECTOR   │
                          │   (Boss)    │
                          └──────┬──────┘
                                 │
            ┌────────────────────┼────────────────────┐
            │                    │                    │
       ┌────┴────┐         ┌─────┴─────┐        ┌────┴────┐
       │  DATA   │         │ ANALYTICS │        │ CONTENT │
       │  TRACK  │         │   TRACK   │        │  TRACK  │
       └────┬────┘         └─────┬─────┘        └────┬────┘
            │                    │                   │
       DataForge            Elias Thorne        SEO Commander
       CodeGuard            DataViz             Head of Content
                            Insight                └── Content Mgr
                                                Head of Asset Strategy
                                                Head of Post Prod
                                                   └── Post Prod Mgr
                                                Affiliate Manager

TEAM ROSTER
================================================================================

LEADERSHIP TRACK
┌─────┬──────────────────┬─────────────────────────────┬─────────────┐
│ ID  │ Persona          │ Role                        │ Reports To  │
├─────┼──────────────────┼─────────────────────────────┼─────────────┤
│ DIR │ The Director     │ Director of AI, Data & BI   │ CTO/CEO     │
│ HOP │ Head of Product  │ Product & Strategy          │ Director    │
└─────┴──────────────────┴─────────────────────────────┴─────────────┘

DATA TRACK
┌─────┬──────────────────┬─────────────────────────────┬─────────────┐
│ ID  │ Persona          │ Role                        │ Reports To  │
├─────┼──────────────────┼─────────────────────────────┼─────────────┤
│ DF  │ DataForge        │ Senior Data Engineer        │ Director    │
│ CG  │ CodeGuard        │ Senior Code Reviewer        │ Director    │
└─────┴──────────────────┴─────────────────────────────┴─────────────┘

ANALYTICS TRACK
┌─────┬──────────────────┬─────────────────────────────┬─────────────┐
│ ID  │ Persona          │ Role                        │ Reports To  │
├─────┼──────────────────┼─────────────────────────────┼─────────────┤
│ ET  │ Elias Thorne     │ ML Engineer / Data Scientist│ Director    │
│ BID │ DataViz          │ Senior BI Developer         │ Director    │
│ DA  │ Insight          │ Senior Data Analyst         │ Director    │
└─────┴──────────────────┴─────────────────────────────┴─────────────┘

DESIGN TRACK
┌─────┬──────────────────┬─────────────────────────────┬─────────────┐
│ ID  │ Persona          │ Role                        │ Reports To  │
├─────┼──────────────────┼─────────────────────────────┼─────────────┤
│ UXD │ PixelPerfect     │ Senior UX/UI Designer       │ Director    │
└─────┴──────────────────┴─────────────────────────────┴─────────────┘

CONTENT TRACK
┌─────┬──────────────────┬─────────────────────────────┬─────────────┐
│ ID  │ Persona          │ Role                        │ Reports To  │
├─────┼──────────────────┼─────────────────────────────┼─────────────┤
│ SEO │ SEO Commander    │ Head of SEO                 │ Director    │
│ HOC │ Head of Content  │ Content Leadership          │ Director    │
│ CM  │ Content Manager  │ Content Production          │ HOC         │
│ HAS │ Head of Asset Strategy │ Content Portfolio     │ Director    │
│ HPPM│ Head of Post Prod│ Post Production Leadership  │ Director    │
│ PPM │ Post Prod Manager│ Production Operations       │ HPPM        │
│ AM  │ Affiliate Manager│ Partnership Management      │ Director    │
└─────┴──────────────────┴─────────────────────────────┴─────────────┘

TRIGGER KEYWORDS
================================================================================

Each team member is automatically assigned when these keywords appear in tasks:

┌──────────────────────┬────────────────────────────────────────────────────────┐
│ Persona              │ Trigger Keywords                                       │
├──────────────────────┼────────────────────────────────────────────────────────┤
│ DataForge            │ pipeline, etl, lakehouse, bronze, silver, gold,       │
│                      │ spark, delta                                           │
├──────────────────────┼────────────────────────────────────────────────────────┤
│ CodeGuard            │ review, pr, standards, security                        │
├──────────────────────┼────────────────────────────────────────────────────────┤
│ Elias Thorne         │ model, ml, prediction, forecast, agent, langchain,    │
│                      │ analytics                                              │
├──────────────────────┼────────────────────────────────────────────────────────┤
│ DataViz              │ dashboard, report, looker, visualization               │
├──────────────────────┼────────────────────────────────────────────────────────┤
│ Insight              │ analysis, insight, cohort, funnel, statistical         │
├──────────────────────┼────────────────────────────────────────────────────────┤
│ PixelPerfect         │ ux, ui, design, wireframe, prototype, figma,          │
│                      │ accessibility                                          │
├──────────────────────┼────────────────────────────────────────────────────────┤
│ SEO Commander        │ seo, keyword, ranking, takeover, serp                  │
├──────────────────────┼────────────────────────────────────────────────────────┤
│ Head of Content      │ editorial, brief                                       │
├──────────────────────┼────────────────────────────────────────────────────────┤
│ Content Manager      │ editorial                                              │
├──────────────────────┼────────────────────────────────────────────────────────┤
│ Head of Asset Strategy│ asset, portfolio, publisher, sponsored,              │
│                      │ update_content, dofollow                               │
├──────────────────────┼────────────────────────────────────────────────────────┤
│ Head of Product      │ product, pattern, experiment, navboost, eeat, sprint   │
├──────────────────────┼────────────────────────────────────────────────────────┤
│ Head of Post Prod    │ publish, qa, qc, release, release_notes                │
├──────────────────────┼────────────────────────────────────────────────────────┤
│ Post Prod Manager    │ publish, qa, finalize                                  │
├──────────────────────┼────────────────────────────────────────────────────────┤
│ Affiliate Manager    │ affiliate, partner, commission                         │
└──────────────────────┴────────────────────────────────────────────────────────┘

CONTENT WORKFLOW TRIGGERS (Full Team)
================================================================================

These keywords trigger the FULL content workflow with writers AND testers:

  content, article, writing  -->  Writers: HOC, CM
                             -->  Testers: SEO, HPPM, PPM

CONTENT WORKFLOW RESPONSIBILITIES
================================================================================

RULE: Content personnel WRITE only. SEO, Post Production, QA TEST all content.

┌──────────────────────┬─────────────────────────────────┬────────┬────────┐
│ Role                 │ Function                        │ Writes │ Tests  │
├──────────────────────┼─────────────────────────────────┼────────┼────────┤
│ Head of Content      │ Strategy, briefs, approval      │  YES   │   NO   │
│ Content Manager      │ Writer management, execution    │  YES   │   NO   │
│ Writers/Freelance    │ Draft content                   │  YES   │   NO   │
├──────────────────────┼─────────────────────────────────┼────────┼────────┤
│ SEO Commander        │ Keyword/H1/H2/E-E-A-T validation│   NO   │  YES   │
│ Head of Post Prod    │ Quality gates, release approval │   NO   │  YES   │
│ Post Prod Manager    │ QC validation, link checks      │   NO   │  YES   │
└──────────────────────┴─────────────────────────────────┴────────┴────────┘

WORKFLOW STAGES:
  Stage 1 (WRITE): HOC --> CM --> Writers
  Stage 2 (TEST):  SEO Commander + HPPM + PPM
  Stage 3 (PUBLISH): PPM --> Publishers

MANDATORY TESTING GATES
================================================================================

┌─────────────────┬──────────────────────┬────────────────────────────────────┐
│ Gate            │ Owner                │ Checks                             │
├─────────────────┼──────────────────────┼────────────────────────────────────┤
│ SEO Gate        │ SEO Commander        │ Keywords, H1/H2, meta tags, E-E-A-T│
│ QC Gate         │ Post Prod Manager    │ Spelling, grammar, links, images   │
│ Release Gate    │ Head of Post Prod    │ All gates passed, approval, notes  │
└─────────────────┴──────────────────────┴────────────────────────────────────┘

DEPLOYED SITES (VERCEL)
================================================================================

BEDROCK AGENT CONTENT VERTICALS
┌─────────────────────────────────┬────────────────────────────────────────────┐
│ Project                         │ URL                                        │
├─────────────────────────────────┼────────────────────────────────────────────┤
│ World Cup 2026                  │ https://wc2026-site.vercel.app             │
│ World Cup 2026 V2               │ https://wc-2026-v2.vercel.app              │
├─────────────────────────────────┼────────────────────────────────────────────┤
│ Premier League 2025-26          │ https://premier-league-2025-26.vercel.app  │
│ Premier League 2025-26 V2       │ https://premier-league-2025-26-v2.vercel.app│
├─────────────────────────────────┼────────────────────────────────────────────┤
│ Italian Serie A                 │ https://italian-serie-a.vercel.app         │
│ Italian Serie A V2              │ https://italian-serie-a-v2.vercel.app      │
├─────────────────────────────────┼────────────────────────────────────────────┤
│ Bundesliga 2025-26              │ https://bundesliga-2025-26.vercel.app      │
│ Bundesliga 2025-26 V2           │ https://bundesliga-2025-26-v2.vercel.app   │
├─────────────────────────────────┼────────────────────────────────────────────┤
│ Tennis Grand Slams              │ https://tennis-grandslams.vercel.app       │
│ Tennis Grand Slams V2           │ https://tennis-grand-slams-v2.vercel.app   │
└─────────────────────────────────┴────────────────────────────────────────────┘

Note: V2 versions use Astro 5.0 with Content Collections and Pagefind search.

COMMANDS
================================================================================

BLACKTEAM COMMANDS
┌─────────────────────┬──────────────────────────────────────────────────────┐
│ Command             │ Description                                          │
├─────────────────────┼──────────────────────────────────────────────────────┤
│ /blackteam          │ Execute project with full team                       │
│ /blackteam_help     │ Show this help (current)                             │
│ /persona [name]     │ Load specific persona                                │
│ /resume_blackteam   │ Resume previous BlackTeam session                    │
└─────────────────────┴──────────────────────────────────────────────────────┘

WORKSPACE COMMANDS
┌─────────────────────┬──────────────────────────────────────────────────────┐
│ Command             │ Description                                          │
├─────────────────────┼──────────────────────────────────────────────────────┤
│ /andre_help         │ Workspace overview                                   │
│ /codeguard          │ Code quality monitoring                              │
│ /githubaccess       │ Add GitHub collaborator                              │
│ /reflect            │ Capture session learnings                            │
│ /tasks_ROI          │ ClickUp task ROI analysis                            │
└─────────────────────┴──────────────────────────────────────────────────────┘

ANALYTICS & CONTENT COMMANDS
┌─────────────────────┬──────────────────────────────────────────────────────┐
│ Command             │ Description                                          │
├─────────────────────┼──────────────────────────────────────────────────────┤
│ /posthog_analysis   │ PostHog analytics reports                            │
│ /bedrock_agent      │ Sports content verticals generator                   │
│ /wc-news-updates    │ World Cup 2026 news system                           │
└─────────────────────┴──────────────────────────────────────────────────────┘

UTILITY COMMANDS
┌─────────────────────┬──────────────────────────────────────────────────────┐
│ Command             │ Description                                          │
├─────────────────────┼──────────────────────────────────────────────────────┤
│ /create_persona     │ Generate new BlackTeam persona                       │
└─────────────────────┴──────────────────────────────────────────────────────┘

PERSONA SHORTCUTS
  /persona director        /persona dataforge       /persona codeguard
  /persona elias           /persona dataviz         /persona insight
  /persona seo             /persona content         /persona asset
  /persona product         /persona postprod        /persona affiliate
  /persona pixelperfect

================================================================================
                    BlackTeam v1.4 | Paradise Media Group
================================================================================
```

---

## Notes

- This command provides a quick reference for the BlackTeam virtual workforce
- For detailed persona information, use `/persona [name]`
- For project execution, use `/blackteam [project description]`
- Team configuration is stored in: `~/Desktop/Virtual ATeam/BlackTeam/TEAM_CONFIG.md`
