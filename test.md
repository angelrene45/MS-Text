Do you have an example or recommended approach for using Snowflake Cortex AI Observability with Cortex Analyst or Cortex Agents from an interactive application such as Streamlit?

We’ve read the documentation, but it focuses on batch evaluations using TruApp.run(). In our case, we need to capture traces from a real-time user interface and still send them to Observability for monitoring and auditability.

Is it currently possible to emit traces from individual LLM agent calls (e.g., answer_query()) without a full evaluation run? If so, could you share a pattern, example, or best practice for this type of use case?
