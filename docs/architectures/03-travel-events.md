# Travel and Events

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
    TOOLS --> DOMAIN["Travel and events tools and partner APIs"]
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


## 24. Travel-planning assistant

### Purpose and user journey
Turns vague travel ideas into a workable trip plan covering destination, dates, budget, and logistics. The user describes goals, compares shortlisted options, refines through conversation, and exports a plan ready for booking.

### Reference architecture
`Chat UI -> Trip planner agent -> Destination/price/weather tools -> Constraint scorer -> Plan builder -> Shareable trip workspace`

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
    A24_0["Chat UI"]
    class A24_0 frontend
    A24_1["Trip planner agent"]
    class A24_1 agent
    A24_2["Destination/price/weather tools"]
    class A24_2 tool
    A24_3["Constraint scorer"]
    class A24_3 tool
    A24_4["Plan builder"]
    class A24_4 frontend
    A24_5["Shareable trip workspace"]
    class A24_5 backend
    A24_0 --> A24_1
    A24_1 --> A24_2
    A24_2 --> A24_3
    A24_3 --> A24_4
    A24_4 --> A24_5
    ID24["Entra ID + managed identity"]
    SAFE24["Policy, validation + approval gates"]
    OBS24["Tracing, metrics + evaluation"]
    class ID24,SAFE24,OBS24 control
    ID24 -. authentication .-> A24_1
    SAFE24 -. enforcement .-> A24_1
    OBS24 -. telemetry .-> A24_1
```

### Core components
Traveler profile, destination knowledge retrieval, budget estimator, seasonality and weather service, visa and entry requirement lookup, option comparer, trip workspace, and collaboration and sharing features.

### Agent/workflow design
The agent clarifies constraints, calls tools for fares, lodging price ranges, and weather, and scores destinations against preferences. It presents tradeoffs, drafts a high-level plan, and delegates detail work to flight, hotel, and itinerary agents.

### Data and integrations
Integrates travel search APIs, weather and climate data, government advisory and entry-requirement sources, maps, and calendars. Stores trips, preferences, and traveler documents' metadata, not the documents themselves.

### Security and safety
Protect passport and identity details and share trips by scoped links. Cite official sources for visa and safety advisories, show data freshness, and avoid presenting unverified entry rules as guaranteed.

### Reliability, observability and evaluation
Degrade gracefully when providers fail, labeling estimates. Trace tool calls and track plan acceptance. Evaluate budget estimate error, advisory accuracy, constraint satisfaction, and user-rated plan usefulness.

### MVP build path
Launch with destination suggestions and budget estimates from one data source. Add weather and entry requirements, then a shareable plan, then integrations to flight, hotel, and itinerary modules and collaborative editing.

## 25. Flight-search assistant

### Purpose and user journey
Finds and compares flights using natural-language preferences. The user states route, dates, flexibility, and priorities; the assistant returns ranked itineraries with tradeoffs, explains fare rules, and can set price alerts.

### Reference architecture
`Chat UI -> Query normalizer -> Flight search APIs -> Itinerary ranker -> Fare-rule explainer -> Price alert service`

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
    A25_0["Chat UI"]
    class A25_0 frontend
    A25_1["Query normalizer"]
    class A25_1 tool
    A25_2["Flight search APIs"]
    class A25_2 external
    A25_3["Itinerary ranker"]
    class A25_3 agent
    A25_4["Fare-rule explainer"]
    class A25_4 tool
    A25_5["Price alert service"]
    class A25_5 backend
    A25_0 --> A25_1
    A25_1 --> A25_2
    A25_2 --> A25_3
    A25_3 --> A25_4
    A25_4 --> A25_5
    ID25["Entra ID + managed identity"]
    SAFE25["Policy, validation + approval gates"]
    OBS25["Tracing, metrics + evaluation"]
    class ID25,SAFE25,OBS25 control
    ID25 -. authentication .-> A25_1
    SAFE25 -. enforcement .-> A25_1
    OBS25 -. telemetry .-> A25_1
```

### Core components
Query normalizer, airport and date flexibility expander, GDS or aggregator connectors, itinerary scorer weighing price, duration, and layovers, fare-rule parser, baggage calculator, and price-alert scheduler.

### Agent/workflow design
The agent translates preferences into structured searches, runs flexible-date and nearby-airport variants in parallel, and ranks results with a transparent score. It explains total cost with bags and seats and never guesses fares.

### Data and integrations
Integrates flight aggregator and airline APIs, airport and airline reference data, loyalty program balances, and calendars. Stores searches, alerts, and preferences such as airlines, seat, and maximum stops.

