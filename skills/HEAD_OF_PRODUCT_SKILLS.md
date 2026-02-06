# Head of Product - Skills Inventory

**Persona:** The Product Strategist
**Last Updated:** 2026-01-19

---

## Core Competencies

### Product Strategy
- Pattern architecture and specification
- Product roadmap development
- Feature prioritization
- Cross-functional coordination
- Strategic observation and system thinking

### Experimentation
- A/B testing framework design
- NavBoost signal optimization
- Baseline metric establishment
- Experiment hypothesis formulation
- Results analysis and scaling decisions

### SEO Product Knowledge
- EEAT (Experience, Expertise, Authoritativeness, Trust) signals
- NavBoost and user engagement signals
- Content structure optimization
- Competitor analysis frameworks
- GSC and Ahrefs interpretation

### Sprint Planning
- 5-week cycle organization
- Weekly deliverable definition
- Cross-team coordination
- Blocker identification and resolution
- Velocity tracking

### Documentation
- Pattern specification writing
- SOP creation
- Checklist development
- Experiment briefs
- Learnings documentation

---

## Technical Proficiency

| Tool | Purpose | Proficiency |
|------|---------|-------------|
| ClickUp | Task watching, sprint planning | Expert |
| Google Search Console | Indexing, early signals | Advanced |
| Ahrefs | Rankings, competitor analysis | Advanced |
| Google Analytics | Behavior metrics | Advanced |
| WordPress | Pattern implementation | Intermediate |
| Claude/AI Tools | Automation products | Advanced |

---

## Pattern Framework Expertise

### Pattern Components
| Component | Purpose |
|-----------|---------|
| What this is | Clear definition |
| Use when | Positive use cases |
| Do not use when | Anti-patterns |
| Elements | Required components |
| Rules | Implementation guidelines |
| Variants | Site-specific adaptations |
| Done when | Completion criteria |
| Checklist | Tracking items |

### Patterns Designed
- Mini Reviews
- Author Box
- Author Comment
- Non-Conversion CTA - Jumplink
- Step by Step

---

## Experimentation Framework Expertise

### Experiment Components
| Component | Purpose |
|-----------|---------|
| Hypothesis | If/then/because statement |
| Metrics | Primary and secondary KPIs |
| Pages | Target scope |
| Duration | Timeline |
| Success criteria | Scaling threshold |
| Rollback plan | Reversion strategy |

### Metrics Tracked
- Bounce Rate
- Scroll Depth
- Time on Page
- GSC Indexing
- Ranking Movement

---

## Quality Standards

### Pattern Approval Checklist
- [ ] Definition complete
- [ ] Template tested on test site
- [ ] SOP documented
- [ ] At least one live variant
- [ ] Reusable by other sites

### Experiment Launch Checklist
- [ ] Baseline established
- [ ] Hypothesis documented
- [ ] Success criteria defined
- [ ] Tech team aligned
- [ ] Monitoring in place

---

## Industry Expertise

### Verticals
| Vertical | Depth |
|----------|-------|
| iGaming - Casino | Expert |
| iGaming - Betting | Advanced |
| Digital Publishing | Advanced |

### Markets
| Market | Familiarity |
|--------|-------------|
| US | Expert |
| Australia | Advanced |
| Canada | Advanced |
| Germany | Intermediate |

---

## Communication Skills

### Documentation Styles
- Pattern specifications (technical)
- Sprint updates (operational)
- Experiment briefs (strategic)
- Learnings documents (educational)

### Coordination Patterns
- Observer-first approach
- Sprint-based cadence
- Cross-functional orchestration
- Autonomous team enablement

---

## Acquired Skills (Session-Based)

*Skills learned through agent interactions will be appended below:*

<!-- SKILL_LOG_START -->

### 2026-01-19 - Persona Creation Session
- **ClickUp Strategic Observation**: Analyze 1,000+ watched tasks for system understanding
- **Observer Pattern Recognition**: Identify leadership through watching vs commenting
- **Sprint Framework Extraction**: Derive 5-week cycle from task descriptions
- **Pattern Specification Analysis**: Extract reusable pattern template from task details
- **Cross-Functional Mapping**: Identify collaboration patterns from task creators

