# Consumer Support and Sustainability Assistants (Apps 85-93)

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
    TOOLS --> DOMAIN["Technology, utilities and sustainability tools and partner APIs"]
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


## 85. Consumer technical-support agent

**Purpose and user journey:** Resolves common product problems through chat or voice, from identification to resolution or handoff. A customer describes an issue, confirms product and warranty, follows guided checks, and receives a fix, replacement or human escalation.

**Reference architecture:** `Customer channel -> Identity/product lookup -> Support agent -> KB retrieval + diagnostic tools -> Policy engine -> Ticket system/human handoff`

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
    A85_0["Customer channel"]
    class A85_0 frontend
    A85_1["Identity/product lookup"]
    class A85_1 tool
    A85_2["Support agent"]
    class A85_2 agent
    A85_3["KB retrieval + diagnostic tools"]
    class A85_3 tool
    A85_4["Policy engine"]
    class A85_4 agent
    A85_5["Ticket system/human handoff"]
    class A85_5 backend
    A85_0 --> A85_1
    A85_1 --> A85_2
    A85_2 --> A85_3
    A85_3 --> A85_4
    A85_4 --> A85_5
    ID85["Entra ID + managed identity"]
    SAFE85["Policy, validation + approval gates"]
    OBS85["Tracing, metrics + evaluation"]
    class ID85,SAFE85,OBS85 control
    ID85 -. authentication .-> A85_1
    SAFE85 -. enforcement .-> A85_1
    OBS85 -. telemetry .-> A85_1
```

**Core components:** Intent classifier, product registry, knowledge-base retrieval, diagnostic runner, warranty and policy engine, ticketing connector, handoff summarizer, satisfaction survey.

**Agent/workflow design:** Verify the customer, identify the product and gather symptoms. Retrieve approved procedures, ask one step at a time, and run diagnostics. If confidence is low or the issue is safety-related, hand off with a full case summary.

**Data and integrations:** CRM, order and warranty systems, device telemetry with consent, knowledge articles, ticketing, shipping and returns APIs. Redact payment data and keep tool permissions scoped per intent.

**Security and safety:** Technical safety: warn about batteries, mains power, overheating and data loss before risky steps, and never give instructions that bypass safeguards. Authenticate before account actions, limit refunds by policy, resist prompt injection from tickets, and honour privacy rights.

**Reliability, observability and evaluation:** Track resolution rate, containment, escalation quality, policy violations, hallucinated procedures and customer satisfaction. Replay transcripts in regression suites, run red-team tests, sample human audits and alert when the knowledge base is stale.

**MVP build path:** Launch for one product line with retrieval-based answers, read-only order lookup and human handoff. Add diagnostics and ticket creation, then limited actions such as return labels, after approval controls and audit logs are working.

## 86. Device-setup assistant

**Purpose and user journey:** Guides users through setting up phones, routers, smart-home devices and peripherals. The user scans a model or QR code, receives a personalized checklist, completes steps with confirmations and finishes with a verification test.

**Reference architecture:** `Model scan -> Device catalog -> Setup agent -> Step-by-step guide + environment check -> Verification tests -> Completion record`

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
    A86_0["Model scan"]
    class A86_0 frontend
    A86_1["Device catalog"]
    class A86_1 tool
    A86_2["Setup agent"]
    class A86_2 agent
    A86_3["Step-by-step guide + environment check"]
    class A86_3 frontend
    A86_4["Verification tests"]
    class A86_4 tool
    A86_5["Completion record"]
    class A86_5 backend
    A86_0 --> A86_1
    A86_1 --> A86_2
    A86_2 --> A86_3
    A86_3 --> A86_4
    A86_4 --> A86_5
    ID86["Entra ID + managed identity"]
    SAFE86["Policy, validation + approval gates"]
    OBS86["Tracing, metrics + evaluation"]
    class ID86,SAFE86,OBS86 control
    ID86 -. authentication .-> A86_1
    SAFE86 -. enforcement .-> A86_1
    OBS86 -. telemetry .-> A86_1
```

