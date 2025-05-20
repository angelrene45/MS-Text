Cortex Analyst – Challenges and Next Steps

Challenges

Interprets same question differently on subsequent runs. May also return different columns in result.

In some cases, the Cortex Analyst makes assumptions if there is ambiguity; in other cases, asks for more information. Should strictly ask for more information if there is ambiguity

Non-Determinism / Ambiguity

Learnings / Potential Mitigations

Can partly be improved via metadata and custom instructions.

For an API client (HR CRM use case), can pre-process user question to strictly define expected columns. May need to use the completions API to pre-process question (query expansion) prior to calling Cortex Analyst.

User question may be arbitrary and don’t want to provide the wrong answer. May need to define “golden questions” that the Analyst can answer which can regression tested for each release and built upon.

Invalid SQL

Syntax errors in generated SQL – wrong/missing aliases, selecting fields from tables where they don’t exist

Next Steps

Add more metadata; expand to medium complexity and difficult questions

Work with Snowflake to integrate the Cortex Search service into Analyst
