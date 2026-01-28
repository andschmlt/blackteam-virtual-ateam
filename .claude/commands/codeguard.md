# /codeguard - CodeGuard Automated Quality & Feedback Workflow

Execute CodeGuard workflows for continuous code quality monitoring and human feedback integration.

## Available Workflows

| Command | Description |
|---------|-------------|
| `/codeguard guard` | Incremental scan - checks changed files since last scan |
| `/codeguard review` | **FULL codebase scan** - reviews ALL Python files, processes human feedback, creates ClickUp tasks |
| `/codeguard task-qa <url>` | **Engineering task QA** - validates ClickUp tasks against ENGINEERING_TASK_STANDARDS.md before dev |

## Persona Loading

**Load CodeGuard persona from:** `/mnt/c/Users/andre/Desktop/Virtual ATeam/Personas/CODEGUARD.md`
**Load skills from:** `/mnt/c/Users/andre/Desktop/Virtual ATeam/learnings/CODEGUARD_SKILLS.md`
**Load code standards from:** `/home/andre/claude/BI-REPO-PARADISEMEDIA/CODE_REVIEW_STANDARDS.md`
**Load task standards from:** `/home/andre/claude/BI-REPO-PARADISEMEDIA/ENGINEERING_TASK_STANDARDS.md`
**Load feedback log from:** `/home/andre/claude/BI-REPO-PARADISEMEDIA/CODEGUARD_CLICKUP_FEEDBACK_LOG.md`

## Configuration

**Main Repository (upstream):** `https://github.com/ParadiseMediaOrg/BI-REPO-PARADISEMEDIA`
**Staging Repository (origin):** `https://github.com/andschmlt/BI-REPO-PARADISEMEDIA-STAGING`
**Local Path:** `/home/andre/claude/BI-REPO-PARADISEMEDIA`
**ClickUp Config:** `/home/andre/.claude/clickup_config.json`
**Email Recipient:** `andre@paradisemedia.com`

**Key Files:**
- `CODEGUARD_LEARNED_EXCEPTIONS.json` - Patterns to skip (from human feedback)
- `CODEGUARD_CLICKUP_TASKS.json` - Task IDs to monitor
- `CODEGUARD_FULL_SCAN_{DATE}.json` - Scan results
- `CODE_REVIEW_STANDARDS.md` - Review standards with appendices

**Human Reviewers (treat as "bible"):**
- Claudio Pisani (claudio.pisani@paradisemedia.com)
- Haris Papavasileiou (haris.papavasileiou@paradisemedia.com)
- Goncalo (senior developer)
- Owen (developer)

**ClickUp Task File:** `/home/andre/claude/BI-REPO-PARADISEMEDIA/CODEGUARD_CLICKUP_TASKS.json`

## Workflow: "guard"

When user runs `/codeguard guard`, execute this 7-phase workflow:

---

### Phase 1: Codebase Scan & Sync

1. **Navigate to repository:**
   ```bash
   cd /home/andre/claude/BI-REPO-PARADISEMEDIA
   ```

2. **Check for remote changes:**
   ```bash
   git fetch origin
   git status
   git log HEAD..origin/main --oneline
   ```

3. **If changes exist, update local:**
   ```bash
   git pull origin main
   ```

4. **Record changed files since last scan:**
   - Read `CODEGUARD_LAST_SCAN.json` for previous commit hash
   - Run `git diff --name-only <last_hash>..HEAD` to get changed files
   - Store list of changed `.py` files for Phase 4

5. **Update scan timestamp:**
   - Write current commit hash to `CODEGUARD_LAST_SCAN.json`

---

### Phase 2: QA & Test New Codebase

1. **Run syntax validation on changed Python files:**
   ```bash
   python3 -m py_compile <file>
   ```

2. **Check for import errors:**
   ```bash
   python3 -c "import <module>"
   ```