**Core components:** Model recognizer, setup-procedure library, compatibility checker, step state tracker, network or app diagnostics, media and AR helper, backup reminders, completion verifier.

**Agent/workflow design:** Identify device and operating context, check compatibility, then produce a short ordered checklist. Deliver one step at a time with confirmation and rollback notes. Detect divergence and switch to troubleshooting.

**Data and integrations:** Manufacturer manuals, firmware metadata, app-store links, router and smart-home APIs, optional screenshots, and account-linking flows. Do not store Wi-Fi passwords or tokens in logs.

**Security and safety:** Technical safety: recommend official firmware, change default passwords, enable updates, warn before factory resets, and avoid unsafe electrical or battery steps. Never request passwords in chat. Check domains for official links and isolate guest or IoT networks when appropriate.

**Reliability, observability and evaluation:** Measure setup completion, time to finish, step abandonment and firmware-version mismatch. Test procedures on real devices, version guides by model and firmware, and mark unsupported models clearly. Collect anonymous failure points to improve guides.

**MVP build path:** Support three popular device types with curated guides, step tracking and a final test checklist. Add model recognition and compatibility checks, then connect to platform APIs with explicit consent and a clear permission screen.

## 87. Troubleshooting assistant

**Purpose and user journey:** Diagnoses faults in appliances, software and connected devices by asking targeted questions and proposing safe tests. A user reports symptoms, answers prompts, applies low-risk fixes and is told when to stop and contact a professional.

**Reference architecture:** `Symptom intake -> Triage agent -> Fault-tree/KB retrieval -> Test planner -> Risk gate -> Fix guidance or professional referral`

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
    A87_0["Symptom intake"]
    class A87_0 frontend
    A87_1["Triage agent"]
    class A87_1 agent
    A87_2["Fault-tree/KB retrieval"]
    class A87_2 tool
    A87_3["Test planner"]
    class A87_3 agent
    A87_4["Risk gate"]
    class A87_4 tool
    A87_5["Fix guidance or professional referral"]
    class A87_5 frontend
    A87_0 --> A87_1
    A87_1 --> A87_2
    A87_2 --> A87_3
    A87_3 --> A87_4
    A87_4 --> A87_5
    ID87["Entra ID + managed identity"]
    SAFE87["Policy, validation + approval gates"]
    OBS87["Tracing, metrics + evaluation"]
    class ID87,SAFE87,OBS87 control
    ID87 -. authentication .-> A87_1
    SAFE87 -. enforcement .-> A87_1
    OBS87 -. telemetry .-> A87_1
```

**Core components:** Symptom extractor, fault-tree library, manuals and forum retrieval, hypothesis ranker, test planner, risk classifier, log analyzer, case memory.

**Agent/workflow design:** Convert symptoms into candidate causes, choose the next most informative test, and update probabilities after each answer. Prefer reversible steps. The risk gate blocks hazardous procedures and routes to service, emergency or manufacturer support.

**Data and integrations:** Official manuals, error-code databases, logs, device status APIs, parts catalogs, service-booking links, and community content with provenance and quality scoring. Share logs only after user approval.

**Security and safety:** Technical safety: forbid opening live electrical equipment, gas appliance repair, bypassing safety interlocks and battery abuse. Give emergency guidance for smoke, gas smell or burning. Sanitize logs, resist malicious forum content, and disclose uncertainty clearly.

**Reliability, observability and evaluation:** Evaluate top-k diagnosis accuracy, average steps to resolution, unsafe-suggestion rate and referral appropriateness. Use expert-reviewed cases, adversarial hazard tests and feedback on fixes. Monitor repeated failures to identify missing fault trees.

**MVP build path:** Begin with home Wi-Fi and one appliance category using curated fault trees and safe tests. Add log upload, case memory and service referrals. Expand categories only after expert-reviewed safety rules exist.

## 88. Telecom-plan assistant

**Purpose and user journey:** Helps customers choose or change mobile, broadband and bundle plans. A user provides usage, location and preferences, compares eligible plans with total cost and contract terms, and receives a switching checklist.

**Reference architecture:** `Usage input -> Customer profile -> Plan agent -> Offer/coverage APIs -> Cost simulator -> Ranked comparison -> Switch checklist`

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
    A88_0["Usage input"]
    class A88_0 frontend
    A88_1["Customer profile"]
    class A88_1 data
    A88_2["Plan agent"]
    class A88_2 agent
    A88_3["Offer/coverage APIs"]
    class A88_3 external
    A88_4["Cost simulator"]
    class A88_4 tool
    A88_5["Ranked comparison"]
    class A88_5 tool
    A88_6["Switch checklist"]
    class A88_6 backend
    A88_0 --> A88_1
    A88_1 --> A88_2
    A88_2 --> A88_3
    A88_3 --> A88_4
    A88_4 --> A88_5
    A88_5 --> A88_6
    ID88["Entra ID + managed identity"]
    SAFE88["Policy, validation + approval gates"]
    OBS88["Tracing, metrics + evaluation"]
    class ID88,SAFE88,OBS88 control
    ID88 -. authentication .-> A88_1
    SAFE88 -. enforcement .-> A88_1
    OBS88 -. telemetry .-> A88_1
```