### Security and safety
Present only provider-returned prices with timestamps. Disclose affiliate relationships, avoid dark patterns, protect loyalty credentials with scoped tokens, and warn that fares change before booking.

### Reliability, observability and evaluation
Cache short-lived results, handle rate limits, and detect stale fares. Log search latency, result coverage, and alert accuracy. Evaluate ranking against human choices and price parity with provider booking pages.

### MVP build path
Start with one aggregator, round-trip search, and ranking with explanations. Add flexible dates and multi-city, then fare rules and baggage cost, then price alerts and loyalty-aware recommendations.

## 26. Hotel recommendation assistant

### Purpose and user journey
Recommends hotels and stays that match traveler needs such as location, budget, amenities, and trip purpose. The user describes the trip, reviews a ranked shortlist with neighborhood context, compares options, and proceeds to booking.

### Reference architecture
`Chat UI -> Requirement extractor -> Hotel inventory APIs -> Review/location analyzer -> Ranker -> Comparison view -> Booking handoff`

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
    A26_0["Chat UI"]
    class A26_0 frontend
    A26_1["Requirement extractor"]
    class A26_1 frontend
    A26_2["Hotel inventory APIs"]
    class A26_2 external
    A26_3["Review/location analyzer"]
    class A26_3 tool
    A26_4["Ranker"]
    class A26_4 agent
    A26_5["Comparison view"]
    class A26_5 tool
    A26_6["Booking handoff"]
    class A26_6 backend
    A26_0 --> A26_1
    A26_1 --> A26_2
    A26_2 --> A26_3
    A26_3 --> A26_4
    A26_4 --> A26_5
    A26_5 --> A26_6
    ID26["Entra ID + managed identity"]
    SAFE26["Policy, validation + approval gates"]
    OBS26["Tracing, metrics + evaluation"]
    class ID26,SAFE26,OBS26 control
    ID26 -. authentication .-> A26_1
    SAFE26 -. enforcement .-> A26_1
    OBS26 -. telemetry .-> A26_1
```

### Core components
Requirement extractor, inventory search, neighborhood and distance scorer, review aspect summarizer, amenity filter, price and fee normalizer, comparison view, and a preference memory.

### Agent/workflow design
The agent applies hard filters, then ranks by weighted preferences such as quiet, walkability, or business facilities. The LLM summarizes review themes by aspect and flags mismatches, while totals including taxes and resort fees are calculated in code.

### Data and integrations
Integrates hotel supply APIs, review sources, maps and transit data, and calendars. Stores preferences, past stays, and shortlists, caching listings within provider terms.

### Security and safety
Disclose sponsored placement and fees. Avoid fabricating amenities and show source and freshness. Use accessibility data carefully and encourage verification with the hotel. Limit the personal data shared with suppliers.

### Reliability, observability and evaluation
Handle inventory changes and fallback providers. Track shortlist-to-booking conversion and complaints about mismatches. Evaluate ranking quality, review summary faithfulness, and fee accuracy against provider checkout totals.

### MVP build path
Build city-level search with filters and ranked results. Add review summaries and neighborhood analysis, then side-by-side comparison, then personalization from past stays and booking handoff.

## 27. Trip-booking assistant

### Purpose and user journey
Executes bookings for flights, hotels, and extras from an approved plan. The user reviews a consolidated itinerary and price, confirms traveler details and payment, and receives confirmations, receipts, and changes in one place.

### Reference architecture
`Approved plan -> Booking orchestrator -> Provider booking APIs -> Payment service -> Confirmation vault -> Itinerary sync/notifications`

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
    A27_0["Approved plan"]
    class A27_0 frontend
    A27_1["Booking orchestrator"]
    class A27_1 agent
    A27_2["Provider booking APIs"]
    class A27_2 external
    A27_3["Payment service"]
    class A27_3 external
    A27_4["Confirmation vault"]
    class A27_4 tool
    A27_5["Itinerary sync/notifications"]
    class A27_5 backend
    A27_0 --> A27_1
    A27_1 --> A27_2
    A27_2 --> A27_3
    A27_3 --> A27_4
    A27_4 --> A27_5
    ID27["Entra ID + managed identity"]
    SAFE27["Policy, validation + approval gates"]
    OBS27["Tracing, metrics + evaluation"]
    class ID27,SAFE27,OBS27 control
    ID27 -. authentication .-> A27_1
    SAFE27 -. enforcement .-> A27_1
    OBS27 -. telemetry .-> A27_1
```

