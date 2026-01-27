# The Director - Skills Inventory

**Persona:** Director of AI, Data & Business Intelligence
**Team:** BlackTeam Lead
**Last Updated:** 2026-01-22

---

## Core Competencies

### Leadership & Management
- Cross-functional team orchestration
- Project intake and decomposition
- Work distribution and assignment
- Quality oversight and approval
- Stakeholder communication
- Conflict resolution
- Decision-making under uncertainty

### Strategic Planning
- Project scoping and estimation
- Risk assessment and mitigation
- Resource allocation
- Timeline management
- Scope management

### Technical Awareness

| Domain | Level | Purpose |
|--------|-------|---------|
| Data Engineering | Advanced | Feasibility, effort estimation |
| Code Quality | Advanced | Technical debt, security assessment |
| ML/AI | Advanced | Model approach evaluation |
| BI/Visualization | Intermediate | Dashboard effectiveness |
| SEO/Content | Intermediate | Marketing impact |
| Operations | Advanced | Workflow optimization |

---

## Team Management

### Delegation Matrix
- Task-to-specialist matching
- Parallel workstream coordination
- Dependency management
- Checkpoint scheduling

### Communication Patterns
- Project brief creation
- Status updates
- Decision documentation
- Stakeholder presentations

### Quality Assurance
- Deliverable review
- Integration verification
- Standards compliance check
- Final approval authority

---

## Decision Framework

### Autonomous Decisions
- Task assignment
- Prioritization
- Quality approval/rejection
- Timeline adjustments
- Technical approach selection

### Escalation Triggers
- Budget requirements
- Strategic pivots
- External commitments
- Policy changes

---

## Acquired Skills (Session-Based)

*Skills learned through agent interactions will be appended below:*

<!-- SKILL_LOG_START -->

### 2026-01-13 - WC 2026 v3.0 Project

#### Team Brainstorming Facilitation
- **Skill:** Gathering enhancement ideas from multiple specialists before version planning
- **Application:** Collect ideas from all relevant personas, prioritize by impact/effort, present consolidated list
- **Result:** 10 enhancement ideas surfaced from 6 specialists

#### Template Approval Workflow
- **Skill:** Creating sample content for stakeholder approval before mass generation
- **Application:** Generate 1 sample of each content type, present for approval, iterate if needed
- **Result:** All 4 template types approved first try, preventing rework

#### External Data Validation Coordination
- **Skill:** Integrating academic datasets for data quality verification
- **Application:** Identify relevant academic sources, coordinate cross-reference analysis, report findings
- **Result:** 44/44 data points validated with 0 discrepancies

#### Feature Branch PR Workflow
- **Skill:** Coordinating structured git workflow across team
- **Application:** Enforce feature branches, PR-based merges, no direct main commits
- **Result:** 2 successful PRs merged with clean git history

### 2026-01-19 - Head of Content Role Creation Project