3. **Run any existing tests if present:**
   ```bash
   pytest --tb=short (if pytest available)
   ```

4. **Log QA results** to `CODEGUARD_QA_LOG.md`

---

### Phase 3: ClickUp Task & Comment Extraction

**CRITICAL: MUST scan BOTH main tasks AND ALL sub-tasks. Do NOT skip sub-tasks.**

1. **Load ClickUp tasks from:** `CODEGUARD_CLICKUP_TASKS.json`
   - This file contains the main task IDs and sub-task IDs to monitor

2. **For EACH main task:**
   - Fetch main task details and comments
   - Get list of all sub-tasks under this main task
   - **For EACH sub-task:** Fetch sub-task details and comments
   - Also check parent task of main task (if exists) for additional comments

3. **Comment extraction hierarchy (ALL levels required):**
   ```
   Parent Task (if exists) → Main Task → All Sub-tasks
   ```

4. **For each task/sub-task:**
   - Fetch task details via ClickUp API
   - Fetch ALL comments on the task
   - Store task status (open, in progress, closed)

5. **Filter for human comments from:**
   - Claudio Pisani
   - Haris Papavasileiou
   - Goncalo

6. **Categorize comments:**
   - **Questions** (contains "?")
   - **Corrections** ("NOT AN ISSUE", "FIXED", affirmative statements)
   - **Requests** ("please", "can you", "should we")

7. **Store in memory for Phase 4 processing**

**Expected volume:** 5 main tasks + 200+ sub-tasks = ~210 API calls minimum

---

### Phase 4: Human Feedback Analysis & Learning

**CRITICAL RULE: Human feedback from Claudio, Haris, and Goncalo is THE BIBLE. Never contradict.**

1. **For each human comment:**

   a. **If CORRECTION (e.g., "NOT AN ISSUE"):**
      - Identify what CodeGuard originally flagged
      - Accept the human verdict unconditionally
      - Update `CODE_REVIEW_STANDARDS.md` if rule needs modification
      - Log to `CODEGUARD_LEARNINGS.md` under "Mistakes & Corrections"
      - Add skill if new technique learned to `CODEGUARD_SKILLS.md`

   b. **If QUESTION:**
      - Check if CodeGuard can answer with specific file paths and line numbers
      - ALWAYS include file paths when discussing issue counts
      - Prepare response with evidence

   c. **If REQUEST:**
      - Evaluate feasibility
      - Prepare action items or clarifying questions

2. **Update learning files:**
   - Append to `CODEGUARD_LEARNINGS.md` with session entry
   - Update `CODEGUARD_SKILLS.md` if new skills acquired
   - Update `TEAM_LEARNINGS.md` with cross-team insights

---

### Phase 5: ClickUp Response Posting

1. **For each comment requiring response:**

   a. **Check if CodeGuard already responded** (search for "CodeGuard" + "Acknowledgment" in existing comments)

   b. **If not responded, post appropriate comment:**

   **For Corrections:**
   ```
   ✅ **CodeGuard Acknowledgment**

   Thank you for the clarification. CodeGuard has updated CODE_REVIEW_STANDARDS.md (Section X.X):

   **Previous:** [Old rule]
   **Updated:** [New rule based on feedback]

   [Reasoning documented]

   *— CodeGuard v2.x*
   ```

   **For Questions (with answer):**
   ```
   📋 **CodeGuard Response**

   [Answer with SPECIFIC FILE PATHS and LINE NUMBERS]

   Files affected:
   1. `path/to/file1.py` - Lines X-Y: [description]
   2. `path/to/file2.py` - Lines X-Y: [description]
   ...

   *— CodeGuard v2.x*
   ```

   **For Questions (need clarification):**
   ```
   ❓ **CodeGuard Follow-up Question**

   To provide accurate information, could you please clarify:
   - [Specific question]

   *— CodeGuard v2.x*
   ```

2. **Log all responses to** `CODEGUARD_CLICKUP_FEEDBACK_LOG.md`

