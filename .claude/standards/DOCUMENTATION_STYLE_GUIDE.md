# Documentation Style Guide

**Version:** 1.0
**Updated:** 2026-02-03
**Purpose:** Ensure consistent documentation across all workspace files

---

## General Principles

1. **Clarity over brevity** - Be clear, even if it means more words
2. **Consistency** - Follow these patterns everywhere
3. **Actionable** - Documentation should enable action
4. **Maintainable** - Easy to update and keep current

---

## File Structure

### Standard Document Header

Every markdown file should start with:

```markdown
# [Document Title]

**Version:** [X.Y]
**Updated:** [YYYY-MM-DD]
**Purpose:** [One-line description]

---
```

### Section Organization

Use this hierarchy:

```markdown
# Title (H1) - One per document

## Major Section (H2)

### Subsection (H3)

#### Detail (H4) - Use sparingly

##### Rarely needed (H5)
```

---

## Formatting Standards

### Headers

- **H1 (#)**: Document title only, one per file
- **H2 (##)**: Major sections
- **H3 (###)**: Subsections
- **H4 (####)**: Details within subsections

**Good:**
```markdown
# API Documentation
## Authentication
### OAuth Flow
#### Token Refresh
```

**Bad:**
```markdown
# API Documentation
# Authentication  <!-- Wrong: multiple H1s -->
#### OAuth Flow   <!-- Wrong: skipped levels -->
```

### Lists

**Unordered lists** for items without sequence:
```markdown
- Item one
- Item two
  - Sub-item (2 spaces indent)
```

**Ordered lists** for sequential steps:
```markdown
1. First step
2. Second step
   1. Sub-step (3 spaces indent)
```

**Definition-style** for key-value pairs:
```markdown
**Term:** Definition here
**Another term:** Another definition
```

### Code Blocks

Always specify the language:

```markdown
```python
def example():
    pass
```
```

```markdown
```bash
echo "Hello"
```
```

```markdown
```json
{"key": "value"}
```
```

For inline code, use single backticks: `code here`

### Tables

Use consistent alignment:

```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |
| Data 4   | Data 5   | Data 6   |
```

- Left-align text columns
- Right-align number columns (when possible)
- Keep headers short

### Emphasis

- **Bold** for important terms, UI elements, warnings
- *Italic* for introducing new terms, book/article titles
- `Code` for commands, file names, variable names
- ~~Strikethrough~~ for deprecated items

---

## Content Patterns

### Rule Boxes

For critical rules, use ASCII boxes:

```markdown
┌─────────────────────────────────────────────────────────────────┐
│  RULE TITLE                                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Rule content here                                               │
│                                                                  │
│  ❌ DON'T: [Bad practice]                                       │
│  ✅ DO: [Good practice]                                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Status Indicators

Use consistent symbols:

| Symbol | Meaning |
|--------|---------|
| ✅ | Complete, passed, approved |
| ❌ | Failed, rejected, don't do |
| ⚠️ | Warning, caution |
| ⛔ | Critical, blocking |
| ☐ | Unchecked checkbox |
| ☑ | Checked checkbox |
| 🔄 | In progress, pending |
| 📁 | Directory/folder |
| 📄 | File |

### Checklists

```markdown
- [ ] Unchecked item
- [x] Checked item
```

Or with symbols:
```markdown
☐ Unchecked item
☑ Checked item
```

### Callouts

**Note:**
```markdown
> **Note:** Additional information here.
```

**Warning:**
```markdown
> **Warning:** Important caution here.
```

**Critical:**
```markdown
> **CRITICAL:** Must not ignore this.
```

---

## Naming Conventions

### Files

| Type | Convention | Example |
|------|------------|---------|
| Commands | lowercase_snake.md | blackteam.md |
| Standards | UPPER_SNAKE.md | VALIDATION_STANDARDS.md |
| Rules | RULE_NAME.md | DIRECTOR_RULES.md |
| Config | lowercase.ext | settings.json |
| Templates | Name_Template.md | FTD_Report_Template.md |

### Directories

- Use lowercase_snake_case
- Be descriptive but concise
- Examples: `commands/`, `standards/`, `blackteam/`

### Headings Within Files

- Use Title Case for H1 and H2
- Use Sentence case for H3 and below
- Example:
  ```markdown
  # Project Documentation
  ## Getting Started
  ### How to install
  ```

---

## Version History

Include at end of document if changes are tracked:

```markdown
## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1 | 2026-02-03 | Added X feature |
| 1.0 | 2026-01-15 | Initial version |
```

---

## Cross-References

### Internal Links

Reference other workspace files:
```markdown
See [TEAM_CONFIG.md](/home/andre/AS-Virtual_Team_System_v2/TEAM_CONFIG.md)
```

Or use relative when in same project:
```markdown
See [Validation Standards](../standards/VALIDATION_STANDARDS.md)
```

### Related Files Section

End documents with:
```markdown
---

## Related Files

- **FILE_NAME.md** - Brief description
- **ANOTHER_FILE.md** - Brief description
```

---

## Common Patterns

### Configuration Tables

```markdown
| Setting | Value | Description |
|---------|-------|-------------|
| `timeout` | 30s | Request timeout |
| `retries` | 3 | Max retry attempts |
```

### Command Documentation

```markdown
## Command Name

**Usage:**
```
/command [required] <optional>
```

**Arguments:**
| Argument | Required | Description |
|----------|----------|-------------|
| `required` | Yes | What it does |
| `optional` | No | What it does |

**Examples:**
```
/command value
/command value --flag
```
```

### API Documentation

```markdown
## Endpoint Name

**Method:** GET/POST/etc.
**URL:** `/api/endpoint`

**Request:**
```json
{
  "field": "value"
}
```

**Response:**
```json
{
  "result": "value"
}
```

**Errors:**
| Code | Description |
|------|-------------|
| 400 | Bad request |
| 404 | Not found |
```

---

## Anti-Patterns (Avoid These)

| Bad | Good |
|-----|------|
| Multiple H1s in one file | Single H1 at top |
| Skipping header levels | Use sequential levels |
| Inconsistent list markers | Pick one style |
| Unspecified code blocks | Always specify language |
| Walls of text | Break into sections |
| Orphan links | Verify all links work |
| Mixed date formats | Use YYYY-MM-DD |
| Ambiguous pronouns | Be explicit |

---

## Quick Reference

```
# H1 - Document title (one only)
## H2 - Major sections
### H3 - Subsections
#### H4 - Details

**Bold** for emphasis
*Italic* for terms
`code` for commands

- Bullet list
1. Numbered list

| Table | Header |
|-------|--------|
| Data  | Here   |

> Blockquote for callouts

```language
code block
```

[Link text](url)

---  (horizontal rule)
```

---

## Related Files

- **PATH_MAPPINGS.md** - File location standards
- **VALIDATION_STANDARDS.md** - Content validation
- **TEAM_CONFIG.md** - Team documentation reference

