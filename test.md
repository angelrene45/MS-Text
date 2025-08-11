# Production Go Live Plan & Architecture Design

## 1. Code Management & DevSecOps
**Technologies:** GitHub, Jenkins Pipelines, SonarQube, Snyk, MkDocs Material  
**Description:**  
- Centralized source code management in GitHub.  
- CI/CD automation using Jenkins, including build, test, and controlled deployments.  
- Integration with SonarQube and Snyk to ensure code quality and security.  
- Project documentation maintained with MkDocs Material.  

---

## 2. DevOps & Deployment
**Technologies:** WebstaX (TAM, CLM, LoadBalancer), Podman, UpLIFT, Treadmill  
**Description:**  
- Backend containerization with Podman.  
- Image publishing to UpLIFT.  
- Deployment on Treadmill with load balancing and SSL certificates managed by CLM.  
- WebstaX recommended by the platform team for streamlined environment management.  

---

## 3. Automated Testing & Evaluation
**Technologies:** TruLens  
**Description:**  
- Automated evaluations on each build or pull request.  
- Metrics include: Final Answer Relevance, Interpretation Accuracy, SQL Relevance, Summarization Groundedness.  
- Thresholds set to detect improvements or regressions per version.  
- Integration with CI/CD pipelines for continuous quality validation.  

---

## 4. Backend API
**Technologies:** FastAPI, Snowflake Cortex Analyst  
**Description:**  
- Backend built with FastAPI, exposing REST APIs on top of Cortex Analyst.  
- Secure Snowflake connection using key pair authentication.  
- Automatic API documentation via OpenAPI/Swagger.  
- Access control through OIDC and corporate LDAP group validation.  

---

## 5. Frontend & User Experience
**Technologies:** AskAI (primary option), Streamlit (POC alternative)  
**Description:**  
- Integration with AskAI agent marketplace to register backend as an OpenAPI agent.  
- Conversational interface for end users, allowing them to enable or disable models from a list.  
- For development or demo purposes, a Streamlit UI can be used as an alternative.  

---

## 6. Observability
**Technologies:** TruLens Dashboard (Dev/QA), OpenTelemetry + Grafana (Prod)  
**Description:**  
- In Dev/QA, TruLens Dashboard is used to visualize evaluation scores and traces in real time.  
- In Prod, metrics and traces sent to an OpenTelemetry collector, stored in approved systems (Tiempo, Cortex) and visualized in Grafana dashboards.  
- Monitoring latency, errors, usage, and estimated costs for operational and financial tracking.  

---

## 7. Data Platform
**Technologies:** Snowflake, Cortex Analyst  
**Description:**  
- Semantic models managed and versioned in Snowflake Runway.  
- Security policies including Row-Level Security (RLS), Column-Level Security (CLS), and data masking.  
- Use of tags and resource monitors for cost control.  

---

## 8. Rollout & Deployment Strategy
**Approach:**  
- Gradual rollout (canary release), starting with a small percentage of traffic before full adoption.  
- Fast rollback controls using previous backend image versions.  
- Pre-production validation with real data and scenarios before go-live.  
