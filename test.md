# ADR-004: Observability Approach for Semantic Models Wrapper API

**Status:** Draft  
**Date:** 2025-08-10  
**Review Level:** Department (Architecture + Observability Teams)  
**Decision Makers:** [Your Name] (Developer / Technical Lead), [Observability Lead], [Data Platform Lead]  
**Consulted:** Runway Team, Platform Observability Team, Research Department  

---

## Context & Problem Statement

The Semantic Models Wrapper API requires observability and evaluation capabilities to track:
- API request/response traces (latency, metadata, SQL queries)
- Evaluation metrics (faithfulness, groundedness, semantic similarity)
- End-user feedback

**Current Dev Setup:**  
We use **TruLens Dashboard** (Streamlit app) integrated with our API. It stores traces, evaluations, and feedback in **Snowflake tables** automatically created by the dashboard.

**Production Constraints:**
1. **Authentication:** TruLens Dashboard only supports password-based Snowflake authentication. Corporate policy requires keypair or OIDC — passwords are prohibited.
2. **Table Creation:** In production, only **Runway** provisioning pipelines can create Snowflake objects. TruLens dashboard's dynamic table creation is non-compliant.
3. **Deployment:** TruLens dashboard (Streamlit) cannot be deployed in our controlled production runtime without significant changes.

These constraints require us to decide on an **observability approach** that works in both Dev and Prod, meeting compliance and operational requirements.

---

## Decision Drivers

- **Compliance:** Must use approved authentication methods (keypair/OIDC).  
- **Governance:** No self-created Snowflake tables in production.  
- **Integration:** Prefer alignment with corporate observability stack (OTEL, Tiempo, Cortex, Grafana).  
- **Developer productivity:** Minimal additional overhead for evaluations in Dev.  
- **User experience:** Ability to visualize metrics and traces easily.

---

## Considered Options

### Option A – TruLens Dashboard (Current Dev Approach)
Use TruLens' built-in Streamlit dashboard and Snowflake storage.

**Pros:**
- Immediate, out-of-the-box visualization.
- No custom dashboard work required.
- Tight integration with TruLens evaluations.

**Cons:**
- Non-compliant authentication method.
- Self-creates Snowflake tables (not allowed in Prod).
- Cannot be deployed in Prod without significant rework.
- Dependent on Streamlit runtime (unsupported in Prod).

---

### Option B – TruLens with OTEL Integration → Corporate Observability
Configure TruLens to send metrics and traces via **OpenTelemetry (OTEL)** to the corporate OTEL collector. Store data in Tiempo/Cortex and visualize via Grafana.

**Pros:**
- Fully compliant with firm authentication and provisioning policies.
- Uses existing observability stack and Grafana dashboards.
- Unified view of API and infrastructure metrics.
- No Snowflake table creation from the API.

**Cons:**
- Requires engineering effort to configure OTEL exporter.
- Custom Grafana dashboard development needed.
- Schema alignment with corporate OTEL required.

---

## Pros and Cons of the Options

| Option | Pros | Cons |
|--------|------|------|
| **A – TruLens Dashboard** | Quick setup, native integration | Non-compliant, table creation issues, unsupported deployment |
| **B – TruLens + OTEL** | Compliant, integrates with existing stack, scalable | More setup effort, requires dashboard development |

---

## Decision Outcome

**Chosen Option:** **B – TruLens with OTEL Integration**  
We will:
- Keep **Option A** for Dev/QA to leverage TruLens’ native dashboard for quick feedback loops.
- For **Production**, configure TruLens to send data to OTEL, store it in Tiempo/Cortex, and create Grafana dashboards.
- Coordinate with Runway and Observability teams for provisioning and schema alignment.

---

## Consequences

- **Positive:** Compliance with authentication and provisioning policies; integration with approved observability tools; single pane of glass for monitoring API and models.  
- **Negative:** Additional upfront engineering work to configure OTEL exporters and develop dashboards.  
- **Follow-ups:**  
  - Engage Runway for Snowflake provisioning in Dev/QA.  
  - Work with Observability team to define OTEL metric schema.  
  - Schedule Grafana dashboard build.

---

## Supporting Documents

- [TruLens OTEL Integration Docs](https://www.trulens.org)  
- [Corporate Observability Standards](/link/to/internal/standards)  
- [Runway Provisioning Guidelines](/link/to/internal/runway-docs)  
