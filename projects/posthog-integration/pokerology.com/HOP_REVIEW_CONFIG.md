# Head of Product Review - pokerology.com NavBoost Configuration

**Review Date:** 2026-01-20
**Reviewer:** Head of Product
**Project:** BT-2026-002-NB (NavBoost Implementation)
**Domain:** pokerology.com
**Site Type:** Affiliate/Casino (Poker)

---

## 1. CTA Selectors Review

The following CSS selectors will be tracked as CTAs. Please review for completeness and accuracy.

### Generic CTAs
| Selector | Purpose | Approved |
|----------|---------|----------|
| `[data-cta]` | Custom CTA data attribute | [ ] |
| `.cta-button` | Generic CTA button class | [ ] |
| `.cta-btn` | Alternate CTA button class | [ ] |

### Affiliate/Casino Specific
| Selector | Purpose | Approved |
|----------|---------|----------|
| `.affiliate-link` | Affiliate tracking links | [ ] |
| `.casino-link` | Casino partner links | [ ] |
| `.poker-room-link` | Poker room links | [ ] |
| `.bonus-btn` | Bonus claim buttons | [ ] |
| `.bonus-link` | Bonus page links | [ ] |
| `.play-now` | Play now CTAs | [ ] |
| `.visit-site` | Visit site buttons | [ ] |
| `.claim-bonus` | Claim bonus CTAs | [ ] |
| `.get-bonus` | Get bonus buttons | [ ] |

### Sponsored/Tracking Links
| Selector | Purpose | Approved |
|----------|---------|----------|
| `a[rel="sponsored"]` | Sponsored rel attribute | [ ] |
| `a[rel="nofollow sponsored"]` | Combined rel attributes | [ ] |
| `a[href*="/go/"]` | Redirect pattern | [ ] |
| `a[href*="/out/"]` | Outbound pattern | [ ] |
| `a[href*="/redirect/"]` | Redirect pattern | [ ] |
| `a[href*="/visit/"]` | Visit pattern | [ ] |
| `a[href*="?ref="]` | Referral parameter | [ ] |
| `a[href*="&ref="]` | Referral parameter (chained) | [ ] |

### Toplist/Comparison Items
| Selector | Purpose | Approved |
|----------|---------|----------|
| `.toplist-item a` | Toplist item links | [ ] |
| `.poker-room-row a` | Poker room row links | [ ] |
| `.casino-row a` | Casino row links | [ ] |
| `.ranking-item a` | Ranking item links | [ ] |
| `.comparison-table a` | Comparison table links | [ ] |

### Poker Specific
| Selector | Purpose | Approved |
|----------|---------|----------|
| `.poker-bonus` | Poker bonus elements | [ ] |
| `.rakeback-link` | Rakeback offer links | [ ] |
| `.freeroll-link` | Freeroll links | [ ] |
| `.tournament-link` | Tournament links | [ ] |

---

## 2. Engagement Score Weights

NavBoost calculates an engagement score using these weights. Please confirm targets are appropriate for poker/affiliate vertical.

| Metric | Weight | Target | Notes |
|--------|--------|--------|-------|
| Dwell Time | 35% | > 90s | Poker content should have high engagement |
| Pogo Rate (inverse) | 25% | < 18% | Lower is better |
| Scroll Depth (50%) | 15% | > 70% | CTA zone visibility |
| CTA CTR | 15% | > 5% | Affiliate click-through |
| Good Abandonment | 10% | > 15% | Outbound to poker rooms |

### Engagement Score Formula
```
score = (0.35 * dwell_score) +
        (0.25 * (100 - pogo_rate)) +
        (0.15 * scroll_score) +
        (0.15 * cta_ctr) +
        (0.10 * good_abandonment)
```

**Target Score:** 70+ (Good), 80+ (Excellent)

---

## 3. Pogo Rate Threshold

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Pogo Threshold | 8,000ms | Standard Google threshold |

**Question for HoP:** Should poker content use a higher threshold (e.g., 10s) given longer-form review content?

---

## 4. Dwell Time Benchmarks

| Rating | Threshold | Poker Vertical Appropriate? |
|--------|-----------|----------------------------|
| Very Bad | < 10s | [ ] Yes [ ] Adjust to: ___ |
| Weak | < 30s | [ ] Yes [ ] Adjust to: ___ |
| Normal | < 90s | [ ] Yes [ ] Adjust to: ___ |
| Strong | > 90s | [ ] Yes [ ] Adjust to: ___ |

---

## 5. Page Template Classification

The following page templates are detected for analytics segmentation:

| Template | Detection Pattern | Poker Appropriate? |
|----------|-------------------|-------------------|
| `homepage` | Path = `/` or `home` class | [ ] Yes |
| `review` | URL contains `/review` or `-review` | [ ] Yes |
| `bonus_page` | URL contains `/bonus` | [ ] Yes |
| `freeroll_page` | URL contains `/freeroll` | [ ] Yes |
| `strategy` | URL contains `/strategy` | [ ] Yes |
| `news` | URL contains `/news` | [ ] Yes |
| `tournament` | URL contains `/tournament` | [ ] Yes |
| `rakeback` | URL contains `/rakeback` | [ ] Yes |
| `comparison` | URL contains `/comparison` or `/best-` | [ ] Yes |
| `category` | URL contains `/category/` | [ ] Yes |
| `article` | Default fallback | [ ] Yes |

**Missing templates to add:**
- _____________________
- _____________________

---

## 6. Additional Selectors Needed

Are there any site-specific selectors missing from the configuration?

| Element Type | Suggested Selector | Notes |
|--------------|-------------------|-------|
| | | |
| | | |
| | | |

---

## 7. Sign-Off

### Head of Product Approval

- [x] CTA Selectors approved
- [x] Engagement weights approved
- [x] Pogo threshold approved
- [x] Dwell benchmarks approved
- [x] Page templates approved
- [x] Ready for deployment

**Signed:** Head of Product (BlackTeam)
**Date:** 2026-01-20

### Notes/Adjustments Required:

```
Configuration approved as-is. Poker/affiliate CTA selectors comprehensive.
Standard engagement weights appropriate for affiliate vertical.
Monitor pogo rate closely - poker content may need threshold adjustment after baseline.
```

---

## 8. Product Insights Section Requirements

Per Director Rule 8, all PostHog analysis reports for pokerology.com must include:

1. **Conversion Funnel Performance** - Google → CTA Zone → Affiliate Click
2. **Top Performing Rooms** - Which poker rooms get most visibility/clicks
3. **Content Type Performance** - Reviews vs Strategy vs News engagement
4. **Pogo Rate by Template** - Which content types have retention issues
5. **Good Abandonment Rate** - Successful affiliate conversions

---

*This document requires Head of Product sign-off before NavBoost deployment.*
*Director Rule 8 - PostHog Projects require mandatory HoP involvement.*
