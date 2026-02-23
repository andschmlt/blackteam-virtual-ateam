# /redteam - Red Team Adversarial Challenge System

Launch the Red Team to challenge WhiteTeam-approved deliverables through adversarial testing.

## Arguments

Arguments: $ARGUMENTS

---

## Team Overview

```
                    RED TEAM
         ================================

    R-REX (Director)
         |
    ┌────┴────────────────────────────────┐
    │                                      │
    META-VALIDATION    ADVERSARIAL         │
    SQUAD (R-OWL)      SQUAD (R-KAT)      │
    ├── R-DLTA         ├── R-BRCH         │
    ├── R-DRFT         ├── R-LENS         │
    ├── R-FORG         ├── R-JOLT         │
    ├── R-ROOT         ├── R-TRIP         │
    ├── R-ECHO         ├── R-NDEL         │
    └── R-SNAR         ├── R-CIPH         │
                       └── R-JAMR         │
                                          │
    SECURITY &          PROCESS &          │
    INTEGRATION         ANALYSIS           │
    (R-ZERO)           (R-SNAR)            │
    ├── R-MESH         ├── R-OVRD         │
    ├── R-NULL         ├── R-BLPR         │
    ├── R-DAGR         ├── R-SENT         │
    ├── R-PROB         ├── R-HAWK         │
    ├── R-KRAT         ├── R-CRSH         │
    └── R-VENM         └── R-VRTX         │
    └──────────────────────────────────────┘
```

**Total Team Size:** 29 personas (1 Director + 28 Specialists)
**Mission:** *"Trust nothing. Verify everything. Break what you can."*

---

## How It Works

### Ribbon Workflow Position

```
[REQUEST] → BLACKTEAM → WHITETEAM → REDTEAM → CERTIFIED
              execute     validate    challenge
                                        │
                                   if FLAGGED:
                                        ↓
                                   BLACKTEAM (remediate)
                                        ↓
                                   WHITETEAM (re-validate)
                                        ↓
                                   REDTEAM (re-check)
                                        ↓
                                   CERTIFIED or ESCALATE
```

Red Team receives deliverables ONLY after WhiteTeam APPROVED status.
Max 2 ribbon cycles. After 2 → escalate to Stakeholder.

---

## Seven Red Gates

| Gate | Code | Lead | Focus | Pass |
|------|------|------|-------|------|
| Validation Integrity | RG-1 | R-OWL | Did WT validate what they claimed? | 100% |
| Adversarial Edge Cases | RG-2 | R-KAT | Empty inputs, boundaries, encoding | 95% |
| Regression & Drift | RG-3 | R-DRFT | Does change break existing work? | 100% |
| Systemic Bias | RG-4 | R-LENS | Hidden bias in content/data/algo | 95% |
| Security Penetration | RG-5 | R-ZERO | Active exploit attempts | 100% |
| Integration Stress | RG-6 | R-MESH + R-JOLT | API resilience, failure cascade | 90% |
| Root Cause & Pattern | RG-7 | R-ROOT | Known anti-pattern repetition? | 100% |

---

## Challenge Outcomes

| Status | Meaning | Next Step |
|--------|---------|-----------|
| **CERTIFIED** | All 7 Red Gates passed | Release authorized (triple sign-off) |
| **FLAGGED** | Issues found WT missed | Return to BT with R-FINDINGS |
| **ESCALATED** | Systemic/process issue | Stakeholder review required |

---

## Execution Phases

### Phase 0: Load Context

```bash
# Read Red Team learnings
ls ~/AS-Virtual_Team_System_v2/redteam/skills/learnings/ | tail -5
# Read anti-pattern database
cat ~/AS-Virtual_Team_System_v2/redteam/anti-patterns/ANTI_PATTERN_DATABASE.md
```

### Phase 1: Challenge Intake (R-REX)

1. Receive T18 Challenge Request from W-WOL
2. Review deliverable package and WT validation summary
3. Assign Red Gate leads
4. Set challenge timeline (6h standard, 3h critical)

### Phase 2: Red Gate Execution (Parallel)