### Core components
Booking orchestrator with saga pattern, traveler profile vault, price revalidation, payment integration, confirmation store, rollback and cancellation handler, receipts service, and notification service.

### Agent/workflow design
The agent assembles a booking checklist, revalidates prices and availability, and obtains one explicit approval summarizing total, fees, and cancellation terms. The orchestrator then books components in order, compensating or cancelling on partial failure.

### Data and integrations
Integrates airline, hotel, and rail booking APIs, payment processors, passport and loyalty profiles, calendars, and email parsing for confirmations. Stores bookings, PNRs, and policies as structured records.

### Security and safety
PCI-compliant tokenized payments, encrypted identity data, strong authentication, and spend limits. Require name-match checks against passports, show refund terms, and keep an immutable audit log of approvals and charges.

### Reliability, observability and evaluation
Use idempotency keys and reconciliation jobs to catch uncertain bookings. Alert on partial failures and price drift. Evaluate with sandbox providers, failure injection, and end-to-end tests for rollback correctness.

### MVP build path
Begin with hotel-only booking in a provider sandbox with approval and confirmation storage. Add flights, then bundled saga orchestration and rollback, then changes and cancellations and corporate policy rules.

## 28. Itinerary generator

### Purpose and user journey
Produces day-by-day itineraries balancing interests, pace, logistics, and opening hours. The user gives destination, dates, and interests, receives a map-aware schedule, and edits by chat or drag and drop.

### Reference architecture
`Preferences -> Candidate POI retrieval -> Route/time optimizer -> Itinerary composer -> Editable map/calendar view -> Export`

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
    A28_0["Preferences"]
    class A28_0 frontend
    A28_1["Candidate POI retrieval"]
    class A28_1 tool
    A28_2["Route/time optimizer"]
    class A28_2 tool
    A28_3["Itinerary composer"]
    class A28_3 tool
    A28_4["Editable map/calendar view"]
    class A28_4 external
    A28_5["Export"]
    class A28_5 backend
    A28_0 --> A28_1
    A28_1 --> A28_2
    A28_2 --> A28_3
    A28_3 --> A28_4
    A28_4 --> A28_5
    ID28["Entra ID + managed identity"]
    SAFE28["Policy, validation + approval gates"]
    OBS28["Tracing, metrics + evaluation"]
    class ID28,SAFE28,OBS28 control
    ID28 -. authentication .-> A28_1
    SAFE28 -. enforcement .-> A28_1
    OBS28 -. telemetry .-> A28_1
```

### Core components
POI retrieval index, opening-hours and ticket checker, travel-time estimator, day clustering optimizer, pace and energy model, itinerary composer, editor, and calendar and offline export.

### Agent/workflow design
The agent retrieves candidates matching interests, clusters them geographically, and runs an optimizer under time constraints. The LLM writes rationale and alternatives, and local edits re-optimize only the affected day while locking pinned items.

### Data and integrations
Integrates places and maps APIs, transit and routing services, event listings, weather, and booked flights and hotels for anchors. Stores itineraries, saved places, and traveler preferences.

### Security and safety
Avoid recommending closed, unsafe, or restricted venues and surface advisories. Check accessibility needs where data exists. Limit location sharing in shared itineraries and mark unverified suggestions clearly.

### Reliability, observability and evaluation
Validate every item for hours and feasibility before display. Track edit rates as a quality signal. Evaluate with test trips for travel-time realism, constraint violations, diversity, and user satisfaction.

### MVP build path
Generate a one-city multi-day plan from curated POIs with travel-time checks. Add map editing and re-optimization, then hours and ticket validation, then booking anchors, offline export, and group preferences.

## 29. Travel-disruption assistant

### Purpose and user journey
Monitors trips for delays, cancellations, and other disruptions and helps recover quickly. The user's itinerary is tracked; on a disruption, the assistant explains impact, proposes rebooking options, and assists with claims.

### Reference architecture
`Itinerary store -> Flight/status monitors -> Disruption detector -> Recovery agent -> Rebooking options -> Approval -> Notifications/claims`

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
    A29_0["Itinerary store"]
    class A29_0 frontend
    A29_1["Flight/status monitors"]
    class A29_1 tool
    A29_2["Disruption detector"]
    class A29_2 tool
    A29_3["Recovery agent"]
    class A29_3 agent
    A29_4["Rebooking options"]
    class A29_4 tool
    A29_5["Approval"]
    class A29_5 frontend
    A29_6["Notifications/claims"]
    class A29_6 backend
    A29_0 --> A29_1
    A29_1 --> A29_2
    A29_2 --> A29_3
    A29_3 --> A29_4
    A29_4 --> A29_5
    A29_5 --> A29_6
    ID29["Entra ID + managed identity"]
    SAFE29["Policy, validation + approval gates"]
    OBS29["Tracing, metrics + evaluation"]
    class ID29,SAFE29,OBS29 control
    ID29 -. authentication .-> A29_1
    SAFE29 -. enforcement .-> A29_1
    OBS29 -. telemetry .-> A29_1
```