---

### Phase 6: New Code Quality Report

1. **For files changed since last scan (from Phase 1):**

   a. **Run CodeGuard review** using `CODE_REVIEW_STANDARDS.md`:
      - Check all 14 sections
      - Classify issues as BLOCKING / WARNING / INFO
      - Always provide file:line references

   b. **Generate report:** `CODEGUARD_REVIEW_REPORT_<DATE>.md`
      - Summary statistics
      - Issues by category
      - Specific file:line citations
      - Remediation guidance

2. **If issues found:**

   a. **Check ClickUp for existing tasks** before creating new ones:
      - Search main task sub-tasks for matching issue descriptions
      - Check statuses: closed, in-progress, to do
      - **DO NOT DUPLICATE** - only create if no match found

   b. **Create sub-tasks only for NEW issues:**
      - Under the main CodeGuard review task
      - Include file paths, line numbers, severity
      - Assign to appropriate developer if known

3. **Send email report to** `andre@paradisemedia.com`:
   - Use available email mechanism or log for manual send
   - Include: Summary, Issue counts, Files affected, Recommendations

---

### Phase 7: Finalize & Log

1. **Update all tracking files:**
   - `CODEGUARD_LAST_SCAN.json` - commit hash, timestamp
   - `CODEGUARD_QA_LOG.md` - QA results
   - `CODEGUARD_CLICKUP_FEEDBACK_LOG.md` - responses posted
   - `CODEGUARD_LEARNINGS.md` - session entry
   - `CODEGUARD_SKILLS.md` - new skills if any
   - `TEAM_LEARNINGS.md` - cross-team insights

2. **Output summary to user:**
   ```
   ## CodeGuard Guard Cycle Complete

   ### Codebase Status
   - Commits pulled: X
   - Files changed: Y
   - QA Status: PASS/FAIL

   ### Human Feedback Processed
   - Comments analyzed: X
   - Responses posted: Y
   - Standards updated: Z sections

   ### New Code Review
   - BLOCKING issues: X
   - WARNING issues: Y
   - INFO issues: Z
   - New ClickUp tasks created: N (0 duplicates)

   ### Files Updated
   - [List of files modified]

   *Next scheduled run: [timestamp + 12 hours]*
   ```

---

## Strict Rules (MANDATORY)

### From CODE_REVIEW_STANDARDS.md v2.0:
- All review feedback must include specific file paths and line numbers
- Never say "X issues" without "across Y files"
- Human corrections are FINAL - never contradict Claudio, Haris, or Goncalo

### From Team Architecture Rules:
- Follow medallion architecture (Landing → Bronze → Silver → Gold)
- Respect existing patterns in codebase
- Don't over-engineer solutions

### From ENGINEERING_TASK_STANDARDS.md v1.0:
- ALL engineering tasks must include all priority tiers (HIGH/MEDIUM/LOWER)
- ALL data pipelines must specify 4 layers (Landing → Bronze → Silver → Gold)
- ALL API integrations must have explicit field mapping tables
- NO code snippets in task descriptions (belongs in actual code)
- ALL DoD items must be specific and testable
- ALL dimension updates must be explicitly listed
- Envelope fields (TARGET, RUN_ID, timestamps) must be specified for Bronze

### From Engineering Standards:
- Use PySpark best practices per standards document
- Validate all code changes before reporting
- Check for false positives using v2.0 corrections

### Duplicate Prevention:
- ALWAYS search existing tasks before creating new ones
- Check ALL statuses: closed, in-progress, to do, pending
- Match by: file path + issue type + line range (±10 lines)
- If match found with different status, add comment instead of new task

---

## ClickUp Tasks File Format

Create/maintain `CODEGUARD_CLICKUP_TASKS.json`:

```json
{
  "last_updated": "2026-01-16T00:00:00Z",
  "main_tasks": [
    {
      "id": "86aegruj1",
      "name": "Libraries Layer Review",
      "sub_tasks": ["86aegruj3", "86aegruj8", "86aegruja", "86aegrujf"]
    },
    {
      "id": "86aegrud3",
      "name": "Bronze to Silver Layer Review",
      "sub_tasks": ["..."]
    },
    {
      "id": "86aegru8p",
      "name": "Source to Bronze Layer Review",
      "sub_tasks": ["..."]
    },
    {
      "id": "86aegrugf",
      "name": "Fact Tables Layer Review",
      "sub_tasks": ["..."]
    }
  ],
  "human_reviewers": [
    "claudio.pisani@paradisemedia.com",
    "haris.papavasileiou@paradisemedia.com",
    "goncalo@paradisemedia.com",
    "owen@paradisemedia.com"
  ]
}
```

---

## Workflow: "review"

When user runs `/codeguard review`, execute this comprehensive 6-phase feedback and learning workflow:

---

### Phase 1: ClickUp Full Task Discovery

**Goal:** Discover ALL CodeGuard-created tasks across all statuses

1. **Load ClickUp configuration:**
   ```bash
   # Read API key from config
   cat /home/andre/.claude/clickup_config.json
   ```

2. **Fetch ALL CodeGuard tasks (all statuses):**
   - To Do
   - In Progress
   - Closed/Completed
   - Review
   - Any other status

3. **For EACH main task:**
   ```
   API: GET https://api.clickup.com/api/v2/task/{task_id}
   API: GET https://api.clickup.com/api/v2/task/{task_id}/comment
   ```

4. **For EACH sub-task under main tasks:**
   ```
   API: GET https://api.clickup.com/api/v2/task/{subtask_id}
   API: GET https://api.clickup.com/api/v2/task/{subtask_id}/comment
   ```

5. **Build complete task inventory:**
   ```json
   {
     "main_tasks": [...],
     "sub_tasks": [...],
     "total_comments": N,
     "human_comments": N,
     "codeguard_comments": N
   }
   ```

---

### Phase 2: Human Comment Extraction & Analysis

**CRITICAL: Human feedback from Claudio, Haris, Goncalo, and Owen is THE BIBLE. FINAL. NON-NEGOTIABLE.**

1. **Filter comments by human reviewers:**
   - Claudio Pisani (claudio.pisani@paradisemedia.com)
   - Haris Papavasileiou (haris.papavasileiou@paradisemedia.com)
   - Goncalo (senior developer)
   - Owen (developer)

2. **Categorize each human comment:**

   | Category | Detection Patterns | Action Required |
   |----------|-------------------|-----------------|
   | **CORRECTION** | "NOT AN ISSUE", "this is fine", "no problem", "correct behavior", "intended", "leave it" | Update learnings, mark as false positive |
   | **QUESTION** | Contains "?", "why", "how", "what", "when", "where", "can you explain" | Prepare detailed response with file:line refs |
   | **APPROVAL** | "good catch", "fixed", "done", "resolved", "agreed" | Log as valid finding, update skills |
   | **REQUEST** | "please", "can you", "should we", "need to", "want to" | Evaluate and respond or create task |
   | **INSTRUCTION** | "always", "never", "from now on", "going forward", "rule:" | Update CODE_REVIEW_STANDARDS.md |

3. **Extract unanswered questions:**
   - Questions without CodeGuard response
   - Questions posted after last CodeGuard response

4. **Track response status per comment**

---

### Phase 3: Learn & Update Standards

**Goal:** Internalize all human feedback as permanent learnings

