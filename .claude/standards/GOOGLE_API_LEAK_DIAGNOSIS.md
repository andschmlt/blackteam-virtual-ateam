# R-SEO-04: Google API Leak Diagnosis Framework

**Priority:** P1 High
**Enforced Since:** 2026-02-26
**Applies To:** ALL sites experiencing traffic decline, ALL SEO audits, `/launch_site` Phase 8, `/A_Virtual_Team` SEO tasks
**Origin:** Google Content Warehouse API leak (May 2024) — 14,014 attributes across 2,596 modules

---

## Purpose

Framework for diagnosing traffic decline using parameters exposed in the Google API leak. Organizes ~50 most relevant attributes into 3 importance tiers with scoring guidance, data collection requirements, and recovery planning.

**Important caveat:** The leak exposed 14,014 attributes. We can reason about ~50 (~0.3% of total signal space). Any diagnosis is an educated guess, not a certainty. The % probabilities are subjective confidence levels. Always validate with actual data (GSC, controlled tests) before making big bets.

---

## Enforcement

| Role | Responsibility |
|------|---------------|
| B-RANK (SEO Commander) | Runs diagnosis, collects data, executes recovery |
| W-LUNA (SEO Commander) | Validates diagnosis accuracy, reviews recovery plan |
| W-EVAN (White Hat) | Validates compliance of recovery actions |
| B-WALT (White Hat Analyst) | Content quality assessment against Panda signals |

---

## Step 1: Data Collection (MANDATORY before diagnosis)

Before running any diagnosis, collect ALL available data:

| Source | Data Required | Tool |
|--------|--------------|------|
| Ahrefs | DR, traffic history (6-12 months), backlink count, ref domains, new/lost backlinks last 30d, anchor text distribution, top pages by traffic | Ahrefs API / Dashboard |
| Content | Total pages, commercial vs informational ratio, last meaningful publish date, recent migrations or URL changes | Site audit / CMS |
| GSC | Indexation status, crawl stats, manual actions, CTR by page, Core Web Vitals scores | Google Search Console |
| History | Boosting campaigns, link campaigns, URL migrations, topic expansions, CMS changes, hosting changes — with dates | PM / team context |
| SERP | Current position for main keywords, who's above you, new competitors, SERP feature changes | DataForSEO / Ahrefs |
| PostHog | NavBoost proxy metrics: pogo rate, dwell time, scroll depth, CTA CTR, engagement score | PostHog dashboard |
| Comparison | Ideally a stable/growing site in the same niche for contrast | Ahrefs |

**Rule:** The more data collected, the better the diagnosis. Skip nothing available.

---

## Step 2: Parameter Evaluation

### TIER 1 — PRIMARY RANKING SIGNALS (check these first)

#### Content Quality & Site Identity

| Parameter | What It Does | How to Check | PostHog Proxy |
|-----------|-------------|--------------|---------------|
| `siteFocusScore` / `siteRadius` / `site2vec` | Measures topical focus. Diluted sites (many unrelated topics) score lower. | Check content categories — is the site focused or scattered? | — |
| `pandaDemotion` / `babyPandaDemotion` / `babyPandaV2Demotion` | Thin content penalty. Triggers on: low word count, high commercial ratio, template abuse. | Count pages <200 words, check commercial:informational ratio. | — |
| `lowQuality` | S2V low quality score from NSR data. | Review content depth, E-E-A-T signals, author markup. | — |
| `contentEffort` | Estimated effort/quality of content production. | Compare word counts, media richness, original research vs. commodity content. | — |
| `siteAuthority` / `authorityPromotion` / `unauthoritativeScore` | Composite site authority signal. | Check DR, referring domains, brand mentions, age. | — |
| `siteType` / `sourceType` | How Google classifies the site (news vs affiliate vs e-commerce). | Review GSC Performance report — which queries trigger which pages? | — |
| `topicEmbeddings` / `pageEmbedding` / `siteEmbedding` | Semantic topic understanding. | Check if page content matches search intent for target queries. | — |

