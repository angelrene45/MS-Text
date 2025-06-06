import pandas as pd
import uuid
from datetime import datetime
import random
import hashlib

# ----------------------------------------
# CONFIGURATION
# ----------------------------------------
RUNS_PER_QUESTION = 5
DATASET_VERSION = "v1"

# ----------------------------------------
# UTILITY: Normalize and hash a DataFrame
# ----------------------------------------
def normalize_and_hash_dataframe(df1: pd.DataFrame, df2: pd.DataFrame) -> tuple:
    """
    Takes two DataFrames and:
    - Identifies union of all columns
    - Adds missing columns as None
    - Normalizes and sorts rows
    - Returns both hashes and warning if any columns are missing
    """
    all_columns = sorted(set(df1.columns).union(set(df2.columns)))

    # Fill missing columns
    for col in all_columns:
        if col not in df1.columns:
            df1[col] = None
        if col not in df2.columns:
            df2[col] = None

    df1 = df1[all_columns]
    df2 = df2[all_columns]

    def hash_df(df):
        df = df.applymap(lambda x: str(round(x, 2)) if isinstance(x, float) else str(x))
        df = df.sort_values(by=all_columns).reset_index(drop=True)
        return hashlib.sha256(df.to_csv(index=False).encode()).hexdigest()

    return hash_df(df1), hash_df(df2)

# ----------------------------------------
# SIMULATED Cortex + SQL response
# ----------------------------------------
def simulate_sql_execution(sql_text: str) -> pd.DataFrame:
    """Returns a simulated resultset as a DataFrame"""
    base = [
        {"company_name": "A", "total": 100},
        {"company_name": "B", "total": 80},
        {"company_name": "C", "total": 60}
    ]
    # Occasionally remove or add a column to simulate model variability
    if "WITH" in sql_text:
        for row in base:
            row.pop("total", None)  # simulate missing column
    if "NULL" in sql_text:
        for row in base:
            row["region"] = "North"  # simulate extra column
    return pd.DataFrame(base)

def simulate_cortex_response(question: str, run_id: str) -> dict:
    interpretations = [
        "Top 7 companies with most interactions, excluding unspecified",
        "Top interacting companies excluding nulls",
        "Companies ranked by number of interactions"
    ]
    sql_variants = [
        "SELECT company_name, COUNT(*) AS total FROM fct_interactions WHERE company_name <> 'UNSPECIFIED' GROUP BY 1 ORDER BY 2 DESC LIMIT 7",
        "WITH clean AS (SELECT * FROM fct_interactions WHERE company_name <> 'UNSPECIFIED') SELECT company_name FROM clean GROUP BY 1 ORDER BY COUNT(*) DESC LIMIT 7",
        "SELECT company_name, COUNT(*) total FROM fct_interactions WHERE company_name IS NOT NULL AND company_name != 'UNSPECIFIED' GROUP BY company_name ORDER BY total DESC LIMIT 7"
    ]

    used_verified_query = random.choice([True, False])
    interpretation = random.choice(interpretations)
    sql_statement = random.choice(sql_variants)
    result_df = simulate_sql_execution(sql_statement)

    return {
        "run_id": run_id,
        "timestamp": datetime.now(),
        "dataset_version": DATASET_VERSION,
        "question": question,
        "interpretation": interpretation,
        "sql_statement": sql_statement,
        "used_verified_query": used_verified_query,
        "result_df": result_df,
        "request_id": str(uuid.uuid4())
    }

# ----------------------------------------
# TEST SETUP: Questions and execution
# ----------------------------------------
questions = [
    "Top 7 companies with the most interactions",
    "How many interactions did each employee have?"
]

# Run Cortex multiple times per question
executions = []
for q in questions:
    for i in range(RUNS_PER_QUESTION):
        run_id = f"{q[:20]}_{i+1}"
        executions.append(simulate_cortex_response(q, run_id))

# Build full table
rows = []
for i in range(len(executions)):
    current = executions[i]
    for j in range(i + 1, len(executions)):
        if executions[j]["question"] != current["question"]:
            continue
        hash1, hash2 = normalize_and_hash_dataframe(current["result_df"], executions[j]["result_df"])
        consistent = hash1 == hash2

        rows.append({
            "question": current["question"],
            "run_id_1": current["run_id"],
            "run_id_2": executions[j]["run_id"],
            "hash_1": hash1,
            "hash_2": hash2,
            "is_semantically_consistent": consistent
        })

# ----------------------------------------
# Display final report
# ----------------------------------------
comparison_df = pd.DataFrame(rows)

import ace_tools as tools; tools.display_dataframe_to_user(name="Pairwise Semantic Consistency Report", dataframe=comparison_df)