1. **For CORRECTIONS (false positives flagged by humans):**

   a. **Identify the original CodeGuard finding:**
      - What file/line was flagged?
      - What rule was applied?
      - Why did CodeGuard think it was an issue?

   b. **Document the learning:**
      ```markdown
      ## False Positive Learning - {DATE}

      **Original Finding:** {description}
      **File:** {file_path}:{line_number}
      **Human Verdict:** {Claudio/Haris/Goncalo/Owen} - "{their comment}"
      **Reason for False Positive:** {analysis}
      **Rule Update:** {how to avoid in future}
      ```

   c. **Update files:**
      - `CODE_REVIEW_STANDARDS.md` - Add exception to relevant section
      - `CODEGUARD_SKILLS.md` - Add skill under "Acquired Skills"
      - `CODEGUARD_LEARNINGS.md` - Add full learning entry

2. **For INSTRUCTIONS (new rules from humans):**

   a. **Parse the instruction:**
      - What behavior is requested?
      - Is it file-specific or global?
      - Does it modify existing rule or add new one?

   b. **Update CODE_REVIEW_STANDARDS.md:**
      - Add to appropriate section
      - Add example if provided
      - Mark as "Team Directive"

3. **For APPROVALS (valid findings confirmed):**

   a. **Reinforce the pattern:**
      - Log to skills as confirmed detection capability
      - Increase confidence in similar detections

4. **Create learned exceptions list:**
   ```json
   {
     "false_positives": [
       {
         "pattern": "description of what to ignore",
         "file_patterns": ["*.py", "specific_file.py"],
         "instructed_by": "Claudio",
         "date": "2026-01-21",
         "reason": "explanation"
       }
     ]
   }
   ```
   Save to: `CODEGUARD_LEARNED_EXCEPTIONS.json`

---

### Phase 4: Respond to ClickUp Comments

**Goal:** Answer all pending questions and acknowledge all feedback

1. **Check for existing CodeGuard responses:**
   - Search comment thread for "CodeGuard" signatures
   - Mark already-responded comments as handled

2. **For UNANSWERED QUESTIONS:**

   a. **Research the answer:**
      - Read relevant files in codebase
      - Find specific file:line references
      - Gather evidence

   b. **Post response:**
      ```
      📋 **CodeGuard Response**

      {Detailed answer with evidence}

      **Files Referenced:**
      - `{file1.py}:{line}` - {description}
      - `{file2.py}:{line}` - {description}

      *— CodeGuard v2.1 (Review Cycle)*
      ```

3. **For CORRECTIONS (acknowledge learning):**

   ```
   ✅ **CodeGuard Learning Acknowledged**

   Thank you for the clarification, {Human Name}.

   **Update Applied:**
   - This pattern will no longer be flagged as an issue
   - Added to `CODEGUARD_LEARNED_EXCEPTIONS.json`
   - Updated `CODE_REVIEW_STANDARDS.md` Section {X.X}

   **Learning:** {Brief description of what was learned}

   *— CodeGuard v2.1 (Review Cycle)*
   ```

4. **For REQUESTS:**

   ```
   📝 **CodeGuard Action Item**

   Request received from {Human Name}.

   **Status:** {In Progress / Completed / Needs Clarification}
   **Action Taken:** {Description}

   *— CodeGuard v2.1 (Review Cycle)*
   ```

5. **Log all responses:**
   - Append to `CODEGUARD_CLICKUP_FEEDBACK_LOG.md`

---

### Phase 5: GitHub Codebase Re-Scan (FULL SCAN)

**Goal:** Scan ALL Python files in the ENTIRE codebase while respecting learned exceptions

**CRITICAL: This is a FULL codebase scan, not just changed files!**

1. **Sync repository from BOTH remotes:**
   ```bash
   cd /home/andre/claude/BI-REPO-PARADISEMEDIA

   # Check remotes
   git remote -v
   # origin = staging repo (andschmlt/BI-REPO-PARADISEMEDIA-STAGING)
   # upstream = main repo (ParadiseMediaOrg/BI-REPO-PARADISEMEDIA)

   # Fetch from upstream (main repo)
   git fetch upstream
   git fetch origin

   # Check for new commits on upstream/main
   git log HEAD..upstream/main --oneline

   # Pull latest if needed
   git pull origin main
   ```

