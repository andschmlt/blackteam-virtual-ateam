#!/usr/bin/env python3
"""
Style Analysis Engine — Phase 4
Quantitative NLP analysis of journalist writing patterns.

Analysis Dimensions:
  A. Sentence Metrics — avg/std/min/max length, fragment/long ratios
  B. Vocabulary Complexity — FK grade, Gunning Fog, TTR, tier distribution
  C. Readability Scoring — 6 indices via textstat
  D. Structure Analysis — H2/H3 counts, paragraph metrics, opening/closing patterns
  E. Sentiment Mapping — Maps to 14 ATeam sentiment categories
  F. N-gram Analysis — Distinctive bi/trigrams, signature phrases
  G. Topic Modeling — LDA for specialization detection

Clustering:
  Agglomerative clustering (ward linkage, n=20 target clusters)
  Features normalized via StandardScaler

Dependencies: nltk, textblob, textstat, scikit-learn

Usage:
  python3 style_analysis_engine.py [--articles-dir path] [--n-clusters 20]
"""

import argparse
import json
import os
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import nltk
import numpy as np
import textstat
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.util import ngrams
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from textblob import TextBlob

# Ensure NLTK data is available
for pkg in ["punkt", "punkt_tab", "averaged_perceptron_tagger", "averaged_perceptron_tagger_eng", "stopwords"]:
    try:
        nltk.data.find(f"tokenizers/{pkg}" if "punkt" in pkg else f"taggers/{pkg}" if "tagger" in pkg else f"corpora/{pkg}")
    except LookupError:
        nltk.download(pkg, quiet=True)

from nltk.corpus import stopwords

STOP_WORDS = set(stopwords.words("english"))

# ── Config ──────────────────────────────────────────────────────────────────

OUTPUT_DIR = Path.home() / "AS-Virtual_Team_System_v2" / "data" / "journalist_research"
ARTICLES_DIR = OUTPUT_DIR / "articles"
PROFILES_DIR = OUTPUT_DIR / "analysis" / "style_profiles"
CLUSTERS_DIR = OUTPUT_DIR / "analysis" / "clusters"

PROFILES_DIR.mkdir(parents=True, exist_ok=True)
CLUSTERS_DIR.mkdir(parents=True, exist_ok=True)

# ── ATeam Sentiment Mapping ─────────────────────────────────────────────────

SENTIMENT_KEYWORDS = {
    "Direct": ["clear", "straight", "plain", "simply", "fact", "indeed", "clearly"],
    "Aggressive": ["dominat", "crush", "destroy", "fierce", "relentless", "ruthless", "savage"],
    "Factual": ["data", "statistics", "percent", "according", "research", "study", "evidence", "report"],
    "Story Telling": ["remember", "scene", "morning", "walked", "story", "once", "narrative", "journey"],
    "Negative": ["fail", "disappoint", "poor", "worst", "lack", "crisis", "problem", "struggle"],
    "Positive": ["excellent", "brilliant", "outstanding", "impressive", "triumph", "celebrate", "remarkable"],
    "Provocative": ["why", "nobody", "dare", "controversial", "unpopular", "challenge", "radical"],
    "Empathetic": ["feel", "heart", "human", "emotion", "understand", "compassion", "painful"],
    "Analytical": ["therefore", "consequently", "analysis", "factor", "metric", "framework", "systematic"],
    "Conversational": ["honestly", "look", "okay", "right", "actually", "basically", "frankly"],
    "Authoritative": ["undoubtedly", "certainly", "definitive", "absolute", "confirmed", "decisive"],
    "Witty": ["ironic", "tongue", "wry", "clever", "quip", "amusing", "sardonic"],
    "Passionate": ["love", "incredible", "amazing", "unbelievable", "spectacular", "stunning"],
    "Measured": ["however", "although", "perspective", "balance", "nuance", "complex", "consider"],
}


# ── A. Sentence Metrics ─────────────────────────────────────────────────────