#### User Behavior & Engagement

| Parameter | What It Does | How to Check | PostHog Proxy |
|-----------|-------------|--------------|---------------|
| `navBoost` (`goodClicks` / `badClicks` / `lastLongestClicks`) | Chrome click satisfaction data. Good clicks = long engagement. Bad clicks = quick bounce. | Track user engagement patterns. | Pogo rate (<18%), Dwell time (>90s), Engagement score (>70) |
| `navDemotion` | Penalty from poor navigation/UX experience. | Check nav structure, mobile UX, interstitial usage. | Session depth, Pages per session |
| `userInteractionData` | Behavioral signals (session duration, scroll, bounce). | Monitor user behavior metrics. | Scroll depth (>60%), CTA CTR, Time on page |
| `serpDemotion` | SERP-level behavior penalty (pogo-sticking, low CTR). | Check GSC CTR by query, compare against expected CTR for position. | SERP return rate (<25%) |

#### Link Quality & Spam

| Parameter | What It Does | How to Check |
|-----------|-------------|--------------|
| `anchorSpamInfo` (`phraseAnchorSpamCount` / `SpamDays` / `SpamFraq` / `SpamRate`) | Anchor text spam detection. Flags unnatural anchor text patterns. | Ahrefs anchor text report — check for exact-match anchor concentration >15%. |
| `anchorMismatchDemotion` | Link source/target topical misalignment. | Review backlinks — are they from topically relevant sites? |
| `spamBrainTotalDocSpamScore` (0-1 float) | AI spam probability score per page. | Check for AI-generated content patterns, thin pages, doorway pages. |
| `spambrainLavcScores` | Low-Authority Verification Content score. | Check if site produces review/comparison content without demonstrated expertise. |
| `CompressedQualitySignals` | Accumulated penalty "rap sheet" — stores all historical demotions. | Historical audit — any past manual actions, penalties, or algorithm hits? |

#### Freshness

| Parameter | What It Does | How to Check |
|-----------|-------------|--------------|
| `lastSignificantUpdate` | Timestamp of last meaningful content change. | Check last publish/update dates across the site. Stale sites penalized for time-sensitive queries. |
| `contentAge` / `bylineDate` | How old the content appears. | Review article dates — are they current? |
| `FreshnessTwiddler` | Date-sensitive ranking adjustments. | Check if target queries have fresh intent (news, events, current year). |

---

### TIER 2 — SECONDARY SIGNALS (check if Tier 1 doesn't explain decline)

#### Technical & Infrastructure

| Parameter | What It Does | How to Check |
|-----------|-------------|--------------|
| `hostAge` | Domain age trust multiplier. Fresh domains sandboxed. | Whois lookup — domains <2 years may face trust deficit. |
| `pageRank` / `homepagePageRank` | Classic link authority. | Check Ahrefs DR and URL Rating for key pages. |
| `exactMatchDomainDemotion` | Keyword-stuffed domain penalty. | Does domain exactly match a commercial keyword? |
| `clutterScore` | Ad density, interstitial penalties. | Count above-the-fold ads, check for interstitials. |
| `violatesMobileInterstitialPolicy` | Mobile popup penalty. | Test mobile — any fullscreen interstitials on first click? |
| `scamness` (0-1023) | Deception probability score. | Check for misleading claims, fake reviews, deceptive practices. |
| `pqData` | Encoded page-level PageQuality signals. | Run Google Rich Results Test, check structured data errors. |
| `productReviewPDemotePage` / `productReviewPDemoteSite` | Review content demotion. | If affiliate/review site — is content first-hand experience or aggregated? |

#### Crawl & Index

