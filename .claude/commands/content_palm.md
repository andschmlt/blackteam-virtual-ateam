# /content_palm - Palm v3 Content Generation Integration

Generate publication-ready SEO articles via Palm v3 API (`https://palmv3-hqoyr.kinsta.app`).
This command is a **READ-ONLY API consumer** — it NEVER modifies, deploys, or commits to the palm_v3 repo.

**Arguments:** $ARGUMENTS

---

## Phase 0: Context Loading (CONDITIONAL)

**Always load:**
- `~/pitaya/knowledge/feedback_corrections.md` — Data accuracy rules, R-DATA-07

**Load when generating money pages (betting, casino):**
- `~/.claude/standards/GOOGLE_API_LEAK_DIAGNOSIS.md` — R-SEO-04 (Firefly/YMYL parameters)
- Key API Leak parameters for money pages: `numOfGamblingPages` (ID 30), `rhubarb` (ID 56), `contentEffort` (ID 45), `racterScores` (ID 52), `productReviewPUhqPage` (ID 178), `affiliateLinkDensity`

**Load when article includes images:**
- `~/.claude/standards/IMAGE_OPTIMIZATION_RULES.md` — R-IMG-01

**Load relevant learnings (match to content type):**
```bash
ls -t ~/AS-Virtual_Team_System_v2/blackteam/skills/learnings/*palm* ~/AS-Virtual_Team_System_v2/blackteam/skills/learnings/*content* 2>/dev/null | head -3
```

**Do NOT load all standards upfront. Read each file only when relevant to the content being generated.**

---

## Phase 0.4: Security Gate (MANDATORY)

**W-GARD enforces R-SEC-01 through R-SEC-06 on all content_palm output.**

1. **R-SEC-01:** PALM_API_TOKEN loaded from `~/.keys/.env` — never hardcoded
2. **R-SEC-02:** Validate Palm API response content before writing to disk (`~/.claude/standards/INPUT_VALIDATION_RULES.md`)
3. **R-SEC-04:** API calls use TLS 1.2+ (default for HTTPS), token comparison via `hmac.compare_digest()`
4. **R-DEPLOY-01:** If deploying generated content to Cloud Run or Vercel — run post-deploy audit

**Palm-specific:** Strip any API keys, tokens, or credentials that may appear in Palm output before committing.

---

## Phase 0.5: Session Logging (MANDATORY)

```bash
python3 /home/andre/.claude/scripts/log_to_db.py --persona B-BOB --action execute --summary "Started /content_palm session" --username $(whoami) --command content_palm
```

---

## Phase 1: Environment Check

Verify that `PALM_API_TOKEN` is set in `~/.keys/.env`.

```bash
grep -q "^PALM_API_TOKEN=" ~/.keys/.env && echo "OK" || echo "MISSING"
```

**If MISSING:** Stop and tell the user:
```
PALM_API_TOKEN is not configured in ~/.keys/.env

To set it up:
1. Log into Palm v3 at https://palmv3-hqoyr.kinsta.app
2. Go to Settings > API Tokens
3. Create a new token
4. Add to ~/.keys/.env:
   PALM_API_TOKEN=palm_<your_token_here>
```

**If OK:** Load the token for use in API calls:
```bash
export PALM_API_TOKEN=$(grep "^PALM_API_TOKEN=" ~/.keys/.env | cut -d'=' -f2)
```

---

## Phase 2: Mode Selection

Present the main menu using `AskUserQuestion`:

```
CONTENT PALM — SELECT MODE
════════════════════════════════════════════════════════════════

  A. Fresh Generation
     → Enter all variables manually from scratch
     → Full control over every parameter

  B. From Bedrock
     → Pre-fill variables from an active /bedrock_agent session
     → Maps: title->topic, country->geo, vertical+subcategory->content_type
     → You can override any pre-filled value

  C. Quick Generate
     → Minimal input: just topic, content_type, and geo
     → Uses sensible defaults for everything else
     → Fastest path to content

════════════════════════════════════════════════════════════════
```

### Mode Routing

- **Mode A (Fresh)** → Proceed through Phases 3-6 collecting all variables
- **Mode B (From Bedrock)** → Load bedrock session variables, pre-fill, then proceed through Phases 3-6 with pre-filled defaults
- **Mode C (Quick Generate)** → Ask only for topic, content_type, and geo, skip Phases 5-6, jump to Phase 7

### Mode B: Bedrock Variable Mapping (AUTOMATED via Bridge Script)

When the user selects Mode B, use the **bedrock_palm_bridge.py** script to automate variable loading:

**Step 1: Check for active session or list projects**

```bash
# Check for saved session first
python3 ~/.claude/scripts/bedrock_palm_bridge.py load 2>/dev/null

# If no session, list available projects
python3 ~/.claude/scripts/bedrock_palm_bridge.py list
```

**Step 2: If no session exists, ask user to select a project**

Present the list of bedrock projects from the `list` output using `AskUserQuestion`. Then load:

```bash
python3 ~/.claude/scripts/bedrock_palm_bridge.py load --project {SELECTED_PROJECT}
```

**Step 3: If session exists, show pre-filled variables**

The bridge script returns JSON with both `bedrock_variables` and `palm_variables`:

