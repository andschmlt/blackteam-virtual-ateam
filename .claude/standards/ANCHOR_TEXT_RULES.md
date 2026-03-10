# R-ANCHOR-01: Keyword-Rich Anchor Text Rules

**Priority:** P1 High
**Created:** 2026-02-26
**Applies To:** All internal links to money pages across all sites

---

## Rule

ALL internal links to money pages MUST use keyword-rich anchor text matching AU search terms.

**NEVER** use generic action-verb anchors.

---

## Banned Anchor Patterns

These anchor text patterns are PROHIBITED:

- "compare the best"
- "find the best"
- "explore the top"
- "check out these"
- "click here"
- "learn more"
- "see our picks"
- "view our list"

These waste link equity and provide zero keyword signal to search engines.

---

## Approved Betting Keywords

| Keyword | Monthly Volume (AU) |
|---------|---------------------|
| best betting sites in Australia | 5,400 |
| AFL betting | 3,600 |
| NRL betting tips | 1,300 |
| Melbourne Cup odds | 8,100 |
| sports betting sites | 1,600 |
| AFL betting sites | — |
| NRL betting sites | — |
| A-League betting odds | — |
| horse racing betting | — |
| cricket betting tips | — |
| Big Bash betting | — |

---

## Approved Casino Keywords

| Keyword | Monthly Volume (AU) |
|---------|---------------------|
| online pokies in Australia | 110,000 |
| best online casinos in Australia | 14,800 |
| top Australian online casinos | 40,500 |
| best pokies online | 33,100 |
| real money casino sites | 6,600 |
| Australian casino sites | — |

---

## Distribution Rules

1. **No single anchor text used >2x across the entire site**
2. **Sport-specific anchors preferred** — use "AFL betting" in AFL articles, not generic "best betting sites"
3. **Anchor text must contain at least one high-volume AU search term**
4. **Vary anchor text across articles** — different article = different anchor

---

## Examples

### CORRECT
```markdown
With the A-League season heating up, fans looking at [A-League betting odds](/betting/best-betting-sites-australia/) will find plenty of value this round.
```

### INCORRECT
```markdown
Want to place a bet? [Compare the best betting sites](/betting/best-betting-sites-australia/) for the latest odds.
```

---

## Enforcement

| System | How Enforced |
|--------|-------------|
| `/A_Virtual_Team` | Anchor Text Gate |
| `/bedrock_agent` | Quality Gates |
| `/launch_site` | Pre-launch SEO check |
| `/news_update_agent` | Content generation |
| `/content_palm` | Content generation |
| `/anchor_manager` | Audit + fix tool |

---

**Version:** 1.0.0
