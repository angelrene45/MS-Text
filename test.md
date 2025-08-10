# ADR 001 – Frontend Integration Choice with AskAI

**Status:** Accepted  
**Date:** YYYY-MM-DD  
**Review Level:** Department / Platform Architecture Board  
**Decision Makers:** [List of accountable & responsible stakeholders]  
**Consulted:** AskAI Team Lead, Platform Security Lead, Product Owner

---

## Context & Problem Statement
The initial plan was to build a custom user interface (UI) using **Streamlit** as a proof of concept to connect to our Python-based backend and the **Cortex Analyst API**.  
However, maintaining an in-house UI would increase development overhead, require dedicated UI resources, and duplicate capabilities already available in **AskAI** — a corporate conversational UI maintained by another department.

AskAI is part of a **strategic agentic frameworks marketplace** initiative in which multiple departments (including Research) will expose their models as agents.  
The platform will allow end users to select and enable agents from a list, making it a centralized entry point for AI-powered capabilities across the company.

**Objectives:**
- Provide business users with a conversational interface to query semantic models.
- Minimize UI development and maintenance within our team.
- Ensure compatibility with the corporate agentic frameworks marketplace.
- Integrate into a unified platform where users can discover and select available agents.

---

## Decision Drivers
- **Strategic alignment:** Leverage the corporate agentic frameworks marketplace.
- **Business priority:** Deliver functional UI access with minimal delay.
- **Technical priority:** Standardized OpenAPI integration with agent registration.
- **Security:** Maintain authentication/authorization via OIDC.
- **Scalability:** UI managed by a dedicated team, capable of onboarding multiple agents.
- **Maintainability:** Reduce UI code maintenance in our backlog.

Cross-functional requirements:
- High availability of the UI (managed externally).
- Compatibility with our API release cycles.
- Alignment with corporate UI/UX and agent lifecycle standards.

---

## Considered Options

### Option 1 – Build Custom UI (Streamlit)
**Pros:**
- Full control over UI/UX design.
- Ability to rapidly prototype and customize.
**Cons:**
- Additional development and maintenance workload.
- Requires UI skillset in our team.
- No integration with the corporate agent marketplace.

### Option 2 – Integrate with AskAI (**Selected**)
**Pros:**
- No UI development or maintenance required internally.
- AskAI supports OpenAPI and agent registration in the corporate marketplace.
- Managed by another department with existing support.
- Aligns with strategic vision for a unified agentic platform.
**Cons:**
- Dependence on another team’s release cycles and roadmap.
- Limited control over UI/UX changes.

---

## Decision Outcome
We will integrate with **AskAI** as the frontend interface, registering our backend as an agent and exposing endpoints via OpenAPI.  
This allows us to focus on backend functionality and semantic model quality while leveraging an existing, supported UI within the company-wide agent marketplace.

---

## Consequences
- **Positive:** Reduced development effort, faster delivery, standard integration, strategic alignment with the marketplace initiative.
- **Negative:** Dependency on AskAI team for UI updates and fixes.
- **Reversibility:** Moderate — could switch to custom UI if AskAI no longer meets needs, but would require significant development effort.
- **Impact:** Requires ongoing coordination with AskAI for testing, deployment, API versioning, and agent lifecycle in the marketplace.

---

## Supporting Documents
- C4 Context Diagram – `high-level-architecture-askai.puml`
- API OpenAPI Specification – `openapi.yaml`
- Corporate Agent Marketplace Overview – [link or document reference]




















# ADR 002 – Deployment Stack Choice: WebstaX vs Podman/Treadmill

**Status:** Accepted  
**Date:** YYYY-MM-DD  
**Review Level:** Department / Platform Architecture Board  
**Decision Makers:** [List of accountable & responsible stakeholders]  
**Consulted:** Platform Deployment Team, DevOps Lead, Security Architect

---

## Context & Problem Statement
For deploying our FastAPI Wrapper API to production, we considered two viable approaches:  
1. **Manual stack** — Podman + UpLIFT + Treadmill + Load Balancer + CLM.  
2. **WebstaX** — Platform-recommended deployment stack that automates provisioning and deployment.

**Objectives:**
- Ensure secure, repeatable, and compliant deployments.
- Reduce manual configuration errors.
- Align with platform team’s recommended and supported tooling.

---

## Decision Drivers
- **Platform alignment:** Using officially supported tooling reduces integration risk.
- **Automation:** Minimize manual provisioning (LB, CLM, OIDC).
- **Compliance:** TAM validation and corporate security standards enforced.
- **Operational efficiency:** Faster deployments, less operational overhead.

Cross-functional requirements:
- High availability and scalability.
- Integration with CI/CD (Train + UpLIFT).
- Secure TLS termination and OIDC authentication.
- Auditability of deployments.

---

## Considered Options

### Option 1 – Manual Stack (Podman + UpLIFT + Treadmill + LB + CLM)
**Pros:**
- Greater flexibility for non-standard configurations.
- Full control over deployment pipeline.
**Cons:**
- Higher manual effort and risk of misconfiguration.
- Requires deeper platform expertise in the team.
- Slower deployment turnaround.

### Option 2 – WebstaX (**Selected**)
**Pros:**
- Fully automated provisioning and deployment.
- Enforces TAM validation and compliance.
- Supported by platform team.
**Cons:**
- Less flexibility for special configurations.
- Dependency on WebstaX team’s release cycles.

---

## Decision Outcome
We will adopt **WebstaX** for production deployments while keeping our CI/CD image build in Train + UpLIFT.  
This ensures automation, compliance, and reduces operational overhead.

---

## Consequences
- **Positive:** Faster deployments, reduced errors, compliance guaranteed.
- **Negative:** Limited ability to deviate from standard configuration.
- **Reversibility:** Low complexity — can revert to manual stack if needed, but would require additional platform configuration.
- **Impact:** Requires collaboration with WebstaX team for deployment scheduling and special requirements.

---

## Supporting Documents
- C4 Container Diagram – `application-runtime-deployment.puml`
- Deployment Pipeline Diagram – `ci-cd-flow.puml`

