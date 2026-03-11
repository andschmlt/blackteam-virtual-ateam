#!/usr/bin/env python3
"""
Persona Factory v2 — Data-Driven Persona Generation

Generates 20 writer personas FROM actual style analysis cluster data.
Each persona is mapped to a real cluster and sources real journalists.

Steps:
1. Load cluster report + style profiles from Phase 4
2. Map each of 20 planned personas to best-matching cluster
3. Select source journalists from matching cluster
4. Derive sentiment, grammar, style attributes FROM cluster data
5. Generate persona files (80 total: 20 × 4 files each)
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent

# ── Config ──────────────────────────────────────────────────────────────────

BASE_DIR = Path.home() / "AS-Virtual_Team_System_v2"
BT_PERSONAS = BASE_DIR / "blackteam" / "personas"
BT_SKILLS = BASE_DIR / "blackteam" / "skills"
BT_PROMPTS = BASE_DIR / "blackteam" / "skills" / "prompts"
WT_PERSONAS = BASE_DIR / "whiteteam" / "personas"
DATA_DIR = BASE_DIR / "data" / "journalist_research"

for d in [BT_PERSONAS, BT_SKILLS, BT_PROMPTS, WT_PERSONAS]:
    d.mkdir(parents=True, exist_ok=True)

TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")

# ── Persona-to-Cluster Mapping ──────────────────────────────────────────────
# Maps each planned persona to the best matching cluster from style analysis.
# The cluster assignment determines which real journalists inspire each persona.

PERSONA_CLUSTER_MAP = [
    {"code": "B-HANA", "name": "Hana Richter", "style_type": "Precision Analyst",
     "geos": ["DACH", "UK"], "grammar": 99.5, "cluster": "analytical_tactical",
     "validator": {"code": "W-HRIC", "name": "Helena Richter-Cruz", "focus": "DACH tactical precision"}},

    {"code": "B-MARC", "name": "Marco Vassallo", "style_type": "Mediterranean Storyteller",
     "geos": ["IT", "ES"], "grammar": 99.2, "cluster": "emotional_storytelling",
     "validator": {"code": "W-MVAS", "name": "Marina Vasquez", "focus": "Mediterranean storytelling authenticity"}},

    {"code": "B-CLEO", "name": "Cleo Dupont", "style_type": "Cultural Critic",
     "geos": ["FR", "UK"], "grammar": 98.5, "cluster": "cultural_commentary",
     "validator": {"code": "W-CDUP", "name": "Claire Durand-Price", "focus": "Cultural criticism quality"}},

    {"code": "B-FINN", "name": "Finn Doyle", "style_type": "Aussie Voice",
     "geos": ["AU", "UK"], "grammar": 97.0, "cluster": "conversational_weekly",
     "validator": {"code": "W-FDOY", "name": "Fiona Doyle-Walsh", "focus": "Australian voice authenticity"}},

    {"code": "B-SURI", "name": "Suri Chen", "style_type": "Data Reporter",
     "geos": ["US", "DACH"], "grammar": 100.0, "cluster": "data_driven_precision",
     "validator": {"code": "W-SCHE", "name": "Sara Chen-West", "focus": "Data accuracy verification"}},

    {"code": "B-RAJA", "name": "Raja Navarro", "style_type": "Latin Fire Columnist",
     "geos": ["ES", "IT"], "grammar": 98.0, "cluster": "provocative_opinion",
     "validator": {"code": "W-RNAV", "name": "Ricardo Navarro-Vega", "focus": "Passionate opinion boundaries"}},

    {"code": "B-YUKI", "name": "Yuki Bergmann", "style_type": "Tactical Innovator",
     "geos": ["DACH", "World"], "grammar": 99.8, "cluster": "analytical_tactical",
     "validator": {"code": "W-YBER", "name": "Yara Bergmann-Reid", "focus": "Tactical analysis depth"}},

    {"code": "B-OLGA", "name": "Olga Marchand", "style_type": "Investigative Long-form",
     "geos": ["FR", "US"], "grammar": 99.5, "cluster": "investigative_depth",
     "validator": {"code": "W-OMAR", "name": "Odette Marchetti", "focus": "Investigative sourcing standards"}},

    {"code": "B-JACK", "name": "Jack Summers", "style_type": "Breaking Pace Setter",
     "geos": ["AU", "US"], "grammar": 97.5, "cluster": "wire_speed_breaking",
     "validator": {"code": "W-JSUM", "name": "James Summerfield", "focus": "Breaking news accuracy"}},

    {"code": "B-ZARA", "name": "Zara Piccoli", "style_type": "Cultural Commentary",
     "geos": ["IT", "FR"], "grammar": 99.0, "cluster": "cultural_commentary",
     "validator": {"code": "W-ZPIC", "name": "Zoe Piccoli-Laurent", "focus": "Cultural sensitivity review"}},

    {"code": "B-LEON", "name": "Leon Torres", "style_type": "Hard News Insider",
     "geos": ["ES", "US"], "grammar": 97.0, "cluster": "insider_network",
     "validator": {"code": "W-LTOR", "name": "Luis Torres-Vega", "focus": "Hard news verification"}},

    {"code": "B-NINW", "name": "Nina Wolff", "style_type": "Weekly Digest",
     "geos": ["DACH", "UK"], "grammar": 98.5, "cluster": "conversational_weekly",
     "validator": {"code": "W-NWOL", "name": "Nora Wolff-Gray", "focus": "Weekly digest completeness"}},

    {"code": "B-HUGL", "name": "Hugo Laurent", "style_type": "Essayist & Thinker",
     "geos": ["FR", "World"], "grammar": 99.8, "cluster": "essayist_intellectual",
     "validator": {"code": "W-HLAU", "name": "Henri Laurent-Moss", "focus": "Essay intellectual rigor"}},

    {"code": "B-ROSA", "name": "Rosa Keating", "style_type": "Feature Profile Writer",
     "geos": ["AU", "UK"], "grammar": 99.2, "cluster": "scene_setting_feature",
     "validator": {"code": "W-RKEA", "name": "Rachel Keating-Dunn", "focus": "Profile accuracy & fairness"}},

    {"code": "B-DAVI", "name": "Davi Rossi", "style_type": "Fast Transfer Specialist",
     "geos": ["IT", "ES"], "grammar": 97.5, "cluster": "rapid_social",
     "validator": {"code": "W-DROS", "name": "Dante Rossi-Valle", "focus": "Transfer accuracy gate"}},

    {"code": "B-KAIA", "name": "Kaia Lundberg", "style_type": "Scandinavian Clarity",
     "geos": ["World", "DACH"], "grammar": 99.5, "cluster": "measured_authority",
     "validator": {"code": "W-KLUN", "name": "Katrine Lundberg-Carr", "focus": "Clarity & balance check"}},

    {"code": "B-ABEL", "name": "Abel Garcia", "style_type": "Opinion Firebrand",
     "geos": ["ES", "FR"], "grammar": 98.0, "cluster": "provocative_opinion",
     "validator": {"code": "W-AGAR", "name": "Arturo Garcia-Roux", "focus": "Opinion boundary enforcement"}},

    {"code": "B-MILA", "name": "Mila Crawford", "style_type": "Narrative Investigator",
     "geos": ["UK", "US"], "grammar": 99.0, "cluster": "narrative_longform",
     "validator": {"code": "W-MCRA", "name": "Morgan Crawford-Hill", "focus": "Narrative investigation sourcing"}},

    {"code": "B-RENO", "name": "Reno DiMarco", "style_type": "Combat Sports & F1",
     "geos": ["IT", "AU"], "grammar": 97.5, "cluster": "tabloid_energy",
     "validator": {"code": "W-RDIM", "name": "Romano DiMarco-West", "focus": "Combat sports accuracy"}},

    {"code": "B-ASHA", "name": "Asha Fontaine", "style_type": "Quiet Authority",
     "geos": ["FR", "AU"], "grammar": 99.8, "cluster": "literary_sports",
     "validator": {"code": "W-AFON", "name": "Amélie Fontaine-Gray", "focus": "Authority & legal accuracy"}},
]


def load_cluster_data():
    """Load cluster report and individual style profiles."""
    cluster_path = DATA_DIR / "analysis" / "clusters" / "cluster_report.json"
    with open(cluster_path) as f:
        cluster_report = json.load(f)

    profiles_dir = DATA_DIR / "analysis" / "style_profiles"
    profiles = {}
    for p_file in profiles_dir.glob("*_style.json"):
        with open(p_file) as f:
            profile = json.load(f)
            profiles[profile["journalist_id"]] = profile

    return cluster_report, profiles


def load_registry():
    """Load journalist registry for name/GEO lookup."""
    reg_path = DATA_DIR / "journalist_registry_v2.json"
    with open(reg_path) as f:
        reg = json.load(f)
    return {j["journalist_id"]: j for j in reg["journalists"]}


def get_cluster_members(cluster_label, cluster_report, profiles, registry):
    """Get journalist details for all members of a cluster."""
    cluster = cluster_report["clusters"].get(cluster_label, {})
    members = []
    for jid in cluster.get("members", []):
        profile = profiles.get(jid, {})
        reg_entry = registry.get(jid, {})
        members.append({
            "journalist_id": jid,
            "name": reg_entry.get("name", jid),
            "geo": reg_entry.get("geo", "?"),
            "outlet": reg_entry.get("primary_outlet", "?"),
            "sport": reg_entry.get("sport", "?"),
            "sentiment_profile": profile.get("sentiment_profile", {}),
            "metrics": profile.get("metrics", {}),
            "readability": profile.get("readability", {}),
        })
    return members


def derive_sentiment_combo(members, persona_geos):
    """Derive 5-sentiment combo from cluster member profiles, weighted by GEO overlap."""
    sentiment_totals = {}
    for m in members:
        dist = m.get("sentiment_profile", {}).get("sentiment_distribution", {})
        # Weight journalists from matching GEOs higher
        weight = 2.0 if m["geo"] in persona_geos else 1.0
        for sentiment, score in dist.items():
            sentiment_totals[sentiment] = sentiment_totals.get(sentiment, 0) + score * weight

    # Top 5 sentiments
    sorted_sentiments = sorted(sentiment_totals.items(), key=lambda x: x[1], reverse=True)
    top5 = [s[0] for s in sorted_sentiments[:5]]

    # Calculate distribution
    total = sum(s[1] for s in sorted_sentiments[:5])
    distribution = {}
    for s_name, s_score in sorted_sentiments[:5]:
        distribution[s_name] = round(s_score / total * 100) if total else 20

    return top5, distribution


def derive_avg_metrics(members):
    """Average NLP metrics across cluster members."""
    metrics_keys = ["avg_sentence_length", "std_sentence_length", "flesch_kincaid_grade",
                    "gunning_fog", "type_token_ratio", "fragment_ratio", "long_sentence_ratio"]
    read_keys = ["flesch_reading_ease", "smog_index", "coleman_liau_index"]

    avg_metrics = {}
    for key in metrics_keys:
        vals = [m["metrics"].get(key, 0) for m in members if m["metrics"].get(key, 0) != 0]
        avg_metrics[key] = round(sum(vals) / max(len(vals), 1), 2)

    avg_read = {}
    for key in read_keys:
        vals = [m["readability"].get(key, 0) for m in members if m["readability"].get(key, 0) != 0]
        avg_read[key] = round(sum(vals) / max(len(vals), 1), 2)

    return avg_metrics, avg_read


# ── File Generation ──────────────────────────────────────────────────────────

def generate_bt_persona(persona, source_journalists, sentiment_combo, sentiment_dist, avg_metrics):
    """Generate BlackTeam persona markdown file."""
    sources_table = ""
    for sj in source_journalists[:3]:
        sources_table += f"| {sj['name']} | {sj['outlet']} | {sj['geo']} | {sj['sport']} |\n"

    sentiment_str = ", ".join(f"{s} ({sentiment_dist.get(s, 20)}%)" for s in sentiment_combo)

    content = f"""# {persona['name']} ({persona['code']})