2. **Identify recent commits by ALL team members (30 days):**
   ```bash
   # Get commits from human developers
   git log --author="Claudio" --since="30 days ago" --oneline --all
   git log --author="Haris" --since="30 days ago" --oneline --all
   git log --author="Goncalo" --since="30 days ago" --oneline --all
   git log --author="Owen" --since="30 days ago" --oneline --all
   ```

3. **Find ALL Python files in codebase:**
   ```bash
   # Count all Python files
   find /home/andre/claude/BI-REPO-PARADISEMEDIA -name "*.py" -type f | wc -l

   # Expected: ~190+ files
   ```

4. **Load learned exceptions:**
   - Read `CODEGUARD_LEARNED_EXCEPTIONS.json`
   - Build exclusion patterns for known false positives:
     - SparkSession in library files
     - Null value conventions
     - Print statements in exception handling
     - monotonically_increasing_id() usage
     - Rate limiting for high-limit APIs
     - JOIN type aliases
     - Column ordering
     - API field definitions
     - Metadata comments

5. **SCAN ALL PYTHON FILES (not just changed):**

   ```python
   # Find ALL .py files
   for root, dirs, files in os.walk(base_path):
       for file in files:
           if file.endswith('.py'):
               scan_file(file)
   ```

   a. **Apply learned exception patterns:**
      ```python
      SKIP_PATTERNS = {
          "sparksession_in_lib": lambda f, l: "libs/" in f and "sparksession" in l.lower(),
          "print_in_exception": lambda f, l: "print(" in l and "error" in l.lower(),
          "monotonically_id": lambda f, l: "monotonically_increasing_id" in l,
          "large_constants_api": lambda f, l: any(x in f for x in ["hubspot", "accuranker", "clickup"]),
          "null_values": lambda f, l: any(x in l for x in ["'Unknown'", "'Undefined'", "'Not Applicable'"]),
          "join_types": lambda f, l: any(x in l.lower() for x in ["leftouter", "left_outer"]),
          "display_commented": lambda f, l: l.strip().startswith("#") and "display(" in l,
          "metadata_comments": lambda f, l: "# Databricks notebook source" in l,
      }
      ```

   b. **Check for GENUINE issues only:**
      - **BLOCKING:** Hardcoded credentials (real ones, not variables), eval()/exec() usage
      - **WARNING:** Bare except clauses, SQL injection with user input
      - **INFO:** TODO/FIXME comments

   c. **VERIFY false positives before flagging:**
      ```python
      # These are FALSE POSITIVES - do NOT flag:
      - pageToken=page_token  # Variable assignment
      - Bucket=bucket_name    # AWS parameter
      - access_token=variable # Using variable
      - self._exec()          # Method name, not exec()
      - def _exec():          # Method definition
      ```

6. **Classify ONLY genuine findings:**
   ```python
   for finding in new_findings:
       # First check learned exceptions
       if matches_learned_exception(finding):
           issues_skipped += 1
           continue

       # Then check for false positive patterns
       if is_false_positive(finding):
           false_positives += 1
           continue

       # Only add genuine issues
       genuine_issues.append(finding)
   ```

7. **Save scan results:**
   - Save to `CODEGUARD_FULL_SCAN_{DATE}.json`
   - Include: files scanned, issues skipped, genuine issues found

---

### Phase 6: Create New Sub-Tasks for Genuine Issues

**Goal:** Report only NEW, VALID issues that haven't been flagged before