```json
{
  "palm_variables": {
    "topic": "Premier League 2025-26",
    "geo": "England",
    "language": "en",
    "content_type_suggestion": "roundup-review",
    "style_variant": "formal",
    "research_flags": {"web_search": true, "fact_check": true}
  }
}
```

**Step 4: Pre-fill Phase 3-6 variables from palm_variables**

| Palm Variable | Pre-filled From | Phase |
|--------------|-----------------|-------|
| `topic` | bedrock `title` | 4 |
| `geo` | bedrock `country` | 4 |
| `language` | derived from country (Italy→it, Germany→de) | 4 |
| `content_type` | bedrock `vertical` + `subcategory` mapping | 3 |
| `style_variant` | bedrock `content_style` (journalism→formal) | 6 |
| `research_flags` | defaults: web_search=true, fact_check=true | 6 |

**Step 5: Present pre-filled summary and let user override**

```
FROM BEDROCK — PRE-FILLED VARIABLES
════════════════════════════════════════════════════════════════
  Project:      {active_project}

  topic:        {palm_variables.topic}
  geo:          {palm_variables.geo}
  language:     {palm_variables.language}
  content_type: {palm_variables.content_type_suggestion} (suggested)
  style:        {palm_variables.style_variant}

  Override any value? (Y/N)
════════════════════════════════════════════════════════════════
```

If user confirms, skip to Phase 7 (Summary Confirmation) with these values.
If user wants to override, proceed through Phases 3-6 with these as defaults.

**Step 6: Save session for future use**

After loading a project in Mode B, the bridge automatically saves the session:
```bash
python3 ~/.claude/scripts/bedrock_palm_bridge.py save --project {PROJECT_NAME}
```
This means next time Mode B is selected, the same project loads automatically.

**Variable mapping reference:**

| Bedrock Variable | Palm Variable | Mapping |
|-----------------|---------------|---------|
| `title` | `topic` | Direct mapping — the article subject |
| `country` | `geo` | Direct mapping — target geography |
| `vertical` | `content_type` | suggestion based on vertical+subcategory |
| `subcategory` | `content_type` | refines suggestion (Football→roundup-review) |
| `content_style` | `style_variant` | Maps: journalism→formal, statistical→data-driven |
| `country` | `language` | Derived: Italy→it, Germany→de, France→fr, default→en |

**Bridge script location:** `~/.claude/scripts/bedrock_palm_bridge.py`
**Session file:** `~/.bedrock_session.json`

---

## Phase 3: Content Type Selection

Present content type menu using `AskUserQuestion`:

```
SELECT CONTENT TYPE
════════════════════════════════════════════════════════════════

  API v2 Types (Token Auth — faster, programmatic)
  ─────────────────────────────────────────────────
  1. roundup-review
     → Multi-brand comparison article (e.g., "Best Online Casinos in Canada")
     → REQUIRES offer_lineup (list of brands/products to review)

  2. roundup-review-sp
     → Spanish-language roundup review
     → REQUIRES offer_lineup
     → Auto-sets language to "es"

  3. single-review
     → In-depth review of a single brand/product/service
     → No lineup required

  API v1 Types (OAuth — full-featured, more options)
  ─────────────────────────────────────────────────
  4. guest-post
     → SEO guest post with backlinks
     → Supports links parameter [{url, anchor}]

  5. analysis
     → Data-driven industry analysis article
     → Supports research_flags for depth control

  6. evergreen-post
     → Timeless informational content
     → Long shelf life, minimal date references

  7. seasonal-events
     → Time-sensitive event coverage
     → Tied to specific dates/seasons

════════════════════════════════════════════════════════════════
```

**Store the selected content_type and determine the API version:**

| Content Type | API Version | Auth Method |
|-------------|-------------|-------------|
| `roundup-review` | v2 | `Bearer palm_<token>` |
| `roundup-review-sp` | v2 | `Bearer palm_<token>` |
| `single-review` | v2 | `Bearer palm_<token>` |
| `guest-post` | v1 | OAuth (session) |
| `analysis` | v1 | OAuth (session) |
| `evergreen-post` | v1 | OAuth (session) |
| `seasonal-events` | v1 | OAuth (session) |

---

## Phase 4: Core Variables

Collect required variables using `AskUserQuestion`:

### 4a. Topic / Keyword

```
Enter the primary topic or keyword for this article:

Examples:
  • "Best Online Casinos in Canada"
  • "Top Sports Betting Sites for Euro 2026"
  • "How to Choose a VPN for Streaming"
  • "Premier League 2025-26 Season Preview"

Topic:
```

### 4b. Geographic Target (geo)

```
Select the target geography:

┌──────────────┬─────────────────────────────────────┐
│ Country      │ Common use cases                    │
├──────────────┼─────────────────────────────────────┤
│ USA          │ US market content (default)         │
│ Canada       │ Canadian iGaming, sports betting    │
│ UK           │ UK gambling, Premier League         │
│ Australia    │ Australian sports, betting          │
│ Germany      │ DACH market content                 │
│ Brazil       │ Brazilian market, Portuguese        │
│ India        │ Indian market, cricket              │
│ Other        │ Specify country                     │
└──────────────┴─────────────────────────────────────┘

Default: USA
```