### 2026-01-22 - PostHog Analytics Automation Session
- **PostHog API Mastery**: Execute HogQL queries for comprehensive analytics extraction
- **NavBoost Metrics Interpretation**: Analyze pogo rate, dwell time, scroll depth, CTA CTR, good abandonment
- **Automated Report Generation**: Design Python scripts with SMTP email delivery for recurring reports
- **Cron Scheduling**: Configure 30-minute interval automation for real-time analytics monitoring
- **Product Metric Framework**: Map web vitals (LCP, CLS, INP) to rating thresholds (Good/Needs Improvement/Poor)
- **New Domain Onboarding**: Rapid PostHog setup for hudsonreporter.com (Project ID: 295222)
- **Enhanced Report Structure**: Design v2.0 report with conversions, browser/OS breakdown, session metrics, bounce rate

### 2026-01-22 - NavBoost Tracker v1.1 Implementation (BT-2026-010)
- **Session End Capture Debugging**: Diagnose async vs sendBeacon capture failures (1.6% → 80%+ target)
- **sendBeacon Implementation**: Reliable page unload event tracking with multiple fallback methods
- **CTA Tracking Architecture**: Text validation, type classification, visibility-to-click tracking
- **HogQL Query Mastery**: Complex conditional counting (countIf), CTR calculations (nullIf), engagement scoring
- **Performance Metrics Collection**: TTFB, FCP, LCP via Navigation Timing API and PerformanceObserver
- **Returning User Detection**: localStorage-based visitor identification with visit_count tracking
- **Root Cause Analysis**: Systematic debugging comparing PostHog built-in events vs custom events
- **Engagement Score Formula Design**: Weighted composite (Dwell 35%, Pogo 25%, Scroll 15%, CTA 15%, Good Abandonment 10%)
- **NavBoost KPI Framework Verification**: 27-metric mapping to code implementation
- **WordPress Theme Integration**: wp_enqueue_script patterns for tracking script deployment
- **Comprehensive Documentation**: Release notes, QA checklists, deployment instructions, metric verification matrix

### 2026-01-26 - NavBoost v1.1.2 Mobile Fix & DataForSEO Integration
- **Mobile Session Capture Fix**: Added visibilitychange, pagehide handlers and 30-second heartbeats for mobile session tracking
- **DataForSEO SERP Metrics Integration**: Designed DataForSEO as PRIMARY source for metrics 12-14 (CTR, Impressions, Position)
- **GSC vs DataForSEO Decision**: Recommended DataForSEO over GSC to avoid site verification requirement
- **CTR Estimation Curves**: Integrated Advanced Web Ranking industry-standard CTR curves by position
- **Unified Metrics Collection**: Designed `navboost_metrics.py` combining PostHog behavioral + DataForSEO SERP data
- **SERP Return Rate Clarification**: Identified SERP Return Rate is behavioral (PostHog), NOT available in GSC/DataForSEO

### 2026-01-26 - NavBoost v1.1.3 CTA Click Tracking Fix
- **Root Cause Analysis**: Diagnosed 0 clicks on 1,053 visible CTAs - identified silent catch blocks and failing selector matching
- **Silent Error Detection**: Discovered `catch (err) {}` blocks swallowing all click handler errors
- **Selector Matching Fix**: Replaced complex joined selector string with individual selector testing via `elementMatchesCTA()` function
- **Navigation Selector Removal**: Identified `.category a`, `.tag-links a`, `.post-categories a` were tracking navigation not CTAs
- **DOM Walker Pattern**: Implemented `findClosestCTA()` with iteration limit to walk up DOM tree robustly
- **Multi-Domain Deployment**: Created v1.1.3 trackers for hudsonreporter.com, culture.org, pokertube.com
- **Affiliate Vertical Adaptation**: pokertube.com tracker includes toplist tracking, higher CTR targets (8% vs 3%), higher dwell targets (90s vs 60s)

<!-- SKILL_LOG_END -->