### Core components
Status polling and webhooks, disruption detector, connection-risk calculator, recovery option generator, rights and compensation rules engine, notification service, rebooking executor, and claim-document builder.

### Agent/workflow design
Events trigger a severity classifier. The agent assesses downstream impacts on connections, hotels, and transfers, ranks recovery options by arrival time and cost, and drafts airline messages. Rebooking or purchases require explicit approval.

### Data and integrations
Integrates flight status APIs, airline rebooking channels, airport and weather feeds, hotel and ground-transport bookings, and messaging or push channels. Stores itineraries, PNRs, and disruption timelines.

### Security and safety
Push alerts only to verified channels and avoid exposing booking codes in plaintext. Present passenger-rights information as guidance with jurisdiction caveats, and require approval before spending or cancelling.

### Reliability, observability and evaluation
Redundant status sources and deduplicated alerts prevent missed or noisy notifications. Track detection latency, false alarms, and recovery success. Evaluate with replayed historical disruptions and rights-rule test suites.

### MVP build path
Start with flight-status monitoring and timely alerts for imported itineraries. Add connection-risk analysis, then recovery option suggestions, then compensation guidance and claim drafting, then approved rebooking actions.

## 30. Local activity concierge

### Purpose and user journey
Suggests things to do nearby right now or later, matched to mood, group, weather, and budget. The user asks for ideas, gets a few time-aware options with logistics, and can save, share, or book.

### Reference architecture
`Context (location/time/weather) -> Concierge agent -> Places/events retrieval -> Context ranker -> Suggestions -> Save/share/book`

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
    A30_0["Context (location/time/weather)"]
    class A30_0 frontend
    A30_1["Concierge agent"]
    class A30_1 agent
    A30_2["Places/events retrieval"]
    class A30_2 tool
    A30_3["Context ranker"]
    class A30_3 agent
    A30_4["Suggestions"]
    class A30_4 tool
    A30_5["Save/share/book"]
    class A30_5 backend
    A30_0 --> A30_1
    A30_1 --> A30_2
    A30_2 --> A30_3
    A30_3 --> A30_4
    A30_4 --> A30_5
    ID30["Entra ID + managed identity"]
    SAFE30["Policy, validation + approval gates"]
    OBS30["Tracing, metrics + evaluation"]
    class ID30,SAFE30,OBS30 control
    ID30 -. authentication .-> A30_1
    SAFE30 -. enforcement .-> A30_1
    OBS30 -. telemetry .-> A30_1
```

### Core components
Context collector, places and events retrieval, weather-aware ranker, travel-time calculator, group preference blender, novelty and diversity controller, saved list, and booking handoff.

### Agent/workflow design
The agent infers intent such as date night or kids' afternoon, retrieves open venues and events within reach, and ranks by fit, travel time, and weather. It offers a small set with one surprise pick and learns from selections.

### Data and integrations
Integrates places, events, weather, and transit APIs, local tourism feeds, and calendars. Stores interests, past choices, and saved places with location history kept on-device or short-lived.

### Security and safety
Use coarse location by default and ask before precise tracking. Filter age-appropriate and safety-relevant content, label sponsored items, and avoid steering users toward unsafe areas or closed venues.

### Reliability, observability and evaluation
Verify hours and event times at request time and cache with short TTLs. Track suggestion click-through and completion. Evaluate relevance, freshness, and diversity using scenario tests across times and weather.

### MVP build path
Build a single-city suggester using places data, weather, and distance. Add events feeds and preference learning, then group and kid modes, then saved plans, booking links, and proactive suggestions.

## 31. Event-planning assistant

### Purpose and user journey
Guides organizers through planning parties, meetings, and gatherings. The user states event type, size, budget, and date; the assistant builds a plan, shortlists venues and vendors, tracks tasks and RSVPs, and manages the timeline.

### Reference architecture
`Brief -> Planner agent -> Venue/vendor search -> Budget/task engine -> Guest/RSVP service -> Timeline dashboard -> Vendor messaging`

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
    A31_0["Brief"]
    class A31_0 frontend
    A31_1["Planner agent"]
    class A31_1 agent
    A31_2["Venue/vendor search"]
    class A31_2 external
    A31_3["Budget/task engine"]
    class A31_3 agent
    A31_4["Guest/RSVP service"]
    class A31_4 tool
    A31_5["Timeline dashboard"]
    class A31_5 tool
    A31_6["Vendor messaging"]
    class A31_6 external
    A31_0 --> A31_1
    A31_1 --> A31_2
    A31_2 --> A31_3
    A31_3 --> A31_4
    A31_4 --> A31_5
    A31_5 --> A31_6
    ID31["Entra ID + managed identity"]
    SAFE31["Policy, validation + approval gates"]
    OBS31["Tracing, metrics + evaluation"]
    class ID31,SAFE31,OBS31 control
    ID31 -. authentication .-> A31_1
    SAFE31 -. enforcement .-> A31_1
    OBS31 -. telemetry .-> A31_1
```

