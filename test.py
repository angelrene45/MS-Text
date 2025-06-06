import pandas as pd
import uuid
from datetime import datetime
import random
import hashlib

# -----------------------------
# Configurable parameters
# -----------------------------
RUNS_PER_QUESTION = 5
DATASET_VERSION = "v1"  # Useful for tracking which data snapshot was used

# -----------------------------
# Simulated Cortex Analyst response and resultset
# -----------------------------
def simulate_sql_execution(sql_text: str) -> list:
    """Simulates SQL execution and returns a consistent mock resultset"""
    base_rows = [
        {"company_name": "A", "total": 100},
        {"company_name": "B", "total": 80},
        {"company_name": "C", "total": 60}
    ]
    if "WITH" in sql_text:
        base_rows[-1]["total"] += 1  # Minor tweak to simulate slight differences
    return base_rows

def compute_result_hash(rows: list) -> str:
    """Computes a hash of the query resultset to compare semantic equality"""
    hasher = hashlib.sha256()
    for row in sorted(rows, key=lambda r: str(r)):
        row_string = "|".join(str(v) for v in row.values())
        hasher.update(row_string.encode("utf-8"))
    return hasher.hexdigest()

def simulate_cortex_response(question: str, run_id: str) -> dict:
    interpretations = [
        "This is our interpretation of your question: Top 7 companies with the most interactions, excluding unspecified companies",
        "We interpreted your request as retrieving the top 7 companies by total number of interactions",
        "Fetching top 7 companies by interactions, excluding NULL or unspecified companies"
    ]
    sql_variants = [
        "SELECT company_name, COUNT(*) AS total FROM fct_interactions WHERE company_name <> 'UNSPECIFIED' GROUP BY 1 ORDER BY 2 DESC LIMIT 7",
        "WITH clean_data AS (SELECT * FROM fct_interactions WHERE company_name <> 'UNSPECIFIED') SELECT company_name, COUNT(*) AS total FROM clean_data GROUP BY 1 ORDER BY 2 DESC LIMIT 7",
        "SELECT company_name, COUNT(*) total FROM fct_interactions WHERE company_name IS NOT NULL AND company_name != 'UNSPECIFIED' GROUP BY company_name ORDER BY total DESC LIMIT 7"
    ]
    used_verified_query = random.choice([True, False])
    interpretation = random.choice(interpretations)
    sql_statement = random.choice(sql_variants)
    result_rows = simulate_sql_execution(sql_statement)
    result_hash = compute_result_hash(result_rows)

    return {
        "run_id": run_id,
        "timestamp": datetime.now(),
        "dataset_version": DATASET_VERSION,
        "question": question,
        "interpretation": interpretation,
        "sql_statement": sql_statement,
        "used_verified_query": used_verified_query,
        "result_hash": result_hash,
        "request_id": str(uuid.uuid4())
    }

# -----------------------------
# List of questions to evaluate
# -----------------------------
questions = [
    "Top 7 companies with the most interactions",
    "How many interactions did each employee have?"
]

# -----------------------------
# Execute the evaluation
# -----------------------------
all_results = []
for q in questions:
    for i in range(RUNS_PER_QUESTION):
        run_id = f"{q[:20]}_{i+1}"
        all_results.append(simulate_cortex_response(q, run_id))

df = pd.DataFrame(all_results)

# -----------------------------
# Semantic metrics summary
# -----------------------------
summary = (
    df.groupby("question")
    .agg(
        total_runs=('run_id', 'count'),
        distinct_sqls=('sql_statement', 'nunique'),
        distinct_result_hashes=('result_hash', 'nunique'),
        verified_query_uses=('used_verified_query', 'sum')
    )
    .assign(
        verified_use_rate=lambda x: round(x["verified_query_uses"] / x["total_runs"] * 100, 1),
        is_semantically_consistent=lambda x: x["distinct_result_hashes"] == 1
    )
    .reset_index()
)

# -----------------------------
# Display results
# -----------------------------
import ace_tools as tools; tools.display_dataframe_to_user(name="Raw Analyst Results with Hashes", dataframe=df)
tools.display_dataframe_to_user(name="Semantic Summary per Question", dataframe=summary)