**Role:** Content Writer — {persona['style_type']}
**Team:** BlackTeam
**Created:** {TODAY}
**Pipeline:** Persona Factory v2 (data-driven from style analysis)

## Identity
- **Name:** {persona['name']}
- **Code:** {persona['code']}
- **Style Type:** {persona['style_type']}
- **Primary GEOs:** {', '.join(persona['geos'])}
- **Grammar Allowance:** {persona['grammar']}%
- **Cluster:** {persona['cluster']} (from agglomerative clustering of 120 journalists)

## Source Journalists (Real, Verified)
| Journalist | Outlet | GEO | Sport |
|-----------|--------|-----|-------|
{sources_table}
*Source: DataForSEO SERP research + NLP style analysis → cluster: {persona['cluster']}*

## Writing Style

### Sentence Metrics (from cluster analysis)
- Average sentence length: {avg_metrics.get('avg_sentence_length', 'N/A')} words
- Sentence length std dev: {avg_metrics.get('std_sentence_length', 'N/A')}
- Flesch-Kincaid Grade: {avg_metrics.get('flesch_kincaid_grade', 'N/A')}
- Gunning Fog Index: {avg_metrics.get('gunning_fog', 'N/A')}

### Sentiment Blend
{sentiment_str}

### Content Types
- Primary: {persona['style_type']}
- GEO Focus: {', '.join(persona['geos'])}

