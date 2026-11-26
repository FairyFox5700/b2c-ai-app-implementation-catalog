# Food and Dining

<!-- azure-icon-views:auto -->
## Azure architecture views

These are **logical reference views**, not a claim that every app needs every service. Select services from the non-functional requirements, traffic, data classification and team constraints.

### 1. System context

Shows the customer, human approver, B2C AI system, identity provider, Microsoft Foundry and domain systems.

![02-food-dining system context](../diagrams/azure/02-food-dining.png)

### 2. Runtime and transaction flow

Shows synchronous ingress, structured model reasoning, controlled tool calls, durable workflow state and asynchronous retry/compensation.

![02-food-dining runtime flow](../diagrams/azure/02-food-dining-runtime.png)

### 3. Security, data and operations

Shows identity, managed authorization, policy and approval gates, grounded retrieval, workflow state, private access, secrets and redacted telemetry.

![02-food-dining security data and operations](../diagrams/azure/02-food-dining-security-data.png)

**Notation:** solid arrows are primary runtime/data flows. Dashed arrows represent identity, policy, secrets or private-network controls. Dotted arrows represent telemetry. The diagrams deliberately split concerns to avoid an unreadable “everything” diagram.


<!-- category-architecture:auto -->
## Category deployment architecture

This Azure-oriented deployment separates deterministic business operations from probabilistic model reasoning. The application owns authorization, validation, workflow state and approval; the model proposes actions only through allowlisted tools.

```mermaid
flowchart LR
    classDef edge fill:#083344,stroke:#22d3ee,color:#ecfeff
    classDef compute fill:#064e3b,stroke:#34d399,color:#ecfdf5
    classDef ai fill:#1e3a8a,stroke:#60a5fa,color:#eff6ff
    classDef data fill:#4c1d95,stroke:#a78bfa,color:#f5f3ff
    classDef integration fill:#78350f,stroke:#fbbf24,color:#fffbeb
    classDef control fill:#881337,stroke:#fb7185,color:#fff1f2

    USER["Web, mobile, voice or partner channel"] --> EDGE["Azure Front Door + WAF"]
    EDGE --> API["API Management"]
    API --> APP["App Service / Container Apps"]
    APP --> ORCH["Microsoft Agent Framework orchestrator"]
    ORCH --> MODEL["Microsoft Foundry model endpoint"]
    ORCH --> TOOLS["Controlled tool gateway"]
    TOOLS --> DOMAIN["Food and dining tools and partner APIs"]
    ORCH --> SEARCH["Azure AI Search / retrieval"]
    ORCH --> STATE["Cosmos DB / SQL workflow state"]
    ORCH --> BUS["Service Bus / durable background work"]

    ID["Entra ID + managed identity"] -. authentication .-> API
    VAULT["Key Vault + configuration"] -. secrets .-> APP
    SAFE["Content safety, policy + human approval"] -. enforcement .-> ORCH
    OBS["Application Insights, traces + evals"] -. telemetry .-> APP

    class USER,EDGE,API edge
    class APP,ORCH compute
    class MODEL ai
    class SEARCH,STATE data
    class TOOLS,DOMAIN,BUS integration
    class ID,VAULT,SAFE,OBS control
```

**Responsibility split**

- **Edge and API layer:** authentication, quotas, request validation and tenant routing.
- **Application/orchestration layer:** deterministic workflow, retries, approvals, state and tool authorization.
- **Model layer:** language understanding, planning and explanation; it never becomes the system of record.
- **Tool layer:** narrow typed operations with idempotency, schema validation and audit events.
- **Data layer:** retrieval indexes are separate from transactional state and sensitive records.
- **Control plane:** identity, secrets, policy, privacy, observability and evaluations apply across every request.


## 17. Grocery-shopping assistant

### Purpose and user journey
Helps households build a weekly grocery list, compare stores, and check out with minimal effort. The user states needs or approves a meal plan, reviews a substituted, priced basket, adjusts quantities, and confirms delivery or pickup.

### Reference architecture
`Chat UI -> Orchestrator agent -> Catalog/price tools -> Basket optimizer -> Retailer cart API -> Approval gate -> Order tracker`