| Parameter | What It Does | How to Check |
|-----------|-------------|--------------|
| `crawlBudget` signals | How frequently Google crawls the site. | GSC Crawl Stats — check pages crawled/day trend. |
| `indexTier` (`HIGH_QUALITY` / `MEDIUM` / `LOW`) | Storage tier affects retrieval speed and ranking consideration. | GSC Index Coverage — check indexed vs discovered ratio. |
| `noindex` / `robots` conflicts | Contradictory directives. | Check for noindex + sitemap inclusion (R-SEO-03h). |
| `canonicalization` signals | Duplicate content handling. | Check canonical tags resolve correctly, no self-referencing errors. |
| `hreflang` processing | International targeting. | Check hreflang tags if multilingual. |

#### YMYL & Trust

| Parameter | What It Does | How to Check |
|-----------|-------------|--------------|
| `YMYL Health Score` | Relevance to Your Money Your Life topics. | If site covers health/finance/legal — extra scrutiny on E-E-A-T. |
| `E-E-A-T` signals | Experience, expertise, authority, trust evaluation. | Check author pages, credentials, citations, About page. |
| `isNews` / `smallPersonalSite` / `isLargeChain` | Site type classifications. | How does Google classify this site? Check GSC query types. |

---

### TIER 3 — CONTEXTUAL SIGNALS (niche-specific)

#### Entity & Knowledge

| Parameter | What It Does |
|-----------|-------------|
| `entityAnnotations` | Recognized entities on the page — proper entity markup helps. |
| `authorAnnotations` | Author identity and credibility signals. |
| `knowledgeGraph` associations | Entity relationships — is the site/author in the Knowledge Graph? |

#### Link Network

| Parameter | What It Does |
|-----------|-------------|
| `linkSpamLevel` | Overall link network spam assessment. |
| `sourceType` of incoming links | HIGH / MEDIUM / LOW quality tier of linking sites. |
| `linkVelocity` signals | Rate of link acquisition/loss — sudden spikes flag manipulation. |
| Penguin-era signals | Fossilized in `CompressedQualitySignals` — historical anchor text penalties. |

#### Behavioral Advanced

| Parameter | What It Does |
|-----------|-------------|
| `crapsNewUrlSignals` / `crapsAbsoluteHostSignals` | CRAPS system click aggregates at URL and host level. |
| `chromeInTotal` | Chrome-specific behavioral data volume — low volume = less signal. |
| `Instant Glue` | 24-hour behavioral window for trending queries. |

#### Commercial & Monetization

| Parameter | What It Does |
|-----------|-------------|
| `adsScore` / `aboveTheFoldAdsRatio` | Ad placement evaluation — too many above-fold = penalty. |
| `affiliateLinkDensity` signals | Commercial intent indicators — high density on thin pages = risk. |
| `experimentalQstarSignal` | Experimental Q* ranking component — unknown weight. |

---

## Step 3: Diagnosis Output Format

After evaluating all relevant parameters:

```markdown
## Traffic Decline Diagnosis — {domain}

### Data Collected
- [ ] Ahrefs: DR, traffic, backlinks, anchors
- [ ] GSC: indexation, crawl stats, CWV, manual actions
- [ ] PostHog: NavBoost proxy metrics
- [ ] Content: page count, commercial ratio, publish dates
- [ ] SERP: positions, competitors, features
- [ ] History: changes timeline
- [ ] Comparison site: {domain}

### Top 3-5 Causes (ranked by confidence)
1. **{Parameter}** — {confidence}% — {explanation with specific data}
2. **{Parameter}** — {confidence}% — {explanation}
3. **{Parameter}** — {confidence}% — {explanation}

### Compound Effects
{Which parameters are amplifying each other — show interaction chain}

### Recovery Plan (ranked by % chance of helping)
1. {Action} — {expected impact}% — {timeline}
2. {Action} — {expected impact}% — {timeline}
3. {Action} — {expected impact}% — {timeline}

### What NOT To Do
- {Common mistake that would make it worse}
- {Common mistake}

### Quick Wins (fixable in days)
- {Misconfiguration or technical fix}
- {Quick fix}

### Data Needed to Increase Confidence
- {Missing data point} — would confirm/rule out {cause}

### Counter-Arguments (argue against own analysis)
- {Where diagnosis could be wrong} — {confidence}%
```

