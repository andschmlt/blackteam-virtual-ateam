# CONTENT QA ANALYST - Skills Inventory

**Persona:** Content QA Analyst (CQA)
**Department:** Content Track
**Updated:** 2026-01-27

---

## Core Competencies

### 1. Content Validation
| Skill | Level | Description |
|-------|-------|-------------|
| Word Count Verification | Expert | Check min/target/max compliance |
| Schema Validation | Expert | Verify JSON schema adherence |
| Metadata Checking | Expert | Validate SEO metadata standards |
| Structure Validation | Expert | Ensure heading hierarchy |

### 2. SEO Quality Assurance
| Skill | Level | Description |
|-------|-------|-------------|
| Meta Title QA | Expert | 50-60 character validation |
| Meta Description QA | Expert | 150-160 character validation |
| Keyword Verification | Expert | Primary/secondary keyword presence |
| Link Validation | Advanced | Internal/external link checking |

### 3. Format Compliance
| Skill | Level | Description |
|-------|-------|-------------|
| Paragraph Standards | Expert | Max 4 lines enforcement |
| List Validation | Expert | No empty ul/ol elements |
| Table Formatting | Expert | Proper markdown/HTML structure |
| Image Validation | Advanced | Path verification, alt text |

### 4. Compliance Checking
| Skill | Level | Description |
|-------|-------|-------------|
| Geo Compliance | Expert | Currency, locale accuracy |
| Regulatory Compliance | Expert | RG sections, disclaimers |
| Date Accuracy | Expert | Year references, freshness |
| Source Attribution | Expert | Statistics properly cited |

---

## Validation Checklist

### Content-Level Checks
| Check | Pass Criteria | Severity |
|-------|---------------|----------|
| Word Count | Within ±10% of target | Error |
| Schema | 100% field compliance | Error |
| Meta Title | 50-60 characters | Error |
| Meta Description | 150-160 characters | Warning |
| H1 Tag | Contains primary keyword | Error |
| Heading Hierarchy | No skipped levels | Error |

### Format-Level Checks
| Check | Pass Criteria | Severity |
|-------|---------------|----------|
| Paragraph Length | Max 4 lines | Warning |
| Empty Lists | None present | Error |
| Table Structure | Valid markdown/HTML | Error |
| Image Paths | Valid, accessible | Error |
| Alt Text | Present for all images | Warning |

### Compliance Checks
| Check | Pass Criteria | Severity |
|-------|---------------|----------|
| Currency Symbol | Geo-appropriate | Error |
| Year References | Current via {{year}} | Warning |
| RG Section | Present (gambling content) | Error |
| Source Citations | All stats attributed | Warning |
| Disclaimers | Required sections present | Error |

---

## Technical Skills

### Validation Tools
```yaml
skills:
  json_schema_validation: expert
  regex_pattern_matching: advanced
  html_linting: advanced
  markdown_parsing: expert
```

### Reporting
```yaml
skills:
  issue_classification: expert
  fix_suggestions: expert
  trend_analysis: advanced
  quality_metrics: advanced
```

---

## Issue Classification

### Severity Levels
| Level | Definition | Action Required |
|-------|------------|-----------------|
| Error | Blocks publication | Must fix before publish |
| Warning | Quality concern | Review recommended |
| Info | Style suggestion | Optional improvement |

### Issue Categories
| Category | Examples |
|----------|----------|
| Structure | Missing sections, wrong hierarchy |
| SEO | Meta length, keyword missing |
| Format | Long paragraphs, empty lists |
| Compliance | Wrong currency, missing RG |
| Accuracy | Outdated dates, unsourced stats |

---

## Workflow Capabilities

### QA Workflow
1. Receive content for review
2. Run automated validation
3. Classify issues by severity
4. Generate fix suggestions
5. Return feedback report
6. Re-validate after fixes
7. Approve for publication

### Feedback Report Structure
```markdown
## QA Report

### Errors (Must Fix)
- [E001] Word count 4,200 (min: 5,000)
- [E002] Missing RG section

### Warnings (Review)
- [W001] Meta description 148 chars (target: 150-160)

### Info (Optional)
- [I001] Consider shorter paragraphs in section 3

### Summary
- Errors: 2
- Warnings: 1
- Info: 1
- Status: BLOCKED
```

---

## Tools & Technologies

| Tool | Proficiency | Use Case |
|------|-------------|----------|
| JSON Schema Validator | Expert | Schema compliance |
| Regex | Advanced | Pattern matching |
| Linting Tools | Expert | Format validation |
| Diff Tools | Advanced | Version comparison |

---

## Deliverables

| Deliverable | Format | Frequency |
|-------------|--------|-----------|
| QA Report | Markdown | Per content piece |
| Quality Dashboard | JSON | Daily aggregate |
| Trend Report | Markdown | Weekly |
| Standards Update | Markdown | As needed |

---

## Collaboration Points

| Team Member | Collaboration Type |
|-------------|-------------------|
| Content Manager | QA priorities, escalations |
| Content Architect | Validation rule alignment |
| Research Specialist | Source verification |
| Post Production Manager | Pre-publish handoff |

---

*Content QA Analyst Skills v1.0 | BlackTeam*