### 4c. Language

```
Select content language:

┌──────────────┬────────────┐
│ Language     │ ISO Code   │
├──────────────┼────────────┤
│ English      │ en         │
│ Spanish      │ es         │
│ Portuguese   │ pt         │
│ German       │ de         │
│ French       │ fr         │
│ Italian      │ it         │
│ Other        │ Specify    │
└──────────────┴────────────┘

Default: en
Note: roundup-review-sp auto-sets to "es"
```

### 4d. Environment

```
Which Palm environment should we use?

┌─────────────┬──────────────────────────────────────────────────┐
│ Environment │ URL                                              │
├─────────────┼──────────────────────────────────────────────────┤
│ Production  │ https://palmv3-hqoyr.kinsta.app                 │
│ Staging     │ https://palm-staging-gs4rl.kinsta.app            │
└─────────────┴──────────────────────────────────────────────────┘

Default: Production
Use Staging for testing new content types or debugging.
```

---

## Phase 5: Content-Type-Specific Variables

Present fields based on the content_type selected in Phase 3.

### If roundup-review or roundup-review-sp

**5a. Offer Lineup (REQUIRED)**

```
Enter the offer lineup — the brands/products to include in the roundup.

You can provide:
  A. Manual list — Enter brand names separated by commas
     Example: "Bet365, DraftKings, FanDuel, BetMGM, Caesars"

  B. ClickUp URL — Extract lineup from a ClickUp task
     Example: "https://app.clickup.com/t/86aeaykdf"

  C. Auto-match — Let Palm match a lineup based on topic + geo
     (Requires ClickUp integration configured on Palm server)

Which method?
```

If A (Manual): Collect comma-separated brand names and store as `offer_lineup: ["Bet365", "DraftKings", ...]`

If B (ClickUp URL): Store the URL as `clickup_url` — Palm will extract keyword, geo, language, and lineup from the task. This **replaces** the keyword and geo from Phase 4.

If C (Auto-match): Set `auto_match_lineup: true` and leave `offer_lineup` empty.

**5b. Auto-Match Lineup (only if not using ClickUp URL)**

```
Enable auto-match lineup from ClickUp master list?

  Yes → Palm will find the best matching lineup for your topic + geo
  No  → Use only the lineup you provided above

Default: Yes
```

### If guest-post

**5c. Backlinks**

```
Enter backlinks to embed in the article.
Format: URL | Anchor Text (one per line)

Example:
  https://example.com/casinos | best online casinos
  https://example.com/bonus | welcome bonus guide

Enter links (or press Enter to skip):
```

Store as `links: [{"url": "...", "anchor": "..."}]`

### If analysis, evergreen-post, seasonal-events

**5d. ClickUp URL (Optional)**

```
Provide a ClickUp task URL for additional context (optional):

This extracts topic, geo, and any linked data from the ClickUp task.

ClickUp URL (or press Enter to skip):
```

---

## Phase 6: Advanced Options

Present advanced options using `AskUserQuestion`. The user can skip all of these.

```
ADVANCED OPTIONS (all optional — press Enter to use defaults)
════════════════════════════════════════════════════════════════

Would you like to configure any advanced options?

  1. Research Flags
     → Control research depth (web_search, competitor_analysis, etc.)

  2. Style Variant
     → Choose writing style (formal, conversational, data-driven)

  3. Author Persona
     → Select a Palm author persona for attribution

  4. Screenshots
     → Auto-generate brand screenshots for the article

  5. Skip All
     → Use defaults for everything

════════════════════════════════════════════════════════════════
```

### If Research Flags selected:

```
Configure research flags:

┌──────────────────────────┬─────────────────────────────────────┬─────────┐
│ Flag                     │ Description                         │ Default │
├──────────────────────────┼─────────────────────────────────────┼─────────┤
│ web_search               │ Enable web search for current data  │ true    │
│ competitor_analysis      │ Analyze competing articles          │ false   │
│ deep_research            │ Extended research pass              │ false   │
│ fact_check               │ Verify claims against sources       │ true    │
└──────────────────────────┴─────────────────────────────────────┴─────────┘

Enter flags to toggle (comma-separated), or Enter for defaults:
```

Store as `research_flags: {"web_search": true, "competitor_analysis": false, ...}`

### If Style Variant selected:

```
Select style variant:

┌──────────────┬──────────────────────────────────────────────────┐
│ Variant      │ Description                                      │
├──────────────┼──────────────────────────────────────────────────┤
│ formal       │ Professional, authoritative tone                  │
│ conversational │ Friendly, approachable tone                    │
│ data-driven  │ Numbers-heavy, analytical tone                   │
│ editorial    │ Opinion-forward, expert commentary               │
│ random       │ Palm selects a variant                           │
└──────────────┴──────────────────────────────────────────────────┘

Default: (Palm decides based on content_type)
```

Store as `style_variant: "formal"` (or whichever selected)

### If Author Persona selected:

