#!/bin/bash
# Session Memory Saver for Claude Code
# Triggered on session exit (Stop hook)
# Works with or without jq installed

MEMORY_DIR="$HOME/.claude/session-memory"
PROJECTS_DIR="$HOME/.claude/projects"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
SESSION_FILE="$MEMORY_DIR/session_$TIMESTAMP.md"

mkdir -p "$MEMORY_DIR"

# Get the most recent session file
LATEST_SESSION=$(find "$PROJECTS_DIR" -name "*.jsonl" -type f -printf '%T@ %p\n' 2>/dev/null | sort -rn | head -1 | cut -d' ' -f2-)

if [ -z "$LATEST_SESSION" ]; then
    echo "No session found to save"
    exit 0
fi

SESSION_ID=$(basename "$LATEST_SESSION" .jsonl)
SESSION_DIR=$(dirname "$LATEST_SESSION")
PROJECT_NAME=$(basename "$SESSION_DIR")

# Function to extract JSON value without jq
extract_summary() {
    grep -oP '"summary"\s*:\s*"\K[^"]+' 2>/dev/null || true
}

extract_user_content() {
    grep -oP '"content"\s*:\s*"\K[^"]{1,500}' 2>/dev/null | head -20 || true
}

# Extract session summaries and key info
{
    echo "# Claude Session Memory"
    echo ""
    echo "**Session ID:** $SESSION_ID"
    echo "**Project:** $PROJECT_NAME"
    echo "**Saved:** $(date '+%Y-%m-%d %H:%M:%S')"
    echo "**Source:** $LATEST_SESSION"
    echo ""
    echo "---"
    echo ""
    echo "## Session Summaries"
    echo ""

    # Extract summary lines from the jsonl file
    if [ -f "$LATEST_SESSION" ]; then
        grep '"type":"summary"' "$LATEST_SESSION" 2>/dev/null | \
        extract_summary | \
        sort -u | \
        while read -r summary; do
            if [ -n "$summary" ]; then
                echo "- $summary"
            fi
        done
    fi

    echo ""
    echo "---"
    echo ""
    echo "## Key Topics Discussed"
    echo ""

    # Extract unique tool uses to understand what was done
    if [ -f "$LATEST_SESSION" ]; then
        grep -oP '"name"\s*:\s*"\K(Read|Write|Edit|Bash|Glob|Grep)[^"]*' "$LATEST_SESSION" 2>/dev/null | \
        sort | uniq -c | sort -rn | head -10 | \
        while read -r count tool; do
            echo "- Used **$tool** ($count times)"
        done
    fi

    echo ""
    echo "---"
    echo ""
    echo "## Files Modified"
    echo ""

    # Extract file paths that were written or edited
    if [ -f "$LATEST_SESSION" ]; then
        grep -oP '"file_path"\s*:\s*"\K[^"]+' "$LATEST_SESSION" 2>/dev/null | \
        sort -u | \
        while read -r filepath; do
            if [ -n "$filepath" ]; then
                echo "- \`$filepath\`"
            fi
        done
    fi

    echo ""
    echo "---"
    echo ""
    echo "## Quick Resume"
    echo ""
    echo "To resume this session:"
    echo "\`\`\`bash"
    echo "claude --resume $SESSION_ID"
    echo "\`\`\`"
    echo ""
    echo "To view session memory:"
    echo "\`\`\`bash"
    echo "cat $SESSION_FILE"
    echo "\`\`\`"

} > "$SESSION_FILE"

# Also create/update a latest session symlink
ln -sf "$SESSION_FILE" "$MEMORY_DIR/latest_session.md"

# Create an index of all sessions
INDEX_FILE="$MEMORY_DIR/INDEX.md"
{
    echo "# Session Memory Index"
    echo ""
    echo "**Last Updated:** $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    echo "## Recent Sessions"
    echo ""
    echo "| Date | Session ID | File |"
    echo "|------|------------|------|"

    ls -1t "$MEMORY_DIR"/session_*.md 2>/dev/null | head -50 | while read -r file; do
        fname=$(basename "$file")
        # Extract date from filename
        session_date=$(echo "$fname" | sed 's/session_\([0-9-]*\)_.*/\1/')
        # Get session ID from the file
        sid=$(grep "Session ID:" "$file" 2>/dev/null | head -1 | sed 's/.*\*\*Session ID:\*\* //')
        echo "| $session_date | \`${sid:-unknown}\` | [$fname]($fname) |"
    done

    echo ""
    echo "---"
    echo ""
    echo "## Usage"
    echo ""
    echo "Sessions are automatically saved when you exit Claude Code."
    echo ""
    echo "**View latest session:**"
    echo "\`\`\`bash"
    echo "cat ~/.claude/session-memory/latest_session.md"
    echo "\`\`\`"
    echo ""
    echo "**Resume a session:**"
    echo "\`\`\`bash"
    echo "claude --resume <session-id>"
    echo "\`\`\`"

} > "$INDEX_FILE"

echo "Session saved to: $SESSION_FILE"