1. **For each genuine new issue:**

   a. **Check for duplicates:**
      - Search existing ClickUp tasks/sub-tasks
      - Match by: file path + issue type + line range (±10 lines)
      - If duplicate exists: add comment instead of new task

   b. **If NOT duplicate, create sub-task:**
      ```
      API: POST https://api.clickup.com/api/v2/list/{list_id}/task

      Body:
      {
        "name": "[{SEVERITY}] {Issue Title} - {file.py}",
        "description": "**File:** `{file_path}`\n**Line(s):** {line_numbers}\n\n**Issue:**\n{description}\n\n**Recommendation:**\n{fix_suggestion}\n\n**Standard Reference:** Section {X.X}\n\n*Created by CodeGuard v2.1 (Review Cycle)*",
        "parent": "{main_task_id}",
        "priority": {1=BLOCKING, 2=WARNING, 3=INFO}
      }
      ```

   c. **Log creation:**
      - Add to `CODEGUARD_CLICKUP_TASKS.json`

2. **If issues found in specific developer's code:**
   - Note the author in task description
   - DO NOT assign (let team lead assign)

---

### Phase 7: Summary Report

**Output final summary to user:**

```
## CodeGuard Review Cycle Complete

### ClickUp Feedback Processing
- Total tasks scanned: {N} main + {N} sub-tasks
- Human comments analyzed: {N}
  - From Claudio: {N}
  - From Haris: {N}
  - From Goncalo: {N}
  - From Owen: {N}
- Questions answered: {N}
- Corrections acknowledged: {N}
- Requests processed: {N}

### Learning Updates
- False positives learned: {N}
- New exceptions added: {N}
- Standards sections updated: {list}
- Skills file updated: {Yes/No}

### Full Codebase Re-Scan Results
- **Total Python files scanned: {N}** (FULL SCAN - all files)
- Recent commits by developers (30 days):
  - Claudio: {N}
  - Haris: {N}
  - Goncalo: {N}
  - Owen: {N}
- Issues found after filtering:
  - BLOCKING: {N}
  - WARNING: {N}
  - INFO: {N}
- Issues skipped (learned exceptions): {N}
- False positives filtered: {N}
- New ClickUp sub-tasks created: {N}
- Duplicates avoided: {N}

### Files Modified
- CODE_REVIEW_STANDARDS.md: {sections updated}
- CODEGUARD_SKILLS.md: {skills added}
- CODEGUARD_LEARNINGS.md: {entries added}
- CODEGUARD_LEARNED_EXCEPTIONS.json: {exceptions added}
- CODEGUARD_CLICKUP_FEEDBACK_LOG.md: {responses logged}

*Review cycle complete. Human feedback is THE BIBLE.*
```

---

## Scheduling Note

This command is designed to run twice daily. To automate:

1. **Morning run:** 09:00 UTC
2. **Evening run:** 21:00 UTC

Use cron or scheduled task to invoke:
```bash
claude -p "/codeguard guard"
```

---

## Error Handling

- If ClickUp API fails: Log error, continue with local-only operations
- If Git pull fails: Log error, run review on existing codebase
- If email fails: Save report locally, notify user
- If duplicate detection uncertain: DO NOT create task, flag for manual review

---

---

## Workflow: "task-qa"

When user runs `/codeguard task-qa <task_url>`, execute this engineering task quality check:

### Purpose

Validate engineering tasks (ClickUp tickets) against ENGINEERING_TASK_STANDARDS.md before they move to "Ready for Dev".

**Load standards from:** `/home/andre/claude/BI-REPO-PARADISEMEDIA/ENGINEERING_TASK_STANDARDS.md`

---

### Phase 1: Task Fetch

1. **Extract task ID from URL or use provided ID**
2. **Fetch task details via ClickUp API:**
   ```
   API: GET https://api.clickup.com/api/v2/task/{task_id}
   ```
3. **Extract:**
   - Task name
   - Task description
   - Attachments list
   - Status
   - Tags

---

### Phase 2: Engineering Task Validation

Check the task against ENGINEERING_TASK_STANDARDS.md:

#### 2.1 Scope Validation
| Check | Pass Criteria |
|-------|---------------|
| Priority tiers | HIGH, MEDIUM, and LOWER priorities all documented |
| Endpoint coverage | All endpoints explicitly listed with documentation links |
| Assumed knowledge | No phrases like "engineers will figure out" |