```
Select author persona:

  A. Persona ID — Enter a Palm persona set ID
     Example: "2026-01-22_canada_sports_betting"

  B. Persona Index — Select persona 0-3 from the default set

  C. ATeam Writer — Select a Virtual ATeam content writer persona
     Apply CW-R9 (GEO routing) + CW-R10 (content type routing):
     ┌─────────┬──────────────────────────────────────────────────┐
     │ GEO     │ Primary Writers                                   │
     ├─────────┼──────────────────────────────────────────────────┤
     │ AU      │ B-FINN, B-JACK, B-ROSA, B-RENO                   │
     │ DACH    │ B-HANA, B-YUKI, B-NINW, B-KAIA                   │
     │ FR      │ B-CLEO, B-OLGA, B-HUGL, B-ABEL, B-ASHA           │
     │ IT      │ B-MARC, B-ZARA, B-DAVI, B-RENO                   │
     │ ES      │ B-RAJA, B-LEON, B-ABEL                            │
     │ UK      │ B-HANA, B-CLEO, B-MILA, B-FINN, B-ROSA           │
     │ US      │ B-SURI, B-JACK, B-MILA, B-OLGA, B-LEON           │
     └─────────┴──────────────────────────────────────────────────┘
     Full roster: rules/CONTENT_WRITER_RULES.md (25 writers)

  D. Skip — Let Palm use the default author

Persona choice:
```

Store as `author_persona_id` and/or `author_persona_index`.
If ATeam Writer selected, load persona variables ([Grammatical_Error_%_Allowance] + [Sentiment]) and pass as style guidance to Palm API.

### If Screenshots selected:

```
Configure screenshot generation:

  Generate screenshots from lineup? (Y/N)
  Default: No

  If Yes:
    Screenshot quality (1-100): 80
    Bottom logo URL (optional): https://example.com/logo.png

  Custom screenshot URLs (optional):
    Enter URLs to screenshot, one per line.
    These will be included in the article.
```

Store as:
- `generate_screenshots: true/false`
- `screenshot_urls: [...]`
- `screenshot_quality: 80`
- `bottom_logo_url: "..."`

---

## Phase 7: Summary Confirmation

Display all collected variables and ask for confirmation:

```
CONTENT PALM — GENERATION SUMMARY
════════════════════════════════════════════════════════════════

  Mode:           Fresh / From Bedrock / Quick Generate
  Content Type:   roundup-review
  API Version:    v2 (Token Auth)
  Environment:    Production

  CORE
  ────
  Topic:          Best Online Casinos in Canada
  Geo:            Canada
  Language:        en

  CONTENT-SPECIFIC
  ────────────────
  Offer Lineup:   Bet365, DraftKings, FanDuel, BetMGM, Caesars
  Auto-Match:     Yes
  ClickUp URL:    (none)
  Links:          (none)

  ADVANCED
  ────────
  Research Flags: web_search=true, fact_check=true
  Style Variant:  (default)
  Author Persona: (default)
  Screenshots:    No

  OUTPUT
  ──────
  Save to:        ~/palm_output/2026-02-22_best-online-casinos-in-canada.md

════════════════════════════════════════════════════════════════

  [Generate]  [Edit]  [Cancel]
```

- **Generate** → Proceed to Phase 8
- **Edit** → Ask which field to change, loop back to the relevant phase
- **Cancel** → Abort and log session end

---

## Phase 8: API Execution

Route the request to the correct API version and send.

### API v2 (roundup-review, roundup-review-sp, single-review)

**Endpoint:** `POST {base_url}/api/v2/generate`

**Headers:**
```
Authorization: Bearer {PALM_API_TOKEN}
Content-Type: application/json
```

**Request body:**
```json
{
  "content_type": "roundup-review",
  "keyword": "Best Online Casinos in Canada",
  "geo": "Canada",
  "language": "en",
  "offer_lineup": ["Bet365", "DraftKings", "FanDuel", "BetMGM", "Caesars"],
  "auto_match_lineup": true,
  "clickup_url": null
}
```

**Execute with curl:**
```bash
PALM_API_TOKEN=$(grep "^PALM_API_TOKEN=" ~/.keys/.env | cut -d'=' -f2)
BASE_URL="https://palmv3-hqoyr.kinsta.app"  # or staging URL

curl -s -X POST "${BASE_URL}/api/v2/generate" \
  -H "Authorization: Bearer ${PALM_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "content_type": "'"${CONTENT_TYPE}"'",
    "keyword": "'"${TOPIC}"'",
    "geo": "'"${GEO}"'",
    "language": "'"${LANGUAGE}"'",
    "offer_lineup": '"${OFFER_LINEUP_JSON}"',
    "auto_match_lineup": '"${AUTO_MATCH}"'
  }'
```

**Expected response:**
```json
{
  "success": true,
  "job_id": "uuid-here",
  "job_number": 123,
  "status_url": "/api/v2/jobs/uuid-here",
  "message": "Generation started for 'Best Online Casinos in Canada' (roundup-review)",
  "lineup_info": {
    "source": "provided",
    "lineup_id": null,
    "lineup_name": null,
    "similarity": null
  }
}
```

### API v1 (guest-post, analysis, evergreen-post, seasonal-events)

**Endpoint:** `POST {base_url}/api/articles/generate`