## Variables
| Variable | Value |
|----------|-------|
| `[Grammar]` | {persona['grammar']}% |
| `[Sentiment]` | {', '.join(sentiment_combo)} |
| `[GEO]` | {', '.join(persona['geos'])} |
| `[Style]` | {persona['style_type']} |

## Rules
- Follow CONTENT_WRITER_RULES.md (all CW-R rules)
- CW-R7: No cross-persona bleed
- CW-R9: GEO-aware selection routes to this persona for {', '.join(persona['geos'])} content
- CW-R10: Content type routing for {persona['style_type'].lower()} articles
"""
    return content


def generate_bt_skills(persona, source_journalists, avg_metrics):
    """Generate BlackTeam skills markdown file."""
    content = f"""# {persona['name']} Skills ({persona['code']}_SKILLS)

## Core Competencies
- **{persona['style_type']}** content for {', '.join(persona['geos'])} markets
- Grammar precision: {persona['grammar']}%
- Cluster archetype: {persona['cluster']}

## Writing Parameters (from NLP analysis)
- Target sentence length: ~{avg_metrics.get('avg_sentence_length', 18)} words
- FK Grade target: {avg_metrics.get('flesch_kincaid_grade', 10)}
- Vocabulary complexity: TTR ~{avg_metrics.get('type_token_ratio', 0.5)}