**Core components:** Usage analyzer, plan catalog, coverage and address checker, total-cost simulator, contract-term extractor, recommendation ranker, switching workflow, explanation generator.

**Agent/workflow design:** Collect needs, estimate monthly usage from bills or manual entry, and filter by availability. Compute twelve- and twenty-four-month costs including promotions, fees, roaming and penalties. Explain trade-offs and ask for confirmation before any action.

**Data and integrations:** Carrier catalogs, regulator comparison data, coverage maps, bills via user upload, number-porting information, affiliate disclosures, CRM or store APIs where operated by the provider.

**Security and safety:** Technical and consumer safety: disclose commissions, avoid dark patterns and never hide minimum terms. Protect bills, phone numbers and addresses. Require strong authentication for plan changes, port-outs or SIM actions to reduce SIM-swap fraud, and keep humans in the loop.

**Reliability, observability and evaluation:** Validate prices daily and flag stale offers. Test the cost simulator against known bills, evaluate ranking with fixed scenarios, track complaint rates and recommendation overrides, and audit explanations for omitted fees or misleading comparisons.

**MVP build path:** Start with one country and mobile plans using manual usage entry, a verified catalog and a transparent cost calculator. Add bill parsing and coverage checks, then a switching checklist. Introduce account actions only after fraud controls are tested.

## 89. Energy-plan comparison assistant

**Purpose and user journey:** Helps households compare electricity and gas tariffs using consumption, time-of-use patterns and priorities such as price, renewable share or stability. The user uploads usage, reviews ranked options and receives switching guidance.

**Reference architecture:** `Bills/smart-meter data -> Usage model -> Energy agent -> Tariff API -> Cost + risk simulator -> Ranked plans -> Switch guide`

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
    A89_0["Bills/smart-meter data"]
    class A89_0 frontend
    A89_1["Usage model"]
    class A89_1 tool
    A89_2["Energy agent"]
    class A89_2 agent
    A89_3["Tariff API"]
    class A89_3 external
    A89_4["Cost + risk simulator"]
    class A89_4 tool
    A89_5["Ranked plans"]
    class A89_5 tool
    A89_6["Switch guide"]
    class A89_6 frontend
    A89_0 --> A89_1
    A89_1 --> A89_2
    A89_2 --> A89_3
    A89_3 --> A89_4
    A89_4 --> A89_5
    A89_5 --> A89_6
    ID89["Entra ID + managed identity"]
    SAFE89["Policy, validation + approval gates"]
    OBS89["Tracing, metrics + evaluation"]
    class ID89,SAFE89,OBS89 control
    ID89 -. authentication .-> A89_1
    SAFE89 -. enforcement .-> A89_1
    OBS89 -. telemetry .-> A89_1