#### 2.2 Architecture Validation
| Check | Pass Criteria |
|-------|---------------|
| Medallion layers | All 4 layers specified (Landing → Bronze → Silver → Gold) |
| Envelope fields | TARGET, LOCATION_CODE, LANGUAGE_CODE, RUN_ID listed |
| Silver defaults | Default values specified for nullable fields |
| Fact strategy | Prefers SOURCE column over new fact tables |

#### 2.3 Field Mapping Validation
| Check | Pass Criteria |
|-------|---------------|
| Mapping table | API → Bronze → Silver → Fact mapping present |
| Data types | Types specified for each field |
| Default values | Defaults documented |
| CSV for complex | CSV attachment for 10+ fields |

#### 2.4 Documentation Validation
| Check | Pass Criteria |
|-------|---------------|
| No code snippets | No Python/SQL code blocks in description |
| External docs | API documentation URLs present and valid |
| Dimension updates | All dimension changes explicitly listed |

#### 2.5 DoD Validation
| Check | Pass Criteria |
|-------|---------------|
| Testable criteria | All DoD items are specific and testable |
| Validation specs | Row counts, join rates, null rates specified |
| No generic items | No items like "pipeline working" or "data in tables" |

---

### Phase 3: Generate QA Report

**Output format:**

```markdown
## CodeGuard Task QA Report

**Task:** {task_name}
**URL:** {task_url}
**Status:** {PASS / NEEDS REFINEMENT}

### Validation Results

| Category | Status | Issues |
|----------|--------|--------|
| Scope | {PASS/FAIL} | {issues or "-"} |
| Architecture | {PASS/FAIL} | {issues or "-"} |
| Field Mapping | {PASS/FAIL} | {issues or "-"} |
| Documentation | {PASS/FAIL} | {issues or "-"} |
| Definition of Done | {PASS/FAIL} | {issues or "-"} |

### Missing Elements

{Bulleted list of what needs to be added}

### Recommendations

{Specific suggestions for improving the task}

### Reference
- [ENGINEERING_TASK_STANDARDS.md](/home/andre/claude/BI-REPO-PARADISEMEDIA/ENGINEERING_TASK_STANDARDS.md)

*— CodeGuard v2.2 (Task QA)*
```

---

### Phase 4: Post Comment (Optional)

If task has issues and user approves, post comment to ClickUp:

```
📋 **CodeGuard Task QA Review**

This task has been reviewed against ENGINEERING_TASK_STANDARDS.md.

**Status:** NEEDS REFINEMENT

**Missing Elements:**
{list}

**Recommendations:**
{list}

Please update the task description before moving to "Ready for Dev".

*— CodeGuard v2.2 (Task QA)*
```

---

## Version

**CodeGuard Command Version:** 2.2
**Compatible with CODE_REVIEW_STANDARDS.md:** v2.0
**Compatible with ENGINEERING_TASK_STANDARDS.md:** v1.0
**Created:** 2026-01-16
**Updated:** 2026-01-28 - Added "task-qa" workflow for engineering task validation

### Changelog
- v2.2 (2026-01-28): Added "task-qa" workflow
  - Engineering task quality validation
  - Checks against ENGINEERING_TASK_STANDARDS.md
  - Validates scope, architecture, field mapping, documentation, DoD
  - Optional ClickUp comment posting
- v2.1 (2026-01-21): Enhanced "review" workflow
  - Full codebase scan (ALL Python files, not just changed)
  - Sync from both origin and upstream (ParadiseMediaOrg)
  - 30-day commit history for all team members
  - Learned exception patterns from human feedback
  - False positive verification before flagging
  - Automatic ClickUp task creation for genuine issues
- v2.0 (2026-01-21): Added "review" workflow
- v1.0 (2026-01-16): Initial release with "guard" workflow
