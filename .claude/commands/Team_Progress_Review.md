# /Team_Progress_Review - Weekly BI Engineering Progress Report

Generate a weekly progress report for the SMT covering all active BI projects and agents.

## Arguments

$ARGUMENTS

---

## Instructions

When `/Team_Progress_Review` is invoked, generate a weekly progress report by:

### Step 1: Gather Data Automatically

For each project below, pull git commits from the last 7 days:

```bash
# Get commit counts and messages for each project
for dir in AS-Virtual_Team_System_v2 pitaya BI-Dragon BI-CARLOS BI-Starfruit Papaya BI-Bedrock_Agent; do
  echo "=== $dir ==="
  cd /home/andre/$dir 2>/dev/null
  git log --since="7 days ago" --oneline --all --no-merges 2>/dev/null | wc -l
  git log --since="7 days ago" --format="- %s" --all --no-merges 2>/dev/null | sort -u
  cd /home/andre
done

# PostHog (subfolder in main repo)
cd /home/andre
git log --since="7 days ago" --format="- %s" --all --no-merges -- "projects/posthog-integration/" 2>/dev/null | sort -u
```

### Step 2: Check ClickUp for Haris's BigQuery AI Layer

```bash
# Fetch task 86aeqebdc comments for latest updates
curl -s -H "Authorization: $(python3 -c "import json; print(json.load(open('/home/andre/.claude/clickup_config.json')).get('CLICKUP_API_KEY',''))")" \
  "https://api.clickup.com/api/v2/task/86aeqebdc/comment"
```

### Step 3: Check for any additional ClickUp tasks mentioned in arguments

If the user provides ClickUp task IDs or URLs, fetch those too.

### Step 4: Generate the Report

Produce TWO outputs:

#### Output A: Slack Message (concise, for posting in Slack)

Format:

```
**BI Engineering — Progress Update | [DATE]**

---

1. **[Project Name]** — [One-line scope]. [One-line achievement summary].
2. ...
```

Keep each project to 1-2 lines maximum. No technical jargon. Focus on business impact.

#### Output B: Detailed Markdown Report (save as attachment)

Save to: `~/reports/BI_Engineering_Progress_Update_[DATE].md`

Format for each project:

```markdown
# BI Engineering — Progress Update | [DATE]

## Summary
[2-3 sentence overview of the week]

## Project Overview

| # | Project | What It Is | Key Achievement | Link |
|---|---------|-----------|-----------------|------|
| 1 | ... | ... | ... | ... |

## Detailed Project Breakdown

### 1. [Project Name]
- [repo or clickup link]
- **What it is:** [Keywords — wow factor descriptors]
- **Scope:** [What it does in plain English]
- **Achievements:** [What was accomplished this period]
```

---

## Project Registry

These are the active BI projects to report on every week:

| # | Project | Type | Repo / Task | Owner |
|---|---------|------|-------------|-------|
| 1 | Virtual ATeam System | AI Development Engine | https://github.com/ParadiseMediaOrg/AS-Virtual_Team_System_v2 | Andre |
| 2 | Pitaya | Slack BI Advisor | https://github.com/ParadiseMediaOrg/pitaya | Andre |
| 3 | Dragon | Workflow Automation | https://github.com/ParadiseMediaOrg/BI-Dragon | Andre |
| 4 | PostHog NavBoost | Behavioural Analytics | ~/projects/posthog-integration/ | Andre |
| 5 | BigQuery AI Layer | Data Infrastructure | https://app.clickup.com/t/86aeqebdc | Haris |
| 6 | Bedrock Agent | Content Factory | https://github.com/ParadiseMediaOrg/BI-Bedrock_Agent | Andre |
| 7 | Papaya | Executive Reporting | https://github.com/ParadiseMediaOrg/Papaya | Andre |
| 8 | Carlos | Multi-Agent Chatbot | https://github.com/ParadiseMediaOrg/BI-CARLOS | Andre / Haris |
| 9 | Starfruit | Bot Orchestration | https://github.com/ParadiseMediaOrg/BI-Starfruit | Andre |

---

## Tone & Style Rules

- Write for Senior Management — no code, no commit hashes, no version numbers unless meaningful
- Focus on business impact: what does this enable, save, or improve?
- Use **What it is** keywords as wow-factor descriptors (e.g. "self-learning knowledge system", "zero-touch processing")
- Keep Slack message to ~15 lines total
- Keep detailed report under 3 pages
- If a project had 0 commits, still list it with current status (e.g. "Phase 1 complete, awaiting Phase 2")
- Always mention team members by name where relevant (Haris, Claudio, Tisha, etc.)

---

## Adding New Projects

To add a new project to the weekly review, add a row to the Project Registry table above with:
- Project name
- Type (what category)
- Repo URL or ClickUp task link
- Owner

The report will automatically pick it up on the next run.

---

## Example Slack Output

```
**BI Engineering — Progress Update | Feb 6, 2026**

---

1. **Virtual ATeam System** — AI engine behind all projects below. Now v3.4.0 with self-learning knowledge base. Claudio & Tisha installing — first team rollout.
2. **Pitaya** — Slack BI advisor. Shipped v2.0 with feedback learning and automated testing. Live and serving the team.
3. **Dragon** — Affiliate link automation. Hit v3.0 with 10 quality auditors and 92% API efficiency gain. Running alongside manual team before handover.
4. **PostHog NavBoost** — Behavioural tracking on 31 domains with CTA detection and PDF reporting.
5. **BigQuery AI Layer** (Haris) — 10 of 11 AI-ready data tables delivered for the chatbot.
6. **Bedrock Agent** — Content factory. World Cup 2026 site live. Framework scales to any new vertical with one command.
7. **Papaya** — Automated monthly domain reports. Phase 1 complete, awaiting Phase 2.
8. **Carlos** — Multi-agent chatbot for analytics. Production-ready.
9. **Starfruit** — Bot orchestration hub. Architecture complete, awaiting deployment.
```

---

## Example Detailed Report

See template at: `~/reports/BI_Engineering_Progress_Update_2026-02-06.md`

This file serves as the reference format for all future reports.
