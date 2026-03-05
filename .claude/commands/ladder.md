# /ladder - Update All Standings & Ladder Pages

Update all standings/ladder pages across australiafootball.com with the latest data from official sources. Fetches current round/matchweek, calculates Monte Carlo probabilities, updates .astro files, builds, deploys, and commits.

## Arguments

```
/ladder                    # Update ALL leagues (full refresh)
/ladder epl                # EPL only
/ladder aleague            # A-League Men only
/ladder wleague            # A-League Women only
/ladder nbl                # NBL only
/ladder --dry-run          # Preview changes without writing
/ladder --check            # Only check freshness, don't update
```

Arguments: $ARGUMENTS

---

## League Configuration

| League | File | Data Source | Season | Off-Season |
|--------|------|-------------|--------|------------|
| **EPL** | `src/pages/epl/standings.astro` | Football-Data.org API v4 (`X-Auth-Token`) | Aug–May | Jun–Jul |
| **A-League Men** | `src/pages/a-league/ladder.astro` | Wikipedia MediaWiki API | Oct–May | Jun–Sep |
| **A-League Women** | `src/pages/w-league/ladder.astro` | Wikipedia MediaWiki API | Nov–Apr | May–Oct |
| **NBL** | `src/pages/nbl/ladder.astro` | Wikipedia MediaWiki API | Sep–Feb | Mar–Aug |
| **AFL** | `src/pages/afl/ladder.astro` | Wikipedia MediaWiki API | Mar–Sep | Oct–Feb |
| **NRL** | `src/pages/nrl/ladder.astro` | Wikipedia MediaWiki API | Mar–Oct | Nov–Feb |
| **Cricket/BBL** | `src/pages/cricket/ladder.astro` | Wikipedia MediaWiki API | Dec–Feb | Mar–Nov |

---

## Execution Steps

### Step 0: Determine Scope

Parse `$ARGUMENTS` to decide which leagues to update:
- No args or `all` → update ALL leagues
- Specific league name → update only that league
- `--dry-run` → preview only, no file writes
- `--check` → freshness audit only (compare site vs source)

### Step 1: Check Off-Season Status (R-CONTENT-05e)

Before fetching data, determine if each league is currently in-season or off-season. **Off-season leagues should NOT be updated** — they should show "Final [YEAR] Standings".

Check method:
1. Read the current .astro file and extract the max `p` (played) value
2. For Wikipedia-sourced leagues, fetch the current season page and check if all teams have P:0 (season not started)
3. If off-season: verify the page title says "Final" — if not, fix it per R-CONTENT-05e

### Step 2: Fetch Current Data

#### EPL (Football-Data.org API)

```bash
source ~/.keys/.env
curl -s -H "X-Auth-Token: $FOOTBALL_DATA_API_KEY" \
  "https://api.football-data.org/v4/competitions/PL/standings"
```

**Rate limit:** 10 requests/minute. If 403, wait 60 seconds and retry once.

**Slug mapping** (API shortName → site slug):
- `Arsenal` → `arsenal`, `Man City` → `manchester-city`, `Man United` → `manchester-united`
- `Brighton Hove` → `brighton`, `Nottingham` → `nottingham-forest`, `Wolverhampton` → `wolves`

**Display name mapping** (for table display):
- `Man United` → `Man Utd`, `Nottingham` → `Nottm Forest`, `Wolverhampton` → `Wolves`

#### A-League Men & Women (Wikipedia)

Use the existing script:
```bash
python3 scripts/update_aleague_standings.py --all
```

Or manually via Wikipedia MediaWiki API:
```
https://en.wikipedia.org/w/api.php?action=parse&page=PAGE_NAME&prop=sections&format=json
```

**CRITICAL:** Always fetch `prop=sections` first to find the correct section number. Section numbers shift when Wikipedia editors restructure pages.

**Wikipedia page names** (use em-dash `–` not hyphen `-`):
- A-League Men: `2025–26_A-League_Men`
- A-League Women: `2025–26_A-League_Women`
- NBL: `2025–26_NBL_season`
- AFL: `2026_AFL_season`
- NRL: `2026_NRL_season`

#### NBL (Wikipedia)

Same pattern as A-League but:
- No draws (W/L only), uses `winPct` field instead of `d` field
- Points = `w * 2` (2 points per win)
- Form uses W/L only (no D)
- If regular season is complete (all teams same P), use seeding-based championship probability instead of Monte Carlo

### Step 3: Calculate Probabilities

#### In-Season: Monte Carlo Simulation (2000+ iterations)

```python
import random
random.seed(42)

for _ in range(N_SIM):
    for team in standings:
        remaining = total_games - played
        ppg = points / played
        strength = ppg / max_ppg
        sim_pts = current_pts
        for _ in range(remaining):
            r = random.random()
            if r < strength * 0.55: sim_pts += 3  # win
            elif r < strength * 0.55 + 0.28: sim_pts += 1  # draw
        final_pts[team] = sim_pts
    # Sort and count placements
```

