# /create_persona - Virtual ATeam Persona Generator

Generate a new virtual persona from a human team member's ClickUp activity data.

## Phase 0: RAG Context Loading

**Load existing persona patterns from RAG before creating new ones.**

```python
from AS-Virtual_Team_System_v2.rag.rag_client import VTeamRAG
rag = VTeamRAG()
persona_patterns = rag.query("persona creation template structure", collection_name="personas", top_k=5)
```

---

## Usage

```bash
/create_persona "Human Name or Email" "Persona Title"
```

## Examples

```bash
/create_persona "giuseppe@paradisemedia.com" "Senior Content Manager"
/create_persona "Anna Miller" "Publisher Relations Manager"
/create_persona "Guillaume Bonastre" "Head of Strategy"
```

## Input Parameters

$ARGUMENTS

Parse the arguments to extract:
1. **Human Identifier** - Name or email address (first quoted string)
2. **Persona Title** - Role title for the new persona (second quoted string)

## Execution Process

### Phase 1: Human Identification

1. **Read the Persona Candidates Registry**:
   - File: `/mnt/c/Users/andre/Desktop/Virtual ATeam/BlackTeam/PERSONA_CANDIDATES.md`
   - Find the human by name or email
   - Extract their ClickUp User ID if available

2. **If not found in registry**, search ClickUp API:
   ```
   GET https://api.clickup.com/api/v2/team
   Header: Authorization: $CLICKUP_API_KEY
   ```
   - Search through team members for matching name/email
   - Extract user ID

### Phase 1.5: Additional Files Prompt (REQUIRED)

**IMPORTANT:** After identifying the human, use the AskUserQuestion tool to prompt the user:

```
Question: "Would you like to add any reference files to enhance the persona creation?"

Header: "Add Files"

Options:
1. "Yes, I have files to add" - Description: "Provide job descriptions, SOPs, training docs, email samples, or other reference materials"
2. "No, use ClickUp data only" - Description: "Create persona using only ClickUp activity data"
```

**If user selects "Yes":**
1. Ask: "Please provide the file paths (one per line or comma-separated)"
2. Read each provided file
3. Extract relevant patterns:
   - Role expectations
   - Communication samples
   - Process documentation
   - Performance criteria
   - Decision frameworks
4. Incorporate findings into the 5 Ralph Loops analysis

**Supported File Types:**
- `.md` - Markdown documentation
- `.txt` - Text files
- `.docx` - Word documents (extract text)
- `.pdf` - PDF documents
- `.json` - Structured data
- `.csv` - Data files
- `.html` - Web content
- `.pbix` - Power BI reports (extract data model, measures, report structure)

**File Analysis Focus:**
| File Type | Extract |
|-----------|---------|
| Job descriptions | Responsibilities, KPIs, qualifications |
| SOPs/Processes | Step-by-step procedures, quality gates |
| Email samples | Communication style, tone, patterns |
| Training docs | Skills required, best practices |
| Performance reviews | Strengths, areas of focus |
| Meeting notes | Decision patterns, collaboration style |
| Power BI reports (.pbix) | Metrics tracked, KPIs monitored, data relationships, DAX measures |

### Phase 2: ClickUp Data Mining (5 Ralph Loops)

Use the ClickUp API to gather comprehensive data about the human's activities.

**API Key:** `$CLICKUP_API_KEY`
**Workspace ID:** `8553292`

#### Loop 1: Task Collection
Query all tasks assigned to the user:
- Space: PUBLISHING (66211463)
- Space: CONTENT WORK ZONE (90090126537)
- Include subtasks: `?subtasks=true&include_closed=true`
- Extract: Task types, statuses, custom fields used

#### Loop 2: Comment Mining
For each task found:
1. Get the parent task ID (if subtask)
2. Query comments on the parent task
3. Filter comments by the user
4. Extract: Communication patterns, decision language, escalation triggers

#### Loop 3: Pattern Analysis
Analyze the collected data for:
- **Must-Do's**: Actions consistently taken
- **Must-Don'ts**: Actions avoided or corrected
- **Decision Triggers**: What prompts action
- **Communication Style**: How they phrase requests, feedback
- **Collaboration Patterns**: Who they work with, @ mention patterns

#### Loop 4: Custom Field Analysis
Identify which custom fields they interact with:
- Fields they update frequently
- Values they set
- Workflow stages they use

#### Loop 5: Synthesis
Combine all findings into persona components:
- Role definition
- Responsibilities
- Decision framework
- Communication protocol
- Quality standards

### Phase 3: Generate Persona Files

Create three files in the BlackTeam directory structure:

#### File 1: Persona Definition
**Path:** `/mnt/c/Users/andre/Desktop/Virtual ATeam/BlackTeam/personas/{PERSONA_NAME_SNAKE_CASE}.md`

