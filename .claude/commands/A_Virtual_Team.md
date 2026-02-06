# /A_Virtual_Team - Full Virtual ATeam Orchestration

Launch the complete Virtual ATeam with **BlackTeam** (execution) and **WhiteTeam** (validation) working together.

## Arguments

Arguments: $ARGUMENTS

---

## Team Overview

```
                    VIRTUAL ATEAM
         ================================

    BLACKTEAM (Execution)     WHITETEAM (Validation)
    ==================        ====================
    B-BOB (Director)    <-->  W-WOL (Director)
         |                         |
    16 Specialists           25 Validators
         |                         |
         v                         v
    [Build & Create]  --->  [Review & Approve]
```

**Total Team Size:** 41+ personas working in concert

---

## How It Works

### Dual-Team Workflow

1. **BlackTeam executes** - Creates, builds, and delivers
2. **WhiteTeam validates** - Reviews, audits, and approves
3. **Loop until approved** - Revisions handled collaboratively
4. **Release** - Only after both teams sign off

```
[Request] --> [BlackTeam Executes] --> [WhiteTeam Validates]
                      ^                        |
                      |                        v
                      +--- [NEEDS_REVISION] ---+
                                               |
                                          [APPROVED]
                                               |
                                               v
                                          [RELEASE]
```

---

## Team Rosters

### BlackTeam (16 Specialists)

| # | Persona | Code | Specialty |
|---|---------|------|-----------|
| 1 | The Director | B-BOB | Strategy, Coordination |
| 2 | DataForge | B-FORG | Data Engineering, Pipelines |
| 3 | CodeGuard | B-CODY | Code Quality, Standards |
| 4 | PixelPerfect | B-MAX | UX/UI Design |
| 5 | SEO Commander | B-RANK | SEO Strategy |
| 6 | Elias Thorne | B-ELIA | ML/Data Science |
| 7 | DataViz | B-DANA | BI Development |
| 8 | Insight | B-ALEX | Data Analysis |
| 9 | Head of Content | B-NINA | Content Strategy |
| 10 | Content Manager | B-CONT | Content Production |
| 11 | Affiliate Manager | B-AMIR | Partnerships |
| 12 | Head of Post Production | B-POST | Production QA |
| 13 | Post Production Manager | B-QUEN | Production Ops |
| 14 | Head of Product | B-PROD | Product Strategy |
| 15 | Head of Asset Strategy | B-HUGO | Portfolio Mgmt |
| 16 | Tech Lead | B-TECH | Infrastructure |

### WhiteTeam (25 Validators)

| # | Persona | Code | Specialty | Validates |
|---|---------|------|-----------|-----------|
| 1 | Wolfgang Meyer | W-WOL | Director | B-BOB |
| 2 | Sven Erikson | W-SVEN | Data Quality | B-FORG |
| 3 | Felix Chang | W-FLUX | Code Security | B-CODY |
| 4 | Maya Patel | W-MAYA | Accessibility | B-MAX |
| 5 | Lars Nielsen | W-LARS | SEO Compliance | B-RANK |
| 6 | Thor Andersen | W-THOR | ML Validation | B-ELIA |
| 7 | Zara Okonkwo | W-ZARA | Report Accuracy | B-DANA |
| 8 | Inga Lindqvist | W-INGA | Analytics QA | B-ALEX |
| 9 | Nina Kowalski | W-NINA | Editorial | B-NINA |
| 10 | Quinn Murphy | W-QUIN | QA Lead | B-QUEN |
| 11 | Gordon Blake | W-GARD | Security | (All) |
| 12 | Kyle Brennan | W-KYLE | Research | B-REES |
| 13 | Petra Novak | W-PETR | Partnerships | B-AMIR |
| 14 | Oscar Mendez | W-OSCA | Production | B-POST |
| 15 | Hannah Park | W-HANN | Product | B-PROD |
| 16 | Ivan Petrov | W-IVAN | Architecture | B-TECH |
| 17 | Eva Schmidt | W-EVA | Portfolio | B-HUGO |
| 18 | Vera Santos | W-VERA | Content | B-CONT |
| 19 | Diana Cross | W-DIAN | Strategy | B-HEAD |
| 20 | Marcus Webb | W-MARC | Compliance | (All) |
| 21 | Lily Chen | W-LILY | Documentation | (All) |
| 22 | Raj Sharma | W-RAJ | Integration | (All) |
| 23 | Astrid Berg | W-ASTR | Performance | (All) |
| 24 | Miles Cooper | W-MILE | Content Architecture | B-NINA |