### Core components
Event brief intake, checklist generator, budget tracker, venue and vendor search, guest list and RSVP service, timeline scheduler, message drafting, and collaborator permissions.

### Agent/workflow design
The agent produces a backward-planned timeline from the date, decomposes it into tasks with owners, and shortlists vendors against budget and capacity. It drafts invitations and quote requests but sends only after approval.

### Data and integrations
Integrates venue and vendor directories, email and SMS, calendars, payment and ticketing tools, and maps. Stores events, guest lists, budgets, quotes, and contracts as structured and file records.

### Security and safety
Protect guest personal data and honor opt-outs. Require confirmation before messaging or spending, review vendor contracts with human oversight, and flag capacity, permit, accessibility, and alcohol-related requirements.

### Reliability, observability and evaluation
Send reminders with retries and track delivery. Monitor task completion, budget variance, and RSVP response rates. Evaluate plan completeness against expert checklists and budget-estimate accuracy across event types.

### MVP build path
Start with a brief-to-checklist and budget planner for one event type. Add guest list and RSVP handling, then venue and vendor search with quote drafts, then timeline automation and collaborator roles.

## 32. Ticket-discovery assistant

### Purpose and user journey
Helps users find tickets to concerts, sports, and shows at fair prices. The user names artists or interests, sees upcoming events and seat or price options, sets alerts, and buys through trusted sellers.

### Reference architecture
`Chat UI -> Event search -> Ticket marketplace APIs -> Price/seat ranker -> Alert service -> Verified seller handoff`

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
    A32_0["Chat UI"]
    class A32_0 frontend
    A32_1["Event search"]
    class A32_1 tool
    A32_2["Ticket marketplace APIs"]
    class A32_2 external
    A32_3["Price/seat ranker"]
    class A32_3 agent
    A32_4["Alert service"]
    class A32_4 tool
    A32_5["Verified seller handoff"]
    class A32_5 backend
    A32_0 --> A32_1
    A32_1 --> A32_2
    A32_2 --> A32_3
    A32_3 --> A32_4
    A32_4 --> A32_5
    ID32["Entra ID + managed identity"]
    SAFE32["Policy, validation + approval gates"]
    OBS32["Tracing, metrics + evaluation"]
    class ID32,SAFE32,OBS32 control
    ID32 -. authentication .-> A32_1
    SAFE32 -. enforcement .-> A32_1
    OBS32 -. telemetry .-> A32_1
```

### Core components
Event and artist resolver, multi-source listing aggregator, all-in price normalizer, seat-view and value ranker, alert and on-sale watcher, calendar conflict checker, and seller handoff.

### Agent/workflow design
The agent resolves entities, finds events near the user, and compares listings by all-in price, seat quality, and seller reliability. It sets on-sale and price-drop alerts and warns about resale markups and unverified listings.

### Data and integrations
Integrates primary ticketing and resale marketplace APIs, artist and venue databases, music or streaming profiles for taste, calendars, and maps. Stores watchlists, alerts, and price histories.

### Security and safety
Prefer verified sellers and flag likely scams, counterfeit listings, and off-platform payment requests. Show fees upfront, disclose affiliate links, and never complete purchases without user approval on the seller's checkout.

### Reliability, observability and evaluation
Handle rapid inventory changes with short caches and re-checks. Track alert timeliness, price accuracy, and handoff conversion. Evaluate event matching, all-in price parity, and scam-detection precision.

### MVP build path
Build event search and price comparison from one or two sources. Add all-in pricing and alerts, then seat-quality ranking and calendar checks, then on-sale watching and personalized discovery from taste profiles.
