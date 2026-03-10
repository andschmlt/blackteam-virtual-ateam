# R-ANCHOR-02: Menu-Priority Anchor Distribution Rules

**Priority:** P1 High
**Created:** 2026-02-26
**Applies To:** Anchor text distribution across all sites with navigation hierarchy

---

## Rule

Anchor text distribution MUST reflect the site's navigation hierarchy. Top-level navigation sports get anchor priority over dropdown/"More" menu sports.

---

## Navigation Hierarchy (australiafootball.com)

### Top-Level Nav (Priority Tier 1)
- A-League
- Matildas
- W-League
- Socceroos
- World Cup

### Dropdown / "More" Menu (Tier 2)
- AFL
- NRL
- Horse Racing
- Cricket
- Tennis
- Esports
- Other sports

---

## Distribution Rules

### Rule 1: Priority Order
Top-level nav sports MUST have anchors **before** any dropdown sport gets a second anchor.

### Rule 2: Density Cap
No sport may have more than **3x the anchor density** (anchors / articles) of any top-level nav sport.

**Example:** If A-League has 0.1 density (1 anchor / 10 articles), no sport can exceed 0.3 density.

### Rule 3: Zero-Anchor Block
Every sport with **3+ published articles** MUST have at least:
- 1 betting anchor
- 1 casino anchor

Zero-anchor sports with 3+ articles = **BLOCKED** violation.

### Rule 4: Pre-Check Before Adding
When adding new articles, check anchor distribution per sport **BEFORE** choosing which article gets the link.

### Rule 5: Inventory Update
After **ANY** anchor text changes to australiafootball.com, update:
```
~/australiafootball.com/docs/ANCHOR_TEXT_INVENTORY.md
```

---

## Validation Checklist

```markdown
## R-ANCHOR-02 Validation

- [ ] Top-level sports have anchors before dropdown sports get extras
- [ ] No sport >3x density of any top-level sport
- [ ] Every sport with 3+ articles has 1 betting + 1 casino anchor
- [ ] Distribution checked BEFORE adding new anchors
- [ ] ANCHOR_TEXT_INVENTORY.md updated after changes
```

---

## Enforcement

| System | How Enforced |
|--------|-------------|
| `/A_Virtual_Team` | Menu-Priority Anchor Distribution Gate |
| `/bedrock_agent` | Quality Gates |
| `/launch_site` | Pre-launch SEO check |
| `/news_update_agent` | Content generation |
| `/anchor_manager` | Audit + fix tool |
| W-LARS | SEO compliance validation |
| W-VERA | Content QA |

---

## Tracking

Distribution is tracked in `docs/ANCHOR_TEXT_INVENTORY.md` per site. The `/anchor_manager audit` command generates fresh reports.

---

**Version:** 1.0.0