---

## Usage

```
/A_Virtual_Team [project or task description]
```

**Examples:**
```
/A_Virtual_Team Build and deploy the new analytics dashboard with full QA
/A_Virtual_Team Create content strategy for europeangaming.eu with SEO audit
/A_Virtual_Team Refactor the ETL pipeline with security review
/A_Virtual_Team Complete end-to-end PostHog integration with validation
```

---

## Execution Phases

### Phase 0: RAG Context Loading (MANDATORY - Before Any Execution)

**CRITICAL:** Before any team member begins work, load relevant knowledge from the RAG system. This ensures learnings from past sessions inform current execution.

**Actions:**

1. **Read RAG learnings files** relevant to the current task:
   ```bash
   # Read recent BlackTeam learnings
   ls ~/AS-Virtual_Team_System_v2/blackteam/skills/learnings/ | tail -5
   # Read each relevant file found above

   # Read recent WhiteTeam learnings
   ls ~/AS-Virtual_Team_System_v2/whiteteam/skills/learnings/ | tail -5
   # Read each relevant file found above
   ```

2. **Read Pitaya feedback corrections** (approved patterns):
   ```bash
   cat ~/pitaya/knowledge/feedback_corrections.md
   ```

3. **Read project-specific context** from RAG sources:
   ```bash
   # Check for relevant project documentation
   ls ~/AS-Virtual_Team_System_v2/docs/

   # Check business questions RAG
   cat ~/AS-Virtual_Team_System_v2/BUSINESS_QUESTIONS_RAG.md | head -100
   ```

4. **Apply loaded context** to the current task:
   - Identify past learnings that apply to this project
   - Note any corrections or patterns from Pitaya feedback
   - Reference relevant rules and governance from RAG
   - Brief both Directors on applicable historical context

**Output:**
```markdown
## RAG Context Loaded

**Collections Consulted:**
- [ ] Learnings (BlackTeam): [N files read, key insights]
- [ ] Learnings (WhiteTeam): [N files read, key insights]
- [ ] Pitaya Feedback Corrections: [N corrections applicable]
- [ ] Project Documentation: [Relevant docs found]
- [ ] Business Questions: [Relevant Q&A patterns]

**Applicable Past Learnings:**
1. [Learning from previous session that applies]
2. [Pattern or correction to follow]

**Context Applied:** YES/NO
```

---

### Phase 1: Joint Intake

**Both Directors consulted:**

1. **B-BOB (BlackTeam Director)** - Assesses execution requirements
2. **W-WOL (WhiteTeam Director)** - Defines validation criteria

```markdown
## Virtual ATeam Project Intake

**Project:** [Name from arguments]
**Date:** [Today]

### BlackTeam Assessment (B-BOB)
- Execution complexity: [High/Medium/Low]
- Required specialists: [List]
- Estimated deliverables: [List]

### WhiteTeam Assessment (W-WOL)
- Validation requirements: [List]
- Required validators: [List]
- Quality gates: [List]

### Cross-Team Coordination
- Critical handoff points: [List]
- Mandatory reviews: [List]
```

### Phase 2: BlackTeam Execution

BlackTeam executes with **built-in validation checkpoints**:

1. **Parallel work streams** - Multiple specialists working simultaneously
2. **Checkpoint triggers** - Auto-notify WhiteTeam at key milestones
3. **Continuous logging** - All activities tracked

**Automatic WhiteTeam Triggers:**
- Code complete -> W-FLUX (Code Auditor)
- Content ready -> W-VERA (Content QA)
- UI changes -> W-MAYA (UX Reviewer)
- Data pipeline -> W-SVEN (Data Validator)
- SEO implementation -> W-LARS (SEO Auditor)
- Security-sensitive -> W-GARD (Guardian)