**Note:** API v1 requires OAuth session authentication. The user must be logged into Palm v3 via browser. For CLI usage, the PALM_API_TOKEN cannot be used with v1 endpoints. Instead, construct the request and provide the user a ready-to-use curl command or open the Palm web UI with pre-filled parameters.

**If v1 content type is selected**, inform the user:

```
API v1 content types (guest-post, analysis, evergreen-post, seasonal-events)
require OAuth authentication which is not available via CLI token.

Options:
  1. Open Palm v3 in browser with pre-filled parameters
     → URL: {base_url}/generate?content_type={type}&topic={topic}&geo={geo}

  2. Use the generated curl command with a session cookie
     → You'll need to copy your session cookie from the browser

  3. Switch to a v2 content type (roundup-review, single-review)
     → These work with your API token
```

**Request body (v1):**
```json
{
  "content_type": "guest-post",
  "topic": "The Rise of Mobile Sports Betting",
  "geo": "USA",
  "language": "en",
  "links": [
    {"url": "https://example.com/betting", "anchor": "sports betting guide"}
  ],
  "research_flags": {"web_search": true, "fact_check": true},
  "style_variant": "formal",
  "author_persona_id": null,
  "author_persona_index": null,
  "generate_screenshots": false,
  "screenshot_urls": null,
  "screenshot_quality": 80,
  "bottom_logo_url": null
}
```

### Error Handling

| HTTP Status | Meaning | Action |
|------------|---------|--------|
| 200 | Success — job created | Proceed to Phase 9 |
| 400 | Bad request — missing/invalid params | Show error details, offer to fix |
| 401 | Unauthorized — invalid/expired token | Re-check PALM_API_TOKEN |
| 429 | Rate limited | Show retry-after, wait and retry |
| 500 | Server error | Show error, suggest trying staging |

---

## Phase 9: Job Polling

After a successful generate request, poll the job status endpoint.

**Poll endpoint (v2):** `GET {base_url}/api/v2/jobs/{job_id}`
**Poll endpoint (v1):** `GET {base_url}/api/articles/{job_id}`

**Polling logic:**

```bash
JOB_ID="<from Phase 8 response>"
TIMEOUT=300    # 5 minutes
INTERVAL=10    # Poll every 10 seconds
ELAPSED=0

while [ $ELAPSED -lt $TIMEOUT ]; do
  RESPONSE=$(curl -s "${BASE_URL}/api/v2/jobs/${JOB_ID}" \
    -H "Authorization: Bearer ${PALM_API_TOKEN}")

  STATUS=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")
  PROGRESS=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['progress'])")
  STAGE=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('stage',''))")

  # Display progress
  echo "[$ELAPSED s] Status: $STATUS | Progress: $PROGRESS% | Stage: $STAGE"

  if [ "$STATUS" = "complete" ]; then
    echo "Generation complete!"
    break
  fi

  if [ "$STATUS" = "failed" ]; then
    ERROR=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('error_message','Unknown error'))")
    echo "Generation FAILED: $ERROR"
    break
  fi

  sleep $INTERVAL
  ELAPSED=$((ELAPSED + INTERVAL))
done

if [ $ELAPSED -ge $TIMEOUT ]; then
  echo "TIMEOUT: Job did not complete within 5 minutes."
  echo "You can check status later: /content_palm status $JOB_ID"
fi
```

**Display progress to user:**
```
PALM GENERATION IN PROGRESS
════════════════════════════════════════════════════════════════
Job ID:  abc123-def456
Type:    roundup-review
Topic:   Best Online Casinos in Canada

[  0s] Status: pending   | Progress: 0%   | Stage: queued
[ 10s] Status: running   | Progress: 15%  | Stage: research
[ 20s] Status: running   | Progress: 35%  | Stage: outlining
[ 30s] Status: running   | Progress: 55%  | Stage: writing
[ 40s] Status: running   | Progress: 75%  | Stage: review
[ 50s] Status: running   | Progress: 90%  | Stage: formatting
[ 60s] Status: complete  | Progress: 100% | Stage: done

Generation complete!
════════════════════════════════════════════════════════════════
```

---

## Phase 10a: Post-Processing (R-PALM-FMT-01)

**MANDATORY** — Apply formatting rules from `~/.claude/standards/PALM_CONTENT_RULES.md` before saving.

### Transforms to Apply

1. **Spec Sheets → Tables**: Convert `Spec Sheet:` + bullet lists into `| Feature | Details |` tables
2. **Ratings → Tables**: Convert `Rating:` + bullet lists into `| Category | Score |` tables
3. **Pros/Cons → Side-by-Side Tables**: Merge sequential `Pros:` and `Cons:` bullets into `| Pros | Cons |` tables
4. **Comparison → Proper Tables**: Convert pipe-delimited bullet lists into proper markdown tables with headers
5. **Clean Artifacts**: Strip `SEO Meta Title:`, `Meta Description:`, `H1:` lines from body; fix duplicates like "free spins free spins"
6. **Whitespace**: Ensure one blank line before/after tables, blockquotes, and headings; no double blank lines
7. **First Look → TechOps TopList Embed (R-TOPLIST-01)**: For ALL money pages (betting, casino, or any new affiliate roundup), **replace** the static "First Look" markdown table with the TechOps TopList embed widget. The user MUST provide the `data-toplist` ID from TechOps. Format:
   ```html
   <div data-toplist="{TOPLIST_ID}"></div>
   <script src="https://cdn-6a4c.australiafootball.com/embed.js"></script>
   ```
   - **MANDATORY**: Ask user for the TopList ID before generating content if not provided
   - The CDN domain `cdn-6a4c.australiafootball.com` must be allowed in CSP (`script-src`, `style-src`, `connect-src`)
   - The static First Look table from Palm output is DISCARDED — the widget replaces it entirely
   - This applies to `roundup-review` and `roundup-review-sp` content types only

