# ADR 001 – Frontend Integration Choice with AskAI

**Date:** YYYY-MM-DD  
**Status:** Accepted  

## Context
The initial plan was to build a user interface (UI) using **Streamlit** as a proof of concept to interact with our Python-based backend and the **Cortex Analyst API**.  
While this approach gave us full control over the UI, it also implied extra development and maintenance work.

## Decision
Integrate with the **AskAI** service — an agent framework acting as a marketplace that already provides a conversational UI.  
Our backend will be registered as an agent and expose endpoints via **OpenAPI** specifications.

## Rationale
- **Reduced development and maintenance effort**: No need to build and maintain our own UI.  
- **Standards and compatibility**: AskAI supports OpenAPI, making integration straightforward.  
- **Backend focus**: Allows us to prioritize backend improvements and semantic model quality.  
- **Cross-team alignment**: AskAI is maintained by another department, reducing UI operational load.

## Consequences
- The UI will not be developed internally; we depend on AskAI for user-facing presentation.  
- Any API change must comply with OpenAPI specifications to maintain compatibility.  
- The final user experience will depend on AskAI’s capabilities and roadmap.  
- Requires close coordination with the AskAI team for versioning, deployments, and testing.








# ADR 002 – Deployment Stack Choice: WebstaX vs Podman/Treadmill

**Date:** YYYY-MM-DD  
**Status:** Accepted  

## Context
For the backend (FastAPI Wrapper API) deployment, we evaluated two main options:

1. **Manual stack**: Podman + UpLIFT + Treadmill + Load Balancer + CLM — greater control and flexibility, but requires more manual configuration.  
2. **WebstaX**: Integrated solution recommended by the platform team, automating CLM, LB, OIDC provisioning, deployment into Treadmill, and TAM validation.

Both options are compatible with our CI/CD pipeline (Train + UpLIFT) and support container execution in Treadmill.

## Decision
Adopt **WebstaX** as the production deployment stack while keeping our image build and packaging flow in Train + UpLIFT.

## Rationale
- **Official recommendation from the platform team** with dedicated support.  
- **Full automation** of LB, certificate, OIDC provisioning, and deployment — reducing manual errors.  
- **Integrated TAM validation** ensuring compliance with corporate standards.  
- **Faster production deployments** and reduced operational burden.

## Consequences
- Less flexibility for non-standard configurations not supported by WebstaX.  
- Dependency on WebstaX team’s roadmap and support timelines.  
- Any special requirements outside the standard config must be coordinated with the platform team.  
- Easier scaling and reproducibility of environments thanks to automation.









@startuml C4_Context
!include <c4/C4.puml>
!include <c4/C4_Context.puml>

Person(user, "End User", "Asks natural language questions")
System_Ext(askai, "AskAI (Frontend)", "Conversational UI maintained by another department")
System_Boundary(yoursys, "Your System – Semantic Answers") {
  System(api, "Wrapper API (FastAPI)", "Exposes /semantic/* via OpenAPI; applies OIDC, guardrails, and observability")
}
System_Ext(snow, "Snowflake + Cortex Analyst", "Generates and executes SQL over semantic models")
System_Ext(idp, "OIDC IdP/SSO", "Issues and validates JWT")
System_Ext(obs, "Observability (Trulens + APM/Logs)", "Traces and evaluates responses")

Rel(user, askai, "Natural language questions")
Rel(askai, api, "HTTPS / OpenAPI", "JWT (OIDC)")
Rel(api, snow, "REST (Cortex Analyst) / SQL indirectly")
Rel(api, idp, "AuthN/AuthZ", "OIDC/JWT")
Rel(api, obs, "Traces + evaluations", "OTel/TruLens")
@enduml














@startuml C4_Containers
!include <c4/C4.puml>
!include <c4/C4_Container.puml>

Person(user, "End User")
System_Ext(askai, "AskAI", "External frontend")

System_Boundary(runtime, "Application Runtime") {
  Container(lb, "LBv3", "Load Balancer", "TLS/DNS; routes to Treadmill")
  Container_Boundary(treadmill, "Treadmill") {
    Container_Boundary(cell, "Cell / Namespace") {
      Container(adc, "httpd ADC", "Reverse proxy", "OIDC + ILS enforced")
      Container(api1, "Wrapper API", "FastAPI container", "Gunicorn/Uvicorn; /semantic/*")
      Container(api2, "Wrapper API (replica)", "FastAPI container", "HPA/auto-scale")
    }
  }
  Rel(lb, adc, "HTTPS")
  Rel(adc, api1, "proxy")
  Rel(adc, api2, "proxy")
}

System_Ext(snow, "Snowflake + Cortex Analyst", "Semantic models + SQL execution")
System_Ext(idp, "OIDC IdP", "SSO/JWT")
System_Ext(obs, "Trulens + APM/Logs", "Evaluations and traces")

Rel(askai, lb, "HTTPS/OpenAPI", "JWT (OIDC)")
Rel(api1, snow, "REST (Cortex Analyst)")
Rel(api1, idp, "Validate tokens / scopes")
Rel(api1, obs, "Traces/Evals")
Rel(api2, snow, "REST")
Rel(api2, idp, "OIDC")
Rel(api2, obs, "Traces/Evals")

System_Ext(train, "Train (CI/CD)", "Build/test jobs")
System_Ext(uplift, "UpLIFT", "Image/package registry")
System_Ext(webstax, "WebstaX", "TAM + CLM + LB/OIDC provisioning + Deployment")

Rel(train, uplift, "Promote image")
Rel(uplift, api1, "Pull image")
Rel(uplift, api2, "Pull image")
Rel(webstax, cell, "Deploy/Provision")
Rel(user, askai, "Uses UI")
@enduml