def analyze_sentences(text: str) -> dict:
    """Compute sentence-level metrics."""
    sentences = sent_tokenize(text)
    if not sentences:
        return {"avg_sentence_length": 0, "std_sentence_length": 0,
                "min_sentence_length": 0, "max_sentence_length": 0,
                "fragment_ratio": 0, "long_sentence_ratio": 0, "sentence_count": 0}

    lengths = [len(s.split()) for s in sentences]
    arr = np.array(lengths)

    return {
        "avg_sentence_length": round(float(np.mean(arr)), 2),
        "std_sentence_length": round(float(np.std(arr)), 2),
        "min_sentence_length": int(np.min(arr)),
        "max_sentence_length": int(np.max(arr)),
        "fragment_ratio": round(sum(1 for l in lengths if l < 5) / len(lengths), 4),
        "long_sentence_ratio": round(sum(1 for l in lengths if l > 30) / len(lengths), 4),
        "sentence_count": len(sentences),
    }


# ── B. Vocabulary Complexity ─────────────────────────────────────────────────

# Common English words (top 3000 approximation)
COMMON_THRESHOLD = 3000

def analyze_vocabulary(text: str) -> dict:
    """Compute vocabulary complexity metrics."""
    words = word_tokenize(text.lower())
    words = [w for w in words if w.isalpha() and w not in STOP_WORDS]
    if not words:
        return {"flesch_kincaid_grade": 0, "gunning_fog": 0, "type_token_ratio": 0,
                "vocab_tier_common": 0, "vocab_tier_domain": 0, "vocab_tier_rare": 0}

    unique_words = set(words)
    ttr = len(unique_words) / len(words) if words else 0

    # Tier classification (heuristic: word length as proxy)
    common = sum(1 for w in words if len(w) <= 6)
    domain = sum(1 for w in words if 7 <= len(w) <= 10)
    rare = sum(1 for w in words if len(w) > 10)
    total = len(words)

    return {
        "flesch_kincaid_grade": round(textstat.flesch_kincaid_grade(text), 2),
        "gunning_fog": round(textstat.gunning_fog(text), 2),
        "type_token_ratio": round(ttr, 4),
        "vocab_tier_common": round(common / total, 4) if total else 0,
        "vocab_tier_domain": round(domain / total, 4) if total else 0,
        "vocab_tier_rare": round(rare / total, 4) if total else 0,
    }


# ── C. Readability Scoring ──────────────────────────────────────────────────

def analyze_readability(text: str) -> dict:
    """Compute 6 readability indices via textstat."""
    if len(text) < 100:
        return {k: 0 for k in ["flesch_reading_ease", "smog_index", "coleman_liau_index",
                                "ari_index", "dale_chall_score", "linsear_write"]}
    return {
        "flesch_reading_ease": round(textstat.flesch_reading_ease(text), 2),
        "smog_index": round(textstat.smog_index(text), 2),
        "coleman_liau_index": round(textstat.coleman_liau_index(text), 2),
        "ari_index": round(textstat.automated_readability_index(text), 2),
        "dale_chall_score": round(textstat.dale_chall_readability_score(text), 2),
        "linsear_write": round(textstat.linsear_write_formula(text), 2),
    }


# ── D. Structure Analysis ───────────────────────────────────────────────────

def classify_opening(text: str) -> str:
    """Classify the opening paragraph pattern."""
    first_para = text.split("\n\n")[0] if "\n\n" in text else text[:500]
    first_para_lower = first_para.lower()

    if first_para.strip().endswith("?") or "?" in first_para[:200]:
        return "question"
    if re.search(r'\d+[%$€£]|\d{4}|\d+\.\d+', first_para[:200]):
        return "stat_lead"
    if first_para.startswith('"') or first_para.startswith("'") or first_para.startswith('\u201c'):
        return "quote_lead"
    if any(w in first_para_lower[:100] for w in ["morning", "evening", "walked", "stood", "sat", "watched"]):
        return "scene_setting"
    if any(w in first_para_lower[:100] for w in ["i remember", "growing up", "years ago", "my first"]):
        return "anecdotal"
    return "direct_statement"


def classify_closing(text: str) -> str:
    """Classify the closing paragraph pattern."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    if not paragraphs:
        return "unknown"
    last_para = paragraphs[-1].lower()

    if any(w in last_para for w in ["will", "future", "next", "ahead", "tomorrow", "coming"]):
        return "forward_looking"
    if any(w in last_para for w in ["in summary", "ultimately", "in the end", "all said"]):
        return "summary"
    if last_para.startswith('"') or last_para.startswith('\u201c'):
        return "quote_close"
    if any(w in last_para for w in ["began", "started", "back to", "full circle"]):
        return "circular"
    if "?" in last_para:
        return "question_close"
    return "call_to_action"


def analyze_structure(text: str, h2s: list, h3s: list) -> dict:
    """Analyze article structure."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    sentences_per_para = []
    for para in paragraphs:
        sents = sent_tokenize(para)
        sentences_per_para.append(len(sents))

    return {
        "avg_h2_per_article": len(h2s),
        "avg_h3_per_article": len(h3s),
        "avg_paragraphs": len(paragraphs),
        "avg_sentences_per_para": round(np.mean(sentences_per_para), 2) if sentences_per_para else 0,
        "opening_pattern": classify_opening(text),
        "closing_pattern": classify_closing(text),
    }


