# Palm Content Formatting Rules (R-PALM-FMT-01)

Standards for post-processing Palm v3 API output into publication-ready markdown.
Applied automatically during Phase 10a of `/content_palm`.

---

## Rule 1: Spec Sheets Must Be Tables

**Trigger:** Any section matching `Spec Sheet:` followed by bullet points.

**Before (raw Palm output):**
```markdown
Spec Sheet:

- **Bonus:** 300% up to $1,500
- **Wagering:** 30x
- **Payout Speed:** 1-3 Days
- **License:** Curacao
```

**After (formatted):**
```markdown
| Feature | Details |
|---------|---------|
| Bonus | 300% up to $1,500 |
| Wagering | 30x |
| Payout Speed | 1-3 Days |
| License | Curacao |
```

**Rules:**
- Strip `Spec Sheet:` header text — the table replaces it
- Each `- **Key:** Value` becomes a table row
- Remove bold markers from keys in the table
- Two columns: `Feature` | `Details`
- Place table directly under the brand heading (### level)

---

## Rule 2: Ratings Must Be Tables with Score Bars

**Trigger:** Any section matching `Rating:` followed by bullet points with `/5` scores.

**Before (raw Palm output):**
```markdown
Rating:

- Market Depth: 4.8/5
- Odds Value: 4.6/5
- Mobile App: 4.5/5
```

**After (formatted):**
```markdown
| Category | Score |
|----------|-------|
| Market Depth | 4.8/5 |
| Odds Value | 4.6/5 |
| Mobile App | 4.5/5 |
```

**Rules:**
- Strip `Rating:` header text — the table replaces it
- Each `- Category: X/5` becomes a row
- Two columns: `Category` | `Score`
- Scores retain the `/5` format

---

## Rule 3: Pros/Cons Must Be Side-by-Side Tables

**Trigger:** Sequential `Pros:` and `Cons:` bullet lists.

**Before (raw Palm output):**
```markdown
Pros:

- Massive sports variety
- High betting limits
- Clean mobile interface

Cons:

- No live streaming
- Strict wagering on bonus
```

**After (formatted):**
```markdown
| Pros | Cons |
|------|------|
| Massive sports variety | No live streaming |
| High betting limits | Strict wagering on bonus |
| Clean mobile interface | |
```

**Rules:**
- Combine Pros and Cons into a single two-column table
- Strip `Pros:` and `Cons:` headers
- If unequal count, leave shorter column cells empty
- Place immediately after the spec sheet table

---

## Rule 4: Comparison Sections Must Be Proper Tables

**Trigger:** Sections with repeated `Brand: Key Value | Key Value` patterns.

**Before (raw Palm output):**
```markdown
## Comparison: Top 5 Picks

- MyStake: Bonus 300% up to $1,500 | Wagering 30x | Speed 1-3 Days | Feature Global Market Depth
- Donbet: Bonus 150% up to $750 | Wagering 20x | Speed 0-48 Hours | Feature High Betting Limits
```

**After (formatted):**
```markdown
## Comparison: Top 5 Picks

| Brand | Bonus | Wagering | Payout Speed | Key Feature |
|-------|-------|----------|--------------|-------------|
| MyStake | 300% up to $1,500 | 30x | 1-3 Days | Global Market Depth |
| Donbet | 150% up to $750 | 20x | 0-48 Hours | High Betting Limits |
```

**Rules:**
- Parse pipe-delimited values from each bullet
- Extract column headers from the `Key Value` pattern
- Create a proper markdown table with headers

---

## Rule 5: Document Alignment and Padding

**Applies to:** All Palm content rendered in Astro.

### Markdown Structure
- All headings must have one blank line before and after
- No double blank lines anywhere in the document
- Tables must have one blank line before and after
- Blockquotes must have one blank line before and after
- Lists must have one blank line before the first item

### Astro Prose Container
- The `.prose` container must set `max-width: 75ch` for readable line lengths
- Horizontal padding: `var(--spacing-lg)` minimum on mobile
- Tables must be full-width within the prose container (`width: 100%`)
- Tables must have consistent cell padding (`0.75rem 1rem`)
- Table headers must have a distinct background color

---

## Rule 6: First Look / Summary Table → TechOps TopList Embed (R-TOPLIST-01)

**Trigger:** The overview table at the top of roundup reviews on money pages.

**IMPORTANT — R-TOPLIST-01:** For ALL money pages (betting, casino, or any affiliate roundup), the static "First Look" markdown table is **REPLACED** by the TechOps TopList embed widget during post-processing.

**Implementation:**
```html
<div data-toplist="{TOPLIST_ID}"></div>
<script src="https://cdn-6a4c.australiafootball.com/embed.js"></script>
```

**Rules:**
- The `data-toplist` ID MUST be provided by TechOps — ask the user if not supplied
- Each money page gets its OWN unique TopList ID (never reuse across pages)
- The Palm-generated static First Look table is DISCARDED — the widget replaces it entirely
- The CDN domain `cdn-6a4c.australiafootball.com` must be allowed in CSP headers
- Applies to `roundup-review` and `roundup-review-sp` content types only

**Fallback rules** (if TopList ID is not yet available, keep the static table temporarily):
- Columns: Brand | Award | Bonus | Rating
- Rating column should show the numeric score (e.g., `5.0`)
- Table must be clean — no garbled bonus text (strip duplicates like "free spins free spins")
- Sort by rating descending

---

## Rule 7: Brand Section Structure Order

Each brand in a roundup-review must follow this exact structure:

```
### N. Brand Name - Award Title

| Feature | Details |          ← Spec Sheet table
|---------|---------|
| ...     | ...     |

| Pros | Cons |                ← Pros/Cons table
|------|------|
| ...  | ...  |

[Editorial paragraphs]         ← Review text

**Testing [Brand]:**           ← Testing section (bold header, not heading)

[Testing paragraphs]

| Category | Score |           ← Rating table
|----------|-------|
| ...      | ...   |

> [Summary blockquote]        ← One-line verdict

[CTA Link]                    ← Affiliate link
```

---

## Rule 8: Clean Up Palm Artifacts

Remove these common Palm output artifacts:
- `SEO Meta Title:` lines in the body
- `Meta Description:` lines in the body
- `H1:` lines in the body
- Duplicate phrases like "free spins free spins"
- Trailing whitespace on any line
- More than one consecutive blank line

---

## Application

These rules are applied in `/content_palm` Phase 10a (Post-Processing) after Palm output is received and before saving to `~/palm_output/`.

The post-processing can be applied:
1. **Automatically** — via regex transforms in the save step
2. **Manually** — by the operator reviewing and reformatting
3. **Retroactively** — to existing articles using the same transform logic

---

*Standard: R-PALM-FMT-01 | Owner: B-NINA (Content Strategy) | Validated: W-VERA (Content QA)*
