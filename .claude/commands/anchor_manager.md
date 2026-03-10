# /anchor_manager - Anchor Text Inventory & Distribution Manager

Manage anchor text distribution across sites, validate R-ANCHOR-01 (keyword-rich anchors) and R-ANCHOR-02 (menu-priority distribution), and maintain the anchor text inventory.

## Arguments

Arguments: $ARGUMENTS

---

## Standards Enforced

- **R-ANCHOR-01:** Keyword-rich anchor text matching AU search terms
- **R-ANCHOR-02:** Menu-priority anchor distribution aligned with site navigation

---

## Modes

### 1. `audit` — Full Anchor Audit

Scan all content files for internal links to money pages and produce a distribution report.

**Steps:**

1. **Identify money pages** for the target site:
   ```bash
   # Example for australiafootball.com
   grep -r "betting\|casino\|pokies" ~/australiafootball.com/src/content/ --include="*.md" --include="*.mdx" -l
   ```

2. **Extract all internal links to money pages:**
   ```bash
   grep -rn "\[.*\](/betting/\|/casino/" ~/australiafootball.com/src/content/ --include="*.md" --include="*.mdx"
   ```

3. **Map anchor text to source articles:**
   - File path (which sport/section)
   - Anchor text used
   - Target URL
   - Sport category

4. **Calculate distribution metrics:**
   - Anchors per sport (count + density = anchors / articles in sport)
   - Top-level nav sports vs. dropdown sports split
   - Unique anchor text count
   - Duplicate anchor detection (>2x same anchor = violation)

5. **Validate against R-ANCHOR-01:**
   - [ ] All anchors use keyword-rich text from approved KW list
   - [ ] No generic action-verb anchors ("compare the best", "find the best")
   - [ ] Each anchor contains at least one high-volume AU search term
   - [ ] No single anchor used >2x across entire site

6. **Validate against R-ANCHOR-02:**
   - [ ] Top-level nav sports (A-League, Matildas, W-League, Socceroos, World Cup) have anchor priority
   - [ ] No sport >3x anchor density of any top-level sport
   - [ ] Every sport with 3+ articles has at least 1 betting + 1 casino anchor
   - [ ] Top-level sports have anchors before dropdown sports get extras

7. **Output report:**

```markdown
## Anchor Text Audit Report

**Site:** [domain]
**Date:** [today]
**Total Money Page Links:** [count]

### Distribution by Sport

| Sport | Nav Level | Articles | Betting Anchors | Casino Anchors | Density |
|-------|-----------|----------|-----------------|----------------|---------|
| A-League | Top | X | Y | Z | A/X |
| ... | ... | ... | ... | ... | ... |

### R-ANCHOR-01 Violations
- [ ] Generic anchors found: [list]
- [ ] Duplicate anchors (>2x): [list]

### R-ANCHOR-02 Violations
- [ ] Top-level sports without anchors: [list]
- [ ] Density imbalance (>3x): [details]
- [ ] Zero-anchor sports with 3+ articles: [list]

### Recommended Actions
1. [specific action items with file paths]
```

---

### 2. `add` — Add Anchors to Content

Add money page links to articles that currently have none, following distribution rules.

**Steps:**

1. Run `audit` mode first to identify gaps
2. Prioritize top-level nav sports with missing anchors
3. Select keyword-rich anchor text from approved list:

**Betting Keywords (by sport):**
| Sport | Anchor Options |
|-------|---------------|
| AFL | "AFL betting sites", "AFL betting tips" |
| NRL | "NRL betting tips", "NRL betting sites" |
| A-League | "A-League betting odds", "best betting sites in Australia" |
| Horse Racing | "Melbourne Cup odds", "horse racing betting" |
| Cricket | "cricket betting tips", "Big Bash betting" |
| General | "best betting sites in Australia", "sports betting sites" |

**Casino Keywords (by sport context):**
| Context | Anchor Options |
|---------|---------------|
| General | "online pokies in Australia", "best online casinos in Australia" |
| Gaming | "top Australian online casinos", "real money casino sites" |
| Entertainment | "best pokies online", "Australian casino sites" |

4. For each article receiving an anchor:
   - Find a sentence where betting/casino is contextually implied
   - Weave link naturally into existing text
   - Use keyword-rich anchor text (NOT generic action verbs)
   - One subtle link per article maximum

5. After adding, update `docs/ANCHOR_TEXT_INVENTORY.md`

---

### 3. `inventory` — View/Update Inventory

Read or update the anchor text inventory file.

```bash
cat ~/australiafootball.com/docs/ANCHOR_TEXT_INVENTORY.md
```

If the file doesn't exist, create it from audit results.

---

### 4. `fix` — Fix Specific Violations

Fix a specific R-ANCHOR-01 or R-ANCHOR-02 violation identified in an audit.

**Input:** Violation type + affected files
**Output:** Fixed files + updated inventory

---

## Approved Keyword Lists

### Betting (High Volume AU)
| Keyword | Monthly Volume |
|---------|---------------|
| best betting sites in Australia | 5,400 |
| AFL betting | 3,600 |
| NRL betting tips | 1,300 |
| Melbourne Cup odds | 8,100 |
| sports betting sites | 1,600 |

### Casino (High Volume AU)
| Keyword | Monthly Volume |
|---------|---------------|
| online pokies in Australia | 110,000 |
| best online casinos in Australia | 14,800 |
| top Australian online casinos | 40,500 |
| best pokies online | 33,100 |
| real money casino sites | 6,600 |

---

## Team Assignments

| Persona | Role |
|---------|------|
| B-RANK | Runs audit, selects anchor text |
| W-LARS | Validates anchor compliance |
| W-LUNA | Validates SEO impact |
| W-VERA | Content quality of woven links |

---

## Quality Gates

- [ ] R-ANCHOR-01: All anchors keyword-rich (no generic action verbs)
- [ ] R-ANCHOR-02: Distribution follows nav hierarchy
- [ ] R-CONTENT-03: Links are subtle, woven into existing sentences
- [ ] Inventory file updated after every change
- [ ] No single anchor >2x across site

---

**Version:** 1.0.0
**Created:** 2026-03-02
