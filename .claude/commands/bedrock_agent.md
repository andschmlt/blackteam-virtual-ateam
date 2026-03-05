# /bedrock_agent - Content Vertical Generator

Create and manage content verticals using The_Agent framework.

---

## Main Menu (MANDATORY FIRST STEP)

**Before doing anything else**, present this menu using `AskUserQuestion`:

```
BEDROCK AGENT — WHAT WOULD YOU LIKE TO DO?
════════════════════════════════════════════════════════════════

  1. New domain
     → Create a brand-new content vertical from scratch
     → Uses full /bedrock_agent wizard, rules & Astro deployment

  2. New article in an existing domain
     → Add new content pages to an existing bedrock_agent project
     → Uses full /bedrock_agent rules & quality gates

  3. Update an existing domain
     → Refresh or add articles to a site you already own
     → Matches the site's existing style, CSS & layout 100%
     → Routes to /bedrock_agent_update

  4. Update an existing article
     → Rewrite or refresh a single article on an existing site
     → Precision style matching for one page
     → Routes to /bedrock_agent_update

════════════════════════════════════════════════════════════════
```

### Menu Routing

- **Option 1 (New domain)** → Continue with `/bedrock_agent new` workflow below (full wizard + 5 Ralph Loops + Astro + Vercel)
- **Option 2 (New article)** → Continue with `/bedrock_agent generate [project]` workflow below (full quality gates apply)
- **Option 3 (Update existing domain)** → Hand off to `/bedrock_agent_update` command (style-locked mode, 3 Fidelity Gates)
- **Option 4 (Update existing article)** → Hand off to `/bedrock_agent_update` command (style-locked mode, 3 Fidelity Gates)

**Key distinction:**
- Options 1-2 = **"New" mode** — Full bedrock_agent rules, templates, scaffolding, deployment pipeline
- Options 3-4 = **"Existing" mode** — The live site IS the style guide. No scaffold rules. Match everything 100%.

When user selects **Option 3 or 4**, invoke `/bedrock_agent_update` with the user's arguments and stop processing this command.

---

## Phase 0: Context Loading (CONDITIONAL — Load What You Need)

**After user selects Option 1 or 2, load the full execution spec:**

```
Read ~/.claude/commands/bedrock_agent_exec.md
```

**Then load context based on what the task requires:**

### Always load (Options 1 and 2):
- `~/pitaya/knowledge/feedback_corrections.md` — Data accuracy rules, R-DATA-07

### Load when building new site structure (Option 1):
- `~/.claude/standards/ASTRO_TECHNICAL_SEO_RULES.md` — R-SEO-03
- `~/.claude/standards/IMAGE_OPTIMIZATION_RULES.md` — R-IMG-01

### Load when generating content (Options 1 and 2):
- Read the 3 most recent BlackTeam learnings matching the project vertical:
  ```bash
  ls -t ~/AS-Virtual_Team_System_v2/blackteam/skills/learnings/*.md | head -3
  ```

### Load only when deploying to Cloud Run:
- `~/.claude/standards/INPUT_VALIDATION_RULES.md` — R-SEC-02
- `~/.claude/standards/CORS_SECURITY_RULES.md` — R-SEC-03
- `~/.claude/standards/CRYPTOGRAPHY_RULES.md` — R-SEC-04
- `~/.claude/standards/SECRETS_ROTATION_SCHEDULE.md` — R-SEC-06

### Load only when adding money page links:
- `~/.claude/standards/ANCHOR_TEXT_RULES.md` — R-ANCHOR-01
- `~/.claude/standards/ANCHOR_DISTRIBUTION_RULES.md` — R-ANCHOR-02

**Do NOT read standards files that are irrelevant to the current task.**

---

## Phase 0.4: Security Gate (MANDATORY)

**W-GARD enforces R-SEC-01 through R-SEC-06 + R-DEPLOY-01 + R-DEBUG-01 on all bedrock_agent output.**

Before generating any code or deploying:

1. **R-SEC-01:** No hardcoded API keys — load from `~/.keys/.env` or Secret Manager
2. **R-SEC-02:** All external input (RSS, API, scrape) validated
3. **R-SEC-03:** CORS on Cloud Run services — no wildcard origins
4. **R-SEC-04:** TLS 1.2+, `hmac.compare_digest()` for tokens
5. **R-DEBUG-01:** Local dry-run BEFORE any Cloud Run deploy
6. **R-DEPLOY-01:** Post-deployment security audit after every deploy

---

## Phase 0.5: Log Session Start (MANDATORY)

```bash
python3 /home/andre/.claude/scripts/log_to_db.py --persona B-BOB --action execute --summary "Started /bedrock_agent session" --username $(whoami) --command bedrock_agent
```

## Phase 0.6: Save Palm Bridge Session (AUTOMATIC)

When working with a specific project, save the session for `/content_palm` Mode B integration:

```bash
python3 /home/andre/.claude/scripts/bedrock_palm_bridge.py save --project {PROJECT_NAME}
```

This enables `/content_palm` to automatically load bedrock variables (title->topic, country->geo, vertical->content_type) without manual re-entry. Session saved to `~/.bedrock_session.json`.

---

**Arguments:** $ARGUMENTS
