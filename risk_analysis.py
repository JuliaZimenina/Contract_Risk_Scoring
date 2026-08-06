import os

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# os.path.join assembles a file path so that it works on both Windows and Mac/Linux
DATA_PATH = os.path.join("data", "raw", "CUAD_v1_master_clauses.csv")
OUTPUT_DIR = "outputs"

# Create a directory "outputs" if it hasn't already been created.
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Loading data.
df = pd.read_csv(DATA_PATH)

print(f"Number of contracts loaded: {len(df)}")
print(f"Total columns in file: {len(df.columns)}")

# Uncomment the following line to see all column names in the file.
# print (list(df.columns))

# We collect a list of all columns whose names contain "-Answer".
answer_columns = [col for col in df.columns if "-Answer" in col]

print(f"Column with Yes/No answers found: {len(answer_columns)}")

# The category name is the column name without the "-Answer" suffix.
# For example: "Non-Complete-Answer" -> "Non-Complete".
def clause_name(answer_col: str) -> str:
    return answer_col.replace("-Answer", "")

# We count the frequency of each clause.
frequency_rows = []

for col in answer_columns:
    values = df[col].astype(str).str.strip().str.lower()

    #Calculate the proportion of rows where the answer is "yes".
    share_yes = (values == "yes").mean() * 100

    frequency_rows.append({
        "clause": clause_name(col),
        "share_present_pct": round(share_yes, 1),
        "count_present": int((values == "yes").sum()),
    })

# Converting a list of dictionaries into a table and sorting them in
# descending order of frequency.
freq_df = pd.DataFrame(frequency_rows).sort_values("share_present_pct", ascending=False)

print("Top 10 most common clauses (percentage of contracts where the clause is present:")
print(freq_df.head(10).to_string(index=False))

# Saving the frequency table to CSV.
freq_df.to_csv(os.path.join(OUTPUT_DIR, "clause_frequency.csv"), index=False)

# We set risk weight
RISK_WEIGHTS = {
    'Uncapped Liability': 10,
    'Non-Complete': 8,
    'Exclusivity': 8,
    'Most Favored Nation': 8,
    'Irrevocable Or Perpetual Licence': 7,
    'Minimum Commitment': 6,
    'Liquidated Damaged': 6,
    'Change Of Control': 5,
    'Audit Rights': 4,
    'Anti-Assignment': 2,
    'Cap On Liability': -6, # protective clause
    'Termination For Convenience': -4, # protective clause
}

DEFAULT_WEIGHT = 1

# Calculating the risk score for each contract.
def contract_risk_score(row) -> int:
    """Calculates the risk score of a single contract:
    the sum of the weights of all the clauses present in it ('Yes' answer)."""
    score = 0
    for col in answer_columns:
        value = str(row[col]).strip().lower()
        if value == "yes":
            name = clause_name(col)
            score += RISK_WEIGHTS.get(name, DEFAULT_WEIGHT)
    return  score

df["risk_score"] = df.apply(contract_risk_score, axis=1)

NAME_COL = "Document Name" if "Document Name" in df.columns else df.columns[0]

print(f"Mean risk-score for all contracts: {df['risk_score'].mean():.1f}")
print(
    f"Highest risk score: {df['risk_score'].max()} "
    f"(contract: {df.loc[df['risk_score'].idxmax(), NAME_COL]})"
)

# Risk concentration analysis.

N_TOP = 15 # How many contracts do we consider "the riskiest".

sorted_df = df.sort_values("risk_score", ascending=False)
top_group = sorted_df.head(N_TOP)
rest_group = sorted_df.iloc[N_TOP:]

print(f"\n---Risk Concentration Analysis (Top - {N_TOP} versus the rest) ---")
print(f"\n---Mean risk-score in the top -{N_TOP}:{top_group['risk_score'].mean():.1f}")
print(f"Mean risk-score for the remaining {len(rest_group)} contracts:{rest_group['risk_score'].mean():.1f}")
print(f"Difference: the top -{N_TOP} contracts are "
      f"{top_group['risk_score'].mean() / rest_group['risk_score'].mean():.1f} times riskier")

#For each condition from the weights, we compare the frequency in the top group against
#the sample—this allows us to see which conditions specifically "move" contracts into the high-risk zone.
print(f"\n--- Which clauses are overloaded in the top -{N_TOP} (frequency in the top vs. in the entire sample.) ---")
concentration_rows = []
for col in answer_columns:
    name = clause_name(col)
    overall_share = (df[col].astype(str).str.strip().str.lower() == "yes").mean()*100
    top_share = (top_group[col].astype(str).str.strip().str.lower() == "yes").mean()*100
    concentration_rows.append({
        "clause": name,
        "share_overall_pct": round(overall_share, 1),
        f"share_top{N_TOP}_pct": round(top_share, 1),
        "gap_pct_points": round(top_share - overall_share, 1)
    })

concentration_df = pd.DataFrame(concentration_rows).sort_values("gap_pct_points", ascending=False)
print(concentration_df.head(8).to_string(index=False))
concentration_df.to_csv(os.path.join(OUTPUT_DIR, "risk_concentration.csv"), index=False)

# The share of contracts with a risk score above average (indicates how heavy the "tail" is).
share_above_mean = (df["risk_score"] > df["risk_score"].mean()).mean()*100
print(f"\n Share of contracts with above average risk-score:{share_above_mean:.1f}%")

# Saving a table with risk scores for each contract
risk_table = df[[NAME_COL, "risk_score"]].sort_values("risk_score", ascending=False)
risk_table.to_csv(os.path.join(OUTPUT_DIR, "contract_risk_scores.csv"), index=False)

# Plotting charts
sns.set_style("whitegrid")

# --- Chart 1: Top 15 most common clauses ---
plt.figure(figsize=(9, 6))
top15 = freq_df.head(15)
sns.barplot(data=top15, x="share_present_pct", y="clause",
color="#4C72B0")
plt.xlabel("Share Of Contracts Where The Clause Is Present (%)")
plt.ylabel("")
plt.title("Top 15 Most Common Contract Clauses (CUAD)")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "clause_frequency.png"), dpi=150)
plt.close()

# --- Chart 2: Distribution of risk scores
plt.figure(figsize=(8, 5))
sns.histplot(df["risk_score"], bins=20, color="#C44E52")
plt.xlabel("Contract Risk-Score")
plt.ylabel("Number Of Contracts")
plt.title("Distribution Of Risk-Scores Across All Contracts")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "risk_score_distribution.png"), dpi=150)
plt.close()

# --- Chart 3: Top 15 Riskiest Contracts
plt.figure(figsize=(9, 6))
top_risky= risk_table.head(15)
sns.barplot(data=top_risky, x="risk_score", y=NAME_COL, color="#55A868")
plt.xlabel="Risk Score"
plt.ylabel=("")
plt.title="Top 15 Riskiest Contracts"
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "top_risky_contracts.png"), dpi=150)
plt.close()

print(f"\nDone. The results saved in the folder.")

