```

**Core components:** Meter-data importer, load-profile estimator, tariff normalizer, cost and exit-fee simulator, renewable-claim checker, solar and battery modeler, comparison explainer, reminder service.

**Agent/workflow design:** Normalize usage, simulate each eligible tariff under baseline and high-use scenarios, and rank by user priorities. Highlight variable-rate risk, standing charges and contract ends. Ask for confirmation before submitting any switch request.

**Data and integrations:** Regulated tariff databases, smart-meter or utility APIs, postal-code eligibility, weather and price indices, provider renewable disclosures, and calendar reminders for contract renewals.

**Security and safety:** Sustainability safety: verify renewable claims, distinguish certificates from physical supply, and avoid greenwashing. Technical safety: do not advise tampering with meters or electrical wiring. Protect meter identifiers and consumption data and require explicit consent for data sharing.

**Reliability, observability and evaluation:** Test bill simulation against actual invoices, monitor tariff freshness and API failures, and report uncertainty ranges. Evaluate ranking quality on historical households, audit fairness for sponsored offers and track realized savings against estimates.

**MVP build path:** Ship manual annual-usage entry, one region's tariff feed, cost comparison and exit-fee warnings. Add bill upload and smart-meter import, then time-of-use simulation and solar scenarios. Integrate switching only after regulatory review.

## 90. Sustainability coach

**Purpose and user journey:** Helps people adopt realistic low-impact habits across home, travel, food and shopping. A user sets goals, receives prioritized actions, tracks progress and gets monthly feedback about effort, cost and likely environmental benefit.

**Reference architecture:** `Goal profile -> Habit planner -> Coach agent -> Impact library + local data -> Action recommender -> Progress tracker -> Check-ins`

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
    A90_0["Goal profile"]
    class A90_0 frontend
    A90_1["Habit planner"]
    class A90_1 agent
    A90_2["Coach agent"]
    class A90_2 agent
    A90_3["Impact library + local data"]
    class A90_3 tool
    A90_4["Action recommender"]
    class A90_4 tool
    A90_5["Progress tracker"]
    class A90_5 tool
    A90_6["Check-ins"]
    class A90_6 backend
    A90_0 --> A90_1
    A90_1 --> A90_2
    A90_2 --> A90_3
    A90_3 --> A90_4
    A90_4 --> A90_5
    A90_5 --> A90_6
    ID90["Entra ID + managed identity"]
    SAFE90["Policy, validation + approval gates"]
    OBS90["Tracing, metrics + evaluation"]
    class ID90,SAFE90,OBS90 control
    ID90 -. authentication .-> A90_1
    SAFE90 -. enforcement .-> A90_1
    OBS90 -. telemetry .-> A90_1
```

**Core components:** Onboarding profile, action library with impact estimates, local-service finder, habit tracker, savings estimator, motivation messaging, community challenge module, evidence registry.

**Agent/workflow design:** Rank actions by impact, feasibility and cost. Break goals into small experiments, adapt after missed check-ins, and explain assumptions. Offer alternatives rather than guilt, and recommend professional help for retrofits or major purchases.

**Data and integrations:** Emission factors, local recycling and transit data, energy and mobility apps, optional wearables or utility feeds, and verified guidance from public agencies. Personal habits stay private unless a user shares them.

**Security and safety:** Sustainability safety: avoid greenwashing, rebound-effect blind spots and unsafe DIY advice for insulation, electrical work, refrigerants or waste disposal. Do not shame users, avoid sponsored bias, and provide consent controls for location, purchase and community data.

**Reliability, observability and evaluation:** Monitor recommendation uptake, retained habits, estimate uncertainty and complaint rates. Audit impact claims against sources, test local-rule accuracy, run user studies on perceived helpfulness and withdraw outdated or unsupported actions.

**MVP build path:** Launch with a questionnaire, ten high-impact action cards, tracking and weekly nudges in one region. Add savings estimates and local resources, then community challenges. Review every claim with a sustainability expert before scaling.

## 91. Carbon-footprint assistant

**Purpose and user journey:** Estimates personal or household emissions and shows how changes would alter them. A user enters or imports travel, energy, diet and purchases, receives a transparent footprint breakdown, compares scenarios and tracks reductions.

