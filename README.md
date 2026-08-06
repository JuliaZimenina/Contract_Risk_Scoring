# Contract Risk Scoring
## ***(Risk scoring of commercial contracts)***

## Business Goal

When entering into dozens or hundreds of commercial contracts, companies physically cannot provide each once with 
an equally in-dept legal review. As a result, contracts with the most dangerous terms (uncapped liability, exclusivity,
volume restrictions, etc.) sometimes receive as much attention as routine NDAs, and legal risk accumulates.

I set myself the task of using a sample of 510 real commercial contracts to determine which terms most often create risk
for a company and to build a prioritization model - a risk score - that allows the legal/complaince department to 
quickly identify contracts requiring priority review.

## Data Sources and Limitations

- **Dataset:** [CUAD (Contract Understanding Atticus Dataset)] (https://www.atticusprojectai.org/cuad) - 510 commercial
contracts from the SEC EDGAR open source system, annotated by practicing attorneys into 41 contract terms and 
conditions. Licensed under CC BY 4.0.

- **Limitations:**
  
  - Contracts are taken from public SEC filings - these are primary contracts of publicly traded US companies; the 
sample isn't representative or private/non-public businesses or non-US jurisdictions.
  - Risk weight for each contract term category are manually assigned based on my expertise in compliance/legal matters,
this is an expert-based, non-statistically derived, model (not machine learning), and this is a deliberate choice for 
this stage project.
  - 81 contracts (15.9% of the sample) have partially redacted text for individual terms and conditions.

## Approach 

1. Automatically identified all conditions in the dataset, labeled a binary (whether the condition is present or not 
in the contract).

2. Calculated the frequency of each condition across the entire sample of 510 contracts.

3. Assigned a risk weight from 1 to 10 condition category based on potential legal/financial consequences it could have 
for the party signing the contract (e.g. Uncapped Liability - 10, Governing Law - default weight).

4. Calculated the risk score for each contract as the sum of the weight of the risky conditions present in it.

5. Visualized the distribution and highlighted the contracts with the highest risk.

**Tools:** Python, Pandas, Matplotlib/Seaborn, Streamlit (for the interactive dashboard).

## Key Insight

The average risk score across the sample of 510 contracts was 11.0 (maximum - 44, for the Content License, Marketing and 
Sales Agreement). The number alone isn't very informative, what matters more is how risk is distributed within the 
sample.

**1. Risk is concentrated in a narrow group of contracts, not spred evenly.** The average risk score among the top 15 
highest-risk contracts (under 3% of the sample) was 36.7 - 3.6 times higher than the remaining 495 contracts (10.3). At 
the same time, only 42,7% of contracts have a risk score above average, meaning the average is artificially inflated by 
a small number of outlier contracts with very high risk, rather than reflecting a typical contract in the sample. 
Practical implication^ reviewing all 510 contracts equally is inefficient, prioritizing by risk score lets a legal/
compliance team focus resources on the small share of contracts where risk is actually concentrated.

**2. Uncapped Liability and Non-Compete are the strongest indicators of high risk - not the most common clauses.** The 
Uncapped Liability clause appears in only 21.8% of contracts overall, but in 93.3% of the top-15 highest-risk (4.3x more
often than average). A similar pattern holds for Non-Compete: 23.3 overall vs. 86.7 in the top 15 (3.7X more often). 
Notably, these aren't the most frequent clauses in the dataset overall (neither ranks in the top 10 by overall frequency
), which is exactly why their presence is a more informative risk indicator than widely-occurring clauses like License 
Grant (50% overall), which appears in almost every top-15 contract but just as often across the sample as a whole. 
Practical implication: the presence of Uncapped Liability or Non-Compete can be used as a quick flag for review 
prioritization, even before calculating the full risk score.

**Practical implication:** for legal/compliance team with limited review time, the data shows that the highest return 
comes not reviewing every contract equally, but from targeted prioritization: by risk score and/or by the presence of 
rare clauses that correlate strongly with risk (primarily Uncapped Liability and Non-Compete).

![Top-10 clauses by frequency](outputs/clause_frequency.png)

![Risk score distribution](outputs/risk_score_distribution.png)

![Top-15 highest-risk contracts](outputs/top_risky_contracts.png)


## Live Dashboard: IN PROGRESS

## What I Would Do With More Time / Data

- Replace the expert-assigned weights with weights statistically derived from historical data on contract disputes/
losses (if such data were available).

- Add contract type classification (NDA, licence, M&A, etc.) and compare risk profiles across types.

- Validate the weigts with input from 2-5 practicing lawyer to reduce model subjectivity.

- Add an NLP module to automatically surface risk categories not yet labeled in the contract text.

## How To Run

```bash

git clone https://github.com/JuliaZimenina/contract-risk-scoring.git
cd contract-risk-scoring
pip install -r requirements.txt
# Download CUAD_v1_master_clauses.csv с 
https://www.kaggle.com/datasets/theatticusproject/atticus-open-contract-dataset-aok-beta
# and put in data/raw/
python risk_analysis.py

```

## Author
Julia Zimenina - 10 years of experience in legal and compliance (banking, energy, healthcare, etc.), currently 
developing my skills in data analytics. 

**[LinkedIn](https://www.linkedin.com/in/julia-zimenina/)** 