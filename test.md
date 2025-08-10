# ISG Solution Architecture Description – Semantic Models Wrapper API

**Business Function:** *Self-service analytics Q&A over governed data*  
**Business Owner:** [TBD]  
**ITSO:** [TBD]  
**Cloud Captain / Delegate:** [TBD]  
**Super Department:** [TBD]  
**Super Department Head:** [TBD]  
**Ecosystem Name(s):** AskAI Marketplace, Snowflake Platform

---

## 1. Executive summary

### 1.1 Overview
Business users need insights without writing SQL or knowing schemas. The **Semantic Models Wrapper API** exposes **Snowflake Cortex Analyst** semantic models via **FastAPI** and **OpenAPI**, so **AskAI** (the corporate agentic frameworks marketplace) can act as the conversational UI. Users select and enable agents (incl. ours) in AskAI; our service turns natural-language questions into governed SQL and returns answers with evidence.

### 1.2 High-level business goals
- Reduce time-to-insight for business questions from hours/days to minutes.
- Scale self-service analytics without increasing BI backlog.
- Enforce governed access to data (least privilege, masking, CLS/RLS).

### 1.3 High-level cloud business goals (if any)
- Consolidate analytics usage on Snowflake; control spend with resource monitors.
- Standardize UI on AskAI marketplace (multi-agent discovery, single entry point).

### 1.4 High-level technology goals
- OpenAPI-first contract; OIDC-based authN/Z; auditable requests and traces.
- Repeatable, compliant deployments via **WebstaX → Treadmill** with **Train + UpLIFT**.
- Measurable answer quality (TruLens) and SLOs (latency, error rate, cost/session).

---

## 2. Requirements

### 2.1 Business function or ecosystem
Self-service Q&A over curated semantic models (Sales, Customers, Products, etc.) using AskAI as the end-user channel. Our team owns the API, semantic guardrails, and integration with Snowflake Cortex Analyst. AskAI (another department) owns the UI, agent registry and user enablement.

### 2.2 Business functional requirements
- NL questions → relevant SQL over approved semantic models.
- Optional “review & execute” mode exposing generated SQL for approval.
- Metadata endpoints for model discovery (tables, measures, joins, synonyms).
- Multi-agent marketplace: agent can be enabled/disabled per user/team.
- Auditable outcomes (question hash, tables used, trace id), no PII in logs.

### 2.3 Architecturally significant constraints
- Identity via **OIDC/JWT**; scopes per domain (`semantic:ventas.read`, …).
- Snowflake access by **key-pair** with least-privilege roles, CLS/RLS, masking.
- Corporate runtime: **LBv3 → httpd ADC → Treadmill**; deployments with **WebstaX**.
- OpenAPI contract published and versioned; AskAI consumes our spec.
- Observability via APM/logs + **TruLens** for answer quality KPIs.

### 2.4 Salient cross-functional requirements (quantified where possible)

| Category | Requirement | Value (Initial Target) |
|---|---|---|
| **Usability** | AskAI UI responsiveness | Managed by AskAI; our API p95 ≤ **3s** E2E at expected load |
| **Reliability** | Availability (API) | **99.9%** (initial), excluding planned maintenance |
|  | RTO | **4 hours** |
|  | RPO | **1 hour** |
|  | MTTR | **1 hour** (S1) |
| **Performance** | Responsiveness & scalability | p95 ≤ **3s** at **10 RPS** steady; burst **25 RPS** (autoscale 2→4 pods) |
|  | Throughput | Typical query result ≤ **5 MB**; pagination for larger |
|  | Latency budgets | Gateway < API < Cortex < Snowflake (timeouts escalonados) |
|  | Efficiency | Cost/session ≤ **$K TBD**; warehouse auto-suspend/resume |
| **Data protection** | Integrity | ACID at Snowflake; `QUERY_TAG` for traceability |
|  | Classification & privacy | **Confidential – Internal**; PII possible in sources → masking + CLS/RLS |
|  | Retention, auditability | Request/trace logs **30 days**; summaries/metrics **90 days** |
| **Security** | Authentication | OIDC (SSO/JWT); token validation at ADC/API |
|  | Authorization | Scopes per model; row/column policies in Snowflake |
|  | Provisioning | WebstaX for LB/CLM/OIDC; role grants via infra-as-code |
| **Supportability** | Reusability/Integrability | OpenAPI, versioned; agent registration in AskAI |
|  | Testability | Contract tests; golden prompts suite; perf & chaos tests |
|  | Observability | OTel traces; Trulens metrics (answer/sql relevance, groundedness) |

---

## 3. Current state architecture

### 3.1 Current state logical view
- Ad-hoc SQL and traditional BI dashboards; limited follow-up Q&A.
- Multiple teams duplicating simple NL→SQL POCs; no shared marketplace.
- Manual data access patterns; inconsistent masking and query tagging.

---

## 4. Target state architecture

### 4.1 Logical view
Use C4 logical diagram and annotate: **`docs/architecture/high-level-architecture-askai.puml`**  
**Shows:**
- End User → AskAI (agent marketplace) → Wrapper API → Cortex Analyst → Snowflake.  
- Identity (OIDC), Observability (APM/TruLens), governance boundaries.

### 4.2 Data view
Use C4 logical data flow (can be a note on the same diagram):
- **Data objects**: Questions (hash only), Semantic metadata, Result sets (tabular/aggregations), SQL (optional, for review).  
- **Authorities**: Snowflake is the system of record; API is a stateless orchestrator.  
- **Classification & protection**: Sources may include PII → masking & policies; in-transit TLS; at-rest encryption managed by Snowflake.  
- **On-prem vs cloud**: N/A or [TBD]. Emphasize no raw data leaves Snowflake; API handles orchestration only.

