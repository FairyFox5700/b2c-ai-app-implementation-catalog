# Architecture overview index

This directory contains proposed, implementation-oriented reference architectures for all **107 B2C AI applications** in the catalog. They are design guides—not claims about the linked example repositories.

Each volume includes multiple diagram levels:

- three **Azure icon views** generated with the [Azure Diagrams skill](https://github.com/cmb211087/azure-diagrams-skill): C4-style system context, runtime/transaction flow, and security/data/operations;
- a **category deployment diagram** showing Azure edge, API, compute, model, tools, data, messaging, identity, security and observability boundaries;
- a distinct **application request-flow diagram** showing the app's channels, orchestration, tools, integrations, data path, policy gates and telemetry.

All Mermaid diagrams are committed as **pre-rendered SVG files** so large GitHub pages display immediately instead of remaining on “Loading.” The editable `.mmd` source is linked directly below every SVG. Rendering is pinned to Mermaid CLI 12.2.0. Run `npm ci` once, then `npm run diagrams:render` after changing a source file or `npm run diagrams:check` to freshly render every source and verify that all 117 committed SVGs are current.

Every app also documents its eight-step **main execution logic** and links to a [runnable C# workflow sample](../../samples/agent-workflow-csharp/README.md) implementing policy checks, approval gates, idempotent tool execution and audit events.

## How to read the architecture views

### View 1: system context — who participates

Use this view to establish the system boundary. The **customer** supplies intent and confirms consequential actions; the **human approver** handles exceptions or regulated decisions; the **B2C AI application** owns the experience and workflow; **Microsoft Foundry** supplies model inference; and **domain systems** remain the source of truth for prices, bookings, accounts, records and other business facts.

This view answers: *Who trusts whom? Which systems are external? Where does responsibility begin and end?*

### View 2: runtime and transaction flow — what happens to one request

1. The channel sends a request through Azure Front Door/WAF and API Management.
2. Application code authenticates the user, validates the schema, attaches a correlation ID and loads only the authorized context.
3. The orchestrator asks the model for a structured proposal using a bounded list of tool schemas.
4. Deterministic policy code checks the proposed tool, arguments, permissions, limits and risk classification.
5. Read operations query retrieval indexes or business APIs. Consequential writes pause for explicit approval.
6. The tool gateway executes with idempotency, timeout and retry controls; durable work moves to Service Bus rather than blocking the request.
7. Transactional state is committed by application services—not by the model—and a grounded response is returned.
8. Redacted traces, metrics and evaluation signals are emitted throughout the flow.

This view answers: *Where can a request fail? Which steps are synchronous? Where are retries, approvals and state transitions owned?*

### View 3: security, data and operations — how production is controlled

The control plane spans the full request path: Entra ID and managed identity establish identity; Key Vault protects secrets; private endpoints restrict network access; content-safety and business-policy checks constrain model output; Application Insights records redacted telemetry; and evaluation pipelines detect regressions. Retrieval indexes are deliberately separated from transactional stores so generated context never becomes an accidental system of record.

This view answers: *Where is sensitive data stored? How is access enforced? What is logged, evaluated and recoverable?*

### Application request-flow color key

- **Teal — channel/edge:** user-facing entry points and ingress.
- **Green — agent/orchestration:** planning, routing and response composition.
- **Amber — controlled tools:** deterministic operations and external API adapters.
- **Violet — data:** retrieval indexes, profiles and workflow state.
- **Blue — application backend:** durable handoffs and business services.
- **Gray — external dependency:** systems outside the application boundary.
- **Red — control plane:** identity, policy, approvals, telemetry and evaluation.

A line in a diagram means a permitted interaction—not unrestricted network access. Production implementations should expose narrow typed contracts, authorize every call, validate every result and keep high-impact writes behind an explicit approval boundary.

Every application overview covers:

1. purpose and user journey;
2. a renderable reference architecture diagram and flow;
3. core components;
4. agent and workflow design;
5. data and integrations;
6. security and safety;
7. reliability, observability and evaluation;
8. an incremental MVP build path.

## Volumes

| Apps | Category | Count | Architecture document |
|---:|---|---:|---|
| 1–16 | Commerce and retail | 16 | [Open](01-commerce-retail.md) |
| 17–23 | Food and dining | 7 | [Open](02-food-dining.md) |
| 24–32 | Travel and events | 9 | [Open](03-travel-events.md) |
| 33–39 | Home and property | 7 | [Open](04-home-property.md) |
| 40–50 | Finance, insurance, legal and automotive | 11 | [Open](05-finance-legal-automotive.md) |
| 51–65 | Health, wellness and pets | 15 | [Open](06-health-wellness-pets.md) |
| 66–71 | Education and learning | 6 | [Open](07-education-learning.md) |
| 72–84 | Career, productivity and family | 13 | [Open](08-career-productivity-family.md) |
| 85–93 | Technology, utilities and sustainability | 9 | [Open](09-technology-sustainability.md) |
| 94–107 | Creative, social, safety and public services | 14 | [Open](10-creative-social-public.md) |
|  | **Total** | **107** |  |

## How to use an overview

- Start with **Purpose and user journey** to validate the customer problem.
- Turn **Reference architecture** into a diagram for stakeholder review.
- Use **Core components** and **Data and integrations** to define service boundaries.
- Treat **Security and safety** as acceptance criteria, not optional hardening.
- Build the smallest slice under **MVP build path** before adding multi-agent orchestration.
- Convert the metrics under **Reliability, observability and evaluation** into automated tests and production dashboards.

## Safety note

Several designs involve health, finance, legal, safety, children, payments or identity data. These require domain-expert review, jurisdiction-specific compliance work, conservative escalation paths and explicit human approval for consequential actions. The documents do not constitute medical, financial or legal advice.