### Phase 3: WhiteTeam Validation

WhiteTeam validators review in parallel with execution:

1. **Concurrent reviews** - Don't wait for full completion
2. **Incremental feedback** - Early issue detection
3. **SLA compliance** - 4-hour response time

**Validation Statuses:**
- `APPROVED` - Ready for next phase/release
- `NEEDS_REVISION` - Returns to BlackTeam with specific feedback
- `REJECTED` - Requires significant rework

### Phase 4: Iteration (if needed)

If `NEEDS_REVISION`:

1. WhiteTeam provides specific, actionable feedback
2. BlackTeam addresses each item
3. Re-submit for validation
4. Repeat until `APPROVED`

### Phase 5: Joint Sign-Off & Release

**Both Directors must approve:**

```markdown
## Virtual ATeam Release Authorization

**Project:** [Name]
**Version:** [X.X]
**Date:** [Today]

### BlackTeam Sign-Off
**Director:** B-BOB (The Director)
**Status:** APPROVED
**Deliverables:**
- [List of completed deliverables]

### WhiteTeam Sign-Off
**Director:** W-WOL (Wolfgang Meyer)
**Status:** APPROVED
**Validations Passed:**
- [List of passed validations]

### Joint Authorization
- [ ] All quality gates passed
- [ ] All validations approved
- [ ] Release notes complete
- [ ] Stakeholder confirmation received

**AUTHORIZED FOR RELEASE:** YES/NO

---
B-BOB Signature: _________________ | Date: _________
W-WOL Signature: _________________ | Date: _________
```

---

## Quality Gates (Combined)

### BlackTeam Gates
- [ ] All tasks completed
- [ ] Code reviewed by CodeGuard
- [ ] Visual QA by PixelPerfect (if UI)
- [ ] Release notes generated

### WhiteTeam Gates
- [ ] Security review by W-GARD
- [ ] Code audit by W-FLUX
- [ ] Content QA by W-VERA (if content)
- [ ] SEO audit by W-LARS (if SEO)
- [ ] Data validation by W-SVEN (if data)
- [ ] UX review by W-MAYA (if UI)

### Numerical Accuracy Gate (R-DATA-07) — MANDATORY FOR ALL RESPONSES
- [ ] All "above/below/higher/lower" comparisons arithmetically verified
- [ ] Metric vs benchmark direction matches language used
- [ ] No auto-generated comparison phrases accepted without math proof
- [ ] Pre-Response Math Check: Extract → Compare → Language → Verify

### Joint Gates
- [ ] Both Directors approve
- [ ] All cross-team handoffs documented
- [ ] Activity logs complete
- [ ] ClickUp updated

---

## Activity Logging

All activities logged to unified system:

```bash
# BlackTeam execution
bash /home/andre/AS-Virtual_Team_System_v2/blackteam/tools/log_activity.sh task "B-BOB" "DataForge" "Build ETL pipeline"

# WhiteTeam validation
bash /home/andre/AS-Virtual_Team_System_v2/blackteam/tools/log_activity.sh review "W-FLUX" "B-CODY" "Code audit complete"

# Cross-team handoff
bash /home/andre/AS-Virtual_Team_System_v2/blackteam/tools/log_activity.sh handoff "B-CODY" "W-FLUX" "Code ready for security review"

# Joint decision
bash /home/andre/AS-Virtual_Team_System_v2/blackteam/tools/log_activity.sh decision "B-BOB+W-WOL" "" "Release authorized"
```

**Fallback:** If logging fails, see `/home/andre/.claude/standards/API_ERROR_HANDLING.md`

---

## File Locations

**Reference:** See `/home/andre/.claude/PATH_MAPPINGS.md` for complete path reference.

### BlackTeam
- **Personas:** `/home/andre/AS-Virtual_Team_System_v2/blackteam/personas/`
- **Skills:** `/home/andre/AS-Virtual_Team_System_v2/blackteam/skills/`
- **Prompts:** `/home/andre/AS-Virtual_Team_System_v2/blackteam/skills/prompts/`
- **Rules:** `/home/andre/AS-Virtual_Team_System_v2/blackteam/rules/`