```markdown
# {Persona Title} - Team Lead/Specialist Persona

---

## Professional Profile

```
Name:           {Persona Name} (Virtual)
Title:          {Persona Title}
Department:     {Derived from activity}
Reports To:     {Based on hierarchy}
Direct Reports: {If leadership role}
Experience:     {X}+ Years (Equivalent)
Location:       Virtual / Asynchronous
Team:           BlackTeam
```

---

## LinkedIn-Style Profile Summary

### Headline
{Generate based on role and activities}

### About
{2-3 paragraphs summarizing expertise, based on activity patterns}

---

## Role Overview

### Primary Function
{List 5-7 key responsibilities derived from task patterns}

---

## Decision Framework

### Quality Triggers - When to Flag Issues
{Table of triggers derived from comments}

### Strategic Decision Points
{When to take which actions}

---

## Communication Protocol

### Standard Response Patterns
{Templates derived from actual comment patterns}

---

## Must Do's (Operational Rules)
{Numbered list of 15-25 rules from behavior analysis}

---

## Must Don'ts (Anti-Patterns to Avoid)
{Numbered list of 15-20 anti-patterns from corrections/escalations}

---

## Key Metrics Monitored
{Table of metrics they track based on custom field usage}

---

## Primary Collaborators
{Table of people they interact with most}

---

## Activation Statement
{1-2 paragraph persona activation prompt}

---

## Analysis Methodology

| Analysis Phase | Data Points |
|----------------|-------------|
| Tasks analyzed | {count} |
| Comments analyzed | {count} |
| Custom fields tracked | {count} |
| Team interactions mapped | {count} pairs |

---

## Document Control

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | {today} | Initial persona creation from ClickUp behavior analysis |

```

#### File 2: Skills Inventory
**Path:** `/mnt/c/Users/andre/Desktop/Virtual ATeam/BlackTeam/skills/{PERSONA_NAME_SNAKE_CASE}_SKILLS.md`

```markdown
# {Persona Title} - Skills Inventory

**Persona:** {Persona Name}
**Last Updated:** {today}

---

## Core Competencies

### {Category 1}
- Skill 1
- Skill 2

### {Category 2}
- Skill 1
- Skill 2

---

## Technical Proficiency

| Tool | Purpose |
|------|---------|
| ClickUp | {usage pattern} |
| {Other tools} | {usage} |

---

## Quality Standards

### Checkpoints
{Derived from QC patterns}

### Performance Metrics
{Derived from custom fields tracked}

---

## Acquired Skills (Session-Based)

<!-- SKILL_LOG_START -->
{Empty - to be populated by /reflect}
<!-- SKILL_LOG_END -->
```

#### File 3: Job Description
**Path:** `/mnt/c/Users/andre/Desktop/Virtual ATeam/BlackTeam/personas/{PERSONA_NAME_SNAKE_CASE}_JOB_DESCRIPTION.md`

```markdown
# {Persona Title} - Job Description

## Position Overview
{Role summary}

## Key Responsibilities (% breakdown)
{List with percentages based on activity distribution}

## Required Qualifications
{Inferred from demonstrated skills}

## KPIs
{Derived from custom fields and metrics tracked}

## Reporting Structure
{Based on collaboration patterns}
```

### Phase 4: Update Registry

Update the PERSONA_CANDIDATES.md file:
- Mark the human as "CREATED"
- Add to "Already Created Personas" table
- Include creation date

### Phase 5: Update Team Config

If this is a leadership role, update `/mnt/c/Users/andre/Desktop/Virtual ATeam/BlackTeam/TEAM_CONFIG.md`:
- Add to team roster
- Add to capability matrix
- Update routing rules if applicable

## Output Format

After completion, display:

```
PERSONA CREATED SUCCESSFULLY

Human Source: {Name} ({email})
ClickUp ID: {id}
Persona Title: {title}

Data Analyzed:
- Tasks: {count}
- Comments: {count}
- Custom Fields: {count}
- Team Interactions: {count}
- Additional Files: {count} (or "None")

Additional Files Used:
- {file1.ext} - {type: job description/SOP/etc}
- {file2.ext} - {type}
(or "No additional files provided")

Files Created:
1. personas/{filename}.md
2. skills/{filename}_SKILLS.md
3. personas/{filename}_JOB_DESCRIPTION.md

Files Updated:
- PERSONA_CANDIDATES.md (marked as created)
- TEAM_CONFIG.md (if leadership role)

Must-Do's Extracted: {count}
Must-Don'ts Extracted: {count}

The persona is ready to use with:
/persona {shortname}
```

## Error Handling

| Error | Resolution |
|-------|------------|
| Human not found | Check spelling, try email instead of name |
| No ClickUp activity | Cannot create persona without activity data |
| API rate limit | Wait and retry with exponential backoff |
| Insufficient comments | Expand search to parent tasks |
| File not found | Verify path, check for typos, confirm file exists |
| Unsupported file type | Convert to supported format (.md, .txt, .docx, .pdf) |
| File read error | Check permissions, try alternative path |
| Empty file | Skip and notify user, continue with other sources |

## Notes

- Minimum 10 comments required for reliable pattern extraction
- Minimum 20 tasks required for activity analysis
- If data is insufficient, report what's available and ask for approval to proceed
- Always run 5 Ralph Loops - do not skip analysis phases
- Reference the Head of Post Production Management persona creation (BT-2026-003) as the gold standard
- **ALWAYS prompt user for additional files** - this enriches persona quality
- Additional files can compensate for limited ClickUp activity data
- File content is merged with ClickUp patterns during Loop 5 (Synthesis)
- If user provides files, mention them in the persona's "Analysis Methodology" section

## Related Commands

- `/persona {name}` - Load an existing persona
- `/blackteam {project}` - Execute a project with BlackTeam
- `/reflect` - Capture session learnings

---

*Command created: 2026-01-19 | Updated: 2026-01-19 (Added file upload prompt) | BlackTeam Virtual ATeam*