## Source Journalist Influences
"""
    for sj in source_journalists[:3]:
        content += f"- **{sj['name']}** ({sj['outlet']}, {sj['geo']}): {sj['sport']} coverage\n"

    content += f"""
## Content Type Expertise
- Primary: {persona['style_type']}
- Sports: Multi-sport across {', '.join(persona['geos'])} markets

## Quality Gates
- Grammar: {persona['grammar']}% minimum
- CW-R7 compliance: no persona bleed
- Validator: {persona['validator']['code']} ({persona['validator']['name']})
"""
    return content


def generate_bt_prompt(persona, sentiment_combo, avg_metrics):
    """Generate BlackTeam prompt markdown file."""
    content = f"""# {persona['name']} Prompt ({persona['code']}_PROMPT)

You are **{persona['name']}** ({persona['code']}), a {persona['style_type'].lower()} writer for Paradise Media.

## Voice
- Style: {persona['style_type']}
- Tone: {', '.join(sentiment_combo[:3])}
- Grammar precision: {persona['grammar']}%
- GEO expertise: {', '.join(persona['geos'])}

## Writing Guidelines
- Target sentence length: ~{avg_metrics.get('avg_sentence_length', 18)} words
- Flesch-Kincaid Grade: {avg_metrics.get('flesch_kincaid_grade', 10)}
- Use varied sentence lengths (std dev: {avg_metrics.get('std_sentence_length', 8)})
- Fragment ratio: {avg_metrics.get('fragment_ratio', 0.05)} (use sparingly for emphasis)

## Sentiment Distribution
"""
    for s in sentiment_combo:
        content += f"- {s}\n"

    content += f"""
## Rules
- NEVER break character
- NEVER exceed {persona['grammar']}% grammar error rate
- ALWAYS maintain {persona['style_type'].lower()} style
- Follow all CW-R rules from CONTENT_WRITER_RULES.md
"""
    return content


def generate_wt_validator(persona):
    """Generate WhiteTeam validator markdown file."""
    v = persona["validator"]
    content = f"""# {v['name']} ({v['code']})
**Role:** Content Validator
**Team:** WhiteTeam
**Validates:** {persona['code']} ({persona['name']})
**Focus:** {v['focus']}
**Created:** {TODAY}

## Validation Checklist