### Brand Section Order (roundup-review)

Each brand must follow this structure:
```
### N. Brand Name - Award Title
[Spec Sheet Table]
[Pros/Cons Table]
[Editorial paragraphs]
**Testing [Brand]:**
[Testing paragraphs]
[Rating Table]
> [Summary blockquote]
[CTA Link]
```

### Runners-Up → Table

Convert bullet-list runners-up into `| Brand | Strength |` table.

### Methodology → Table

Convert methodology criteria into `| Criteria | What We Checked |` table.

---

## R-CONTENT-04: Timestamp Stagger Rule (MANDATORY)

When generating content for any site:
- Use `date: "YYYY-MM-DDTHH:MM"` in frontmatter (NOT date-only `YYYY-MM-DD`)
- Minimum **2-hour gap** between articles published on the same day
- Each article committed and pushed **separately** — never batch-push multiple articles
- Check existing articles for today before assigning a time to avoid collisions

---

## Phase 10c: API Leak Compliance Gate (R-SEO-04 — MANDATORY for Money Pages)

**CRITICAL:** Palm generates the content that Google's Firefly system scrutinizes most heavily. Every money page MUST pass these checks before saving. Reference: SEO Strategy KB (`seo-strategy-hphbw.sevalla.app/api-leak`), Atom #3076 (Safe Publishing Pattern).

### Pre-Save Checks

| # | Check | API Leak Parameter | Pass Criteria | HARD? |
|---|-------|--------------------|---------------|-------|
| 1 | Gambling Ratio Impact | `numOfGamblingPages` (ID 30) | After adding this page, gambling pages remain < 5% of total indexed pages | **HARD** |
| 2 | Content Effort | `contentEffort` (ID 45) | Article has > 1,500 words, ≥ 5 subheadings, comparison data, unique analysis paragraphs | SOFT |
| 3 | AI Content Enrichment | `racterScores` (ID 52) | Human must add ≥ 3 unique data points Palm wouldn't generate: local regulations, payment methods tested, personal testing notes, date-stamped comparisons | **HARD** |
| 4 | Review Quality (UHQ) | `productReviewPUhqPage` (ID 178) | For roundup-review: testing evidence, screenshots, original comparison criteria, methodology section | SOFT |
| 5 | Affiliate Link Density | `affiliateLinkDensity` | Max 1 affiliate/sponsored link per 300 words. TopList embed = 1 link cluster. Count total | SOFT |
| 6 | Quality Delta Readiness | `rhubarb` (ID 56) | Money page word count, image count, and section depth must be ≥ site editorial average. Flag if significantly less rich than news articles | **HARD** |
| 7 | YMYL Compliance | `YMYL Health Score` | Gambling = highest YMYL. Verify: responsible gambling notice present, author attribution set, no hyperbolic claims ("guaranteed wins", "risk-free") | **HARD** |
| 8 | Topical Coherence | `siteFocusScore` | Content must be sports-betting or casino-gambling within the site's declared vertical. No off-topic tangents | SOFT |

### How to Apply

```markdown
## Phase 10c: API Leak Compliance — {content_type}

| # | Check | Status | Notes |
|---|-------|--------|-------|
| 1 | Gambling ratio after this page | [X%] — [PASS/FAIL] | [current count + 1] / [total indexed] |
| 2 | Content effort | [PASS/FLAG] | [word count], [heading count], [unique analysis?] |
| 3 | AI enrichment (≥ 3 unique data points) | [PASS/FAIL] | [list the unique additions] |
| 4 | Review quality (UHQ signals) | [PASS/FLAG] | [testing evidence? screenshots? methodology?] |
| 5 | Affiliate link density | [PASS/FLAG] | [X links / Y words = 1 per Z words] |
| 6 | Quality delta vs site avg | [PASS/FAIL] | [money page depth vs editorial avg] |
| 7 | YMYL compliance | [PASS/FAIL] | [responsible gambling? no hyperbolic claims?] |
| 8 | Topical coherence | [PASS/FLAG] | [within vertical?] |

**Gate Result:** [PASS / BLOCKED — fix items marked FAIL]
```

**HARD GATE:** Any check marked **HARD** that fails = content is BLOCKED until fixed. SOFT failures are flagged for manual review but don't block.

**Atom #3076 Reminder:** "Casino pages must get engagement" — if this is a money page for a site with PostHog data, check the existing money page engagement. If existing money pages have < 30% scroll depth, enriching them is higher priority than adding new ones.

---

## Phase 10: Output Handling

When the job completes successfully, extract the content and save as Astro-compatible markdown.

