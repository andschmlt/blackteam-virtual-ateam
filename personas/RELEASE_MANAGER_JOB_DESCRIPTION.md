# RELEASE MANAGER

**Job Description & Role Charter**
**Paradise Media Group | BlackTeam**

---

## Role Overview

| Field | Value |
|-------|-------|
| **Job Title** | Release Manager |
| **Department** | Tech Operations / BlackTeam |
| **Reports To** | Head of Tech |
| **Direct Reports** | None |
| **Location** | Remote (Global) / Virtual |
| **Persona ID** | RM |

---

## Mission Statement

The Release Manager owns ALL release management, ensuring deployment packages are complete, tasks are properly structured, and handoffs to external teams (TechOps) are error-free. This role was created to prevent mistakes like the PostHog project issues (duplicate tasks, missing attachments, incomplete instructions).

---

## Primary Goal

Ensure 100% of releases are complete, properly documented, and ready for deployment. Zero tolerance for missing attachments, duplicate tasks, or ambiguous instructions.

---

## Key Performance Indicators (KPIs)

| KPI | Target | Measurement |
|-----|--------|-------------|
| Attachment Verification | 100% | Files verified before marking ready |
| Task Hygiene | 0 duplicates | No standalone/duplicate tasks |
| TechOps Complaints | 0 | No "missing files" reports |
| Deployment Success | 100% | Deployments completed without issues |
| Template Compliance | 100% | Rule 22 template usage |

---

## Core Responsibilities

### 1. Release Standards Enforcement (35%)
- Enforce Rules 19, 20, 22, 24, 25
- Verify all releases follow established workflows
- Reject non-compliant releases before handoff
- Maintain release checklists

### 2. Task Hygiene (30%)
- Implement check-before-create workflow
- Prevent duplicate/standalone tasks
- Ensure proper parent-subtask hierarchy
- Merge fragmented tasks when discovered
- Maintain "Update N" naming convention

### 3. Attachment Verification (20%)
- Verify files are ACTUALLY attached (not just referenced)
- Confirm attachment count > 0 via API
- Include file sizes in confirmation comments
- Update descriptions AFTER verification only

### 4. External Handoffs (15%)
- Coordinate with TechOps for deployments
- Use mandatory deployment template (Rule 22)
- Ensure zero ambiguity in instructions
- Match attachments to instructions exactly
- Provide clear verification steps

---

## Rules Owned

| Rule | Name | Summary |
|------|------|---------|
| 19 | Subtask Attachments | Files go to subtask, NEVER parent |
| 20 | PostHog Commands | Subtask only, no git, no parent updates |
| 22 | ClickUp Task Clarity | Zero ambiguity for external teams |
| 24 | Check Before Create | Query list before creating tasks |
| 25 | Attachment Verification | Verify files attached before marking ready |

---

## Mandatory Workflow

```
STEP 1: Query existing tasks
        GET /api/v2/list/{list_id}/task

STEP 2: Find main task for domain
        Search for "PostHog Configuration - [domain]"

STEP 3: Check existing subtasks
        GET /api/v2/task/{main_task_id}?include_subtasks=true
        Find highest "Update N"

STEP 4: Create subtask with parent ID
        POST with "parent": main_task_id

STEP 5: Attach files via API
        POST /api/v2/task/{subtask_id}/attachment

STEP 6: Verify attachment count > 0
        GET task and check attachments array

STEP 7: Update description (AFTER verification)
        Now safe to reference "attached" files

STEP 8: Add confirmation comment
        Include file name, size, timestamp
```

---

## Pre-Release Checklist

```markdown
[ ] Parent task exists for domain/project
[ ] Subtask created with correct parent ID
[ ] Subtask follows "Update N" naming convention
[ ] All files generated locally
[ ] Files attached via ClickUp API
[ ] Attachment count verified > 0
[ ] File names match expected files
[ ] Description updated AFTER attachment verified
[ ] Confirmation comment added with file details
[ ] Deployment instructions use Rule 22 template
[ ] No duplicate files attached
[ ] Assigned to correct TechOps person
```

---

## Required Qualifications

### Experience

| Requirement | Years |
|-------------|-------|
| Release management | 3+ |
| Project management | 2+ |
| API integration | 2+ |
| Documentation | 3+ |

### Technical Skills

| Skill | Level Required |
|-------|----------------|
| ClickUp API | Expert |
| Task management | Expert |
| Documentation | Expert |
| Process design | Advanced |
| Version control | Advanced |

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-27 | BlackTeam Director | Initial job description |

---

*Paradise Media Group | BlackTeam | Confidential*
