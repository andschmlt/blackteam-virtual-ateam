# /leaderboard - Virtual ATeam Leaderboard

Display persona and human user rankings, efficiency metrics, and time saved statistics.

## Phase 0: RAG Context Loading

**Load persona roster from RAG.**

```python
from AS-Virtual_Team_System_v2.rag.rag_client import VTeamRAG
rag = VTeamRAG()
roster = rag.query("persona roster leaderboard rankings", collection_name="personas", top_k=5)
```

---

## Arguments

Arguments: $ARGUMENTS

## Usage

```
/leaderboard                    # Show both persona and human rankings
/leaderboard --personas         # Show only persona rankings
/leaderboard --humans           # Show only human user rankings
/leaderboard --all              # Show all entries (not just top 10)
/leaderboard --team BlackTeam   # Filter by team
/leaderboard --stats            # Show only system stats
/leaderboard --weekly           # Show weekly activity summary
```

---

## Execution

When `/leaderboard` is invoked, Claude MUST:

### 1. Connect to Database

```python
import sys
sys.path.insert(0, '/home/andre/AS-Virtual_Team_System_v2')
from database.db_client import ATeamDB

db = ATeamDB()
```

### 2. Fetch Leaderboard Data

```python
# Get persona leaderboard
persona_leaderboard = db.get_leaderboard(limit=20)

# Get human leaderboard
human_leaderboard = db.get_human_leaderboard(limit=20)

# Get stats
stats = db.get_stats()
```

### 3. Display Results

Format output showing both leaderboards.

---

## Full Implementation

```python
import sys
sys.path.insert(0, '/home/andre/AS-Virtual_Team_System_v2')
from database.db_client import ATeamDB

def format_duration(minutes):
    """Format minutes as Xh Ym."""
    if not minutes:
        return "0m"
    hours = int(minutes // 60)
    mins = int(minutes % 60)
    if hours > 0:
        return f"{hours}h {mins}m"
    return f"{mins}m"

def format_tokens(tokens):
    """Format token count with K/M suffix."""
    if not tokens:
        return "0"
    if tokens >= 1000000:
        return f"{tokens/1000000:.1f}M"
    if tokens >= 1000:
        return f"{tokens/1000:.1f}K"
    return str(tokens)

def display_leaderboard(limit=10, show_personas=True, show_humans=True, show_stats=True):
    db = ATeamDB()

    # Get data
    stats = db.get_stats()

    # Header
    print("\n" + "="*70)
    print("                    VIRTUAL ATEAM LEADERBOARD")
    print("="*70)

    if show_stats:
        print(f"\n📊 System Overview:")
        print(f"   Active Projects: {stats['projects_active']}")
        print(f"   Completed Projects: {stats['projects_completed']}")
        print(f"   Completed Tasks: {stats['tasks_completed']}")
        print(f"   Total Interactions: {stats['total_interactions']}")
        print(f"   Total Time Saved: {format_duration(stats['total_minutes_saved'])}")
        print(f"   Total Tokens: {stats['total_tokens_in'] + stats['total_tokens_out']:,}")

    # Persona Leaderboard
    if show_personas:
        leaderboard = db.get_leaderboard(limit=limit)
        print("\n🤖 AI PERSONA RANKINGS:")
        print("-"*70)
        print(f"{'#':>3} │ {'Persona':<10} │ {'Tasks':>6} │ {'Projects':>8} │ {'Efficiency':>10} │ {'Time Saved':>12}")
        print("-"*70)

        for i, entry in enumerate(leaderboard, 1):
            persona = entry.get('persona_code', 'N/A')
            tasks = entry.get('tasks_completed', 0) or 0
            projects = entry.get('projects_completed', 0) or 0
            efficiency = entry.get('cache_efficiency_pct', 0) or 0
            time_saved = format_duration(entry.get('total_minutes_saved', 0))

            print(f"{i:>3} │ {persona:<10} │ {tasks:>6} │ {projects:>8} │ {efficiency:>9.1f}% │ {time_saved:>12}")

        print("-"*70)

    # Human Leaderboard
    if show_humans:
        human_board = db.get_human_leaderboard(limit=limit)
        print("\n👤 HUMAN USER RANKINGS:")
        print("-"*70)
        print(f"{'#':>3} │ {'User':<12} │ {'Sessions':>8} │ {'Projects':>8} │ {'Tokens':>10} │ {'Efficiency':>10}")
        print("-"*70)

        if human_board:
            for i, entry in enumerate(human_board, 1):
                username = entry.get('username', 'N/A')[:12]
                sessions = entry.get('total_interactions', 0) or 0
                projects = entry.get('projects_completed', 0) or 0
                tokens = format_tokens((entry.get('total_tokens_in', 0) or 0) + (entry.get('total_tokens_out', 0) or 0))
                efficiency = entry.get('cache_efficiency_pct', 0) or 0

                print(f"{i:>3} │ {username:<12} │ {sessions:>8} │ {projects:>8} │ {tokens:>10} │ {efficiency:>9.1f}%")
        else:
            print("    No human activity tracked yet.")
            print("    Interactions will appear as users work with the system.")

        print("-"*70)

    print("\n📈 Efficiency = (Cached Tokens / Total Tokens) × 100")
    print("👤 Human tracking: Based on Claude Code username\n")

    db.close()

# Run
display_leaderboard()
```

---

## Options

| Option | Description |
|--------|-------------|
| `--all` | Show all entries (not just top 10) |
| `--personas` | Show only AI persona rankings |
| `--humans` | Show only human user rankings |
| `--team [name]` | Filter by BlackTeam or WhiteTeam |
| `--stats` | Show only system stats |
| `--weekly` | Show weekly activity summary |
| `--tokens` | Show token efficiency breakdown |

---

## Data Sources

### Persona Metrics

| Metric | Source | Calculation |
|--------|--------|-------------|
| Tasks Completed | `tasks` table | COUNT WHERE status='completed' |
| Projects Completed | `projects` table | COUNT WHERE status='completed' |
| Cache Efficiency | `interactions` table | (tokens_cached / (tokens_in + tokens_out)) × 100 |
| Time Saved | `tasks` table | estimated_manual_minutes - duration_minutes |

### Human Metrics

| Metric | Source | Calculation |
|--------|--------|-------------|
| Sessions | `interactions` table | COUNT per username |
| Projects Touched | `interactions` table | COUNT DISTINCT project_id |
| Total Tokens | `interactions` table | SUM(tokens_in + tokens_out) |
| Cache Efficiency | `interactions` table | (tokens_cached / total_tokens) × 100 |

---

## User Tracking

Human users are tracked by their Claude Code username. The system:

1. **Auto-creates users** on first interaction
2. **Updates last_active_at** on each session
3. **Aggregates metrics** across all sessions

To log an interaction with user tracking:

```python
db.log_interaction_with_user(
    persona_code="B-BOB",
    action_type="execute",
    summary="Completed task",
    username="andre",  # Claude Code username
    tokens_in=1000,
    tokens_out=2000,
    tokens_cached=500
)
```

---

## Database Connection

The leaderboard connects to Cloud SQL:

| Setting | Value |
|---------|-------|
| Host | 35.226.3.139 |
| Port | 5432 |
| Database | virtual_ateam_v2 |
| User | ateam_admin |

Connection is persistent and isolated from container restarts.

---

## Refresh Schedule

The leaderboard views refresh:
- **Persona leaderboard:** Materialized view, refreshes on query
- **Human leaderboard:** Regular view, always current

---

*Leaderboard tracks both AI persona and human user efficiency and productivity.*