### Extract content from response

The completed job response includes:
- `content` — Full markdown article body
- `h1` — Article H1 heading
- `meta_title` — SEO title tag
- `meta_description` — SEO meta description
- `word_count` — Article word count
- `job_id` — Palm job UUID

### Generate output file

**Filename:** `~/palm_output/{date}_{slug}.md`
- `date` = today's date (YYYY-MM-DD)
- `slug` = slugified topic (lowercase, hyphens, no special chars)

**File format — Astro Content Collection compatible:**

```markdown
---
title: "{h1 from Palm response}"
section: "{user-specified or auto-mapped from content_type}"
type: "{content_type}"
date: "{today YYYY-MM-DD}"
author: "Paradise Media"
description: "{meta_description from Palm, 150-160 chars}"
keywords: ["{extracted from topic and Palm content}"]
metaTitle: "{meta_title from Palm}"
metaDescription: "{meta_description from Palm}"
palmJobId: "{job_id from Palm}"
contentType: "{content_type}"
geo: "{geo}"
language: "{language}"
generatedAt: "{ISO 8601 timestamp}"
---

{Palm markdown content body}
```

### Section mapping for frontmatter

| Content Type | Default Section |
|-------------|----------------|
| `roundup-review` | `reviews` |
| `roundup-review-sp` | `reviews` |
| `single-review` | `reviews` |
| `guest-post` | `articles` |
| `analysis` | `analysis` |
| `evergreen-post` | `guides` |
| `seasonal-events` | `events` |

Ask the user if they want to override the default section.

### Keyword extraction

Extract keywords from:
1. The topic/keyword input
2. The geo target
3. Key phrases from the Palm h1 and meta_title

Store as a YAML array in frontmatter: `keywords: ["keyword1", "keyword2", "keyword3"]`

### Save the file

```bash
mkdir -p ~/palm_output
# Write the Astro-compatible markdown file
cat > ~/palm_output/${DATE}_${SLUG}.md << 'PALMEOF'
---
title: "..."
...
---

{content}
PALMEOF
```

### Display output summary

```
OUTPUT SAVED
════════════════════════════════════════════════════════════════

  File:         ~/palm_output/2026-02-22_best-online-casinos-in-canada.md
  Word Count:   2,450
  Content Type: roundup-review
  Palm Job ID:  abc123-def456-ghi789

  Frontmatter:
    title:       "Best Online Casinos in Canada 2026"
    section:     reviews
    metaTitle:   "Best Online Casinos in Canada - Expert Reviews 2026"
    keywords:    [online casinos, Canada, gambling, Bet365, DraftKings]

════════════════════════════════════════════════════════════════
```

---

## Phase 10b: Bedrock Integration

After saving the output file, offer to publish into an active bedrock project.

```
BEDROCK INTEGRATION
════════════════════════════════════════════════════════════════

Would you like to publish this article to a bedrock project?

  Y → Copy into a bedrock project's content directory
  N → Keep in ~/palm_output/ only

════════════════════════════════════════════════════════════════
```

### If Yes:

**Step 1: Select bedrock project**

List available projects from `~/AS-Virtual_Team_System_v2/projects/bedrock_agent/`:

```bash
ls -d ~/AS-Virtual_Team_System_v2/projects/bedrock_agent/*_Astro/ 2>/dev/null
```

Present as a selectable list:
```
Select target bedrock project:

  1. Australian_Sports_Hub_Astro
  2. WC_2026_Astro_V2
  3. Italian_Serie_A_Astro
  4. F1_2026_Astro
  5. Bundesliga_2025-26_Astro_V2
  6. Premier_League_2025-26_Astro
  7. Ligue_1_2025-26_Astro
  8. Other (enter path)

Project:
```

**Step 2: Specify target section**

```
Enter the target section directory:

This maps to: {project}/src/content/articles/{section}/

Common sections:
  • reviews      — Product/brand reviews
  • analysis     — Data analysis articles
  • guides       — How-to and informational content
  • news         — News articles
  • events       — Event coverage

Section:
```

**Step 3: Copy file**

```bash
PROJECT_PATH=~/AS-Virtual_Team_System_v2/projects/bedrock_agent/{selected_project}
SECTION={user_section}
SLUG={article_slug}
SOURCE=~/palm_output/${DATE}_${SLUG}.md
DEST="${PROJECT_PATH}/src/content/articles/${SECTION}/${SLUG}.md"

# Create section directory if needed
mkdir -p "${PROJECT_PATH}/src/content/articles/${SECTION}"

# Copy the file
cp "$SOURCE" "$DEST"
```

**Step 4: Validate (if Astro project)**

```bash
cd "${PROJECT_PATH}" && npx astro check 2>&1 | tail -20
```

**Step 5: Confirm**

```
BEDROCK PUBLISH COMPLETE
════════════════════════════════════════════════════════════════

  Source:  ~/palm_output/2026-02-22_best-online-casinos-in-canada.md
  Target:  {project}/src/content/articles/reviews/best-online-casinos-in-canada.md

  Astro Check: PASSED (0 errors)

  Next steps:
    1. Review the article in the project
    2. Run: cd {project} && npm run build
    3. Deploy: vercel deploy --prod

════════════════════════════════════════════════════════════════
```