---

## Step 4: Follow-Up Analysis

After initial diagnosis, always run these follow-ups:

1. **Self-critique:** "Where could I be wrong? Give % confidence for each counter-argument."
2. **Data gaps:** "What data would confirm or rule out each cause?"
3. **Compound effects:** "Which parameters are amplifying each other? Show the interaction chain."
4. **Comparison:** "Compare against {stable site} in same niche — why is one declining and the other isn't?"
5. **Expected value:** "If I could only do ONE thing, what has the highest expected value?"

---

## Integration with Existing Rules

| Existing Rule | Leak Parameters Covered |
|---------------|------------------------|
| R-SEO-03i (thin content) | `pandaDemotion`, `babyPandaDemotion`, `contentEffort` |
| R-SEO-03h (sitemap parity) | `noindex`/`robots` conflicts, `indexTier` |
| R-SEO-03b (no hotlinks) | `clutterScore` (external resource loading) |
| R-SEO-03g (schema) | `entityAnnotations`, `pqData` |
| R-IMG-01 (image optimization) | `clutterScore`, Core Web Vitals signals |
| PostHog NavBoost metrics | `navBoost` (`goodClicks`/`badClicks`/`lastLongestClicks`), `serpDemotion`, `userInteractionData` |
| R-CONTENT-03 (subtle betting links) | `affiliateLinkDensity`, `spambrainLavcScores` |

---

## When to Run This Diagnosis

| Trigger | Action |
|---------|--------|
| Traffic drop >10% in 30 days | Full Tier 1 + Tier 2 diagnosis |
| Traffic drop >25% in 30 days | Full Tier 1-3 diagnosis + comparison site |
| Core update within 2 weeks | Tier 1 focused on `pandaDemotion`, `siteAuthority`, `navBoost` |
| Manual action in GSC | Immediate full diagnosis |
| Monthly routine (preventive) | Tier 1 quick-check against PostHog NavBoost metrics |
| `/launch_site` Phase 8 | Baseline check — ensure no red flags before indexing |

---

## Validation Checklist

```markdown
## R-SEO-04 DIAGNOSIS CHECKLIST
- [ ] All available data collected (Step 1)
- [ ] Tier 1 parameters evaluated
- [ ] Tier 2 parameters evaluated (if Tier 1 inconclusive)
- [ ] Top 3-5 causes identified with % confidence
- [ ] Compound effects documented
- [ ] Recovery plan ranked by expected impact
- [ ] Quick wins identified
- [ ] Counter-arguments provided (self-critique)
- [ ] Comparison site analyzed (if available)
```

---

## Related Files

- **R-SEO-02:** `~/.claude/standards/ASTRO_SEO_RULES.md` — astro-seo component standards
- **R-SEO-03:** `~/.claude/standards/ASTRO_TECHNICAL_SEO_RULES.md` — technical SEO rules
- **R-IMG-01:** `~/.claude/standards/IMAGE_OPTIMIZATION_RULES.md` — image optimization
- **POSTHOG_RULES:** `~/.claude/standards/POSTHOG_RULES.md` — NavBoost metrics (R18)
- **W-LUNA Skills:** `~/AS-Virtual_Team_System_v2/whiteteam/skills/SEO_COMMANDER_SKILLS.md`
- **B-RANK Skills:** `~/AS-Virtual_Team_System_v2/blackteam/skills/SEO_COMMANDER_SKILLS.md`

---

*Rule R-SEO-04 | Created 2026-02-26 | Source: Google Content Warehouse API leak (May 2024)*
*Approved by: B-BOB (BlackTeam Director) + W-WOL (WhiteTeam Director)*