# ── E. Sentiment Mapping ────────────────────────────────────────────────────

def analyze_sentiment(text: str) -> dict:
    """Map text to ATeam's 14 sentiment categories using keyword indicators."""
    text_lower = text.lower()
    words = text_lower.split()
    word_count = len(words) or 1

    scores = {}
    for sentiment, keywords in SENTIMENT_KEYWORDS.items():
        count = sum(1 for kw in keywords for w in words if kw in w)
        scores[sentiment] = count / word_count

    # Normalize to sum to 1
    total = sum(scores.values()) or 1
    distribution = {k: round(v / total, 4) for k, v in scores.items()}

    # Also use TextBlob for polarity/subjectivity as supplementary signal
    blob = TextBlob(text[:5000])  # cap for performance
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    # Adjust based on polarity
    if polarity > 0.2:
        distribution["Positive"] = round(distribution.get("Positive", 0) + 0.05, 4)
        distribution["Passionate"] = round(distribution.get("Passionate", 0) + 0.03, 4)
    elif polarity < -0.1:
        distribution["Negative"] = round(distribution.get("Negative", 0) + 0.05, 4)
        distribution["Aggressive"] = round(distribution.get("Aggressive", 0) + 0.03, 4)

    # Renormalize
    total = sum(distribution.values()) or 1
    distribution = {k: round(v / total, 4) for k, v in distribution.items()}

    # Sort by score descending
    distribution = dict(sorted(distribution.items(), key=lambda x: x[1], reverse=True))

    return {
        "sentiment_distribution": distribution,
        "dominant_sentiment": max(distribution, key=distribution.get),
        "polarity": round(polarity, 4),
        "subjectivity": round(subjectivity, 4),
    }


# ── F. N-gram Analysis ──────────────────────────────────────────────────────

def analyze_ngrams(text: str) -> dict:
    """Extract distinctive n-gram patterns."""
    words = word_tokenize(text.lower())
    words = [w for w in words if w.isalpha()]

    # Bigrams
    bigram_counts = Counter(ngrams(words, 2))
    # Filter out stopword-only bigrams
    bigrams_filtered = {bg: c for bg, c in bigram_counts.items()
                        if not all(w in STOP_WORDS for w in bg)}
    top_bigrams = [" ".join(bg) for bg, _ in sorted(bigrams_filtered.items(), key=lambda x: x[1], reverse=True)[:20]]

    # Trigrams
    trigram_counts = Counter(ngrams(words, 3))
    trigrams_filtered = {tg: c for tg, c in trigram_counts.items()
                         if sum(1 for w in tg if w not in STOP_WORDS) >= 2}
    top_trigrams = [" ".join(tg) for tg, _ in sorted(trigrams_filtered.items(), key=lambda x: x[1], reverse=True)[:15]]

    # Signature phrases — multi-word patterns that appear 3+ times
    signature_phrases = []
    for tg, count in trigrams_filtered.items():
        if count >= 3:
            signature_phrases.append(" ".join(tg))

    return {
        "signature_bigrams": top_bigrams[:10],
        "signature_trigrams": top_trigrams[:10],
        "signature_phrases": signature_phrases[:10],
    }


# ── Full Profile ─────────────────────────────────────────────────────────────