---

## Phase 10.5: Red Team Challenge (R-WORKFLOW-02 — MANDATORY, NEVER SKIP)

**DELIVERY BLOCKED until Red Team passes. This phase is NON-NEGOTIABLE.**

Before publishing, deploying, or marking session complete, run RedTeam challenge:

1. **R-REX reviews** the generated content and any code changes
2. **Execute applicable Red Gates:**
   - RG-1: Validation Integrity — did Ralph Loops actually validate what they claimed? (100%)
   - RG-2: Adversarial Edge Cases — broken links, missing images, encoding issues (95%)
   - RG-3: Regression & Drift — does new content break existing pages? (100%)
   - RG-4: Systemic Bias — hidden bias in brand recommendations, content framing (95%)
   - RG-5: Security — no leaked keys, no XSS in embeds (100%)
   - RG-7: Root Cause & Pattern — no known anti-pattern repetition (100%)

3. **Challenge Report:**
   - `CERTIFIED` — Proceed to Phase 11
   - `FLAGGED` — Fix issues, re-run affected Ralph Loops (max 2 cycles)

```
RT CHALLENGE REPORT
Status: CERTIFIED / FLAGGED
Gates Passed: X/7
Findings: [list or "none"]
```

**If RedTeam is skipped:** The session is NON-COMPLIANT with R-WORKFLOW-02.

---

## Phase 11: Session Completion Logging

```bash
python3 /home/andre/.claude/scripts/log_to_db.py --persona B-BOB --action complete --summary "Completed /content_palm session: ${CONTENT_TYPE} for '${TOPIC}' (${GEO}) — Job ${JOB_ID}" --username $(whoami) --command content_palm
```

Display final summary:

```
SESSION COMPLETE
════════════════════════════════════════════════════════════════

  Command:      /content_palm
  Content Type: {content_type}
  Topic:        {topic}
  Geo:          {geo}
  Palm Job ID:  {job_id}
  Output:       ~/palm_output/{filename}.md
  Bedrock:      {published_to or "not published"}
  Status:       SUCCESS

════════════════════════════════════════════════════════════════
```

---

## Quick Reference: All Palm v3 Parameters

| Parameter | Type | Required | API | Phase |
|-----------|------|----------|-----|-------|
| `content_type` | string | YES | v1+v2 | 3 |
| `keyword` / `topic` | string | YES | v1+v2 | 4 |
| `geo` / `country` | string | NO (default: USA) | v1+v2 | 4 |
| `language` | string | NO (default: en) | v1+v2 | 4 |
| `offer_lineup` | string[] | YES for roundup types | v2 | 5 |
| `auto_match_lineup` | bool | NO (default: true) | v2 | 5 |
| `clickup_url` | string | NO | v2 | 5 |
| `links` | [{url, anchor}] | NO | v1 | 5 |
| `research_flags` | dict | NO | v1 | 6 |
| `style_variant` | string | NO | v1 | 6 |
| `author_persona_id` | string | NO | v1 | 6 |
| `author_persona_index` | int | NO | v1 | 6 |
| `generate_screenshots` | bool | NO | v1 | 6 |
| `screenshot_urls` | string[] | NO | v1 | 6 |
| `screenshot_quality` | int | NO (default: 80) | v1 | 6 |
| `bottom_logo_url` | string | NO | v1 | 6 |

---

## API Endpoints Reference

### Production: `https://palmv3-hqoyr.kinsta.app`
### Staging: `https://palm-staging-gs4rl.kinsta.app`

| Method | Endpoint | Auth | Purpose |
|--------|----------|------|---------|
| `POST` | `/api/v2/generate` | Bearer token | Start v2 generation |
| `GET` | `/api/v2/jobs/{job_id}` | Bearer token | Poll v2 job status |
| `GET` | `/api/v2/health` | None | Health check |
| `POST` | `/api/articles/generate` | OAuth session | Start v1 generation |
| `GET` | `/api/articles/{job_id}` | OAuth session | Get v1 article |

---

## Error Recovery

| Scenario | Action |
|----------|--------|
| Token invalid/expired | Re-check `~/.keys/.env`, regenerate token in Palm UI |
| Rate limited (429) | Wait for Retry-After header, or try again later |
| Job timeout (5min) | Job may still be running — check status with `curl` |
| Job failed | Check `error_message` in response, fix input params, retry |
| Network error | Check connectivity to `palmv3-hqoyr.kinsta.app` |
| v1 auth required | Use browser or session cookie approach |

---

## Inline Status Check

If `$ARGUMENTS` starts with `status`, check a job:

```
/content_palm status <job_id>
```

Execute:
```bash
PALM_API_TOKEN=$(grep "^PALM_API_TOKEN=" ~/.keys/.env | cut -d'=' -f2)
curl -s "https://palmv3-hqoyr.kinsta.app/api/v2/jobs/${JOB_ID}" \
  -H "Authorization: Bearer ${PALM_API_TOKEN}" | python3 -m json.tool
```

---

*Content Palm — Palm v3 API Integration for /bedrock_agent*
*R-SEC-01 Compliant: Token loaded from ~/.keys/.env, never hardcoded*
