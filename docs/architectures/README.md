# Architecture overview index

This directory contains proposed, implementation-oriented reference architectures for all **107 B2C AI applications** in the catalog. They are design guides—not claims about the linked example repositories.

Each volume includes multiple diagram levels:

- three **Azure icon views** generated with the [Azure Diagrams skill](https://github.com/cmb211087/azure-diagrams-skill): C4-style system context, runtime/transaction flow, and security/data/operations;
- a **category deployment diagram** showing Azure edge, API, compute, model, tools, data, messaging, identity, security and observability boundaries;
- a distinct **application request-flow diagram** showing the app's channels, orchestration, tools, integrations, data path, policy gates and telemetry.

Every app now also documents its eight-step **main execution logic** and links to a [runnable C# workflow sample](../../samples/agent-workflow-csharp/README.md) implementing policy checks, approval gates, idempotent tool execution and audit events.

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
