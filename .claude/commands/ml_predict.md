# /ml_predict - ML Prediction for Domains & Articles

Invoke Elias Thorne (B-ELIA) to run ML predictions using the Competitive Analysis framework.

## Arguments

Arguments: $ARGUMENTS

---

## Phase 0: RAG Context Loading (MANDATORY)

**Load relevant context from the RAG system before running predictions.**

Read these files for prior learnings and corrections:
- `~/pitaya/knowledge/feedback_corrections.md` — Data accuracy rules, R-DATA-07 numerical validation
- `~/.claude/context/skills/ML_COMPETITIVE_ANALYSIS.md` — ML framework

**RAG Query:**
```python
from AS-Virtual_Team_System_v2.rag.rag_client import VTeamRAG
rag = VTeamRAG()
context = rag.query("ML prediction competitive analysis domain", top_k=5)
learnings = rag.query("ML prediction accuracy corrections", collection_name="learnings", top_k=3)
```

---

## Skill Reference

**Loads:** `~/.claude/context/skills/ML_COMPETITIVE_ANALYSIS.md`

---

## BigQuery Configuration

### Service Account
```bash
export GOOGLE_APPLICATION_CREDENTIALS=/home/andre/secrets/bi-chatbot-sa.json
# Account: andre-claude@paradisemedia-bi.iam.gserviceaccount.com
```

**DO NOT USE:** `/home/andre/secrets/paradisemedia-bi-sa.json` (papaya-drive-uploader - no BQ access)

---

## Quick Reference

### Available Models

| Model | Type | Use Case | Features |
|-------|------|----------|----------|
| Linear Regression | Simple | Baseline, single feature | N_OVERALL_Score |
| Linear HR/MR/LR | Risk-adjusted | Conservative/Balanced/Optimistic | Risk-weighted scores |
| XGBoost | Advanced | Multi-feature, non-linear | 25+ features |

### Prediction Targets

| Target | Description |
|--------|-------------|
| Commission | Revenue prediction (12 months) |
| Traffic | Organic traffic forecast |
| Domain Value | Acquisition valuation |

---

## Usage

```
/ml_predict [domain or task description]
```

**Examples:**
```
/ml_predict Predict commission for competitor domains in CA dataset
/ml_predict Score europeangaming.eu against competitors
/ml_predict Train new XGBoost model with updated data
/ml_predict Evaluate model accuracy on test set
```

---

## Workflow

### Phase 1: Data Assessment

Elias Thorne assesses available data:

1. **Check data sources** - Domain Stats, Grades, Commission history
2. **Identify gaps** - Missing metrics, null values
3. **Recommend model** - Linear vs XGBoost based on data quality

### Phase 2: Model Selection

| Data Quality | Recommended Model |
|--------------|-------------------|
| <50 rows, few features | Linear Regression (baseline) |
| 50-200 rows, many features | XGBoost with early stopping |
| >200 rows, complete features | XGBoost with tuned parameters |

### Phase 3: Execution

**For New Predictions:**
```sql
SELECT domain, predicted_commission
FROM ML.PREDICT(MODEL `ML_XGBOOST_REG`, input_data)
WHERE commission IS NULL;
```

**For Model Training:**
```sql
CREATE OR REPLACE MODEL `ML_XGBOOST_REG`
OPTIONS(...) AS
SELECT features, target FROM training_data;
```

### Phase 4: Validation

W-THOR (Thor Andersen) validates:
- Model accuracy metrics (MAE, MSE, R2)
- Prediction reasonableness
- Edge case handling

---

## Key Metrics

### Feature Weights (Domain Rating)

| Metric | Weight | Impact |
|--------|--------|--------|
| CPC (traffic value) | 0.30 | Highest |
| DA, Quality Links | 0.02-0.03 | High |
| Organic Traffic | 0.025 | Medium |
| Keywords 1-3 | 0.015 | Medium |
| Backlinks, RD | 0.005 | Low |

### Risk Multipliers

| Risk Level | Multiplier | When to Use |
|------------|------------|-------------|
| High Risk | 0.4 | Conservative budgeting |
| Medium Risk | 0.6 | Balanced planning |
| Low Risk | 0.8 | Optimistic forecasts |

---

## XGBoost Parameters

```sql
OPTIONS(
  model_type = 'BOOSTED_TREE_REGRESSOR',
  max_iterations = 300,    -- Up to 300 trees
  max_tree_depth = 6,      -- Prevent overfitting
  subsample = 0.8,         -- 80% data per tree
  learn_rate = 0.1,        -- Gradual learning
  early_stop = TRUE,       -- Stop if no improvement
  data_split_method = 'AUTO_SPLIT'  -- 80/20 split
)
```

---

## Output Format

```markdown
## ML Prediction Results

**Model:** [XGBoost/Linear]
**Target:** [Commission/Traffic/Value]
**Date:** [Today]

### Top Predictions

| Domain | Predicted Commission | Score | Confidence |
|--------|---------------------|-------|------------|
| domain1.com | $12,500 | 8.2 | High |
| domain2.com | $8,300 | 7.1 | Medium |

### Model Metrics

| Metric | Value |
|--------|-------|
| R2 Score | 0.85 |
| MAE | $1,200 |
| Training Samples | 85 |

### Recommendations

1. [Action based on predictions]
2. [Data quality improvements]
```

---

## Integration

### With BlackTeam
```
/blackteam Build prediction pipeline for Q1 acquisition targets
> Elias Thorne leads ML, DataForge handles ETL
```

### With WhiteTeam
```
/whiteteam Validate ML predictions before board presentation
> Thor Andersen audits model accuracy
```

---

## Your Task

When `/ml_predict` is invoked:

1. **Load ML_COMPETITIVE_ANALYSIS.md skill**
2. **Assess the request** - training, prediction, or evaluation
3. **Select appropriate model** based on data/task
4. **Execute or provide SQL** for BigQuery
5. **Format results** with confidence indicators
6. **Recommend next steps**

---

**Persona:** Elias Thorne (B-ELIA) - ML Engineer / Data Scientist
**Validator:** Thor Andersen (W-THOR) - ML Validation
