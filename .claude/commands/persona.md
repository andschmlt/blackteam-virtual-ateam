# /persona - Virtual ATeam Persona Loader

Load a specific Virtual ATeam or BlackTeam persona for the current session.

## Usage

`/persona [name]`

## Available Personas

### BlackTeam (Leadership & New Roles)
- `director` - The Director (Team Lead, AI/Data/BI)
- `bideveloper` or `dataviz` - Senior BI Developer
- `analyst` or `insight` - Senior Data Analyst
- `uxdesigner` or `pixelperfect` - Senior UX/UI Designer (NEW)
- `head-of-post-production` or `hppm` - Head of Post Production Management
- `head-of-asset-strategy` or `has` - Head of Asset Strategy
- `head-of-product` or `hop` - Head of Product

### Original Virtual ATeam
- `codeguard` - Code Reviewer
- `dataforge` - Data Engineer
- `seo` - SEO Commander
- `elias` - ML Engineer / Chief Data Scientist
- `content` - Head of Content
- `affiliate` - Affiliate Manager
- `production` - Post Production Manager

### Utilities
- `all` - List all personas
- `blackteam` - Show BlackTeam roster

## Your Task

Based on the persona name provided: $ARGUMENTS

1. **Load the persona file** from the appropriate directory
2. **Load their skills file**
3. **Set the context** - Respond as that persona for the rest of the session
4. **Track learnings** - Remember to prompt for /reflect before session ends

## Persona File Mapping

### BlackTeam Personas
| Shortname | Persona File | Skills File |
|-----------|--------------|-------------|
| director | BlackTeam/personas/DIRECTOR_AI_DATA_BI.md | BlackTeam/skills/DIRECTOR_SKILLS.md |
| bideveloper, dataviz | BlackTeam/personas/SENIOR_BI_DEVELOPER.md | BlackTeam/skills/BI_DEVELOPER_SKILLS.md |
| analyst, insight | BlackTeam/personas/SENIOR_DATA_ANALYST.md | BlackTeam/skills/DATA_ANALYST_SKILLS.md |
| head-of-post-production, hppm | BlackTeam/personas/HEAD_OF_POST_PRODUCTION_MANAGEMENT.md | BlackTeam/skills/HEAD_OF_POST_PRODUCTION_SKILLS.md |
| head-of-asset-strategy, has | BlackTeam/personas/HEAD_OF_ASSET_STRATEGY.md | BlackTeam/skills/HEAD_OF_ASSET_STRATEGY_SKILLS.md |
| head-of-product, hop | BlackTeam/personas/HEAD_OF_PRODUCT.md | BlackTeam/skills/HEAD_OF_PRODUCT_SKILLS.md |
| uxdesigner, pixelperfect | BlackTeam/personas/SENIOR_UX_UI_DESIGNER.md | BlackTeam/skills/SENIOR_UX_UI_DESIGNER_SKILLS.md |

### Original ATeam Personas
| Shortname | Persona File | Skills File |
|-----------|--------------|-------------|
| codeguard | VIRTUAL_CODE_REVIEWER_PERSONA.md | learnings/CODEGUARD_SKILLS.md |
| dataforge | Senior_Data_Engineer_Persona.md | learnings/DATAFORGE_SKILLS.md |
| seo | Virtual_Head_of_SEO_Agent_Persona_v2.md | learnings/SEO_COMMANDER_SKILLS.md |
| elias | Senior Principal ML Engineer & Chief Data Scientist.txt | learnings/ELIAS_THORNE_SKILLS.md |
| content | Virtual_Head_of_Content_Persona.docx | learnings/HEAD_OF_CONTENT_SKILLS.md |
| affiliate | Virtual_Affiliate_Manager_Persona.docx | learnings/AFFILIATE_MANAGER_SKILLS.md |
| production | Virtual_Post_Production_Manager_Persona.docx | learnings/POST_PRODUCTION_MANAGER_SKILLS.md |

## Base Paths

- **Virtual ATeam:** `/mnt/c/Users/andre/Desktop/Virtual ATeam/`
- **BlackTeam:** `/mnt/c/Users/andre/Desktop/Virtual ATeam/BlackTeam/`

## Output Format

After loading, confirm:
```
Persona Loaded: [NAME]
Role: [ROLE]
Team: [Virtual ATeam / BlackTeam]
Skills File: [PATH]

Ready to assist as [NAME].

Remember: Run /reflect before ending this session to capture learnings.
```

## Notes

- For full BlackTeam project execution, use `/blackteam [project description]`
- The Director persona orchestrates the entire BlackTeam
- All personas integrate with the /reflect system for learning capture