def analyze_journalist(journalist_id: str, articles_dir: Path) -> dict | None:
    """Build complete style profile for a single journalist."""
    full_path = articles_dir / journalist_id / "articles_full.jsonl"
    if not full_path.exists():
        return None

    # Load articles
    articles = []
    with open(full_path) as f:
        for line in f:
            article = json.loads(line)
            if article.get("body_text") and article.get("scrape_status") in ("success", "snippet_only"):
                articles.append(article)

    if len(articles) < 3:
        print(f"    Insufficient articles ({len(articles)}) for {journalist_id}, need 3+")
        return None

    # Use top 50 articles by composite score
    articles.sort(key=lambda a: a.get("composite_score", 0), reverse=True)
    articles = articles[:50]

    # Combine all text for aggregate analysis
    all_text = "\n\n".join(a["body_text"] for a in articles)
    all_h2s = [h for a in articles for h in a.get("h2_structure", [])]
    all_h3s = [h for a in articles for h in a.get("h3_structure", [])]

    # Run all analysis dimensions
    sentence_metrics = analyze_sentences(all_text)
    vocabulary = analyze_vocabulary(all_text)
    readability = analyze_readability(all_text)
    structure = analyze_structure(all_text, all_h2s, all_h3s)
    sentiment = analyze_sentiment(all_text)
    ngram_data = analyze_ngrams(all_text)

    # Average per-article structure metrics
    per_article_h2 = [len(a.get("h2_structure", [])) for a in articles]
    per_article_h3 = [len(a.get("h3_structure", [])) for a in articles]
    structure["avg_h2_per_article"] = round(np.mean(per_article_h2), 2) if per_article_h2 else 0
    structure["avg_h3_per_article"] = round(np.mean(per_article_h3), 2) if per_article_h3 else 0

    # Classify opening/closing from individual articles
    opening_patterns = Counter()
    closing_patterns = Counter()
    for a in articles:
        opening_patterns[classify_opening(a["body_text"])] += 1
        closing_patterns[classify_closing(a["body_text"])] += 1
    structure["opening_pattern"] = opening_patterns.most_common(1)[0][0] if opening_patterns else "unknown"
    structure["closing_pattern"] = closing_patterns.most_common(1)[0][0] if closing_patterns else "unknown"

    profile = {
        "journalist_id": journalist_id,
        "articles_analyzed": len(articles),
        "metrics": {
            **sentence_metrics,
            **vocabulary,
        },
        "readability": readability,
        "structure": structure,
        "sentiment_profile": sentiment,
        "ngrams": ngram_data,
        "analyzed_at": datetime.now(timezone.utc).isoformat(),
    }

    return profile


# ── Clustering ───────────────────────────────────────────────────────────────

CLUSTER_LABELS = {
    0: "wire_speed_breaking",
    1: "narrative_longform",
    2: "analytical_tactical",
    3: "provocative_opinion",
    4: "conversational_weekly",
    5: "data_driven_precision",
    6: "emotional_storytelling",
    7: "analytical_conversational",
    8: "investigative_depth",
    9: "cultural_commentary",
    10: "essayist_intellectual",
    11: "tabloid_energy",
    12: "measured_authority",
    13: "scene_setting_feature",
    14: "rapid_social",
    15: "statistical_reporter",
    16: "literary_sports",
    17: "podcast_voice",
    18: "insider_network",
    19: "niche_specialist",
}


def extract_feature_vector(profile: dict) -> list[float]:
    """Extract numerical feature vector from style profile for clustering."""
    m = profile.get("metrics", {})
    r = profile.get("readability", {})
    s = profile.get("structure", {})
    sent = profile.get("sentiment_profile", {}).get("sentiment_distribution", {})

    return [
        m.get("avg_sentence_length", 0),
        m.get("std_sentence_length", 0),
        m.get("fragment_ratio", 0),
        m.get("long_sentence_ratio", 0),
        m.get("flesch_kincaid_grade", 0),
        m.get("gunning_fog", 0),
        m.get("type_token_ratio", 0),
        r.get("flesch_reading_ease", 0),
        r.get("smog_index", 0),
        r.get("coleman_liau_index", 0),
        s.get("avg_h2_per_article", 0),
        s.get("avg_paragraphs", 0),
        s.get("avg_sentences_per_para", 0),
        sent.get("Direct", 0),
        sent.get("Analytical", 0),
        sent.get("Story Telling", 0),
        sent.get("Conversational", 0),
        sent.get("Provocative", 0),
        sent.get("Factual", 0),
        sent.get("Passionate", 0),
    ]