#### Season Complete: Seeding-Based Estimates

When regular season is over (all teams played same number of games), positions are locked. Use championship probability based on seeding:
- %Win = championship probability (top seed ~30%, 2nd ~22%, 3rd ~18%, etc.)
- %Top3 = 100% for top 3, 0% for rest (locked)
- %Finals = 100% for qualified teams, 0% for eliminated

### Step 4: Update .astro Files

**CRITICAL:** Only update the `const teams = [...]` array in the frontmatter. NEVER change:
- Layout, HTML structure, or CSS
- Component imports
- Table headers or column structure
- Legend or methodology notes (unless factually wrong)

Update the season notes paragraph with current leader info.
Update the "Last Updated" date in the `<p><strong>Note:</strong>` section.
Update the `description` meta tag if the matchweek/round number is mentioned.

### Step 5: Build & Verify

```bash
npm run build 2>&1 | tail -5
# Verify 0 errors, check page count hasn't changed
```

### Step 6: Deploy

```bash
npx vercel --prod
```

### Step 7: Commit & Push

```bash
git add src/pages/*/ladder.astro src/pages/*/standings.astro
git commit -m "Update standings: [leagues updated] — [round/matchweek info]

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
git push origin main
```

---

## Freshness Check Mode (`--check`)

When `--check` is passed, do NOT update any files. Instead:

1. For each in-season league, fetch current data from source
2. Compare current round/matchweek with what's on the site
3. Report staleness:

```
Standings Freshness Report — 27 Feb 2026
=========================================
EPL           MW28 (site) vs MW28 (API)    ✓ CURRENT
A-League Men  R19 (site) vs R19 (Wiki)     ✓ CURRENT
A-League Wom  R17 (site) vs R17 (Wiki)     ✓ CURRENT
NBL           R33 (site) vs R33 (Wiki)     ✓ CURRENT (season complete)
AFL           Final 2025                    ✓ OFF-SEASON (correct label)
NRL           Final 2025                    ✓ OFF-SEASON (correct label)
Cricket/BBL   Final                         ✓ OFF-SEASON (correct label)
=========================================
Overall: 7/7 current ✓
```

Flag any league that is >1 round/matchweek behind as **STALE**.

---

## Data Source Fallback Order

If primary source fails:

1. **Football-Data.org API** → retry once after 60s → use Wikipedia EPL page
2. **Wikipedia** → try alternate section numbers → check if page was renamed
3. **All sources fail** → report failure, do NOT update file with stale/partial data

**NEVER** write partial data or estimated standings to a file. Either the data is complete and verified, or the update is skipped.

---

## Rules Enforced

- **R-CONTENT-05a**: No false freshness claims — "Last Updated" date must be accurate
- **R-CONTENT-05d**: Every data page must show "Last Updated: DD Mon YYYY"
- **R-CONTENT-05e**: Off-season pages must say "Final [YEAR] Standings"
- **R-DATA-07**: All numerical comparisons verified (leader points, goal difference, position)

---

## Red Team Challenge (R-WORKFLOW-02 — MANDATORY, NEVER SKIP)

**DELIVERY BLOCKED until Red Team passes. This phase is NON-NEGOTIABLE.**

Before committing or deploying ladder/standings updates:

1. **R-REX reviews** all data accuracy and page integrity
2. **Execute applicable Red Gates:**
   - RG-1: Validation Integrity — did data checks verify actual source values? (100%)
   - RG-2: Adversarial Edge Cases — empty tables, missing teams, encoding (95%)
   - RG-3: Regression & Drift — do updates break existing pages or navigation? (100%)
   - RG-7: Root Cause & Pattern — R-DATA-07 numerical comparison verified (100%)

3. **Challenge Report:** `CERTIFIED` to proceed, `FLAGGED` to fix (max 2 cycles)

**If RedTeam is skipped:** The session is NON-COMPLIANT with R-WORKFLOW-02.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Football-Data.org 403 | Rate limited (10 req/min). Wait 60s. Check `$FOOTBALL_DATA_API_KEY` in `~/.keys/.env` |
| Wikipedia returns empty | Section number changed. Fetch `prop=sections` and find "Standings" or "Ladder" |
| Wikipedia page not found | Season year may have changed. Check page title format: `YYYY–YY_League_Name` |
| NBL shows wrong data | Verify page is `2025–26_NBL_season` not `2025–26_NBL_(Australia)_season` |
| Monte Carlo gives flat values | Check `random.seed(42)` is set. Ensure strength calculation uses PPG not raw points |
| Build fails after update | Check for syntax errors in teams array (missing comma, unescaped quotes in team names) |
