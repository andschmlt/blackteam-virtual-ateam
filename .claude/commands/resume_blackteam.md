# /resume_blackteam - Resume BlackTeam Session

Resume or review previous BlackTeam sessions.

## Phase 0: RAG Context Loading

**Load session context from RAG before resuming.**

```python
from AS-Virtual_Team_System_v2.rag.rag_client import VTeamRAG
rag = VTeamRAG()
context = rag.query("blackteam session resume", top_k=3)
learnings = rag.query("recent session learnings", collection_name="learnings", top_k=5)
```

---

## Session Directory
`/mnt/c/Users/andre/Desktop/Virtual ATeam/BlackTeam/sessions/`

## Instructions

1. **Read the Session Index**
   Read `/mnt/c/Users/andre/Desktop/Virtual ATeam/BlackTeam/sessions/SESSION_INDEX.md`

2. **Display Available Sessions**
   Show the user a formatted list of recent sessions:
   ```
   ── BLACKTEAM SESSIONS ──

   RECENT SESSIONS
   | ID | Date | Topic | Status |
   |....|....|.......|........|

   Enter session ID to resume, or 'new' to start fresh.
   ```

3. **If user provides a session ID:**
   - Read the session log file from the sessions directory
   - Display the session context and last state
   - Ask: "Ready to continue from [last action]?"
   - On confirmation, load The Director persona and continue

4. **If user provides 'new':**
   - Start a fresh /blackteam session

5. **If session was interrupted:**
   - Show what was in progress
   - Offer to resume or abandon

## Session Log Format

When resuming, create/update entries in the session log:

```markdown
### [TIME] - [ACTION]
[Description of what happened]
```

## Auto-Logging Instructions

**IMPORTANT:** When running ANY /blackteam session, automatically log to the sessions directory:

1. **On Session Start:**
   - Generate Session ID: `BT-S-YYYY-NNN`
   - Create session file: `YYYY-MM-DD_topic-slug.md`
   - Add entry to SESSION_INDEX.md

2. **During Session:**
   - Log major actions with timestamps
   - Update status as work progresses

3. **On Session End:**
   - Mark status as 'completed' or 'interrupted'
   - Update SESSION_INDEX.md

## Session File Template

```markdown
# BlackTeam Session Log

## Session Metadata
- **Session ID:** BT-S-YYYY-NNN
- **Topic:** [Short descriptive title]
- **Started:** YYYY-MM-DD HH:MM
- **Status:** active | completed | interrupted
- **Project ID:** BT-YYYY-NNN (if applicable)

## Description
[2-3 sentence description of what this session is about]

## Participants
- [List of personas involved]

## Session Log

### HH:MM - [Action Title]
[Description]

## Deliverables
- [ ] Item 1
- [ ] Item 2

## Notes
[Any additional context]

---
*Session managed by The Director*
```

## Quick Commands

- `/resume_blackteam` - Show session list
- `/resume_blackteam [session-id]` - Resume specific session
- `/resume_blackteam new` - Start new session
- `/resume_blackteam status` - Show active sessions only

Arguments: $ARGUMENTS