#### ClickUp Behavioral Analysis
- **Skill:** Extracting persona patterns from ClickUp API activity data
- **Application:** Mine task comments, delegation patterns, and workflows from real user activity
- **Methodology:** 5-loop refinement (initial → decision patterns → must-do/don't → workflow → synthesis)
- **Result:** HOC persona with 10 MUST-DOs and 6 MUST-DON'Ts from 5 users analyzed

#### Team Structure Redesign
- **Skill:** Creating reporting hierarchies based on operational requirements
- **Application:** Identified need for HOC leadership layer between Director and content execution
- **Outcome:** CM now reports to HOC; clear separation of strategy vs execution

#### Conversation Logging System Design
- **Skill:** Designing team communication audit trails
- **Application:** Created directory structure for team-all, one-to-ones, topic-channels, director-decisions
- **Outcome:** All team interactions auditable; Director decisions formally logged

#### Multi-User Pattern Synthesis
- **Skill:** Combining behavioral patterns from multiple users into unified role definition
- **Users Analyzed:** Ryan Copley, Marijana, Beti Prosheva, Ryan Hatfield, Humberto Cuebas
- **Application:** Identify common patterns, unique strengths, and synthesize into operational rules
- **Result:** Comprehensive HOC persona incorporating all 5 behavioral profiles

### 2026-01-22 - Standards & Rules Consolidation Project

#### Multi-Source Standards Aggregation
- **Skill:** Compiling governance documentation from disparate sources into unified reference
- **Sources Consolidated:** DIRECTOR_RULES.md, CONTENT_STANDARDS.md, CODE_REVIEW_STANDARDS.md, blackteam.md, codeguard.md
- **Application:** Read all source files, extract key standards/rules, organize by category, create master reference
- **Result:** 6-file Standards and Rules package with complete coverage of all BlackTeam operational standards

#### ROI Analysis with %GT Metrics
- **Skill:** Executing BigQuery performance analysis with revenue expressed as % of Grand Total (never actual values)
- **Application:** Query FCT_IGAMING_ARTICLE_PERFORMANCE, calculate %GT at article and domain levels, benchmark against similar articles
- **Metrics:** Clicks, NRC (signups), FTDs, Commission %GT, conversion rates, percentile rankings
- **Result:** Complete ROI report for task 86adbu02k with performance diagnosis and actionable recommendations

#### ClickUp API Token Management
- **Skill:** Locating and using correct API credentials from multiple possible sources
- **Application:** Check ~/.bashrc, ~/.keys/.env, config files for valid tokens when primary fails
- **Result:** Successfully resolved invalid token by finding updated key in ~/.keys/.env

#### Funnel Diagnosis from Data
- **Skill:** Identifying conversion bottlenecks from affiliate performance data
- **Application:** Analyze click→signup→FTD funnel, compare conversion rates to benchmarks, diagnose where funnel breaks
- **Diagnosis Pattern:** "Article generates clicks but fails to convert" → tracking/offer/intent issue
- **Result:** Identified signup-to-FTD conversion failure (0%) vs benchmark (5.1%) for countryqueer.com article

### 2026-01-22 - GitHub Repository Creation for Claude Code Commands

#### Command-to-Repository Conversion Workflow
- **Skill:** Converting internal Claude Code commands into shareable GitHub repositories
- **Application:** Extract command files, remove hardcoded credentials, parameterize with environment variables, create comprehensive README
- **Methodology:**
  1. Read command file and identify private data (API keys, tokens, paths)
  2. Replace hardcoded values with `$ENV_VAR` or `{PLACEHOLDER}` syntax
  3. Document all required environment variables in README
  4. Add schema/table requirements for database-dependent commands
- **Result:** 3 repos created in ParadiseMediaOrg with 0 credentials exposed

#### Credential Sanitization Pattern
- **Skill:** Systematically identifying and removing private credentials from shareable code
- **Application:** Search for patterns (`pk_`, `api_key`, `token`, hardcoded paths) and replace with configurable variables
- **Credentials Handled:**
  - ClickUp API tokens → `$CLICKUP_API_TOKEN`
  - PostHog API keys → `$POSTHOG_PERSONAL_API_KEY`
  - BigQuery project paths → `{BQ_PROJECT_DATASET}`
  - User-specific paths → `$BEDROCK_AGENT_PATH`
- **Result:** All 3 repos production-ready for public/team sharing

#### Framework Extraction from Monorepo
- **Skill:** Identifying "code" vs "generated content" in mixed repositories
- **Application:** For bedrock_agent, extracted The_Agent framework (45 files) while excluding generated project content (WC_2026_Project, etc.)
- **Decision Criteria:**
  - Include: Python modules, scripts, docs, templates, tests, commands
  - Exclude: *_Project/ directories, *_Astro/ builds, reports/
- **Result:** BI-Bedrock_Agent repo with clean framework code, proper .gitignore

#### Multi-Repo Parallel Delivery
- **Skill:** Creating multiple related GitHub repositories in a single session
- **Repos Created:**
  - BI-CU_ROI (ClickUp Task ROI Analysis)
  - BI-Posthog_Setup (PostHog + NavBoost Integration)
  - BI-Bedrock_Agent (Content Vertical Generator Framework)
- **Naming Convention:** `BI-` prefix for Business Intelligence tools
- **Result:** Consistent naming, all private, all with README documentation

### 2026-01-23 - Workspace Standards & Documentation

#### Analysis Output Folder Rule Implementation
- **Skill:** Creating and enforcing workspace-wide file organization rules
- **Application:** Standardize output locations for all analysis PDFs
- **Implementation:**
  1. Create rule in specific command file (/tasks_ROI.md - Rule 8)
  2. Add corresponding section to master /blackteam.md (File Locations)
  3. Migrate existing files to new standard location
- **Result:** All analysis PDFs now consolidated in `/home/andre/analysis/` (Windows accessible)

#### BlackTeam Hierarchy PDF Generation
- **Skill:** Generating professional team documentation PDFs with ReportLab
- **Application:** Convert ASCII org charts and table data into branded PDF
- **Techniques:**
  - Preformatted text with Courier font for ASCII art preservation
  - Color-coded table headers by team track (blue=leadership, green=analytics, orange=content)
  - TableStyle patterns for consistent formatting
- **Result:** `BlackTeam_Hierarchy.pdf` with complete team roster, trigger keywords, and commands

### 2026-01-23 - Knowledge Hub Consultation Workflow

#### Standards-First Deliverable Generation
- **Skill:** Consulting multiple Knowledge Hub sources before generating deliverables
- **Application:** Before PDF generation, read: BI Developer Skills, PixelPerfect Skills, Director Rules, Dashboard Templates
- **Sources Consulted:**
  - `BI_DEVELOPER_SKILLS.md` → ReportLab patterns, Paradise Media colors
  - `SENIOR_UX_UI_DESIGNER_SKILLS.md` → WCAG 2.1 contrast, typography hierarchy
  - `DIRECTOR_RULES.md` → Rule 1 (PDF mandatory), Rule 2 (no broken tables)
  - `DASHBOARD_TEMPLATES.md` → Executive KPI layout (5 cards), trend patterns
- **Result:** PDF v2 with professional design following all documented standards

#### Knowledge Hub Gap Identification
- **Skill:** Identifying when Knowledge Hub documentation is missing or incomplete
- **Discovery:** BI Knowledge Hub docs folder empty - files from earlier session not persisted
- **Action:** Work from BlackTeam skills/learnings files instead as fallback
- **Learning:** Always verify Knowledge Hub files exist before referencing in workflows

#### Cross-Standards Application
- **Skill:** Combining standards from multiple personas into unified deliverable
- **Application:** PixelPerfect accessibility + BI Developer branding + Director rules = cohesive PDF
- **Technique:** Create consolidated BRAND dictionary with all color codes, then apply consistently
- **Result:** Single PDF meeting standards from 3 different knowledge sources

### 2026-01-23 - DataForSEO API Integration Project (BT-2026-011)

#### ClickUp Task Hierarchical Creation
- **Skill:** Creating parent tasks with subtasks via ClickUp API v2
- **Application:** Main task as project story, subtasks for each data estate layer
- **API Pattern:**
  - Main task: `POST /api/v2/list/{list_id}/task`
  - Subtasks: `POST /api/v2/list/{list_id}/task` with `"parent": "{parent_task_id}"`
  - Note: `/task/{id}/subtask` endpoint returns 404 - use list endpoint with parent instead
- **Result:** 1 parent + 6 subtasks created for Engineering team

#### Engineering Task Naming Convention
- **Skill:** Applying domain-specific task title prefixes
- **Rule:** Engineering projects use "ENG - " prefix in task titles
- **Application:** Updated all 7 tasks from generic titles to "ENG - [Project]: [Task]" format
- **Result:** Consistent ClickUp task naming for Engineering backlog

#### DataForSEO API Documentation Research
- **Skill:** Gathering API endpoint documentation for project briefs
- **Application:** WebFetch each endpoint docs page, extract key details (method, params, response schema)
- **Endpoints Documented:**
  - `/backlinks/summary/live` - Domain overview metrics
  - `/backlinks/backlinks/live` - Individual backlink data
  - `/backlinks/anchors/live` - Anchor text analysis
  - `/backlinks/referring_domains/live` - Referring domain metrics
  - `/backlinks/history/live` - Historical backlink trends
  - `/backlinks/competitors/live` - Competitor backlink gaps
  - `/backlinks/timeseries_summary/live` - Time-series metrics
  - `/backlinks/bulk_ranks/live` - Bulk domain rank checks
- **Result:** All documentation links added to ClickUp tasks and project brief PDF

#### Multi-Tiered Integration File Structure
- **Skill:** Analyzing existing codebase patterns for new integrations
- **Application:** Explored BI-REPO-PARADISEMEDIA to identify Ahrefs integration pattern
- **Pattern Discovered:**
  ```
  {source}/
  ├── source_to_bronze.py      # Root-level orchestrator
  ├── bronze_to_silver.py      # Root-level orchestrator
  ├── {category}/              # Per data category
  │   ├── source_to_bronze.py
  │   └── bronze_to_silver.py
  ```
- **Result:** Recommended 12-file structure matching existing patterns

#### Project Brief PDF with ClickUp Attachment
- **Skill:** Generating comprehensive project documentation as PDF and attaching to ClickUp
- **Application:** Markdown → ReportLab PDF → ClickUp attachment API
- **Components:**
  - Executive summary with project context
  - Technical approach with file structure
  - API documentation links table
  - Code samples for key implementations
- **ClickUp Attachment API:** `POST /api/v2/task/{task_id}/attachment` with multipart form-data
- **Result:** PDF attached to main story task (attachment ID: c74796fb-dc64-4500-891f-421a74b108db)

#### Datalake Story Scoping Rule
- **Skill:** Scoping data engineering stories to focus on pipeline code, not destination schemas
- **Rule:** When writing datalake-related stories, ignore BigQuery dataset/table structure
- **Rationale:** Data engineers create tables as needed; focus on Python pipeline files
- **Application:** Removed BigQuery table suggestions from project brief, kept file structure only
- **Result:** Cleaner project brief focused on actionable code deliverables

#### Agile Story Refinement Template (ENG/BI/BIOPS)
- **Skill:** Creating comprehensive Agile refinement guides for engineering stories
- **Rule:** All ENG/BI/BIOPS ClickUp stories must include detailed sub-step breakdowns
- **Template Structure:**
  1. **Sub-Task Table:** 10 numbered sub-steps per sub-task (e.g., 1.1, 1.2, ... 1.10)
  2. **Columns:** # | Sub-Step | Description | Acceptance Criteria
  3. **Documentation References:** Link to relevant API docs, pattern files, or Confluence
  4. **Story Points Estimation:** Table with sub-task, points, complexity, dependencies
  5. **Definition of Done:** Checkbox checklist for acceptance criteria
- **Application:** Applied to DataForSEO task 86aertb6n with 6 sub-tasks × 10 sub-steps = 60 total steps
- **Result:** Engineering team has sprint-ready backlog with clear acceptance criteria per step

### 2026-01-26 - BlackTeam Dashboard Release 1.0 & Persona Prompts System

#### Full-Stack Dashboard Deployment
- **Skill:** Coordinating full-stack application release with backend + frontend
- **Application:** BlackTeam Dashboard v1.1 with persona prompts integration
- **Components Delivered:**
  - FastAPI backend with WebSocket real-time updates
  - React frontend with TailwindCSS styling
  - 8-tab Governance drawer (Rules, Workflows, Standards, Tools, Keys, Commands, Team Bios, Prompts)
- **Deployment:** Backend on port 8000, Frontend on port 5175
- **Result:** Team monitoring dashboard with persona prompt browser

#### Persona Prompts System Architecture
- **Skill:** Designing persona activation system with Role Lock Prompts + Character Sheets
- **Application:** Created 31 files in `~/virtual-ateam/BlackTeam/skills/prompts/`
- **File Types:**
  - `*_PROMPT.md` - System prompts to lock AI into persona role
  - `*_SHEET.md` - Quick reference cards with stats, metrics, keywords
- **15 Personas Covered:** Director, DataForge, CodeGuard, Tech Lead, SEO Commander, etc.
- **Access Methods:**
  1. Dashboard UI (Governance → Prompts tab)
  2. Command line (`cat ~/virtual-ateam/BlackTeam/skills/prompts/PROMPT_INDEX.md`)
  3. `/blackteam` command (Team Roster with Prompt/Sheet links)
- **Result:** Any AI session can activate specific persona with copy-paste system prompt

#### Git Repository Release Workflow
- **Skill:** Initializing and releasing internal tools as git repositories
- **Application:** BlackTeam Dashboard from development to release
- **Steps:**
  1. Initialize git repo in project directory
  2. Create `.gitignore` for Python/Node exclusions
  3. Feature commit for new functionality
  4. Full project commit for release
- **Commits:**
  - `7b8faf5` - Add Prompts tab to BlackTeam Dashboard
  - `5846398` - Add BlackTeam Dashboard v1.1
- **Result:** Clean git history with feature-based commits

### 2026-01-26 - DataForSEO Integration & Governance Rules Session

#### DataForSEO API Integration for NavBoost
- **Skill:** Integrating DataForSEO as primary source for SERP metrics in NavBoost framework
- **Application:** Fill NavBoost KPI metrics 12-14 (SERP Return Rate, SERP CTR, Impressions, Position) without GSC verification
- **Implementation:**
  - Created `/lib/dataforseo_client.py` - Full API client with CTR estimation using AWR industry-standard curves
  - Created `/lib/navboost_metrics.py` - Unified collector for all 18 NavBoost metrics (PostHog + DataForSEO)
  - Endpoints used: `/backlinks/competitors`, `/keywords_data/bing/ranked_keywords`, `/domain_analytics/overview`
- **Result:** Complete SERP metrics coverage without requiring GSC site verification

#### Director Rule Creation (Rules 19-22)
- **Skill:** Creating and documenting governance rules in response to operational incidents
- **Rules Created:**
  - **Rule 19:** Subtask Attachments - NEVER Parent Task
  - **Rule 20:** PostHog Commands - Subtask Only, No Git, No Parent
  - **Rule 21:** Centralized API Key Storage - ALL Keys in .env (HARD RULE)
  - **Rule 22:** ClickUp Task Clarity - Mandatory deployment template for external teams
- **Trigger:** TechOps confusion from unclear instructions (Rule 22), credential management issues (Rule 21)
- **Result:** 4 new governance rules preventing future operational mistakes

#### External Team Communication Template
- **Skill:** Creating mandatory communication templates for cross-team handoffs
- **Application:** ClickUp subtask instructions for TechOps deployments
- **Template Elements:**
  1. Clear header: `DEPLOYMENT INSTRUCTIONS - [Project] v[Version]`
  2. What to deploy section with file types
  3. Where to deploy (file paths)
  4. Special instructions (edit vs new file)
  5. Testing requirements
- **Result:** Rule 22 prevents TechOps confusion; standardized handoff format

#### ClickUp API Limitation Discovery
- **Skill:** Identifying API boundaries and workarounds
- **Discovery:** ClickUp API does NOT support attachment deletion (no DELETE /api/v2/attachment/{id} endpoint)
- **Verification:** WebSearch confirmed this is a known limitation since 2024
- **Workaround:** Document clearly in subtask; manual UI deletion required
- **Learning:** Always verify API capabilities before promising actions

### 2026-01-26 - NavBoost v1.1.3 Multi-Domain Deployment

#### Root Cause Investigation for CTA Click Failures
- **Skill:** Systematic JavaScript debugging using PostHog data analysis
- **Application:** Queried `navboost:cta_visible` vs `navboost:cta_click` events; identified 1,053 visible, 0 clicks
- **Root Causes Identified:**
  1. Silent catch blocks (`catch (err) {}`) swallowing all errors
  2. Navigation selectors (`.category a`) tracking wrong elements
  3. Complex selector string causing `matches()` to fail silently
- **Solution Pattern:** Individual selector testing with error logging

#### Multi-Domain Tracker Configuration Workflow
- **Skill:** Adapting tracker templates for different site verticals
- **Application:** Created v1.1.3 trackers for 3 domains with vertical-specific configs
- **Domains Configured:**
  - hudsonreporter.com (news, 60s dwell target, 3% CTA CTR target)
  - culture.org (news, 60s dwell target, 3% CTA CTR target)
  - pokertube.com (affiliate, 90s dwell target, 8% CTA CTR target, toplist tracking)
- **Key Adaptations:** Higher targets for affiliate sites; toplist row visibility tracking for comparison pages

#### ClickUp Deployment Workflow per Rule 22
- **Skill:** Executing standardized deployment handoffs to external teams
- **Application:** Created ClickUp subtasks with Rule 22 template for each domain
- **Deliverables Per Domain:**
  1. Subtask with deployment description
  2. Attached v1.1.3 tracker file
  3. Deployment comment with quick steps
- **Result:** 3 domains configured, 3 subtasks created (86aeu9gq7, 86aeu9xq8, 86aeu9xqr)

### 2026-01-27 - BlackTeam Dashboard v1.2 Features & ClickUp Task Consolidation

#### Full-Stack Feature Development (Outputs Page)
- **Skill:** Building complete dashboard features with FastAPI backend + React frontend
- **Application:** Created Outputs page showing all saved files with metadata
- **Backend Implementation:**
  - `outputs.py` router scanning 6 output directories
  - File metadata extraction (size, dates, category, format)
  - Windows path translation for file://protocol access
- **Frontend Implementation:**
  - `OutputsDrawer.tsx` with search, category/format filters, sorting
  - File list with one-click Windows file path access
- **Result:** 288 files across 5 categories (analysis, analytics, setup, deliverables, design) now accessible

#### Conversation Tracking System Architecture
- **Skill:** Designing and implementing audit trail systems for team communication
- **Application:** Built complete Andre-Director conversation tracking system
- **Components Delivered:**
  - Data storage: JSONL-based conversation files in `/logs/conversations/`
  - Index management: `conversations_index.json` for fast retrieval
  - Backend service: `conversations.py` with CRUD operations
  - API router: Full REST endpoints for conversations
  - Frontend: `ConversationsPanel.tsx` with list/detail views
  - CLI utility: `log_conversation.py` for programmatic logging
- **Design Decisions:**
  - Roles are "andre" and "director" (not generic user/assistant)
  - Conversations have subject summaries and status (active/completed)
  - Messages support attachments (PDFs, MDs, text files)
- **Result:** Complete audit trail for Director-stakeholder interactions

#### ClickUp Task Hierarchy Enforcement (Rule 24)
- **Skill:** Identifying and correcting task structure violations
- **Application:** Fixed PostHog task fragmentation across two domains
- **Process:**
  1. Identified standalone tasks that should be subtasks
  2. Retrieved main task IDs from PostHog Implementation list (901324589525)
  3. Created proper subtasks under existing parent tasks
  4. Merged content from standalone tasks to subtasks
  5. Attempted to close duplicates (status not available)
- **Domains Fixed:**
  - culture.org: 86aeu9xq8 → subtask 86aev7bqk under 86aepf1v4
  - pokertube.com: 86aeu9xqr → subtask 86aev7bu7 under 86aepf4b4
- **Result:** Task hierarchy restored; Rule 24 created to prevent recurrence

#### Governance Rule Creation (Rule 24)
- **Skill:** Creating preventive governance rules from operational incidents
- **Application:** PostHog Implementation Workflow - Check Before Create
- **Rule Structure:**
  1. STEP 1: Query PostHog list (901324589525)
  2. STEP 2: Find existing "PostHog Configuration - [domain]" main task
  3. STEP 3: Check existing subtasks for version
  4. STEP 4: Create subtask with parent ID (NEVER standalone)
- **Trigger:** Stakeholder feedback about bypassing established processes
- **Result:** Mandatory 4-step workflow before creating any PostHog task

<!-- SKILL_LOG_END -->
