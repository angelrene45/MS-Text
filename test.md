from pathlib import Path

# Create a Python script with a production-grade, observable version of ResearchDataAssistantWithObservability
code = """
from trulens.otel import instrument
from trulens.otel.semconv.trace import SpanAttributes
import logging

logger = logging.getLogger(__name__)

class ResearchDataAssistantWithObservability:

    def __init__(self, semantic_models, host, api_endpoint, env_name, proxies):
        self.semantic_models = semantic_models
        self.host = host
        self.api_endpoint = api_endpoint
        self.env_name = env_name
        self.proxies = proxies

    @instrument(span_type=SpanAttributes.SpanType.GENERATION)
    def generate_sql(self, question: str) -> dict:
        try:
            response = query_cortex_analyst(
                user_message=question,
                semantic_models=self.semantic_models,
                host=self.host,
                api_endpoint=self.api_endpoint,
                env_name=self.env_name,
                proxies=self.proxies
            )

            response_json = response.json()
            logger.info(f"Received response from Cortex Analyst: {response_json}")

            content_items = response_json.get("message", {}).get("content", [])
            sql_statement = None
            verified_query_info = None

            for item in content_items:
                if item.get("type") == "sql":
                    sql_statement = item.get("statement")
                    verified_query_info = item.get("confidence", {}).get("verified_query_used_", {})

            return {
                "sql": sql_statement,
                "response_json": response_json,
                "verified_query": verified_query_info
            }
        except Exception as e:
            logger.error(f"Error in generate_sql: {e}")
            return {"sql": None, "error": str(e), "response_json": {}}

    @instrument(span_type=SpanAttributes.SpanType.INVOCATION)
    def execute_sql(self, sql: str) -> tuple[str, bool]:
        if not sql:
            logger.warning("No SQL to execute.")
            return "-- No SQL provided", False
        try:
            df_response = get_query_exec_result(sql)
            return str(df_response), True
        except Exception as e:
            logger.error(f"SQL execution failed: {e}")
            return str(e), False

    @instrument(span_type=SpanAttributes.SpanType.RECORD_ROOT,
                attributes={
                    SpanAttributes.RECORD_ROOT.INPUT: "question",
                    SpanAttributes.RECORD_ROOT.OUTPUT: "return"
                })
    def answer_query(self, question: str) -> dict:
        logger.info(f"Processing question: {question}")

        result_gen = self.generate_sql(question)
        sql = result_gen.get("sql")
        verified_query = result_gen.get("verified_query")
        response_json = result_gen.get("response_json")

        result_exec, success = self.execute_sql(sql)

        return {
            "question": question,
            "sql": sql,
            "sql_execution_success": success,
            "query_result": result_exec,
            "verified_query": verified_query,
            "cortex_response": response_json
        }
"""

path = Path("/mnt/data/assistant_observable_sql_app.py")
path.write_text(code)
path
