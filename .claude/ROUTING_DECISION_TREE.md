# Command Routing Decision Tree

**Version:** 1.0
**Updated:** 2026-02-03
**Purpose:** Clear guidance on which command to use for any given request

---

## Quick Reference

| Command | Use When | Team(s) | Validation |
|---------|----------|---------|------------|
| `/blackteam` | Direct execution, known approach | BlackTeam only | Built-in QA |
| `/whiteteam` | Execution OR validation of existing work | WhiteTeam only | Embedded |
| `/director` | New project requiring full planning + approval | BlackTeam | Full workflow |
| `/A_Virtual_Team` | Full lifecycle with cross-team validation | Both teams | Maximum |
| `/persona [name]` | Single specialist task | One persona | None |

---

## Decision Flowchart

```
                    START
                      |
                      v
            Is this a NEW project?
                   /    \
                 YES     NO
                  |       |
                  v       v
        Need full     Is it validation
        planning?     of existing work?
         /    \           /    \
       YES    NO        YES     NO
        |      |          |       |
        v      v          v       v
   /director  Is it    /whiteteam  Is it a
              complex?  (VALIDATE)  quick task?
              /    \               /    \
            YES    NO            YES    NO
             |      |             |       |
             v      v             v       v
        /blackteam  /persona   /persona  /blackteam
                    [name]     [name]
```

---

## Detailed Decision Guide

### Use `/director` when:

- Starting a **new multi-phase project**
- Need **stakeholder approval** before execution
- Project requires **planning and coordination**
- Multiple teams or personas will be involved
- Want **full audit trail** from intake to delivery
- Unsure which team should handle the request

**Examples:**
```
/director Build a new analytics dashboard for PostHog
/director Create content strategy for Q2 2026
/director Implement new data pipeline for affiliates
```

**What happens:**
1. Director classifies request (PROJECT/TASK/CHAT/GENERAL)
2. Checks existing ClickUp tasks
3. Assigns team based on routing rules
4. Requires explicit approval before execution
5. Full planning with leadership consultation
6. Execution with Ralph Loops QA

---

### Use `/blackteam` when:

- **Know the approach** - no planning needed
- Want **direct execution** without approval gates
- Task is **well-defined** with clear deliverables
- Don't need cross-team validation
- Time-sensitive work where planning overhead is unnecessary

**Examples:**
```
/blackteam Generate the weekly PostHog report
/blackteam Update the bedrock agent with new player data
/blackteam Fix the broken link in the WC 2026 pages
```

**What happens:**
1. Director creates project brief (lighter than /director)
2. Awaits brief approval
3. Executes with parallel specialists
4. Built-in QA (Visual QA, Release Notes, etc.)
5. Delivery with Director sign-off

---

### Use `/whiteteam` when:

**EXECUTE Mode** (keywords: build, create, implement, develop):
- Want **embedded validation** at every step
- Building something that needs continuous QA
- Quality is critical from the start

**VALIDATE Mode** (keywords: review, validate, audit, check):
- Have **existing work** that needs review
- Need **security audit** of code
- Want **SEO compliance** check
- Need **data quality** validation

**Examples:**
```
# EXECUTE mode
/whiteteam Build the authentication module with security review

# VALIDATE mode
/whiteteam Review the ETL pipeline code
/whiteteam Audit the PostHog implementation for compliance
```

**What happens:**
- **EXECUTE:** Builds with validation embedded at every step
- **VALIDATE:** Reviews existing work against standards, returns structured response

---

### Use `/A_Virtual_Team` when:

- Need **maximum quality assurance**
- Project requires **both execution AND validation**
- Want **cross-team collaboration**
- Building something **production-critical**
- Need **dual Director sign-off**

**Examples:**
```
/A_Virtual_Team Build and deploy the new dashboard with full QA
/A_Virtual_Team Complete PostHog integration with security review
/A_Virtual_Team Refactor ETL pipeline with data validation
```

**What happens:**
1. Both Directors (B-BOB + W-WOL) assess project
2. Joint planning with unified brief
3. BlackTeam executes with WhiteTeam validation checkpoints
4. Iterative revision cycles until approved
5. Joint sign-off before release

---

### Use `/persona [name]` when:

- Need a **single specialist** for a focused task
- Task is **simple and contained**
- No coordination needed
- Quick consultation or specific expertise

**Examples:**
```
/persona DataForge - Check the BigQuery query syntax
/persona SEO Commander - Quick keyword analysis for this URL
/persona PixelPerfect - Review this color scheme
```

**What happens:**
1. Loads single persona context
2. Persona executes their specialty
3. Direct response, no overhead

---

## Scenario Examples

### Scenario 1: "Generate a weekly PostHog report"
**Analysis:** Known task, well-defined, recurring
**Use:** `/blackteam`

### Scenario 2: "We need a new data pipeline for the affiliate system"
**Analysis:** New project, needs planning, multi-persona
**Use:** `/director`

### Scenario 3: "Review this code for security issues"
**Analysis:** Validation of existing work
**Use:** `/whiteteam`

### Scenario 4: "Build the new dashboard with full security audit"
**Analysis:** Execution + validation, production-critical
**Use:** `/A_Virtual_Team`

### Scenario 5: "Quick question about SEO best practices"
**Analysis:** Single specialist consultation
**Use:** `/persona SEO Commander`

### Scenario 6: "Implement authentication with built-in testing"
**Analysis:** Execution with embedded validation
**Use:** `/whiteteam` (EXECUTE mode)

---

## Anti-Patterns (What NOT to Do)

| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| Using `/director` for simple tasks | Unnecessary overhead | Use `/blackteam` or `/persona` |
| Using `/blackteam` when unsure of approach | May miss requirements | Use `/director` for planning |
| Using `/A_Virtual_Team` for validation-only | Overkill | Use `/whiteteam` in VALIDATE mode |
| Using `/persona` for complex multi-step work | No coordination | Use `/blackteam` or `/director` |
| Mixing commands in same session | Confusion | Stick to one command per workflow |

---

## Command Comparison Matrix

| Feature | /director | /blackteam | /whiteteam | /A_Virtual_Team | /persona |
|---------|-----------|------------|------------|-----------------|----------|
| Planning Phase | Full | Light | Light | Full | None |
| Approval Gates | Yes | Brief only | Brief only | Yes | None |
| Team Size | 16+ | 16 | 25 | 41+ | 1 |
| Validation | Ralph Loops | Built-in | Embedded | Cross-team | None |
| Overhead | High | Medium | Medium | High | Low |
| Best For | New projects | Known work | QA-focused | Critical work | Quick tasks |

---

## Related Files

- **TEAM_CONFIG.md** - Full team roster and routing rules
- **RALPH_LOOPS_SPECIFICATION.md** - QA iteration criteria
- **blackteam.md** - Full BlackTeam command reference
- **whiteteam.md** - Full WhiteTeam command reference
- **director.md** - Full Director workflow reference
- **A_Virtual_Team.md** - Full dual-team reference

