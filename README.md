# Contract Risk Scoring
### Prioritizing legal review of commercial contracts using clause-level risk indicators

## Key Takeaway

Reviewing every contract with equal depth wastes limited legal capacity.
Analysis of 510 real commercial contracts shows ***risk is highly concentrated**: the top 15 contracts (3% of the 
portfolio) carry an average risk score 3.6x higher than rest of the sample. Two specific clauses - **Uncapped 
Liability** and **Non-Compete** - are present in over 90% of thesr high-risk contracts, despite being relatively rare 
overall, making them reliable early-warning flags.

**Recommendation:** prioritize legal review using a risk score, and treat the presence of Uncapped Liability or 
Non-Compete as an immediate red flag - even before a full score is calculated. This lets a legal/compliance team focus 
limited review time, where risk is actually concentrated, instead of spreading it evenly across the portfolio.

![Risk score sistribution](outputs/risk_score_distribution.png)

## Business Context

Companies signing dozens or hundreds of commercial contracts cannot give each one an equally in-depth legal review. As a
result, contracts with dangerous terms (uncapped liability, exclusivity, volume restrictions, etc.) sometimes get the 
same attention as routine NDAs, and legal risk quietly accumulates. This project builds a lightweight, transparent 
prioritization model - a risk score - that a legal or compliance team can use to identify which contracts need priority 
review.

## Key Findings

**1. Risk is concentrated in a small group of contracts, not evenly distributed.**
The average risk score across the full sample was **11.0** (max: 44, for a Content License, Marketing and Sales 
Agreement). The top 15 highest-risk contracts (under 3% of the sample) averaged **36.7** - 3.6x higher than the 
remaining 495 contracts (10.3). Only 42.7% of contracts scored above the sample average, meaning the average is pulled 
up by a small number of outliers rather than reflecting a typical contract.

*Implication: reviewing all 510 contracts equally is inefficient prioritizing by score concentrates review time risk 
actually lives*

**2. Uncapped Liability and Non-Compete are the strongest risk indicators - not most common clauses.**
Uncapped Liability appears in only 21.8% of contracts overall, but in 93.3% of the top-15 highest-risk contracts (4.3x 
more often). Non-Compete shows a similar pattern: 23.3% overall vs. 86.7% in the top 15 (3.7x more often). Notably, 
neither ranks in the top 10 most  frequent clauses overall - unlike License Grant (50% of contracts), which is common 
but not discriminative, appearing in high-risk and routine contracts alike.

*Implication: the presence of Uncapped Liability or Non-Compete can be used as a fast triage flag, even before a full 
risk score is calculated*

![Top-10 clauses by frequency](outputs/clause_frequency.png)

![Top-15 highest-risk contracts](outputs/top_risky_contracts.png)

<!-- TODO - enhancements planned, not yet computed:
1. Pareto chart: cumulative % of total portfolio risk captured by top X% of contracts by score. Same underlying scores, 
just sorted + cumsum - strong "80/20" visual for business stakeholders.
2. Clause-level lift table across all 41 clause types (not just the top 2): overall frequency | frequency in top-15 | 
lift ratio. Surface more indicators beyond Uncapped Liability / Non-Compete.
3. Risk tiers (e.g. Critical / High / Medium / Low, via score quartiles) as an operational triangle framework instead of 
a single top-15 cutoff. -->

<!-- ![Risk Concentration: Pareto Curve](outputs/risk_pareto.png) -->

## Data & Methodology

**Dataset:** [CUAD(Contract Understanding Atticus Dataset)](https://www.atticusprojectai.org/cuad) - 510 commercial 
contracts from SEC EDGAR fillings, annotated by practicing attorneys across 41 clause categories. Licensed under CC BY 
4.0.

**Approach:**
1. Flag the presence / absence of each of the 41 clause categories per contract.
2. Calculated each clause's frequency across the full sample.
3. Assign each clause category a risk weight from 1-10, based on its potential legal/financiak consequence for the 
signing party (e.g. Uncapped Liability: 10; Governing Law: default weight).
4. Compute each contract's risk score as the sum of weights of the risky clause present.
5. Visualize the distribution and flag the highest-risk contracts. 

**Limitations (by design, at this stage):**
- Contracts are drawn from public SEC fillings of publicly traded US companies - the sample - is not representative of 
private or non-US business.
- Risk weights are expert-assigned based on legal/complience judgment, not statically derived - this is an expert-based 
model, not machine learning, by deliberate choice at this stage.
- 81 contracts (15.9% of the sample) have partially redacted text for individual clause.

**Tools:** Python, NumPy, Pandas, Matplotlib/Seaborn

## Roadmap / Next Steps
- Replace expert-assigned weights with weights statistically derived from historical contracts dispute/loss data, if 
available.
- Add contract type classification with input from 2-5 practicing lawyers to reduce model subjectivity,
- Add NLP module to surface risk-reevant language not yet captured by the labeled clause categories.
- Build an interactive Streamlit dashboard for exploring contracts by score and clause.

## How to Run

```bash
git clone https://github.com/JuliaZimenina/Contract_Risk_Scoring.git
cd Contract_Risk_Scoring
pip install -r requirements.txt
# Download CUAD_v1_master_clauses.csv from:
# https://www.kaggle.com/datasets/theatticusproject/atticus-open-contract-dataset-aok-beta
# and place it in data/raw/
python risk_analysis.py
```

## About the Author 

Julia Zimenina - Data Analyst with 10+ years of experience in legal and compliance (banking, energy, healthcare, 
manufacturing, agriculture), now applying that domain expertise and analytical mindset to data. This project reflect how 
I approach analysis: start from a real business problem, stay honest about model's limitations, and translate findings 
into a recommendation someone can act on.

**[LinkedIn](https://www.linkedin.com/in/julia-zimenina/)** 