### 1. Grammar Compliance
- [ ] Grammar score ≥ {persona['grammar']}% (persona's declared allowance)
- [ ] No systematic grammar patterns outside persona's style

### 2. Sentiment Blend
- [ ] Content matches persona's 5-sentiment distribution
- [ ] No unexpected sentiment shifts

### 3. GEO Cultural Tone
- [ ] Appropriate for {', '.join(persona['geos'])} target markets
- [ ] Cultural references accurate and current

### 4. Content Type Match
- [ ] Matches {persona['style_type']} specialization
- [ ] Structure follows {persona['cluster']} archetype patterns

### 5. Cross-Persona Bleed (CW-R7)
- [ ] Voice is distinctly {persona['name']}, not another persona
- [ ] No borrowed phrases from other writers
- [ ] Style metrics within expected ranges

## Escalation
If validation fails: return to {persona['code']} with specific feedback.
If systemic issue: escalate to W-VERA (Content QA Lead).
"""
    return content


def main():
    print("=" * 60)
    print("PERSONA FACTORY v2.0 — Data-Driven Generation")
    print(f"Date: {TODAY}")
    print("=" * 60)

    # Load data
    cluster_report, profiles = load_cluster_data()
    registry = load_registry()

    print(f"Loaded: {len(profiles)} style profiles, {len(cluster_report['clusters'])} clusters")

    generation_log = []
    files_created = 0

    for persona in PERSONA_CLUSTER_MAP:
        code = persona["code"]
        name = persona["name"]
        cluster_label = persona["cluster"]

        print(f"\n  Generating {code} ({name}) from cluster: {cluster_label}")

        # Get cluster members
        members = get_cluster_members(cluster_label, cluster_report, profiles, registry)
        if not members:
            print(f"    WARNING: No members in cluster {cluster_label}, using fallback")
            members = [{"name": "Generic", "geo": "US", "outlet": "N/A", "sport": "Multi",
                        "sentiment_profile": {}, "metrics": {}, "readability": {}}]

        # Derive attributes from cluster data
        sentiment_combo, sentiment_dist = derive_sentiment_combo(members, persona["geos"])
        avg_metrics, avg_read = derive_avg_metrics(members)

        # Select source journalists (prefer GEO match, max 3)
        geo_match = [m for m in members if m["geo"] in persona["geos"]]
        other = [m for m in members if m["geo"] not in persona["geos"]]
        source_journalists = (geo_match + other)[:3]

        source_names = [sj["name"] for sj in source_journalists]
        print(f"    Sources: {', '.join(source_names)}")
        print(f"    Sentiment: {', '.join(sentiment_combo[:3])}")
        print(f"    Avg sentence length: {avg_metrics.get('avg_sentence_length', 'N/A')}")

        # Generate files
        # 1. BT Persona
        bt_persona = generate_bt_persona(persona, source_journalists, sentiment_combo, sentiment_dist, avg_metrics)
        bt_path = BT_PERSONAS / f"{name.upper().replace(' ', '_')}.md"
        with open(bt_path, "w") as f:
            f.write(bt_persona)
        files_created += 1

        # 2. BT Skills
        bt_skills = generate_bt_skills(persona, source_journalists, avg_metrics)
        skills_path = BT_SKILLS / f"{name.upper().replace(' ', '_')}_SKILLS.md"
        with open(skills_path, "w") as f:
            f.write(bt_skills)
        files_created += 1

        # 3. BT Prompt
        bt_prompt = generate_bt_prompt(persona, sentiment_combo, avg_metrics)
        prompt_path = BT_PROMPTS / f"{name.upper().replace(' ', '_')}_PROMPT.md"
        with open(prompt_path, "w") as f:
            f.write(bt_prompt)
        files_created += 1

        # 4. WT Validator
        wt_validator = generate_wt_validator(persona)
        validator_name = persona["validator"]["name"].upper().replace(" ", "_").replace("-", "_")
        wt_path = WT_PERSONAS / f"{validator_name}.md"
        with open(wt_path, "w") as f:
            f.write(wt_validator)
        files_created += 1

        generation_log.append({
            "persona_code": code,
            "persona_name": name,
            "cluster": cluster_label,
            "source_journalists": source_names,
            "sentiment_combo": sentiment_combo,
            "grammar": persona["grammar"],
            "geos": persona["geos"],
            "avg_metrics": avg_metrics,
            "files_generated": [str(bt_path), str(skills_path), str(prompt_path), str(wt_path)],
        })

    # Save generation log
    log_path = DATA_DIR / "personas" / "generation_log_v2.json"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "w") as f:
        json.dump({
            "metadata": {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "pipeline_version": "2.0",
                "data_driven": True,
                "source": "style_analysis_clusters",
            },
            "personas": generation_log,
        }, f, indent=2)

    print(f"\n{'='*60}")
    print(f"PERSONA FACTORY v2.0 COMPLETE")
    print(f"  Personas generated: {len(generation_log)}")
    print(f"  Files created: {files_created}")
    print(f"  Generation log: {log_path}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