**Reference architecture:** `Activity data -> Normalizer -> Footprint agent -> Emission-factor engine -> Scenario simulator -> Report + uncertainty ranges -> History store`

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
    A91_0["Activity data"]
    class A91_0 frontend
    A91_1["Normalizer"]
    class A91_1 tool
    A91_2["Footprint agent"]
    class A91_2 agent
    A91_3["Emission-factor engine"]
    class A91_3 agent
    A91_4["Scenario simulator"]
    class A91_4 tool
    A91_5["Report + uncertainty ranges"]
    class A91_5 tool
    A91_6["History store"]
    class A91_6 data
    A91_0 --> A91_1
    A91_1 --> A91_2
    A91_2 --> A91_3
    A91_3 --> A91_4
    A91_4 --> A91_5
    A91_5 --> A91_6
    ID91["Entra ID + managed identity"]
    SAFE91["Policy, validation + approval gates"]
    OBS91["Tracing, metrics + evaluation"]
    class ID91,SAFE91,OBS91 control
    ID91 -. authentication .-> A91_1
    SAFE91 -. enforcement .-> A91_1
    OBS91 -. telemetry .-> A91_1
```

**Core components:** Activity importers, unit normalizer, emission-factor database, calculation engine, uncertainty estimator, scenario planner, methodology explainer, report exporter, offset-claim checker.

**Agent/workflow design:** Parse activities, ask for missing quantities, and use the calculation engine rather than model arithmetic. Select region- and year-specific factors, show ranges, and simulate changes such as commuting or tariff switching. The agent explains method and limits.

**Data and integrations:** Public emission-factor datasets, grid intensity APIs, mobility and utility imports, receipts or bank categories with opt-in, product databases, and standards such as the GHG Protocol. Version all factors.

**Security and safety:** Sustainability safety: state boundaries, avoid false precision, never present offsets as erasing emissions, and disclose data gaps. Technical and privacy safety: minimize bank and location access, encrypt histories, support deletion, and prevent calculation tools from executing untrusted code.

**Reliability, observability and evaluation:** Unit-test calculations against reference cases, track factor versions, flag outliers and measure estimate error where verified data exist. Evaluate explanations for correct caveats and monitor user correction rates and unsupported category mappings.

**MVP build path:** Build a manual calculator for transport, home energy and food with a versioned factor table, ranges and an explanation of method. Add imports and scenario comparisons next, then independent methodology review before any public claims.

## 92. Gardening assistant

**Purpose and user journey:** Helps home gardeners plan, plant and maintain gardens. A user enters location, space, sun, soil and goals, receives a seasonal plan, plant suggestions, watering and pest-prevention reminders, and logs progress with photos.

**Reference architecture:** `Garden profile -> Climate/soil lookup -> Garden agent -> Plant database + calendar planner -> Reminders -> Journal/photo log`

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
    A92_0["Garden profile"]
    class A92_0 frontend
    A92_1["Climate/soil lookup"]
    class A92_1 tool
    A92_2["Garden agent"]
    class A92_2 agent
    A92_3["Plant database + calendar planner"]
    class A92_3 data
    A92_4["Reminders"]
    class A92_4 tool
    A92_5["Journal/photo log"]
    class A92_5 backend
    A92_0 --> A92_1
    A92_1 --> A92_2
    A92_2 --> A92_3
    A92_3 --> A92_4
    A92_4 --> A92_5
    ID92["Entra ID + managed identity"]
    SAFE92["Policy, validation + approval gates"]
    OBS92["Tracing, metrics + evaluation"]
    class ID92,SAFE92,OBS92 control
    ID92 -. authentication .-> A92_1
    SAFE92 -. enforcement .-> A92_1
    OBS92 -. telemetry .-> A92_1
```

**Core components:** Hardiness-zone lookup, plant and companion database, planting-calendar engine, watering scheduler, soil-test interpreter, weather connector, garden journal, shopping list generator.

