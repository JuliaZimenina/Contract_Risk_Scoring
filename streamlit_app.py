import os
import pandas as pd
import streamlit as st

# Page setup.
st.set_page_config(
    page_title="Contract Risk Scoring",
    page_icon="📄",
    layout = "wide"
)

# Title and introduction.
st.title("📄 Contract Risk Scoring Dashboard")
st.caption(
    "Interactive exploration of risk-scoring results for 510 commercial contracts "
    "from the CUAD dataset, Full methodology: see README.md"
)

# Loading data with protection against missing files.
OUTPUTS_DIR = "outputs"

# Create a dictionary for all file paths.
FILES = {
    "scores": os.path.join(OUTPUTS_DIR, "contract_risk_scores.csv"),
    "frequency": os.path.join(OUTPUTS_DIR, "clause_frequency.csv"),
    "concentration": os.path.join(OUTPUTS_DIR, "risk_concentration.csv"),
    "lift": os.path.join(OUTPUTS_DIR, "top_lift_clauses.csv"),
    "tiers": os.path.join(OUTPUTS_DIR, "risk_tiers.csv")
}

# Checking that all files exits before reading them.
missing = [name for name, path in FILES.items() if not os.path.exists(path)]

if missing:
    # st.error draws a red block with error text.
   st.error(
       f"Missing output files: {missing}. "
       f"Run `python risk_analysis.py` first to generate them."
   )
   # st.stop() - stops the script execution.
   st.stop()

# @st.cache_data - this is a "decorator".
@st.cache_data
def load_data():
    scores_df = pd.read_csv(FILES["scores"])
    freq_df = pd.read_csv(FILES["frequency"])
    concentration_df = pd.read_csv(FILES["concentration"])
    lift_df = pd.read_csv(FILES["lift"])
    tiers_df = pd.read_csv(FILES["tiers"])
    return scores_df, freq_df, concentration_df, lift_df, tiers_df

# Call a function to unpack five tables at once.
scores_df, freq_df, concentration_df, lift_df, tiers_df = load_data()

NAME_COL = "Document Name"

# We recalculate the tier for each contract (not just the summary).
scores_df["risk_tier"] = pd.qcut(
    scores_df["risk_score"],
    q=4,
    labels=["Low", "Medium", "High", "Critical"],
)

# KPI.
col1, col2, col3, col4 = st.columns(4)

# Widget for KPI.
col1.metric("Total contracts", len(scores_df))
col2.metric("Mean risk score", round(scores_df["risk_score"].mean(), 1))
col3.metric("Max risk score", int(scores_df["risk_score"].max()))

# Calculating the share of contracts with a risk score above average.
share_above_mean = (scores_df["risk_score"] > scores_df["risk_score"].mean()).mean() * 100
col4.metric("Above-average share", f"{share_above_mean:.1f}%")

st.divider()

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Clause Frequency",
    "Risk Concentration",
    "Risk Tiers",
    "Riskiest Contracts",
])

# --- Tab 1: clause frequency
with tab1:
    st.subheader("Most common clauses across all 510 contracts")
    st.write(
        "Frequency alone does not indicate risk - see the Risk Concentration tab "
        "for which clauses actually correlate with high-risk contracts."
    )

    # Slider for selecting the number of Top rows.
    top_n_freq = st.slider("Number of clauses to show", min_value=5, max_value=30, value=15)

    # We sort top N rows (freq_df was previously sorted in risk_analysis.py) again so that the dasboard doesn't depend
    # on the CSV order not changing in the future.
    top_freq = freq_df.sort_values("share_present_pct", ascending=False).head(top_n_freq)

    # Bar Chart
    st.bar_chart(top_freq.set_index("clause")["share_present_pct"], horizontal=True)
    st.dataframe(top_freq, use_container_width=True, hide_index=True)

# --- Tab 2: risk concentration (gap and lift) ---
with tab2:
    st.subheader("Which clauses are over-represented in high-risk contracts")

    # Switch with multiple options.
    metric_choice = st.radio(
        "Rank clauses by:",
        options = ["Gap (percentage points)", "Lift (relative multiplier)"],
        horizontal=True, # We arrange the options in a row, not in a column.
    )

    if metric_choice == "Gap (percentage points)":
        display_df = concentration_df.sort_values("gap_pct_points", ascending=False).head(10)
        y_col = "gap_pct_points"
        st.caption(
            "Gap = share of contracts with this clause in the top-15 minus share overall. "
            "Favors clauses that are almost universal in high-risk contracts."
        )
    else:
        display_df = lift_df.sort_values("lift", ascending=False).head(10)
        y_col = "lift"
        st.caption(
            "Lift = how many times often the clauses appears in the top-15 vs. overall. "
            "Favors rare-but-concentrated clauses - a stronger early-warning signal."
        )

    st.bar_chart(display_df.set_index("clause")[y_col], horizontal=True)
    st.dataframe(display_df, use_container_width=True, hide_index=True)

# --- Tab 3: risk tiers ---
with tab3:
    st.subheader("Contracts grouped into quartile-based risk tiers")

    # Summary table (average and quantity for each tier).
    st.dataframe(tiers_df, use_container_width=True, hide_index=True)

    # We recalculate the number of contracts per tier from score_df
    # (with the recalculated tier at the contract level) and usr in
    # for the graph.
    tier_counts = scores_df["risk_tier"].value_counts().reindex(
        ["Low", "Medium", "High", "Critical"] # We fix the order of bars using reindex.
    )

    st.bar_chart(tier_counts)

    st.divider()
    st.write("**Browse contracts within a specific tier:**")

    # Drop-down list with one choice.
    selected_tier = st.selectbox("Select tier", options=["Low", "Medium", "High", "Critical"])

    # Filter the contracts table by the selected tier.
    filtered_by_tier = scores_df[scores_df["risk_tier"] == selected_tier].sort_values(
        "risk_score", ascending=False
    )
    st.dataframe(filtered_by_tier, use_container_width=True, hide_index=True)

# --- Tab 4: "Riskiest Contracts" ---
with tab4:
    st.subheader("Explore contracts by risk score")

    min_score = int(scores_df["risk_score"].min())
    max_score = int(scores_df["risk_score"].max())

    # Range slider with two values.
    score_range = st.slider(
        "Filter by risk score range",
        min_value=min_score,
        max_value=max_score,
        value=(min_score, max_score), # Starting position - full range.
    )

    # Filter the table: leave only contracts within the selected range.
    filtered = scores_df[scores_df["risk_score"].between(*score_range)].sort_values("risk_score", ascending=False)

    st.write(f"Showing {len(filtered)} of {len(scores_df)} contracts")
    st.dataframe(filtered, use_container_width=True, hide_index=True)

    # Button to download the filtered file.
    st.download_button(
        label="Download filtered contracts as CSV",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="filtered_contracts.csv",
        mime="text/csv",
    )

# Footer with methodological information.
st.divider()
st.caption(
    "Risk scores are computed from expert-assigned weights (1-10 for risky clauses, "
    "negative weight for protective clauses like Cap On Liability). "
    "A score of 0 means no flagged clauses; negative scores indicate a net-protective "
    "contract. Full methodology and limitations: see README.md in the repository."
)