<!-- architecture-diagram:auto -->
```mermaid
flowchart LR
    classDef frontend fill:#083344,stroke:#22d3ee,color:#ecfeff
    classDef agent fill:#064e3b,stroke:#34d399,color:#ecfdf5
    classDef tool fill:#78350f,stroke:#fbbf24,color:#fffbeb
    classDef data fill:#4c1d95,stroke:#a78bfa,color:#f5f3ff
    classDef backend fill:#1e3a8a,stroke:#60a5fa,color:#eff6ff
    classDef external fill:#1e293b,stroke:#94a3b8,color:#f8fafc
    classDef control fill:#881337,stroke:#fb7185,color:#fff1f2
    A17_0["Chat UI"]
    class A17_0 frontend
    A17_1["Orchestrator agent"]
    class A17_1 agent
    A17_2["Catalog/price tools"]
    class A17_2 tool
    A17_3["Basket optimizer"]
    class A17_3 tool
    A17_4["Retailer cart API"]
    class A17_4 external
    A17_5["Approval gate"]
    class A17_5 frontend
    A17_6["Order tracker"]
    class A17_6 backend
    A17_0 --> A17_1
    A17_1 --> A17_2
    A17_2 --> A17_3
    A17_3 --> A17_4
    A17_4 --> A17_5
    A17_5 --> A17_6
    ID17["Entra ID + managed identity"]
    SAFE17["Policy, validation + approval gates"]
    OBS17["Tracing, metrics + evaluation"]
    class ID17,SAFE17,OBS17 control
    ID17 -. authentication .-> A17_1
    SAFE17 -. enforcement .-> A17_1
    OBS17 -. telemetry .-> A17_1
```

<!-- main-logic:auto -->
**Main execution logic**

1. **Authenticate and validate:** the edge/API layer verifies identity, tenant, request schema, quotas and correlation ID before agent execution.
2. **Load trusted context:** the application loads the minimum required profile, conversation checkpoint, domain state and authorization scope; sensitive fields stay outside prompts unless necessary.
3. **Plan with bounded authority:** the Foundry/Agent Framework adapter receives only allowlisted tool schemas and returns a structured proposal. The app-specific path is `Chat UI -> Orchestrator agent -> Catalog/price tools -> Basket optimizer -> Retailer cart API -> Approval gate -> Order tracker`.
4. **Ground every decision:** current facts such as price, availability, policy, entitlement or status come from retrieval and typed tools—not model memory.
5. **Apply deterministic policy:** code validates tool name, arguments, user authority, limits, risk class and output schema. Invalid proposals are rejected and audited.
6. **Approve consequential actions:** writes, purchases, bookings, messages, account changes and other high-impact operations pause for explicit human approval.
7. **Execute safely:** the controlled gateway invokes the narrow business operation with an idempotency key, timeout, bounded retry and compensation or dead-letter behavior.
8. **Commit and learn:** persist the result, return a source-grounded response, emit redacted traces and feed curated outcomes into regression evaluations.