### 4.3 Deployment view
Diagram: **`docs/architecture/application-runtime-deployment.puml`**  
- **Scale**: 2–4 replicas (HPA) of FastAPI behind httpd ADC and LBv3.  
- **Resilience**: Pod restarts, rolling updates; circuit breaker & retries to Cortex.  
- **Replication**: None for API state (stateless); data consistency guaranteed by Snowflake.

### 4.4 Security view
- **Access management**: OIDC/JWT; scopes per model; group mapping (LDAP/IdP).  
- **Identity management**: Token lifetime and refresh per corporate policy.  
- **Cloud specifics**: Certificates via CLM; network policies; possible PrivateLink to Snowflake (if available).  
- **App-level guardrails**: allowlist of schemas, prompt hygiene, size/time limits, `QUERY_TAG`.

---

## 5. Interim states (if any)
- **Phase 0 (POC)**: Streamlit UI for internal testing only (no external users).  
- **Phase 1 (MVP)**: AskAI integration (agent registration), single domain (e.g., Sales), “auto-execute” with safe filters.  
- **Phase 2 (Scale)**: Additional domains; “review & execute” option for sensitive models; FinOps dashboards; PrivateLink (if applicable).

---

## 6. Related ADRs
- **ADR-001** – Frontend Integration with AskAI (`docs/architecture-decisions/adr-001-askai.md`)  
- **ADR-002** – Deployment Stack: WebstaX vs Podman/Treadmill (`docs/architecture-decisions/adr-002-deployment-stack.md`)  
- **ADR-003** – Wrapper API over direct AskAI→Cortex Analyst (planned)

---

## 7. Related Cloud Pipelines
- **Train** – CI build/test job (unit, contract, SAST)  
- **UpLIFT** – Image/package promotion and registry  
- **WebstaX** – Provisioning (TAM validation, CLM, LBv3, OIDC) & deployment to **Treadmill**

---

## 8. Additional information

### 8.1 Challenges & lessons learnt (if any)
- NL ambiguity requires good synonyms and examples in semantic models.  
- Early perf tests show long-tail latency dominated by warehouse cold starts → mitigate with schedules/warmers.

### 8.2 Assessments conducted
- [SD review] – [link]  
- **SecArch (mandatory)** – [link]  
- [Dept/Platform reviews] – [link]

---

## 9. Alignment with ISG Architecture Principles

| Theme | Principle | Aligned (Y/N/NA) | Rationale |
|---|---|:--:|---|
| Business Enablement | Base technology decisions on business value | **Y** | AskAI marketplace reduces time-to-insight; reusable API |
| Security | Build appropriate security controls | **Y** | OIDC, CLS/RLS, masking, WAF/rate-limit, TLS, audit |
| Common Solutions | Prefer common platforms/patterns | **Y** | AskAI marketplace, WebstaX, Treadmill, Snowflake |
| Simplicity | Keep architecture simple/evolvable | **Y** | Stateless API, clear boundaries, OpenAPI contract |
| Modern & Evergreen | Use current standards | **Y** | FastAPI, OpenAPI, OIDC, IaC pipelines |
| Minimize Technical Debt | Enable future extension/modernization | **Y** | Versioned APIs, semantic model governance, ADR log |
| Data – Quality | Ensure accuracy & governance | **Y** | Semantic models, `QUERY_TAG`, audits |
| Data – Security & Privacy | Manage PII/Confidential data | **Y** | CLS/RLS/masking, no raw data leaves Snowflake |
| Data Lifecycle | Manage data through lifecycle | **Y** | Retention policies for logs/metrics; data at source |
| Data Architecture | Scalability, resilience, effectiveness | **Y** | Warehouse sizing, autoscaling API, resource monitors |
| Reliability/Resilience/Recovery | Meet SLOs & DR objectives | **Y** | 99.9% availability, RTO 4h, RPO 1h, autoscaling |
| Technology Practices | Maintain documentation | **Y** | Docs repo with ADRs, C4 diagrams, OpenAPI |

---

## 10. Risk Profile

| # | Description | Mitigation | Owner | Target date |
|---|---|---|---|---|
| R1 | Dependency on AskAI roadmap / agent marketplace changes | Versioned OpenAPI; consumer-driven contract tests; joint release calendar | PO / Integration Lead | [TBD] |
| R2 | Cost spikes on Snowflake (heavy/long queries) | Resource monitors, warehouse sizing, query limits, pagination, caching metadata | Data Lead | [TBD] |
| R3 | Prompt injection / over-permissive SQL | Guardrails, allowlist schemas, enforced filters, review-and-execute for sensitive domains | Backend Lead | [TBD] |
| R4 | Token/OIDC misconfig in runtime | WebstaX templates; pre-prod penetration test; ADC policy checks | Platform Sec | [TBD] |
| R5 | Schema/semantic drift breaking answers | Golden prompts regression, CI validations, semantic versioning | Data Lead | [TBD] |

---

### Appendix – Optional

**A1. Architectural triggers (checklist):**
- Introduction of new agent on corporate marketplace ✅  
- New containerized API on platform runtime ✅  
- Use of strategic technologies (Snowflake Cortex Analyst, WebstaX) ✅

**A2. Ecosystem**
- **Diagram**: see `docs/architecture/high-level-architecture-askai.puml`  
- **Associated applications**: AskAI, Wrapper API, Snowflake/Cortex Analyst, IdP, Observability stack

---

### Diagrams (C4 references)
- **Context (with AskAI):** `docs/architecture/high-level-architecture-askai.puml`  
- **Runtime & Deployment:** `docs/architecture/application-runtime-deployment.puml`  
