# Validation Standards

**Version:** 1.0
**Updated:** 2026-02-03
**Purpose:** Define accuracy and validation requirements for all Claude responses and agent outputs

---

## Core Principles

1. **Accuracy over speed** - Never sacrifice correctness for quick responses
2. **Explicit over implicit** - State assumptions, don't hide them
3. **Verifiable claims** - Every claim should be traceable to a source
4. **Confidence transparency** - Always indicate certainty level

---

## Mandatory Response Elements

Every response involving data, analysis, or recommendations MUST include:

### 1. Confidence Scoring

```markdown
**Confidence:** [HIGH | MEDIUM | LOW]
```

| Level | Definition | When to Use |
|-------|------------|-------------|
| HIGH | >90% certain, verified against source | Direct data from trusted source, verified calculation |
| MEDIUM | 70-90% certain, some inference | Derived metrics, reasonable assumptions |
| LOW | <70% certain, significant uncertainty | Limited data, multiple assumptions, extrapolation |

### 2. Data Source Citation

```markdown
**Sources:**
- [Source 1]: [What data came from here]
- [Source 2]: [What data came from here]
```

**Required for:**
- All numerical data
- All metrics and KPIs
- All factual claims
- All external references

### 3. Assumptions Acknowledgment

```markdown
**Assumptions:**
- [Assumption 1]
- [Assumption 2]
```

**Must acknowledge when:**
- Using default values
- Inferring from incomplete data
- Making projections
- Applying business rules not explicitly stated

### 4. Caveats and Limitations

```markdown
**Caveats:**
- [Limitation 1]
- [Limitation 2]
```

**Must include when:**
- Data may be delayed
- Sample size is small
- Comparison period differs
- External factors not accounted for

---

## Pre-Response Checklist

Before finalizing ANY response, verify:

```markdown
## VALIDATION CHECKLIST
- [ ] Confidence level explicitly stated
- [ ] All data sources cited
- [ ] All assumptions acknowledged
- [ ] Caveats/limitations noted
- [ ] No vanity metrics used
- [ ] Actionable insights provided
- [ ] Rule compliance verified
- [ ] All numerical comparisons arithmetically verified (R-DATA-07)
- [ ] All "above/below" language matches actual math direction
```

---

## Data Validation Rules

### Rule V1: Source Verification
Before reporting any number, verify:
- Source table/API is correct
- Date range is accurate
- Filters are properly applied
- Aggregation is correct

### Rule V2: Cross-Reference Check
For critical metrics, cross-reference against:
- Power BI dashboards (18_iGaming_360v1.11)
- Known benchmarks
- Historical patterns

### Rule V3: Sanity Check
Before presenting data, ask:
- Does this number make sense?
- Is it within expected range?
- Does it match historical trends?
- Are there obvious anomalies?

### Rule V5: Numerical Comparison Validation (R-DATA-07) — MANDATORY
**Added:** 2026-02-06 | **Severity:** P0 (Critical) | **Applies to:** ALL teams, ALL responses

Before using ANY comparative language (above/below/higher/lower/exceeds/trails/outperforms):

| Step | Action | Example |
|------|--------|---------|
| **1. Extract** | Identify both numbers (metric + benchmark) | EPF = $430.91, Portfolio avg = $536.44 |
| **2. Compare** | Perform arithmetic: is metric > or < benchmark? | $430.91 < $536.44 |
| **3. Language** | Use correct directional word | "below" (NOT "above") |
| **4. Verify** | Re-read the full sentence — does it make mathematical sense? | "$430.91 EPF ($105.53 below portfolio average of $536.44)" |

**Comparison Language Rules:**

| Condition | Correct Language | Wrong Language |
|-----------|-----------------|----------------|
| Metric > Benchmark | "above", "exceeds", "outperforms", "higher than" | "below", "under", "trails" |
| Metric < Benchmark | "below", "under", "trails", "lower than" | "above", "exceeds", "outperforms" |
| Metric ≈ Benchmark (±5%) | "in line with", "close to", "comparable to" | "well above", "well below" |

**Origin:** Pitaya stated "$430.91 EPF (well above portfolio average of $536.44)" — a mathematical inversion error caught by Andre Schembri.

**Enforcement:**
- **BlackTeam:** B-DANA (DataViz), B-ALEX (Insight) must validate before presenting
- **WhiteTeam:** W-ZARA (Report Accuracy), W-INGA (Analytics QA) must catch in review
- **Pitaya/Agents:** Pre-response math check is MANDATORY

**Failure = AUTOMATIC REVISION** — any response with inverted comparison language must be corrected immediately.

### Rule V4: Unit Clarity
Always specify:
- Currency ($, EUR, etc.)
- Time period (daily, weekly, monthly)
- Percentage basis (of what?)
- Absolute vs relative values

---

## Prohibited Practices

### Never Do:
- Present unverified data as fact
- Use vanity metrics (impressions without context)
- Make claims without sources
- Hide assumptions
- Overstate confidence
- Ignore anomalies
- Round numbers without noting

### Always Avoid:
- "I believe..." (use data instead)
- "Probably..." without confidence level
- "Approximately..." without range
- "Many/few..." without numbers

---

## Output Format Templates

### Analysis Response Template

```markdown
## [Analysis Title]

**Confidence:** [HIGH/MEDIUM/LOW]
**Data Period:** [Date range]

### Key Findings
1. [Finding 1] - Source: [Source]
2. [Finding 2] - Source: [Source]

### Metrics
| Metric | Value | Source | Confidence |
|--------|-------|--------|------------|
| [Metric 1] | [Value] | [Source] | [H/M/L] |

### Assumptions
- [Assumption 1]

### Caveats
- [Caveat 1]

### Recommendations
1. [Actionable recommendation]
```

### Data Query Response Template

```markdown
## Query Results

**Query:** [Description]
**Source:** [Table/API]
**Confidence:** [HIGH/MEDIUM/LOW]

### Results
[Data presentation]

### Validation
- Cross-checked against: [Reference]
- Sanity check: [PASS/NOTE]

### Notes
- [Any relevant context]
```

---

## Agent-Specific Standards

### BI-Chatbot
- Must distinguish NP vs LP revenue
- Must include LIMIT clause
- Must exclude Jan 1 for FTD trends
- Must log all sessions

### Pitaya (WOL)
- Max 3 recommendations per response
- No vanity metrics
- Revenue = Commission + Fixed Fees
- Brand ≠ Domain ≠ URL

### CARLOS
- Must strip ID fields from SQL results
- Must cite query source
- Must indicate routing confidence

---

## Quality Metrics

Track these for continuous improvement:

| Metric | Target | Measurement |
|--------|--------|-------------|
| Source Citation Rate | 100% | Claims with sources / Total claims |
| Confidence Accuracy | >90% | Correct predictions at stated confidence |
| Assumption Transparency | 100% | Stated assumptions / Actual assumptions |
| Rework Rate | <10% | Corrections needed / Total responses |

---

## Enforcement

### Self-Check
Before sending any response, run through the validation checklist.

### Peer Review
For critical outputs, request WhiteTeam validation.

### Audit Trail
All responses should be traceable:
- What data was used
- What assumptions were made
- What confidence was assigned

---

## Related Files

- **RALPH_LOOPS_SPECIFICATION.md** - QA iteration standards
- **TEAM_CONFIG.md** - Validator assignments
- **API_ERROR_HANDLING.md** - Error handling standards