**Runnable code pattern:** [C# policy, approval, idempotency and audit sample](../../samples/agent-workflow-csharp/README.md).


### Core components
Conversation service, pantry inventory store, product-matching engine, price and promotion index, substitution ranker, basket optimizer, retailer connectors, approval screen, and a preference profile covering brands, budget, diet, and delivery windows.

### Agent/workflow design
A planner agent parses intent, expands generic items into SKUs, and calls the optimizer. Deterministic code handles totals, unit prices, and limits. The agent explains substitutions, asks only when ambiguity affects cost or allergens, and never submits an order without explicit approval.

### Data and integrations
Stores purchase history, pantry counts, and preferences in a relational database with a vector index for product search. Integrates retailer catalog and cart APIs, loyalty accounts, and recipe or meal-plan services, with fallback CSV or receipt import.

### Security and safety
Tokenize retailer credentials and use scoped OAuth. Enforce spending caps, confirm payment through the retailer, and flag allergens and dietary conflicts. Minimize retained receipt data, and make purchase history exportable and deletable.

### Reliability, observability and evaluation
Cache catalog data with freshness stamps and handle out-of-stock errors with retries. Trace each basket build, log substitution acceptance, and track price accuracy. Evaluate on replayed lists for match precision, savings, and allergen safety.

### MVP build path
Start with one retailer, text list to matched basket, and manual checkout handoff. Add pantry tracking and substitutions next, then price comparison across stores, then recurring lists and approval-gated cart submission.

## 18. Meal-planning coach

### Purpose and user journey
Creates weekly meal plans fitted to goals, time, budget, and tastes, then adapts as life changes. The user completes onboarding, receives a plan, swaps meals, gets a shopping list, and logs feedback that improves later weeks.

### Reference architecture
`Onboarding UI -> Planner agent -> Constraint solver -> Recipe retrieval -> Nutrition calculator -> Plan calendar -> Grocery list export`

<!-- architecture-diagram:auto -->
```mermaid
flowchart LR
    classDef frontend fill:#083344,stroke:#22d3ee,color:#ecfeff
    classDef agent fill:#064e3b,stroke:#34d399,color:#ecfdf5
    classDef tool fill:#78350f,stroke:#fbbf24,color:#fffbeb
    classDef data fill:#4c1d95,stroke:#a78bfa,color:#f5f3ff
    classDef backend fill:#1e3a8a,stroke:#60a5fa,color:#eff6ff
    classDef external fill:#1e293b,stroke:#94a3b8,color:#f8fafc
    classDef control fill:#881337,stroke:#fb7185,color:#fff1f2
    A18_0["Onboarding UI"]
    class A18_0 frontend
    A18_1["Planner agent"]
    class A18_1 agent
    A18_2["Constraint solver"]
    class A18_2 agent
    A18_3["Recipe retrieval"]
    class A18_3 tool
    A18_4["Nutrition calculator"]
    class A18_4 tool
    A18_5["Plan calendar"]
    class A18_5 external
    A18_6["Grocery list export"]
    class A18_6 backend
    A18_0 --> A18_1
    A18_1 --> A18_2
    A18_2 --> A18_3
    A18_3 --> A18_4
    A18_4 --> A18_5
    A18_5 --> A18_6
    ID18["Entra ID + managed identity"]
    SAFE18["Policy, validation + approval gates"]
    OBS18["Tracing, metrics + evaluation"]
    class ID18,SAFE18,OBS18 control
    ID18 -. authentication .-> A18_1
    SAFE18 -. enforcement .-> A18_1
    OBS18 -. telemetry .-> A18_1
```

<!-- main-logic:auto -->
**Main execution logic**

1. **Authenticate and validate:** the edge/API layer verifies identity, tenant, request schema, quotas and correlation ID before agent execution.
2. **Load trusted context:** the application loads the minimum required profile, conversation checkpoint, domain state and authorization scope; sensitive fields stay outside prompts unless necessary.
3. **Plan with bounded authority:** the Foundry/Agent Framework adapter receives only allowlisted tool schemas and returns a structured proposal. The app-specific path is `Onboarding UI -> Planner agent -> Constraint solver -> Recipe retrieval -> Nutrition calculator -> Plan calendar -> Grocery list export`.
4. **Ground every decision:** current facts such as price, availability, policy, entitlement or status come from retrieval and typed tools—not model memory.
5. **Apply deterministic policy:** code validates tool name, arguments, user authority, limits, risk class and output schema. Invalid proposals are rejected and audited.
6. **Approve consequential actions:** writes, purchases, bookings, messages, account changes and other high-impact operations pause for explicit human approval.
7. **Execute safely:** the controlled gateway invokes the narrow business operation with an idempotency key, timeout, bounded retry and compensation or dead-letter behavior.
8. **Commit and learn:** persist the result, return a source-grounded response, emit redacted traces and feed curated outcomes into regression evaluations.

**Runnable code pattern:** [C# policy, approval, idempotency and audit sample](../../samples/agent-workflow-csharp/README.md).


### Core components
Profile service, constraint engine for calories, diet, allergens, and prep time, recipe retrieval index, nutrition calculator, plan calendar, leftovers scheduler, feedback store, and reminder service for prep and thawing.

### Agent/workflow design
The agent gathers constraints, calls the solver for candidate plans, and has the LLM rank them for variety and preference fit. Users edit conversationally; the agent re-solves only the affected days and keeps ingredient reuse high to reduce waste.

### Data and integrations
Stores profiles, ratings, plans, and pantry data. Integrates recipe databases, nutrition datasets such as USDA, grocery list export, calendar apps, and optional wearable or weight-tracking data with user consent.

### Security and safety
Treat health data as sensitive and encrypt it. Add medical disclaimers, avoid extreme calorie targets, escalate eating-disorder or medical-condition signals to professional resources, and hard-block declared allergens in every candidate.

### Reliability, observability and evaluation
Validate plans against constraints before display. Monitor swap rates, adherence, and solver failures. Evaluate with test personas for constraint satisfaction, nutrition accuracy, variety, and dietitian review of sampled plans.

### MVP build path
Ship a seven-day dinner planner with diet and allergen filters over a curated recipe set. Add shopping-list export, then swaps and feedback learning, then leftovers, pantry awareness, and multi-person household plans.

## 19. Recipe assistant

### Purpose and user journey
Finds, adapts, and guides cooking of recipes. The user describes ingredients, cuisine, or constraints, picks a result, scales or substitutes ingredients, and receives hands-free step-by-step guidance with timers and troubleshooting.

### Reference architecture
`Text/voice UI -> Intent router -> Recipe search (hybrid) -> Adaptation engine -> Cooking-mode session -> Timer/voice output`

<!-- architecture-diagram:auto -->
```mermaid
flowchart LR
    classDef frontend fill:#083344,stroke:#22d3ee,color:#ecfeff
    classDef agent fill:#064e3b,stroke:#34d399,color:#ecfdf5
    classDef tool fill:#78350f,stroke:#fbbf24,color:#fffbeb
    classDef data fill:#4c1d95,stroke:#a78bfa,color:#f5f3ff
    classDef backend fill:#1e3a8a,stroke:#60a5fa,color:#eff6ff
    classDef external fill:#1e293b,stroke:#94a3b8,color:#f8fafc
    classDef control fill:#881337,stroke:#fb7185,color:#fff1f2
    A19_0["Text/voice UI"]
    class A19_0 frontend
    A19_1["Intent router"]
    class A19_1 agent
    A19_2["Recipe search (hybrid)"]
    class A19_2 tool
    A19_3["Adaptation engine"]
    class A19_3 agent
    A19_4["Cooking-mode session"]
    class A19_4 tool
    A19_5["Timer/voice output"]
    class A19_5 backend
    A19_0 --> A19_1
    A19_1 --> A19_2
    A19_2 --> A19_3
    A19_3 --> A19_4
    A19_4 --> A19_5
    ID19["Entra ID + managed identity"]
    SAFE19["Policy, validation + approval gates"]
    OBS19["Tracing, metrics + evaluation"]
    class ID19,SAFE19,OBS19 control
    ID19 -. authentication .-> A19_1
    SAFE19 -. enforcement .-> A19_1
    OBS19 -. telemetry .-> A19_1
```

<!-- main-logic:auto -->
**Main execution logic**

1. **Authenticate and validate:** the edge/API layer verifies identity, tenant, request schema, quotas and correlation ID before agent execution.
2. **Load trusted context:** the application loads the minimum required profile, conversation checkpoint, domain state and authorization scope; sensitive fields stay outside prompts unless necessary.
3. **Plan with bounded authority:** the Foundry/Agent Framework adapter receives only allowlisted tool schemas and returns a structured proposal. The app-specific path is `Text/voice UI -> Intent router -> Recipe search (hybrid) -> Adaptation engine -> Cooking-mode session -> Timer/voice output`.
4. **Ground every decision:** current facts such as price, availability, policy, entitlement or status come from retrieval and typed tools—not model memory.
5. **Apply deterministic policy:** code validates tool name, arguments, user authority, limits, risk class and output schema. Invalid proposals are rejected and audited.
6. **Approve consequential actions:** writes, purchases, bookings, messages, account changes and other high-impact operations pause for explicit human approval.
7. **Execute safely:** the controlled gateway invokes the narrow business operation with an idempotency key, timeout, bounded retry and compensation or dead-letter behavior.
8. **Commit and learn:** persist the result, return a source-grounded response, emit redacted traces and feed curated outcomes into regression evaluations.

**Runnable code pattern:** [C# policy, approval, idempotency and audit sample](../../samples/agent-workflow-csharp/README.md).


### Core components
Hybrid keyword and vector recipe index, ingredient parser, unit converter, substitution knowledge base, scaling engine, cooking-mode state machine, timer manager, and a pantry-aware ranker.

### Agent/workflow design
A router separates search, adaptation, and live-cooking questions. Adaptation uses deterministic scaling plus LLM-proposed substitutions validated against rules. Cooking mode tracks the current step, answers questions in context, and re-times steps when quantities change.

### Data and integrations
Uses licensed or user-imported recipes with structured ingredients, steps, and nutrition. Integrates the pantry, grocery list, smart speakers or displays, and URL import via schema.org Recipe markup with attribution.

### Security and safety
Respect recipe licensing and avoid verbatim copying of protected content. Surface allergen warnings, safe internal temperatures, and food-handling cautions. Flag risky substitutions in baking or canning and treat web imports as untrusted input.

### Reliability, observability and evaluation
Parse failures fall back to the raw text view. Log search success, substitution acceptance, and abandoned cooking sessions. Evaluate retrieval relevance, scaling accuracy, and substitution safety against curated test cases.

### MVP build path
Build ingredient-based search over a licensed set and a clean recipe view. Add scaling and unit conversion, then substitutions, then step-by-step cooking mode with timers, and finally URL import and voice control.

## 20. Nutrition coach

### Purpose and user journey
Helps users understand and improve eating habits through logging, insights, and goal-based guidance. The user logs meals by text or photo, sees nutrient trends against goals, and receives small weekly adjustments.

### Reference architecture
`Log UI (text/photo) -> Food parser -> Nutrient DB lookup -> Trend analyzer -> Coaching agent -> Safety filter -> Weekly report`

<!-- architecture-diagram:auto -->
```mermaid
flowchart LR
    classDef frontend fill:#083344,stroke:#22d3ee,color:#ecfeff
    classDef agent fill:#064e3b,stroke:#34d399,color:#ecfdf5
    classDef tool fill:#78350f,stroke:#fbbf24,color:#fffbeb
    classDef data fill:#4c1d95,stroke:#a78bfa,color:#f5f3ff
    classDef backend fill:#1e3a8a,stroke:#60a5fa,color:#eff6ff
    classDef external fill:#1e293b,stroke:#94a3b8,color:#f8fafc
    classDef control fill:#881337,stroke:#fb7185,color:#fff1f2
    A20_0["Log UI (text/photo)"]
    class A20_0 frontend
    A20_1["Food parser"]
    class A20_1 tool
    A20_2["Nutrient DB lookup"]
    class A20_2 tool
    A20_3["Trend analyzer"]
    class A20_3 tool
    A20_4["Coaching agent"]
    class A20_4 agent
    A20_5["Safety filter"]
    class A20_5 tool
    A20_6["Weekly report"]
    class A20_6 backend
    A20_0 --> A20_1
    A20_1 --> A20_2
    A20_2 --> A20_3
    A20_3 --> A20_4
    A20_4 --> A20_5
    A20_5 --> A20_6
    ID20["Entra ID + managed identity"]
    SAFE20["Policy, validation + approval gates"]
    OBS20["Tracing, metrics + evaluation"]
    class ID20,SAFE20,OBS20 control
    ID20 -. authentication .-> A20_1
    SAFE20 -. enforcement .-> A20_1
    OBS20 -. telemetry .-> A20_1
```

<!-- main-logic:auto -->
**Main execution logic**

1. **Authenticate and validate:** the edge/API layer verifies identity, tenant, request schema, quotas and correlation ID before agent execution.
2. **Load trusted context:** the application loads the minimum required profile, conversation checkpoint, domain state and authorization scope; sensitive fields stay outside prompts unless necessary.
3. **Plan with bounded authority:** the Foundry/Agent Framework adapter receives only allowlisted tool schemas and returns a structured proposal. The app-specific path is `Log UI (text/photo) -> Food parser -> Nutrient DB lookup -> Trend analyzer -> Coaching agent -> Safety filter -> Weekly report`.
4. **Ground every decision:** current facts such as price, availability, policy, entitlement or status come from retrieval and typed tools—not model memory.
5. **Apply deterministic policy:** code validates tool name, arguments, user authority, limits, risk class and output schema. Invalid proposals are rejected and audited.
6. **Approve consequential actions:** writes, purchases, bookings, messages, account changes and other high-impact operations pause for explicit human approval.
7. **Execute safely:** the controlled gateway invokes the narrow business operation with an idempotency key, timeout, bounded retry and compensation or dead-letter behavior.
8. **Commit and learn:** persist the result, return a source-grounded response, emit redacted traces and feed curated outcomes into regression evaluations.

**Runnable code pattern:** [C# policy, approval, idempotency and audit sample](../../samples/agent-workflow-csharp/README.md).


### Core components
Meal logging pipeline with photo recognition, food database matcher, portion estimator, goal engine, trend and insight analyzer, coaching agent, safety and referral filter, and notification scheduler.

### Agent/workflow design
The parser converts input to foods and portions, asking clarifying questions when confidence is low. Analytics are computed in code. The coaching agent turns trends into one or two achievable actions, using motivational-interviewing tone without moralizing about food.

### Data and integrations
Stores logs, goals, and measurements. Integrates nutrition databases, barcode lookups, wearables and health platforms such as Apple Health or Google Fit, and optional dietitian sharing, all consent-driven.

### Security and safety
Encrypt sensitive health data and give users granular consent and deletion. Do not diagnose or prescribe. Detect disordered-eating or medical-risk signals and redirect to professionals. Cap aggressive deficit goals and review claims against guidelines.

### Reliability, observability and evaluation
Show confidence for estimated entries and allow easy correction. Track logging retention, correction rates, and insight usefulness. Evaluate calorie and macro estimation error, and red-team safety responses for vulnerable users.

### MVP build path
Begin with text logging, database matching, and daily macro summaries. Add barcode and photo logging, then weekly insights and goal setting, then wearable integration and professional-sharing options.

## 21. Restaurant recommendation assistant

### Purpose and user journey
Recommends restaurants that fit a group's tastes, budget, location, and occasion. The user describes the situation, sees a short ranked list with reasons, refines by chatting, and moves on to booking or directions.

### Reference architecture
`Chat UI -> Preference parser -> Places search APIs -> Review/fit ranker -> Explanation generator -> Map/booking handoff`

<!-- architecture-diagram:auto -->
```mermaid
flowchart LR
    classDef frontend fill:#083344,stroke:#22d3ee,color:#ecfeff
    classDef agent fill:#064e3b,stroke:#34d399,color:#ecfdf5
    classDef tool fill:#78350f,stroke:#fbbf24,color:#fffbeb
    classDef data fill:#4c1d95,stroke:#a78bfa,color:#f5f3ff
    classDef backend fill:#1e3a8a,stroke:#60a5fa,color:#eff6ff
    classDef external fill:#1e293b,stroke:#94a3b8,color:#f8fafc
    classDef control fill:#881337,stroke:#fb7185,color:#fff1f2
    A21_0["Chat UI"]
    class A21_0 frontend
    A21_1["Preference parser"]
    class A21_1 tool
    A21_2["Places search APIs"]
    class A21_2 external
    A21_3["Review/fit ranker"]
    class A21_3 agent
    A21_4["Explanation generator"]
    class A21_4 tool
    A21_5["Map/booking handoff"]
    class A21_5 backend
    A21_0 --> A21_1
    A21_1 --> A21_2
    A21_2 --> A21_3
    A21_3 --> A21_4
    A21_4 --> A21_5
    ID21["Entra ID + managed identity"]
    SAFE21["Policy, validation + approval gates"]
    OBS21["Tracing, metrics + evaluation"]
    class ID21,SAFE21,OBS21 control
    ID21 -. authentication .-> A21_1
    SAFE21 -. enforcement .-> A21_1
    OBS21 -. telemetry .-> A21_1
```

<!-- main-logic:auto -->
**Main execution logic**

1. **Authenticate and validate:** the edge/API layer verifies identity, tenant, request schema, quotas and correlation ID before agent execution.
2. **Load trusted context:** the application loads the minimum required profile, conversation checkpoint, domain state and authorization scope; sensitive fields stay outside prompts unless necessary.
3. **Plan with bounded authority:** the Foundry/Agent Framework adapter receives only allowlisted tool schemas and returns a structured proposal. The app-specific path is `Chat UI -> Preference parser -> Places search APIs -> Review/fit ranker -> Explanation generator -> Map/booking handoff`.
4. **Ground every decision:** current facts such as price, availability, policy, entitlement or status come from retrieval and typed tools—not model memory.
5. **Apply deterministic policy:** code validates tool name, arguments, user authority, limits, risk class and output schema. Invalid proposals are rejected and audited.
6. **Approve consequential actions:** writes, purchases, bookings, messages, account changes and other high-impact operations pause for explicit human approval.
7. **Execute safely:** the controlled gateway invokes the narrow business operation with an idempotency key, timeout, bounded retry and compensation or dead-letter behavior.
8. **Commit and learn:** persist the result, return a source-grounded response, emit redacted traces and feed curated outcomes into regression evaluations.

**Runnable code pattern:** [C# policy, approval, idempotency and audit sample](../../samples/agent-workflow-csharp/README.md).


### Core components
Preference and constraint parser, geospatial search, review summarizer, hybrid ranker, group-preference merger, opening-hours validator, explanation generator, and a feedback loop recording choices.

### Agent/workflow design
The agent extracts hard constraints, such as diet, distance, and hours, and soft preferences, such as vibe and cuisine. Candidates come from search tools, deterministic filters apply, and the LLM ranks and explains with citations to review snippets.

### Data and integrations
Integrates map and places APIs, review sources, reservation platforms, menu data, and the user's saved places. Stores preference embeddings and choice feedback, respecting each provider's terms and caching limits.

### Security and safety
Minimize location sharing and retain only what is needed. Mark sponsored results clearly and avoid fabricated claims. Verify dietary and allergen claims against sources and caution that venues should be contacted to confirm them.

### Reliability, observability and evaluation
Handle API quota and stale-hours issues with caching and fallbacks. Log recommendations, clicks, and bookings. Evaluate relevance with labeled queries, hours accuracy, constraint violations, and hallucination rate in explanations.

### MVP build path
Start with one city, a places API, and filters plus LLM ranking with explanations. Add preference memory and group mode, then review-based fit summaries, then direct handoff to reservation and navigation.

## 22. Restaurant reservation assistant

### Purpose and user journey
Books, modifies, and cancels restaurant tables on the user's behalf. The user gives party size, time window, and preferences; the assistant checks availability, proposes options, confirms details, books, and adds the reservation to the calendar.

### Reference architecture
`Chat UI -> Reservation agent -> Availability connectors -> Booking executor -> Confirmation store -> Calendar/reminders`

<!-- architecture-diagram:auto -->
```mermaid
flowchart LR
    classDef frontend fill:#083344,stroke:#22d3ee,color:#ecfeff
    classDef agent fill:#064e3b,stroke:#34d399,color:#ecfdf5
    classDef tool fill:#78350f,stroke:#fbbf24,color:#fffbeb
    classDef data fill:#4c1d95,stroke:#a78bfa,color:#f5f3ff
    classDef backend fill:#1e3a8a,stroke:#60a5fa,color:#eff6ff
    classDef external fill:#1e293b,stroke:#94a3b8,color:#f8fafc
    classDef control fill:#881337,stroke:#fb7185,color:#fff1f2
    A22_0["Chat UI"]
    class A22_0 frontend
    A22_1["Reservation agent"]
    class A22_1 agent
    A22_2["Availability connectors"]
    class A22_2 external
    A22_3["Booking executor"]
    class A22_3 tool
    A22_4["Confirmation store"]
    class A22_4 data
    A22_5["Calendar/reminders"]
    class A22_5 external
    A22_0 --> A22_1
    A22_1 --> A22_2
    A22_2 --> A22_3
    A22_3 --> A22_4
    A22_4 --> A22_5
    ID22["Entra ID + managed identity"]
    SAFE22["Policy, validation + approval gates"]
    OBS22["Tracing, metrics + evaluation"]
    class ID22,SAFE22,OBS22 control
    ID22 -. authentication .-> A22_1
    SAFE22 -. enforcement .-> A22_1
    OBS22 -. telemetry .-> A22_1
```

<!-- main-logic:auto -->
**Main execution logic**

1. **Authenticate and validate:** the edge/API layer verifies identity, tenant, request schema, quotas and correlation ID before agent execution.
2. **Load trusted context:** the application loads the minimum required profile, conversation checkpoint, domain state and authorization scope; sensitive fields stay outside prompts unless necessary.
3. **Plan with bounded authority:** the Foundry/Agent Framework adapter receives only allowlisted tool schemas and returns a structured proposal. The app-specific path is `Chat UI -> Reservation agent -> Availability connectors -> Booking executor -> Confirmation store -> Calendar/reminders`.
4. **Ground every decision:** current facts such as price, availability, policy, entitlement or status come from retrieval and typed tools—not model memory.
5. **Apply deterministic policy:** code validates tool name, arguments, user authority, limits, risk class and output schema. Invalid proposals are rejected and audited.
6. **Approve consequential actions:** writes, purchases, bookings, messages, account changes and other high-impact operations pause for explicit human approval.
7. **Execute safely:** the controlled gateway invokes the narrow business operation with an idempotency key, timeout, bounded retry and compensation or dead-letter behavior.
8. **Commit and learn:** persist the result, return a source-grounded response, emit redacted traces and feed curated outcomes into regression evaluations.

**Runnable code pattern:** [C# policy, approval, idempotency and audit sample](../../samples/agent-workflow-csharp/README.md).


### Core components
Request parser, availability search across platforms, slot ranker, booking executor with idempotency, policy reader for deposits and cancellations, confirmation store, calendar sync, and reminder service.

### Agent/workflow design
The agent searches flexible windows, offers two or three slots, and states the cancellation terms before booking. A state machine moves from searching to proposed to confirmed. Where no API exists, it escalates to a call-script or email handoff.

### Data and integrations
Integrates reservation platforms such as OpenTable or Resy where permitted, restaurant phone or email channels, calendars, and messaging. Stores bookings, party profiles, and dietary notes with user consent.

### Security and safety
Require explicit confirmation before booking or paying any deposit. Show fees and no-show penalties. Guard against double-booking, protect guests' personal data, and limit automatic retries to avoid spamming venues.

### Reliability, observability and evaluation
Use idempotency keys, confirmation re-verification, and reminder checks to avoid ghost bookings. Track booking success, time to confirm, and cancellation rates. Evaluate against sandbox availability and simulated conflicts.

### MVP build path
Build availability lookup and a booking link handoff first. Then add API booking for one platform with confirmation and calendar events, then modification and cancellation, then multi-platform search and phone-call fallback.

## 23. Food-ordering agent

### Purpose and user journey
Orders delivery or pickup meals from natural-language requests. The user asks for a dish or reorder, the agent finds matching menus, builds the cart with customizations, displays the total, and places the order after approval, then tracks it.

### Reference architecture
`Chat UI -> Ordering agent -> Menu search -> Cart builder -> Price/ETA check -> Approval -> Payment/order API -> Tracker`

<!-- architecture-diagram:auto -->
```mermaid
flowchart LR
    classDef frontend fill:#083344,stroke:#22d3ee,color:#ecfeff
    classDef agent fill:#064e3b,stroke:#34d399,color:#ecfdf5
    classDef tool fill:#78350f,stroke:#fbbf24,color:#fffbeb
    classDef data fill:#4c1d95,stroke:#a78bfa,color:#f5f3ff
    classDef backend fill:#1e3a8a,stroke:#60a5fa,color:#eff6ff
    classDef external fill:#1e293b,stroke:#94a3b8,color:#f8fafc
    classDef control fill:#881337,stroke:#fb7185,color:#fff1f2
    A23_0["Chat UI"]
    class A23_0 frontend
    A23_1["Ordering agent"]
    class A23_1 agent
    A23_2["Menu search"]
    class A23_2 tool
    A23_3["Cart builder"]
    class A23_3 frontend
    A23_4["Price/ETA check"]
    class A23_4 tool
    A23_5["Approval"]
    class A23_5 frontend
    A23_6["Payment/order API"]
    class A23_6 external
    A23_7["Tracker"]
    class A23_7 backend
    A23_0 --> A23_1
    A23_1 --> A23_2
    A23_2 --> A23_3
    A23_3 --> A23_4
    A23_4 --> A23_5
    A23_5 --> A23_6
    A23_6 --> A23_7
    ID23["Entra ID + managed identity"]
    SAFE23["Policy, validation + approval gates"]
    OBS23["Tracing, metrics + evaluation"]
    class ID23,SAFE23,OBS23 control
    ID23 -. authentication .-> A23_1
    SAFE23 -. enforcement .-> A23_1
    OBS23 -. telemetry .-> A23_1
```

<!-- main-logic:auto -->
**Main execution logic**

1. **Authenticate and validate:** the edge/API layer verifies identity, tenant, request schema, quotas and correlation ID before agent execution.
2. **Load trusted context:** the application loads the minimum required profile, conversation checkpoint, domain state and authorization scope; sensitive fields stay outside prompts unless necessary.
3. **Plan with bounded authority:** the Foundry/Agent Framework adapter receives only allowlisted tool schemas and returns a structured proposal. The app-specific path is `Chat UI -> Ordering agent -> Menu search -> Cart builder -> Price/ETA check -> Approval -> Payment/order API -> Tracker`.
4. **Ground every decision:** current facts such as price, availability, policy, entitlement or status come from retrieval and typed tools—not model memory.
5. **Apply deterministic policy:** code validates tool name, arguments, user authority, limits, risk class and output schema. Invalid proposals are rejected and audited.
6. **Approve consequential actions:** writes, purchases, bookings, messages, account changes and other high-impact operations pause for explicit human approval.
7. **Execute safely:** the controlled gateway invokes the narrow business operation with an idempotency key, timeout, bounded retry and compensation or dead-letter behavior.
8. **Commit and learn:** persist the result, return a source-grounded response, emit redacted traces and feed curated outcomes into regression evaluations.

**Runnable code pattern:** [C# policy, approval, idempotency and audit sample](../../samples/agent-workflow-csharp/README.md).


### Core components
Menu index, item-to-modifier mapper, cart builder, fee and ETA estimator, approval step, payment handoff, order tracker, reorder history, and a dietary and allergen filter.

### Agent/workflow design
The agent resolves requests to menu items and modifiers, validates required options, and compares restaurants by price, fees, and ETA. It shows the complete cart and total before approval, then tracks status and handles substitutions or delays.

### Data and integrations
Integrates delivery platform or restaurant ordering APIs, payment providers, maps and tracking, and the user's address book. Stores order history, favorite items, and allergen preferences.

### Security and safety
Use tokenized payments, never raw card data. Enforce spending limits, explicit confirmation, and address verification. Treat allergen claims as unverified and recommend confirming with the restaurant. Log all actions for dispute resolution.

### Reliability, observability and evaluation
Handle unavailable items, price changes, and order failures with user prompts. Track conversion, error codes, and delivery-time accuracy. Evaluate menu-mapping accuracy, modifier correctness, and order success in sandbox tests.

### MVP build path
Begin with reorder of past orders on one platform with an approval screen. Add natural-language menu search and customizations, then multi-restaurant comparison, then live tracking, issue handling, and refund requests.