```
RG-1 (R-OWL) ──► Sequential first (must pass)
                     │
          ┌──────────┼──────────┐──────────┐
          │          │          │          │
       RG-2       RG-3       RG-4       RG-5
      (R-KAT)   (R-DRFT)   (R-LENS)   (R-ZERO)
          │          │          │          │
          └──────────┼──────────┘──────────┘
                     │
          ┌──────────┼──────────┐
          │          │          │
       RG-6       RG-7
    (R-MESH+JOLT) (R-ROOT)
          │          │
          └──────────┘
                │
          CERTIFICATION
```

### Phase 3: Findings & Report

1. Each gate lead submits findings
2. R-REX aggregates into T19 Challenge Report
3. Issue: CERTIFIED / FLAGGED / ESCALATED
4. If FLAGGED: Generate R-FINDINGS with remediation instructions

### Phase 4: Triple Sign-Off (if CERTIFIED)

```markdown
B-BOB Signature: _________________ | APPROVED
W-WOL Signature: _________________ | APPROVED
R-REX Signature: _________________ | CERTIFIED
```

---

## Red Team Rules

| Rule | Description |
|------|-------------|
| R-RED-01 | Independence — no BT/WT communication during challenge |
| R-RED-02 | Evidence-based — every FLAG needs reproducible proof |
| R-RED-03 | Proportional response — severity matches actual risk |
| R-RED-04 | No execution — Red tests/reports, never creates/fixes |
| R-RED-05 | WT notification — gaps in WT validation reported in T19 |
| R-RED-06 | Anti-pattern database — all findings logged |
| R-RED-07 | Scoped re-check — only re-check flagged items |
| R-RED-08 | Challenge SLA — 6h standard, 3h critical |
| R-RED-09 | Quarterly self-audit — WT reviews Red false positive rate |
| R-RED-10 | Cycle limits — max 2 ribbon cycles then escalate |

---

## File Locations

- **Personas:** `~/AS-Virtual_Team_System_v2/redteam/personas/`
- **Skills:** `~/AS-Virtual_Team_System_v2/redteam/skills/`
- **Prompts:** `~/AS-Virtual_Team_System_v2/redteam/skills/prompts/`
- **Rules:** `~/AS-Virtual_Team_System_v2/redteam/rules/`
- **Frameworks:** `~/AS-Virtual_Team_System_v2/redteam/frameworks/`
- **Templates:** `~/AS-Virtual_Team_System_v2/redteam/templates/`
- **Workflows:** `~/AS-Virtual_Team_System_v2/redteam/workflows/`
- **Anti-Patterns:** `~/AS-Virtual_Team_System_v2/redteam/anti-patterns/`

---

## Usage

```
/redteam [deliverable or challenge description]
```

**Examples:**
```
/redteam Challenge the australiafootball.com deployment
/redteam Stress-test the PostHog integration for betanews.com
/redteam Audit the SEO implementation for europeangaming.eu
/redteam Security review of the ETL pipeline
```

---

## Output Format

```markdown
## Red Team Challenge Report (T19)

### Challenge: [Name]
**Status:** CERTIFIED / FLAGGED / ESCALATED
**Date:** [Today]
**Challenge ID:** RT-YYYY-NNN

### Red Gate Results

| Gate | Lead | Score | Status |
|------|------|-------|--------|
| RG-1 | R-OWL | XX% | PASS/FAIL |
| RG-2 | R-KAT | XX% | PASS/FAIL |
| RG-3 | R-DRFT | XX% | PASS/FAIL |
| RG-4 | R-LENS | XX% | PASS/FAIL |
| RG-5 | R-ZERO | XX% | PASS/FAIL |
| RG-6 | R-MESH+R-JOLT | XX% | PASS/FAIL |
| RG-7 | R-ROOT | XX% | PASS/FAIL |

### Findings Summary
[Findings or "No actionable findings"]

### Anti-Pattern Check
[Matched patterns or "No known anti-patterns detected"]

### Certification

---
R-REX Signature: _________________ | CERTIFIED/FLAGGED/ESCALATED
Date: _________________
```

---

*Red Team Motto: "Trust nothing. Verify everything. Break what you can."*
