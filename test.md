# Project Documentation – Semantic Models Wrapper API

Welcome to the official documentation for the **Semantic Models Wrapper API** project.  
This project provides a backend service that exposes **Snowflake Cortex Analyst semantic models** through a **FastAPI wrapper** with **OpenAPI specifications**, enabling integration with the corporate **AskAI agentic frameworks marketplace**.

---

## 📌 Overview
- **Goal**: Allow business users to query semantic models using natural language through a conversational UI (AskAI), without needing SQL knowledge.
- **Frontend**: Provided by AskAI (agent marketplace), enabling users to select and activate agents.
- **Backend**: FastAPI service applying OIDC authentication, guardrails, and integration with Cortex Analyst.
- **Deployment**: Automated through WebstaX (Treadmill + UpLIFT + LBv3 + CLM).

---

## 📂 Documentation Structure

| Section | Description |
|---------|-------------|
| [Architecture Decisions](architecture-decisions/) | All Architecture Decision Records (ADRs) explaining major technical choices. |
| [Developer Guide](developer-guide/) | Technical documentation for setting up, running, and contributing to the backend service. |
| [User Guide](user-guide/) | Step-by-step instructions for end users to use the POC via the Streamlit interface. |
| [Assets](assets/) | Diagrams, screenshots, and visual references used in the documentation. |

---

## 🚀 Quick Links
- **Latest ADRs**: [View ADRs](architecture-decisions/)  
- **Developer Setup**: [Read the Developer Guide](developer-guide/)  
- **Using the POC**: [Open the User Guide](user-guide/)  

---

## 📄 Related Resources
- [Snowflake Cortex Analyst Documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex-analyst)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAPI Specification](https://swagger.io/specification/)

---

_Last updated: YYYY-MM-DD_
