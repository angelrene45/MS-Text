# Prod Go-Live & Architecture Design – Semantic Models Wrapper API

**Date:** 2025-08-10  
**Audience:** Architecture Review Board, Observability Team, Runway Team, Research Dept.

---

## 1. Executive Summary

The Semantic Models Wrapper API enables business users to query governed Snowflake semantic models using natural language, via **Cortex Analyst**, without writing SQL.  
Integration with **AskAI** provides a marketplace-based UI for model access, allowing users to enable our agent from a list.

**Goals:**
- Natural language → SQL → governed datasets.
- Secure, compliant, observable.
- Production-grade deployment with rollback.

---

## 2. Problem & Business Goals

**Current challenges:**
- Users rely on BI backlog; no self-service for ad-hoc questions.
- Lack of natural language interface for semantic models.
- UI development would delay delivery.

**Objectives:**
- Expose semantic models via secure API.
- Integrate with AskAI (corporate agent marketplace) as frontend.
- Meet compliance on auth, governance, and observability.

---

## 3. High-Level Architecture (C4 Level 1)

![High Level with AskAI](../diagrams/high-level-askai.png)

**Flow:**
1. User selects our agent in AskAI marketplace.
2. AskAI sends request to Wrapper API via OpenAPI spec.
3. Wrapper API invokes Cortex Analyst → Snowflake.
4. Response returned to AskAI for UI display.

---

## 4. Application Runtime & Deployment (C4 Level 2)

![Application Runtime Deployment](../diagrams/application-runtime.png)

**Deployment:**
- Load Balancer → ADC → Treadmill pods (FastAPI).
- CI/CD via Train + UpLIFT + WebstaX.
- OIDC-based authentication.
- Observability via OTEL → Tiempo/Cortex.

---

## 5. Wrapper API Components (C4 Level 3)

![Wrapper Components](../diagrams/wrapper-components.png)

**Key endpoints:**
- `/semantic/{model}/ask`
- `/metadata/*`
- `/sql/execute` (optional)

**Guardrails:**
- Schema allowlist
- Role-based filters
- Prompt injection prevention

---

## 6. Integration with AskAI

**Why AskAI:**
- Existing corporate framework for agent discovery.
- No need to build UI.
- OpenAPI compatibility.

**Usage:**
- Register our API as agent.
- Users enable agent from list.
- Requests flow via AskAI → Wrapper API.

---

## 7. Security & Compliance

- **AuthN/Z:** OIDC/JWT at ADC + API.
- **Snowflake Access:** Keypair authentication, CLS/RLS, masking.
- **Network:** TLS end-to-end, CLM.
- **Governance:** Only Runway can create Snowflake objects in Prod.

---

## 8. Observability & Quality (ADR-004)

**Dev/QA:** TruLens dashboard (fast feedback).  
**Prod:** TruLens → OTEL → Tiempo/Cortex → Grafana.

Metrics tracked:
- Latency (p50, p95)
- Error rates
- Evaluation metrics (relevance, groundedness)
- Cost/session

---

## 9. Performance & Cost Controls

- Snowflake warehouse autosuspend/resume.
- Pagination & query limits.
- Resource monitors & alerts.
- Cache metadata.

---

## 10. Go-Live Plan

**T-14 to T-7:**  
- Freeze semantic models.
- Performance & load testing.
- Security review.

**T-7 to T-2:**  
- Canary deploy in pre-prod.
- Runbook validation.

**T-0:**  
- Rollout: 5% → 25% → 100% traffic.
- Live monitoring of KPIs.

**Rollback:**  
- Feature flag disable.
- Deploy previous image.

---

## 11. Go-Live Gates

- p95 latency ≤ 3s
- Error rate ≤ 2%
- Answer relevance ≥ 0.75
- Compliance approvals complete
- Observability configured

---

## 12. RACI

| Area | Role | Name |
|------|------|------|
| Product Owner | A | [Name] |
| Architecture | A | [Name] |
| Backend/API | R | [Name] |
| Data/Semantic | R | [Name] |
| AskAI Integration | C/R | [Name] |
| Platform/Observability | C | [Name] |
| Security | C | [Name] |

---

## 13. Risks & Mitigations

| ID | Risk | Mitigation |
|----|------|------------|
| R1 | OTEL config delays | Pairing with Obs team, pre-prod POC |
| R2 | Snowflake cost spikes | Limits, monitors, pagination |
| R3 | Prompt injection | Guardrails, allowlist |
| R4 | OIDC misconfig | WebstaX templates + security tests |
| R5 | Semantic drift | Golden prompt regression tests |

---

## Appendix: ADR-004 (Observability Decision)

**Decision:**  
- Dev/QA: TruLens dashboard with Snowflake tables.  
- Prod: TruLens with OTEL exporter to Tiempo/Cortex, dashboards in Grafana.

**Reasoning:**
- Compliance with auth and provisioning rules.
- Integration with corporate observability stack.
- Unified monitoring for API and models.

