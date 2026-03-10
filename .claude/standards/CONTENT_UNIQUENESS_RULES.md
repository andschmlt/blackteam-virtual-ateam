# R-CONTENT-06: Money Page Content Uniqueness Gate

**Priority:** P1 High
**Added:** 2026-03-03
**Origin:** CEO directive — all casino/money pages must be substantially different to avoid Google's `racterScores` (API leak ID 52) and duplicate content penalties.

## Rule

All money pages (casino, betting, affiliate roundup) on the same site MUST have **≥50% pairwise content difference** as measured by SequenceMatcher normalized text comparison.

## When to Check

**MANDATORY** after every Palm article generation (`/content_palm` Phase 10a post-processing):

1. After Palm returns the article content
2. Before saving to the content collection
3. Compare the NEW article against ALL existing money pages on the same site
4. If any pairwise similarity exceeds 50%, the article is **BLOCKED** until rewritten

## How to Check

```python
from difflib import SequenceMatcher
import re

def normalize(text):
    """Strip markdown, lowercase, collapse whitespace."""
    text = re.sub(r'[#*|\-_\[\]()>]', ' ', text.lower())
    return re.sub(r'\s+', ' ', text).strip()

def check_uniqueness(new_body, existing_bodies):
    """Returns list of (filename, similarity%) pairs that FAIL."""
    new_norm = normalize(new_body)
    failures = []
    for name, body in existing_bodies.items():
        ratio = SequenceMatcher(None, new_norm, normalize(body)).ratio()
        sim_pct = ratio * 100
        if sim_pct > 50:
            failures.append((name, sim_pct))
    return failures
```

## Thresholds

| Metric | Threshold | Action |
|--------|-----------|--------|
| Pairwise text similarity | ≤50% | PASS |
| Pairwise text similarity | 50-65% | SOFT FAIL — flag for review, may pass with justification |
| Pairwise text similarity | >65% | HARD FAIL — BLOCKED, must rewrite |
| Duplicate sentences (>40 chars) | ≤10 shared sentences | PASS (boilerplate like disclaimers OK) |
| Duplicate sentences | >10 shared sentences | FLAG — review for templated content |

## What Counts as "Different"

Acceptable similarities (excluded from penalty):
- TopList embed code (identical across all money pages — structural)
- Responsible gambling disclaimers (legally required boilerplate)
- Registration step instructions (factual process description)
- Brand spec sheets (factual data — bonus amounts, wagering, license)

Must be unique per article:
- Introduction / hook paragraph
- Brand review narrative and testing sections
- Comparison analysis and editorial opinion
- FAQ questions and answers
- Methodology description
- Conclusion / summary

## Integration Points

- `/content_palm` Phase 10a: Run uniqueness check before saving
- `/A_Virtual_Team` Quality Gates: Add "Content Uniqueness Gate"
- `PALM_CONTENT_RULES.md`: Reference this rule
- WhiteTeam W-VERA: Validate uniqueness during content QA

## Current Baseline (2026-03-03)

australiafootball.com casino articles — all pairs ≥89.9% different:

| Pair | Similarity | Difference |
|------|-----------|------------|
| Highest: blackjack vs payid | 10.1% | 89.9% |
| Lowest: casinos vs payid | 2.8% | 97.2% |
| Average across 15 pairs | ~6.5% | ~93.5% |

## API Leak Context

- `racterScores` (ID 52): Google flags sites with templated/duplicate content across money pages
- `contentEffort` (ID 45): Each page must demonstrate unique editorial effort
- Pokerology.com decline likely caused by high gambling ratio + similar content across pages
- This rule prevents the same pattern on australiafootball.com