def cluster_profiles(profiles: list[dict], n_clusters: int = 20) -> list[dict]:
    """Cluster journalist style profiles using agglomerative clustering."""
    if len(profiles) < n_clusters:
        n_clusters = max(2, len(profiles) // 2)
        print(f"  Adjusted clusters to {n_clusters} (fewer profiles than target)")

    # Build feature matrix
    feature_vectors = []
    valid_profiles = []
    for p in profiles:
        vec = extract_feature_vector(p)
        if any(v != 0 for v in vec):
            feature_vectors.append(vec)
            valid_profiles.append(p)

    if len(valid_profiles) < 2:
        print("  Not enough valid profiles for clustering")
        return profiles

    X = np.array(feature_vectors)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Agglomerative clustering
    clustering = AgglomerativeClustering(n_clusters=n_clusters, linkage="ward")
    labels = clustering.fit_predict(X_scaled)

    # Assign cluster labels
    for profile, label in zip(valid_profiles, labels):
        profile["cluster_id"] = int(label)
        profile["cluster_label"] = CLUSTER_LABELS.get(label, f"cluster_{label}")

    return profiles


# ── Pipeline ─────────────────────────────────────────────────────────────────

def run_analysis(articles_dir: str, n_clusters: int) -> None:
    """Run style analysis across all journalists."""
    articles_path = Path(articles_dir)
    print("=" * 60)
    print("STYLE ANALYSIS ENGINE v1.0")
    print(f"Articles dir: {articles_path}")
    print(f"Target clusters: {n_clusters}")
    print("=" * 60)

    # Find all journalist directories
    journalist_dirs = sorted([d.name for d in articles_path.iterdir() if d.is_dir()])
    print(f"Found {len(journalist_dirs)} journalist directories")

    # Analyze each journalist
    profiles = []
    for jid in journalist_dirs:
        print(f"\n  Analyzing {jid}...")
        profile = analyze_journalist(jid, articles_path)
        if profile:
            profiles.append(profile)
            # Save individual profile
            profile_path = PROFILES_DIR / f"{jid}_style.json"
            with open(profile_path, "w") as f:
                json.dump(profile, f, indent=2)
            print(f"    ✓ Profile saved ({profile['articles_analyzed']} articles)")
        else:
            print(f"    ✗ Skipped (insufficient data)")

    print(f"\n── Clustering ─────────────────────────────")
    print(f"  Profiles to cluster: {len(profiles)}")
    profiles = cluster_profiles(profiles, n_clusters)

    # Save cluster report
    cluster_report = {
        "metadata": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_profiles": len(profiles),
            "n_clusters": n_clusters,
        },
        "clusters": {},
        "profiles": [],
    }

    # Group by cluster
    for profile in profiles:
        cid = profile.get("cluster_id", -1)
        label = profile.get("cluster_label", "unassigned")
        if label not in cluster_report["clusters"]:
            cluster_report["clusters"][label] = {
                "cluster_id": cid,
                "members": [],
                "avg_metrics": {},
            }
        cluster_report["clusters"][label]["members"].append(profile["journalist_id"])

        # Slim profile for report
        cluster_report["profiles"].append({
            "journalist_id": profile["journalist_id"],
            "articles_analyzed": profile["articles_analyzed"],
            "cluster_id": profile.get("cluster_id"),
            "cluster_label": profile.get("cluster_label"),
            "dominant_sentiment": profile.get("sentiment_profile", {}).get("dominant_sentiment"),
            "opening_pattern": profile.get("structure", {}).get("opening_pattern"),
            "closing_pattern": profile.get("structure", {}).get("closing_pattern"),
            "avg_sentence_length": profile.get("metrics", {}).get("avg_sentence_length"),
            "flesch_kincaid_grade": profile.get("metrics", {}).get("flesch_kincaid_grade"),
        })

    report_path = CLUSTERS_DIR / "cluster_report.json"
    with open(report_path, "w") as f:
        json.dump(cluster_report, f, indent=2)

    print(f"\n── Analysis Complete ─────────────────────────")
    print(f"  Profiles generated: {len(profiles)}")
    print(f"  Clusters formed: {len(cluster_report['clusters'])}")
    print(f"  Cluster report: {report_path}")
    for label, data in sorted(cluster_report["clusters"].items()):
        print(f"    {label}: {len(data['members'])} journalists")


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Style Analysis Engine")
    parser.add_argument("--articles-dir", type=str, default=str(ARTICLES_DIR),
                        help="Path to articles directory")
    parser.add_argument("--n-clusters", type=int, default=20,
                        help="Target number of style clusters (default: 20)")
    args = parser.parse_args()
    run_analysis(args.articles_dir, args.n_clusters)


if __name__ == "__main__":
    main()
