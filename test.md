# ✅ Best Practices: Building a Semantic Model with Snowflake Cortex Analyst

## 📌 Context
Over the past few months, our engineering and analyst teams have been exploring the **Snowflake Cortex Analyst** and its capabilities to enable **Text-to-SQL** for self-service analytics. As part of this initiative, we implemented a **POC (Proof of Concept)** using real data from various domains such as CRM, Research Reports, and vendor platforms like Visible Alpha.

---

## 🧠 Cortex Analyst Semantic Model Calibration

> _The heart of any Text-to-SQL system is a calibrated and aligned semantic model._

The process of calibrating the semantic model involves a **cyclical, iterative workflow**, ensuring alignment between the data schema, domain-specific language, and validated SQL queries. Below is the calibration loop we followed:

![Semantic Model Calibration](attachment:23937a03-60e8-4009-bd4b-ff263a400bb3.png)

### Calibration Loop:
1. **Semantic Model Description**: Define key entities, metrics, and relationships in business terms.
2. **DB Schema Mapping**: Align semantic descriptions with physical Snowflake schema (tables, views).
3. **Cortex Search Integration**: Enable literal search over metadata to improve grounding.
4. **Custom Instructions**: Tailor the analyst behavior to handle domain-specific vocabulary and intent.
5. **Verified Queries**: Validate generated SQL outputs with SMEs and QA feedback.
6. **Re-calibrate**: Update semantic models based on verified feedback and improve the loop.

---

## 🧪 Key Learnings from the Text-to-SQL POC

![Snowflake Cortex Analyst POC](attachment:361bfb65-4cdd-)