### WhiteTeam
- **Personas:** `/home/andre/AS-Virtual_Team_System_v2/whiteteam/personas/`
- **Skills:** `/home/andre/AS-Virtual_Team_System_v2/whiteteam/skills/`
- **Prompts:** `/home/andre/AS-Virtual_Team_System_v2/whiteteam/skills/prompts/`
- **Rules:** `/home/andre/AS-Virtual_Team_System_v2/whiteteam/rules/`

### Shared Configuration
- **Team Config:** `/home/andre/AS-Virtual_Team_System_v2/TEAM_CONFIG.md`
- **Ralph Loops:** `/home/andre/AS-Virtual_Team_System_v2/RALPH_LOOPS_SPECIFICATION.md`
- **Routing Guide:** `/home/andre/.claude/ROUTING_DECISION_TREE.md`
- **Activity Logs:** `/home/andre/AS-Virtual_Team_System_v2/blackteam/logs/`
- **Project Registry:** `/home/andre/AS-Virtual_Team_System_v2/PROJECT_REGISTRY.json`

---

## Your Task

When `/A_Virtual_Team` is invoked:

1. **Load RAG context (Phase 0)** - Read learnings, corrections, and patterns from past sessions (MANDATORY)
2. **Activate both teams** - Load BlackTeam and WhiteTeam contexts
3. **Joint intake** - Both Directors assess the project (informed by RAG context)
4. **Create unified brief** - Combined execution + validation plan
5. **Execute with validation checkpoints** - BlackTeam builds, WhiteTeam reviews
6. **Iterate until approved** - Handle revisions collaboratively
7. **Joint sign-off** - Both Directors authorize release
8. **Log all activities** - Unified activity tracking
9. **Invoke /reflect** - Capture learnings from both teams
10. **Invoke /capture_learnings** - Update RAG index (MANDATORY - closes the read/write loop)

---

## Output Format

```markdown
## Virtual ATeam Execution Complete

### Project: [Name]
**Status:** [Complete/Partial/Blocked]
**Teams Engaged:** BlackTeam (16) + WhiteTeam (25)

### Execution Summary (BlackTeam)
- Specialists activated: [Count]
- Tasks completed: [Count]
- Deliverables: [List]

### Validation Summary (WhiteTeam)
- Validators engaged: [Count]
- Reviews completed: [Count]
- Final status: [All APPROVED]

### Cross-Team Metrics
- Handoffs: [Count]
- Revision cycles: [Count]
- Time to approval: [Duration]

### Deliverables
[List of final deliverables]

### Joint Recommendations
1. [Recommendation from combined team insight]
2. [Recommendation]

---
**BlackTeam Director (B-BOB):** APPROVED
**WhiteTeam Director (W-WOL):** APPROVED

*Full activity log available at ~/virtual-ateam/BlackTeam/logs/*
```

---

## Quick Reference

| Command | Team | Purpose |
|---------|------|---------|
| `/blackteam` | BlackTeam only | Execution without validation |
| `/whiteteam` | WhiteTeam only | Validation of existing work |
| `/A_Virtual_Team` | Both teams | Full execution + validation |
| `/persona [name]` | Single persona | Load specific specialist |
| `/reflect` | Both teams | Capture learnings |

---

---

## Knowledge Capture (MANDATORY)

At the end of every Virtual ATeam session, **ALWAYS** invoke `/capture_learnings`:

```bash
# Update RAG with session learnings
python3 ~/AS-Virtual_Team_System_v2/rag/scripts/index_all.py
```

This ensures:
- Learnings are written to markdown files (BlackTeam + WhiteTeam)
- RAG index is updated with new knowledge
- Document count is verified
- Changes are committed to git

**Rule G4:** All learnings must be captured to BOTH files AND RAG for semantic retrieval.

---

**Virtual ATeam Motto:** *"Build with excellence. Validate with rigor. Ship with confidence."*
