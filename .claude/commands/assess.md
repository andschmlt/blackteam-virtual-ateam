# Workspace Assessment Command

Run a comprehensive assessment of the workspace to identify issues in:
- **Code Efficiency** - Performance patterns, complexity, redundancy
- **Code Security** - OWASP Top 10, injection flaws, secrets detection
- **System Security** - File permissions, API keys, configuration exposure
- **Instruction Quality** - CLAUDE.md consistency, routing overlaps, completeness

## Phase 0: RAG Context Loading

**Load assessment baselines and prior findings from RAG.**

```python
from AS-Virtual_Team_System_v2.rag.rag_client import VTeamRAG
rag = VTeamRAG()
context = rag.query("workspace assessment code security standards", top_k=5)
learnings = rag.query("assessment findings corrections", collection_name="learnings", top_k=3)
```

---

## Usage

```
/assess           # Full workspace assessment
/assess code      # Code efficiency + security only
/assess security  # Security categories only
/assess --quick   # Fast scan with limited file sampling
```

## How to Run

**Option 1: CLI Script (Standalone)**
```bash
cd ~/workspace-assessment-dashboard
npm install  # First time only
npx tsx scripts/assess-command.ts
```

**Option 2: Full Dashboard (Recommended)**
```bash
cd ~/workspace-assessment-dashboard
npm install  # First time only
npm run dev  # Starts server on localhost:3001 and UI on localhost:3000
```

Then open http://localhost:3000 in your browser.

## Scoring System

### Category Weights
| Category | Weight |
|----------|--------|
| Code Security | 35% |
| System Security | 30% |
| Code Efficiency | 20% |
| Instruction Quality | 15% |

### Severity Deductions
| Severity | Points |
|----------|--------|
| CRITICAL | -25 |
| HIGH | -15 |
| MEDIUM | -8 |
| LOW | -3 |
| INFO | 0 |

### Letter Grades
| Score | Grade |
|-------|-------|
| 93+ | A |
| 90-92 | A- |
| 87-89 | B+ |
| 83-86 | B |
| 80-82 | B- |
| 77-79 | C+ |
| 73-76 | C |
| 70-72 | C- |
| 60-69 | D |
| <60 | F |

## Known Issues to Watch

Based on previous scans of this workspace:
- **CRITICAL**: 0777 permissions on BlackTeam files
- **HIGH**: Routing keyword overlaps in CLAUDE.md
- **HIGH**: Hardcoded API keys in configuration files
- **MEDIUM**: Version drift between CLAUDE.md files
- **MEDIUM**: Missing sections in instruction files

## Project Location

```
~/workspace-assessment-dashboard/
```

## Tech Stack

- Frontend: React 18 + TypeScript + Vite + shadcn/ui
- Backend: Express.js + TypeScript
- Database: PostgreSQL + Drizzle ORM
- Charts: Recharts

---

*Project ID: BT-2026-009*
*Created: January 2026*