**Agent/workflow design:** Build a profile, filter plants by climate and constraints, create a sequenced calendar and adjust for weather. Ask clarifying questions when soil or light data is missing. Prefer low-risk cultural practices before products, and escalate serious problems to local extension services.

**Data and integrations:** Local climate and frost dates, weather forecasts, regional plant databases, extension-service guidance, soil-test results, calendar and notification systems, optional garden-sensor feeds. Location precision is user-controlled.

**Security and safety:** Sustainability safety: recommend native or non-invasive species, water-saving practices and integrated pest management. Technical and health safety: warn about toxic plants for children and pets, pesticide label compliance, tool and electrical hazards, and foraging risks. Avoid unverified chemical mixes.

**Reliability, observability and evaluation:** Evaluate zone and frost-date accuracy, plant suitability, invasive-species checks and reminder usefulness. Monitor weather API failures and user corrections. Use horticulturist-reviewed scenarios and regional regression tests, and expire stale seasonal advice.

**MVP build path:** Start with one climate region and 100 common vegetables and herbs. Deliver profile intake, planting calendar, watering reminders and a journal. Add weather adjustment and soil-test interpretation, then expand regions with local expert review.

## 93. Plant-diagnosis assistant

**Purpose and user journey:** Identifies likely causes of plant problems from photos and descriptions, then suggests confirmation tests and treatments. A user uploads leaf, stem and whole-plant images, answers care questions, and receives ranked possibilities with confidence and next steps.

**Reference architecture:** `Photo/care intake -> Image quality check -> Vision + symptom models -> Diagnosis agent -> Differential list -> Treatment guide -> Follow-up tracker`

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
    A93_0["Photo/care intake"]
    class A93_0 frontend
    A93_1["Image quality check"]
    class A93_1 tool
    A93_2["Vision + symptom models"]
    class A93_2 tool
    A93_3["Diagnosis agent"]
    class A93_3 agent
    A93_4["Differential list"]
    class A93_4 tool
    A93_5["Treatment guide"]
    class A93_5 frontend
    A93_6["Follow-up tracker"]
    class A93_6 backend
    A93_0 --> A93_1
    A93_1 --> A93_2
    A93_2 --> A93_3
    A93_3 --> A93_4
    A93_4 --> A93_5
    A93_5 --> A93_6
    ID93["Entra ID + managed identity"]
    SAFE93["Policy, validation + approval gates"]
    OBS93["Tracing, metrics + evaluation"]
    class ID93,SAFE93,OBS93 control
    ID93 -. authentication .-> A93_1
    SAFE93 -. enforcement .-> A93_1
    OBS93 -. telemetry .-> A93_1
```

**Core components:** Image quality checker, plant identifier, disease and pest classifier, symptom questionnaire, care-history analyzer, differential ranker, treatment knowledge base, outcome tracker, expert escalation.

**Agent/workflow design:** Check the image, identify the plant, and ask about watering, light, recent changes and pests. Combine visual and contextual evidence into ranked hypotheses. Recommend non-chemical tests first, then treatments, and ask for a follow-up photo.

**Data and integrations:** Labeled plant-pathology images, extension-service diagnostics, regional pest alerts, weather and care logs, garden-profile integration, and lab or expert-referral links. Images are stored privately and metadata location can be removed.

**Security and safety:** Technical and health safety: do not overstate confidence, never recommend mixing chemicals, enforce label and local legal limits, and warn about toxicity to people, pets and pollinators. Sustainability safety: favor cultural and biological controls and prevent spreading quarantined pests.

**Reliability, observability and evaluation:** Measure top-three accuracy by species and region, calibration, low-quality-image rejection, harmful-advice rate and follow-up recovery. Test with expert-labeled holdout images, confusing look-alikes and out-of-distribution plants. Show uncertainty and route unknowns to experts.

**MVP build path:** Launch with a narrow set of common houseplants and vegetables, image-quality checks, ranked causes and conservative cultural advice. Add the follow-up tracker, regional pest alerts and expert review queue before enabling any pesticide-specific recommendations.
