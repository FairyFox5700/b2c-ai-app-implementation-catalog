# Commerce and retail architecture overviews

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
    TOOLS --> DOMAIN["Commerce and retail tools and partner APIs"]
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


## 1. Personal shopping assistant

**Purpose and user journey**
A conversational assistant that turns a vague need ("running shoes under 120 EUR for flat feet") into a ranked shortlist. The user states a need, answers one or two clarifying questions, reviews product cards with reasons, then saves items or sends them to the cart.

**Reference architecture**
Chat UI -> API gateway -> orchestrator agent -> [catalog search | profile memory | price/stock tools] -> ranker -> product cards -> cart handoff

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
    A1_0["Chat UI"]
    class A1_0 frontend
    A1_1["API gateway"]
    class A1_1 external
    A1_2["orchestrator agent"]
    class A1_2 agent
    A1_3["catalog search"]
    class A1_3 tool
    A1_4["profile memory"]
    class A1_4 data
    A1_5["price/stock tools"]
    class A1_5 tool
    A1_6["ranker"]
    class A1_6 agent
    A1_7["product cards"]
    class A1_7 tool
    A1_8["cart handoff"]
    class A1_8 backend
    A1_0 --> A1_1
    A1_1 --> A1_2
    A1_2 --> A1_3
    A1_2 --> A1_4
    A1_2 --> A1_5
    A1_3 --> A1_6
    A1_4 --> A1_6
    A1_5 --> A1_6
    A1_6 --> A1_7
    A1_7 --> A1_8
    ID1["Entra ID + managed identity"]
    SAFE1["Policy, validation + approval gates"]
    OBS1["Tracing, metrics + evaluation"]
    class ID1,SAFE1,OBS1 control
    ID1 -. authentication .-> A1_1
    SAFE1 -. enforcement .-> A1_1
    OBS1 -. telemetry .-> A1_1
```

**Core components**
- Web/mobile chat front end.
- Orchestrator on Azure Container Apps or Functions, calling Azure OpenAI.
- Hybrid keyword and vector index (Azure AI Search).
- Profile store (Cosmos DB).
- Ranking service.
- Guardrail layer (Azure AI Content Safety).
- Telemetry (Application Insights).

**Agent/workflow design**
One tool-using agent runs a plan-act loop. It classifies intent, extracts constraints into a structured filter schema, calls search, reranks, and explains each pick. It makes at most four tool calls per turn and asks a clarifying question only when a missing constraint would change the results. Session summary is kept by default; long-term preferences are opt-in.

**Data and integrations**
Product feed (SKU, attributes, price, stock), reviews, user profile and order history. Integrations: commerce platform APIs (Shopify, Commerce Cloud, Magento), inventory service, merchant feeds, analytics events.

**Security and safety**
Expose read tools plus add-to-cart, and require user confirmation for the cart action. Minimize PII and get consent before storing preferences. Filter prompt injection in review and product text. Take price and stock only from tool results, never from model memory. Use managed identity and Key Vault.

**Reliability, observability and evaluation**
Cache frequent catalog queries and fall back to keyword search if the LLM is down. Trace every tool call. Track shortlist click-through, add-to-cart rate, constraint satisfaction and hallucinated-attribute rate. Evaluate offline on about 200 labeled queries and red-team before launch.

**MVP build path**
Weeks 1-2: ingest the feed and build the hybrid index. Weeks 3-4: single-agent chat with the search tool. Week 5: profile memory and cart handoff. Week 6: eval harness and a pilot in one category.

## 2. Fashion and styling assistant

**Purpose and user journey**
Suggests complete outfits for an occasion, body preference and budget. The user describes an event or uploads a reference photo, gets three outfit options with swap-able items, and buys the full look or single pieces.

**Reference architecture**
Chat/photo UI -> style agent -> [attribute extractor | outfit composer | catalog + inventory search] -> compatibility scorer -> outfit cards -> cart

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
    A2_0["Chat/photo UI"]
    class A2_0 frontend
    A2_1["style agent"]
    class A2_1 agent
    A2_2["attribute extractor"]
    class A2_2 tool
    A2_3["outfit composer"]
    class A2_3 tool
    A2_4["catalog + inventory search"]
    class A2_4 tool
    A2_5["compatibility scorer"]
    class A2_5 tool
    A2_6["outfit cards"]
    class A2_6 tool
    A2_7["cart"]
    class A2_7 backend
    A2_0 --> A2_1
    A2_1 --> A2_2
    A2_1 --> A2_3
    A2_1 --> A2_4
    A2_2 --> A2_5
    A2_3 --> A2_5
    A2_4 --> A2_5
    A2_5 --> A2_6
    A2_6 --> A2_7
    ID2["Entra ID + managed identity"]
    SAFE2["Policy, validation + approval gates"]
    OBS2["Tracing, metrics + evaluation"]
    class ID2,SAFE2,OBS2 control
    ID2 -. authentication .-> A2_1
    SAFE2 -. enforcement .-> A2_1
    OBS2 -. telemetry .-> A2_1
```

**Core components**
- Multimodal LLM (Azure OpenAI vision) for photo and attribute reading.
- Fashion taxonomy service (category, color, fit, season, formality).
- Embedding index (Azure AI Search) over product images and text.
- Outfit composer with compatibility rules.
- Size and fit service.
- Profile store.

**Agent/workflow design**
Two-stage flow. A planner turns the occasion, weather, dress code and style profile into outfit slots (top, bottom, shoes, layer). A retriever fills each slot, then a scorer checks color harmony, formality match, budget total and stock of every size. If any slot fails, the agent substitutes and explains the change.

**Data and integrations**
Product images and attributes, size charts, return-by-size statistics, trend and season metadata, user style profile. Integrations: retailer catalog, weather API, calendar (optional, consent-based), visual-embedding service.

**Security and safety**
Strip EXIF and face data from uploads, store images with short retention, and avoid inferring sensitive traits such as body shape unless the user states them. Use inclusive sizing language. Moderate uploads and keep fit claims tied to size-chart data.

**Reliability, observability and evaluation**
Outfit coverage (percent of slots filled in stock), acceptance rate, outfit-level conversion, and return rate by suggested size. Use human stylist review of a sampled set. A/B test rules-only against LLM-composed outfits.

**MVP build path**
Start with one gender-neutral category set and a rules-based composer. Add photo input in week 4, size recommendation in week 6, and stylist feedback loops after pilot.

## 3. Personal wardrobe assistant

**Purpose and user journey**
Helps users catalog clothes they already own, plan outfits from them, and spot gaps worth buying. The user photographs items, confirms detected attributes, gets daily outfit suggestions, and sees targeted purchase suggestions.

**Reference architecture**
Photo capture -> image pipeline (segment, tag, embed) -> wardrobe store -> outfit agent -> daily plan / gap analysis -> optional shop links

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
    A3_0["Photo capture"]
    class A3_0 frontend
    A3_1["image pipeline (segment, tag, embed)"]
    class A3_1 tool
    A3_2["wardrobe store"]
    class A3_2 data
    A3_3["outfit agent"]
    class A3_3 agent
    A3_4["daily plan / gap analysis"]
    class A3_4 tool
    A3_5["optional shop links"]
    class A3_5 backend
    A3_0 --> A3_1
    A3_1 --> A3_2
    A3_2 --> A3_3
    A3_3 --> A3_4
    A3_4 --> A3_5
    ID3["Entra ID + managed identity"]
    SAFE3["Policy, validation + approval gates"]
    OBS3["Tracing, metrics + evaluation"]
    class ID3,SAFE3,OBS3 control
    ID3 -. authentication .-> A3_1
    SAFE3 -. enforcement .-> A3_1
    OBS3 -. telemetry .-> A3_1
```

**Core components**
- Mobile app with camera and offline queue.
- Image pipeline: background removal, classification, color extraction (Azure AI Vision plus a custom model).
- Wardrobe database (Cosmos DB, per-user partition).
- Blob Storage for images.
- Outfit agent.
- Notification service.

**Agent/workflow design**
Ingestion is a deterministic pipeline with human confirmation, not free agent behavior. The outfit agent receives weather, calendar events and wear history, then proposes outfits from owned items. A gap-analysis job compares wardrobe coverage against the user's lifestyle profile and calls the product-search tool only when the user opts in.

**Data and integrations**
Item records (type, color, material, brand, wear count, last worn, cost), user preferences, outfit history. Integrations: weather API, calendar, optional retailer catalogs and resale marketplaces.

**Security and safety**
Private by default. Encrypt images, use per-user storage isolation, and provide full export and deletion. Keep wardrobe data out of ad targeting. Avoid storing background content such as faces or home interiors, and crop to the item where possible.

**Reliability, observability and evaluation**
Measure tag accuracy after user correction, outfits accepted, items worn per month, and upload completion rate. Keep a golden image set for classifier regression. Log pipeline failures and retry through queues.

**MVP build path**
Build upload-and-tag with manual correction first. Then add weather-based daily outfit suggestions, wear tracking, and finally gap analysis with shop links.

## 4. Product discovery assistant

**Purpose and user journey**
Helps shoppers who do not know what to search for. They browse by need, mood or use case, refine through facets and conversation, and discover products they would not have found by keyword.

**Reference architecture**
Query/browse UI -> intent and facet agent -> hybrid retrieval (keyword + vector + graph) -> diversified reranker -> explained results -> refinement loop

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
    A4_0["Query/browse UI"]
    class A4_0 frontend
    A4_1["intent and facet agent"]
    class A4_1 agent
    A4_2["hybrid retrieval (keyword + vector + graph)"]
    class A4_2 data
    A4_3["diversified reranker"]
    class A4_3 agent
    A4_4["explained results"]
    class A4_4 tool
    A4_5["refinement loop"]
    class A4_5 backend
    A4_0 --> A4_1
    A4_1 --> A4_2
    A4_2 --> A4_3
    A4_3 --> A4_4
    A4_4 --> A4_5
    ID4["Entra ID + managed identity"]
    SAFE4["Policy, validation + approval gates"]
    OBS4["Tracing, metrics + evaluation"]
    class ID4,SAFE4,OBS4 control
    ID4 -. authentication .-> A4_1
    SAFE4 -. enforcement .-> A4_1
    OBS4 -. telemetry .-> A4_1
```

**Core components**
- Query understanding service (LLM with schema output).
- Azure AI Search hybrid index with semantic ranking.
- Product knowledge graph (categories, use cases, accessories).
- Reranker blending relevance, popularity, margin limits and diversity.
- Facet generator.
- Event pipeline (Event Hubs).

**Agent/workflow design**
The agent rewrites free text into filters and several sub-queries, runs them in parallel, merges results, and generates dynamic facets from the result set. It proposes next refinements such as "quieter", "cheaper" or "for small spaces". Conversation state holds the current constraints so each refinement edits them rather than restarting.

**Data and integrations**
Catalog enrichment with LLM-generated use-case tags validated against source attributes, clickstream, reviews, search logs. Integrations: commerce platform, CDP/analytics, merchandising rules tool.

**Security and safety**
Apply merchandising and legal filters (age-restricted, region-restricted products) after retrieval, not by prompt. Label sponsored placements. Do not use sensitive attributes for personalization. Sanitize generated tags.

**Reliability, observability and evaluation**
Track zero-result rate, query reformulation rate, click depth, discovery-to-purchase conversion and result diversity. Evaluate with NDCG on judged queries plus LLM-assisted relevance labeling checked by humans. Keep a plain keyword fallback.

**MVP build path**
Step 1: hybrid index and query rewriting. Step 2: dynamic facets. Step 3: knowledge-graph expansion. Step 4: personalization and diversity reranking after enough click data.

## 5. Product comparison assistant

**Purpose and user journey**
Compares two to five products on the criteria the user cares about. The user picks items or describes a decision, receives a normalized comparison table with a plain-language verdict, and can adjust priorities.

**Reference architecture**
Selected SKUs -> spec normalizer -> criteria weighting -> evidence retriever (specs, reviews) -> comparison generator -> table + verdict + citations

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
    A5_0["Selected SKUs"]
    class A5_0 frontend
    A5_1["spec normalizer"]
    class A5_1 tool
    A5_2["criteria weighting"]
    class A5_2 tool
    A5_3["evidence retriever (specs, reviews)"]
    class A5_3 tool
    A5_4["comparison generator"]
    class A5_4 tool
    A5_5["table + verdict + citations"]
    class A5_5 backend
    A5_0 --> A5_1
    A5_1 --> A5_2
    A5_2 --> A5_3
    A5_3 --> A5_4
    A5_4 --> A5_5
    ID5["Entra ID + managed identity"]
    SAFE5["Policy, validation + approval gates"]
    OBS5["Tracing, metrics + evaluation"]
    class ID5,SAFE5,OBS5 control
    ID5 -. authentication .-> A5_1
    SAFE5 -. enforcement .-> A5_1
    OBS5 -. telemetry .-> A5_1
```

**Core components**
- Spec normalization service mapping units and attribute names across brands.
- Review mining pipeline (aspect-based sentiment).
- Azure AI Search for evidence passages.
- Comparison agent (Azure OpenAI with structured output).
- Weighting UI.
- Citation store.

**Agent/workflow design**
The agent first clarifies the decision criteria and converts them into weights. Specs are compared by deterministic code; the LLM only writes the explanation and trade-offs from retrieved evidence. Each claim must carry a source reference to a spec field or review excerpt, and unsupported claims are dropped by a verifier step.

**Data and integrations**
Manufacturer specs, retailer attributes, reviews, price history, warranty and return terms. Integrations: catalog API, review provider, price-history service, optional expert-review feeds.

**Security and safety**
Guard against fake or injected reviews by using verified-purchase filters and anomaly detection. Disclose sponsored or affiliate relationships. Do not state safety or medical claims beyond source data. Keep verdicts neutral and show uncertainty when data is missing.

**Reliability, observability and evaluation**
Measure citation coverage, factual-accuracy rate on spec comparisons, user-adjusted weight rate, and decision conversion. Run regression tests on a fixed product-pair set. Alert on normalization failures.

**MVP build path**
Pick one spec-heavy category such as laptops. Build normalization and the table first, then add review aspects, then the weighted verdict and citations.

## 6. Gift recommendation assistant

**Purpose and user journey**
Finds suitable gifts for a recipient, occasion and budget. The buyer answers a short guided interview, gets diverse ideas with rationale, and can order with gift wrap, a message and a delivery date.

**Reference architecture**
Gift brief form/chat -> recipient profile builder -> idea generator -> catalog matcher + delivery-date filter -> curated shortlist -> gift checkout options

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
    A6_0["Gift brief form/chat"]
    class A6_0 frontend
    A6_1["recipient profile builder"]
    class A6_1 frontend
    A6_2["idea generator"]
    class A6_2 tool
    A6_3["catalog matcher + delivery-date filter"]
    class A6_3 tool
    A6_4["curated shortlist"]
    class A6_4 tool
    A6_5["gift checkout options"]
    class A6_5 backend
    A6_0 --> A6_1
    A6_1 --> A6_2
    A6_2 --> A6_3
    A6_3 --> A6_4
    A6_4 --> A6_5
    ID6["Entra ID + managed identity"]
    SAFE6["Policy, validation + approval gates"]
    OBS6["Tracing, metrics + evaluation"]
    class ID6,SAFE6,OBS6 control
    ID6 -. authentication .-> A6_1
    SAFE6 -. enforcement .-> A6_1
    OBS6 -. telemetry .-> A6_1
```

**Core components**
- Guided intake UI.
- Recipient profile service (relationship, interests, age band, past gifts).
- LLM idea generator.
- Azure AI Search catalog matcher.
- Delivery-promise service.
- Gift options module (wrap, note, hide price).

**Agent/workflow design**
The agent produces idea categories first (experience, consumable, personalized, practical), then queries the catalog per category, enforces budget and arrival date, and balances the final list for diversity. It asks about the relationship and tone rather than inferring them. Rejected ideas feed back as negative constraints.

**Data and integrations**
Catalog, bestseller and gifting-tagged data, occasion calendar, buyer's order history for avoiding duplicates, delivery estimates. Integrations: retailer APIs, carrier cut-off times, optional wishlist links, e-gift-card provider.

**Security and safety**
Treat recipient information as third-party personal data: collect minimal details, do not persist without consent, and never infer sensitive traits such as health or orientation. Block inappropriate gift categories for minors. Hide prices on gift receipts and verify addresses.

**Reliability, observability and evaluation**
Track shortlist acceptance, on-time-arrival rate, gift return rate and idea diversity. Use human panel evaluation for appropriateness. Keep seasonal load tests for peak periods and a deterministic fallback of curated gift guides.

**MVP build path**
Launch with five occasions and a curated catalog subset. Add delivery-date filtering, then gift wrap and notes, then wishlist integration.

## 7. Visual product-search app

**Purpose and user journey**
Lets users search with a photo, screenshot or sketch to find the same or similar products. The user takes a photo, crops the region of interest, receives exact and similar matches, and refines with text such as "in blue".

**Reference architecture**
Image upload -> preprocessing/detection -> embedding model -> vector index -> exact-match verifier + similar-item ranker -> results -> text refinement

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
    A7_0["Image upload"]
    class A7_0 frontend
    A7_1["preprocessing/detection"]
    class A7_1 tool
    A7_2["embedding model"]
    class A7_2 tool
    A7_3["vector index"]
    class A7_3 data
    A7_4["exact-match verifier + similar-item ranker"]
    class A7_4 agent
    A7_5["results"]
    class A7_5 tool
    A7_6["text refinement"]
    class A7_6 backend
    A7_0 --> A7_1
    A7_1 --> A7_2
    A7_2 --> A7_3
    A7_3 --> A7_4
    A7_4 --> A7_5
    A7_5 --> A7_6
    ID7["Entra ID + managed identity"]
    SAFE7["Policy, validation + approval gates"]
    OBS7["Tracing, metrics + evaluation"]
    class ID7,SAFE7,OBS7 control
    ID7 -. authentication .-> A7_1
    SAFE7 -. enforcement .-> A7_1
    OBS7 -. telemetry .-> A7_1
```

**Core components**
- Mobile and web capture SDK.
- Object detection and cropping service.
- Image embedding model (CLIP-style or Azure AI Vision multimodal embeddings).
- Vector index (Azure AI Search or pgvector).
- Attribute re-ranker.
- Catalog image ingestion pipeline.

**Agent/workflow design**
Mostly a deterministic retrieval pipeline. An LLM is used only to interpret refinement text into filters and to describe differences between match and query. Exact-match verification uses local-feature or high-threshold similarity, and low-confidence results are labeled as similar rather than identical.

**Data and integrations**
Catalog images from several angles, attributes, brand and logo data, user query images with short retention, click feedback. Integrations: PIM or DAM, commerce APIs, camera SDKs, optional AR try-on.

**Security and safety**
Scan uploads for malware and inappropriate content, strip EXIF location data, and blur faces and license plates by default. Set retention to hours unless the user saves a search. Avoid person-identification and rate-limit uploads to deter scraping.

**Reliability, observability and evaluation**
Measure recall at k on labeled query-to-product pairs, latency (target under one second), exact-match precision, and search-to-cart rate. Re-embed the catalog when the model changes using versioned indexes with blue-green swap.

**MVP build path**
Build a catalog embedding job, then single-object search with a pre-trained model, then crop and detect, then text refinement, then fine-tuning on your own click data.

## 8. Shopping-cart assistant

**Purpose and user journey**
Helps users complete and optimize a cart. While shopping, it flags compatibility problems, suggests missing accessories, finds cheaper alternatives or bundles, and reminds users about abandoned items.

**Reference architecture**
Cart events -> cart-state service -> assistant agent -> [compatibility rules | pricing/promo engine | inventory | recommendations] -> inline suggestions -> user-approved cart change

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
    A8_0["Cart events"]
    class A8_0 frontend
    A8_1["cart-state service"]
    class A8_1 tool
    A8_2["assistant agent"]
    class A8_2 agent
    A8_3["compatibility rules"]
    class A8_3 tool
    A8_4["pricing/promo engine"]
    class A8_4 agent
    A8_5["inventory"]
    class A8_5 tool
    A8_6["recommendations"]
    class A8_6 tool
    A8_7["inline suggestions"]
    class A8_7 tool
    A8_8["user-approved cart change"]
    class A8_8 frontend
    A8_0 --> A8_1
    A8_1 --> A8_2
    A8_2 --> A8_3
    A8_2 --> A8_4
    A8_2 --> A8_5
    A8_2 --> A8_6
    A8_3 --> A8_7
    A8_4 --> A8_7
    A8_5 --> A8_7
    A8_6 --> A8_7
    A8_7 --> A8_8
    ID8["Entra ID + managed identity"]
    SAFE8["Policy, validation + approval gates"]
    OBS8["Tracing, metrics + evaluation"]
    class ID8,SAFE8,OBS8 control
    ID8 -. authentication .-> A8_1
    SAFE8 -. enforcement .-> A8_1
    OBS8 -. telemetry .-> A8_1
```

**Core components**
- Cart service exposing events and mutation API.
- Compatibility and rules engine.
- Promotion and pricing API.
- Recommendation service.
- Agent runtime (Azure OpenAI with function calling).
- Notification service for recovery messages.

**Agent/workflow design**
Event-triggered rather than purely chat-based. On cart change the agent runs a limited check list: stock, compatibility, free-shipping threshold, bundle savings and duplicate items. Suggestions are ranked by user benefit, not only margin. Any cart mutation is a proposal that needs an explicit click.

**Data and integrations**
Cart contents, product relationships (accessory, substitute, bundle), prices, promotions, stock, session behavior. Integrations: commerce platform cart API, promo engine, inventory service, email or push provider.

**Security and safety**
Authorize every cart operation against the session user and make mutations idempotent. Never silently add items. Recompute prices server-side. Respect marketing consent for recovery messages, and cap their frequency. Disclose sponsored suggestions.

**Reliability, observability and evaluation**
Track suggestion acceptance, average order value change, cart abandonment, incorrect-compatibility rate and complaint rate. Add circuit breakers so the cart never blocks if the assistant fails. Test via A/B with a holdout group.

**MVP build path**
Start with rule-based checks (stock, shipping threshold, duplicates), then compatibility for one category, then LLM-written explanations, then recovery messaging.

## 9. Checkout assistant

**Purpose and user journey**
Reduces friction and errors during checkout. It helps with address correction, shipping choice, payment-method questions, tax and fee explanations, and failed-payment recovery, while keeping payment handling out of the model.

**Reference architecture**
Checkout UI -> checkout orchestrator -> [address validation | shipping options | tax/fees | payment provider hosted fields] -> assistant explanations -> order confirmation

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
    A9_0["Checkout UI"]
    class A9_0 frontend
    A9_1["checkout orchestrator"]
    class A9_1 agent
    A9_2["address validation"]
    class A9_2 tool
    A9_3["shipping options"]
    class A9_3 tool
    A9_4["tax/fees"]
    class A9_4 tool
    A9_5["payment provider hosted fields"]
    class A9_5 external
    A9_6["assistant explanations"]
    class A9_6 tool
    A9_7["order confirmation"]
    class A9_7 backend
    A9_0 --> A9_1
    A9_1 --> A9_2
    A9_1 --> A9_3
    A9_1 --> A9_4
    A9_1 --> A9_5
    A9_2 --> A9_6
    A9_3 --> A9_6
    A9_4 --> A9_6
    A9_5 --> A9_6
    A9_6 --> A9_7
    ID9["Entra ID + managed identity"]
    SAFE9["Policy, validation + approval gates"]
    OBS9["Tracing, metrics + evaluation"]
    class ID9,SAFE9,OBS9 control
    ID9 -. authentication .-> A9_1
    SAFE9 -. enforcement .-> A9_1
    OBS9 -. telemetry .-> A9_1
```

**Core components**
- Checkout service (system of record).
- Assistant panel with function calling.
- Address validation service.
- Shipping-rate and delivery-promise API.
- Payment service provider with hosted fields (Stripe, Adyen, or Azure-hosted gateway integration).
- Fraud screening.

**Agent/workflow design**
The assistant is advisory and checkout logic is deterministic. It answers questions using read-only tools (delivery estimates, fee breakdown, return terms), proposes address fixes, and recommends the best shipping option for the user's stated priority. On payment failure it maps the provider error code to a plain explanation and next steps.

**Data and integrations**
Cart, address book, shipping methods, tax engine, payment status codes, consent flags. Integrations: tax service, carriers, PSP webhooks, fraud tools, loyalty balance lookup.

**Security and safety**
Remain outside PCI scope: card data goes only into PSP-hosted fields and never reaches the LLM or logs. Mask addresses in telemetry, require step-up authentication for saved-payment use, and prevent the agent from changing totals. Defend against prompt injection from address fields.

**Reliability, observability and evaluation**
Track checkout completion, payment success, address-correction acceptance, assistant-handled-question rate and error rate. Use synthetic checkout monitoring, idempotency keys, and a fully working checkout when the assistant is disabled.

**MVP build path**
Ship address validation and a delivery/fee FAQ panel first. Add shipping recommendation, then payment-failure guidance, then personalized reassurance for abandoned checkouts.

## 10. Order-tracking assistant

**Purpose and user journey**
Answers "where is my order?" across channels. The user asks via chat, SMS or email, is verified, and receives a plain status with an estimated delivery window, proactive updates, and options such as rerouting or notifications.

**Reference architecture**
Channel (web/SMS/WhatsApp) -> identity check -> tracking agent -> [order API | carrier tracking aggregator | event store] -> status explanation -> proactive notifier

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
    A10_0["Channel (web/SMS/WhatsApp)"]
    class A10_0 frontend
    A10_1["identity check"]
    class A10_1 tool
    A10_2["tracking agent"]
    class A10_2 agent
    A10_3["order API"]
    class A10_3 external
    A10_4["carrier tracking aggregator"]
    class A10_4 tool
    A10_5["event store"]
    class A10_5 data
    A10_6["status explanation"]
    class A10_6 tool
    A10_7["proactive notifier"]
    class A10_7 backend
    A10_0 --> A10_1
    A10_1 --> A10_2
    A10_2 --> A10_3
    A10_2 --> A10_4
    A10_2 --> A10_5
    A10_3 --> A10_6
    A10_4 --> A10_6
    A10_5 --> A10_6
    A10_6 --> A10_7
    ID10["Entra ID + managed identity"]
    SAFE10["Policy, validation + approval gates"]
    OBS10["Tracing, metrics + evaluation"]
    class ID10,SAFE10,OBS10 control
    ID10 -. authentication .-> A10_1
    SAFE10 -. enforcement .-> A10_1
    OBS10 -. telemetry .-> A10_1
```

**Core components**
- Omnichannel gateway (Azure Communication Services).
- Identity verification (order number plus email or login).
- Order management system client.
- Carrier tracking aggregator.
- Event store of normalized tracking events (Cosmos DB or Postgres).
- Notification service.

**Agent/workflow design**
A small agent with two read tools. It maps raw carrier scan codes to a normalized status model (placed, packed, in transit, out for delivery, delayed, delivered, exception), gets the ETA, and rewrites it for the user. If the status is exception or ETA is missed, it hands off to the delivery-exception flow. Proactive messages are triggered by event rules, not the LLM.

**Data and integrations**
Orders, shipments, carrier events, ETAs, notification preferences. Integrations: OMS/ERP, carrier APIs or aggregators (AfterShip, Shippo), SMS/email providers, webhook receivers.

**Security and safety**
Verify the requester before showing address or items. Return limited information to unauthenticated users, rate-limit lookups to prevent order enumeration, and mask address data. Honor opt-in rules for SMS. Sign and validate carrier webhooks.

**Reliability, observability and evaluation**
Track deflection rate, status accuracy against carrier truth, event lag, WISMO contact reduction and proactive-message opt-out rate. Handle carrier API outages with cached last-known status and clear staleness labels.

**MVP build path**
Build order lookup and a single carrier integration first. Add status normalization, then webhook-driven proactive notices, then multi-channel support.

## 11. Delivery-exception assistant

**Purpose and user journey**
Detects and resolves delivery problems such as delays, failed attempts, damage, lost parcels and address issues. The customer is notified before they ask, picks a resolution (reschedule, pickup point, reship, refund), and the case is closed or escalated.

**Reference architecture**
Carrier events -> exception detector -> case manager -> resolution agent -> [carrier actions | reship/refund engine | customer messaging] -> outcome tracking

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
    A11_0["Carrier events"]
    class A11_0 frontend
    A11_1["exception detector"]
    class A11_1 tool
    A11_2["case manager"]
    class A11_2 tool
    A11_3["resolution agent"]
    class A11_3 agent
    A11_4["carrier actions"]
    class A11_4 tool
    A11_5["reship/refund engine"]
    class A11_5 agent
    A11_6["customer messaging"]
    class A11_6 tool
    A11_7["outcome tracking"]
    class A11_7 backend
    A11_0 --> A11_1
    A11_1 --> A11_2
    A11_2 --> A11_3
    A11_3 --> A11_4
    A11_3 --> A11_5
    A11_3 --> A11_6
    A11_4 --> A11_7
    A11_5 --> A11_7
    A11_6 --> A11_7
    ID11["Entra ID + managed identity"]
    SAFE11["Policy, validation + approval gates"]
    OBS11["Tracing, metrics + evaluation"]
    class ID11,SAFE11,OBS11 control
    ID11 -. authentication .-> A11_1
    SAFE11 -. enforcement .-> A11_1
    OBS11 -. telemetry .-> A11_1
```

**Core components**
- Event stream processor (Event Hubs and Functions).
- Exception rules and ML delay predictor.
- Case management system (Dynamics 365 or equivalent).
- Resolution policy engine.
- Carrier API connectors.
- Customer messaging service.

**Agent/workflow design**
Exceptions are classified and given a severity score. A policy engine determines allowed remedies by order value, customer tier, carrier and elapsed time. The agent presents permitted options and executes the chosen one through tools such as redirect, reship or refund. Cases above thresholds or involving damage disputes go to human agents with a full summary.

**Data and integrations**
Tracking events, order value, customer history, carrier performance, photos of damage, case notes. Integrations: carrier APIs, OMS, WMS for reship stock, payments for refunds, support desk.

**Security and safety**
Enforce refund and reship limits in the policy engine, not prompts. Log approvals for audit. Validate damage photos and use fraud signals for repeated claims. Verify identity before address changes to avoid redirection scams.

**Reliability, observability and evaluation**
Track time to detection, proactive contact rate, first-contact resolution, cost per exception, and claim-fraud rate. Evaluate the delay predictor with precision and recall. Use idempotent actions and dead-letter queues for failed carrier calls.

**MVP build path**
Start with rule-based detection of stalled and failed-attempt shipments plus proactive messages. Add self-service reschedule, then policy-driven reship/refund, then predictive delay detection.

## 12. Returns and refunds assistant

**Purpose and user journey**
Guides customers through eligibility, reason capture, return method, label creation and refund or exchange, then keeps them informed until the money is returned. It also helps merchants cut avoidable returns.

**Reference architecture**
Return request -> eligibility engine -> returns agent -> [label/carrier | exchange suggester | refund service] -> warehouse receipt -> refund status updates

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
    A12_0["Return request"]
    class A12_0 frontend
    A12_1["eligibility engine"]
    class A12_1 agent
    A12_2["returns agent"]
    class A12_2 agent
    A12_3["label/carrier"]
    class A12_3 tool
    A12_4["exchange suggester"]
    class A12_4 tool
    A12_5["refund service"]
    class A12_5 tool
    A12_6["warehouse receipt"]
    class A12_6 tool
    A12_7["refund status updates"]
    class A12_7 backend
    A12_0 --> A12_1
    A12_1 --> A12_2
    A12_2 --> A12_3
    A12_2 --> A12_4
    A12_2 --> A12_5
    A12_3 --> A12_6
    A12_4 --> A12_6
    A12_5 --> A12_6
    A12_6 --> A12_7
    ID12["Entra ID + managed identity"]
    SAFE12["Policy, validation + approval gates"]
    OBS12["Tracing, metrics + evaluation"]
    class ID12,SAFE12,OBS12 control
    ID12 -. authentication .-> A12_1
    SAFE12 -. enforcement .-> A12_1
    OBS12 -. telemetry .-> A12_1
```

**Core components**
- Return policy engine with versioned rules.
- Returns management system (RMA).
- Label and drop-off location API.
- Exchange and size recommender.
- Payments refund API.
- Warehouse receiving integration.

**Agent/workflow design**
The agent identifies the order and items, checks eligibility through the policy engine, asks for the reason, and tries relevant alternatives such as exchange for another size or a partial refund. Final decisions come from policy rules. Ambiguous or high-value cases route to a human. Refund triggers wait for warehouse scan or a trusted-customer rule.

**Data and integrations**
Orders, return policies, item condition, reasons, customer return history, carrier labels, refund transactions. Integrations: OMS, WMS, PSP refund API, carriers, loyalty system for point reversal.

**Security and safety**
Authenticate before showing orders. Detect return fraud with velocity and pattern checks, but give humans the final adverse decision. Make refunds idempotent and reconcile them against payments. Comply with consumer-rights rules such as the EU 14-day withdrawal period.

**Reliability, observability and evaluation**
Track return-initiation completion, exchange-over-refund rate, time to refund, policy-decision accuracy, fraud loss and reason-code trends. Test the policy engine with scenario suites. Reconcile daily refund totals.

**MVP build path**
Build the policy engine and label generation first. Add reason capture, then exchange suggestions, then refund status updates, then fraud scoring.

## 13. E-commerce customer-support agent

**Purpose and user journey**
A general support agent that resolves common customer requests across orders, products, policies and accounts, and hands complex cases to humans. The customer asks in chat or email, gets an answer or action, and can escalate with context preserved.

**Reference architecture**
Channel -> router/intent classifier -> support agent -> [knowledge RAG | order tools | account tools | specialist sub-agents] -> response or human handoff -> QA loop

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
    A13_0["Channel"]
    class A13_0 frontend
    A13_1["router/intent classifier"]
    class A13_1 agent
    A13_2["support agent"]
    class A13_2 agent
    A13_3["knowledge RAG"]
    class A13_3 tool
    A13_4["order tools"]
    class A13_4 tool
    A13_5["account tools"]
    class A13_5 tool
    A13_6["specialist sub-agents"]
    class A13_6 agent
    A13_7["response or human handoff"]
    class A13_7 tool
    A13_8["QA loop"]
    class A13_8 backend
    A13_0 --> A13_1
    A13_1 --> A13_2
    A13_2 --> A13_3
    A13_2 --> A13_4
    A13_2 --> A13_5
    A13_2 --> A13_6
    A13_3 --> A13_7
    A13_4 --> A13_7
    A13_5 --> A13_7
    A13_6 --> A13_7
    A13_7 --> A13_8
    ID13["Entra ID + managed identity"]
    SAFE13["Policy, validation + approval gates"]
    OBS13["Tracing, metrics + evaluation"]
    class ID13,SAFE13,OBS13 control
    ID13 -. authentication .-> A13_1
    SAFE13 -. enforcement .-> A13_1
    OBS13 -. telemetry .-> A13_1
```

**Core components**
- Omnichannel inbox (Dynamics 365 Contact Center, Zendesk or similar).
- Intent router.
- RAG over help center and policies (Azure AI Search).
- Tool layer for order, account and refund actions.
- Handoff service with conversation summary.
- QA and feedback pipeline.

**Agent/workflow design**
A router sends tracking, returns, subscription and loyalty intents to the specialist flows and handles general questions itself. The agent answers policy questions only from retrieved documents with citations. Write actions use scoped tools with limits and confirmations. A confidence threshold or sentiment trigger escalates to a human with a structured summary.

**Data and integrations**
Knowledge base, policies, ticket history, orders, customer profile, macros. Integrations: OMS, CRM, payments, carrier tracking, identity provider, analytics.

**Security and safety**
Verify identity before any account data is shown. Redact PII and card numbers from transcripts and prompts. Use least-privilege service credentials per tool, rate limits, and an audit trail of all actions. Sanitize inbound email content against prompt injection. Disclose that the user is talking to AI.

**Reliability, observability and evaluation**
Track containment rate, CSAT, escalation quality, wrong-answer rate, average handling time and policy-citation coverage. Build a regression set from past tickets, review sampled conversations weekly, and keep human takeover available at all times.

**MVP build path**
Begin with RAG answers for FAQs and read-only order lookup. Add handoff with summaries, then low-risk actions such as address update, then specialist flows and QA dashboards.

## 14. Subscription-management assistant

**Purpose and user journey**
Lets customers manage recurring orders: skip, delay, swap products, change frequency, update payment or cancel. It also helps merchants retain customers with fair offers and prevents surprise charges.

**Reference architecture**
User request -> authentication -> subscription agent -> [subscription API | billing/dunning | catalog swaps | retention offers] -> confirmation -> scheduled-event updates

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
    A14_0["User request"]
    class A14_0 frontend
    A14_1["authentication"]
    class A14_1 tool
    A14_2["subscription agent"]
    class A14_2 agent
    A14_3["subscription API"]
    class A14_3 external
    A14_4["billing/dunning"]
    class A14_4 tool
    A14_5["catalog swaps"]
    class A14_5 tool
    A14_6["retention offers"]
    class A14_6 tool
    A14_7["confirmation"]
    class A14_7 tool
    A14_8["scheduled-event updates"]
    class A14_8 backend
    A14_0 --> A14_1
    A14_1 --> A14_2
    A14_2 --> A14_3
    A14_2 --> A14_4
    A14_2 --> A14_5
    A14_2 --> A14_6
    A14_3 --> A14_7
    A14_4 --> A14_7
    A14_5 --> A14_7
    A14_6 --> A14_7
    A14_7 --> A14_8
    ID14["Entra ID + managed identity"]
    SAFE14["Policy, validation + approval gates"]
    OBS14["Tracing, metrics + evaluation"]
    class ID14,SAFE14,OBS14 control
    ID14 -. authentication .-> A14_1
    SAFE14 -. enforcement .-> A14_1
    OBS14 -. telemetry .-> A14_1
```

**Core components**
- Subscription billing engine (Recharge, Stripe Billing or Zuora).
- Subscription management API.
- Assistant with function calling.
- Retention offer rules engine.
- Reminder scheduler.
- Dunning and payment-update flow.

**Agent/workflow design**
The agent maps requests to atomic operations (skip, pause, swap, change interval, cancel) and shows the exact effect on next charge date and price before confirming. For cancellation it asks the reason and may present one relevant offer, but must always provide a clear path to cancel. Reminders before renewal are generated by the scheduler, not the LLM.

**Data and integrations**
Subscriptions, billing schedule, payment status, product substitutions, usage and consumption signals, cancellation reasons. Integrations: billing provider, OMS, catalog, email and SMS, payment-update hosted page.

**Security and safety**
Require authentication and step-up verification for payment changes. Make operations idempotent and logged. Avoid dark patterns and comply with consumer rules such as easy cancellation and renewal notices. Keep payment details out of the model through hosted forms.

**Reliability, observability and evaluation**
Track self-service rate, involuntary churn recovery, save-offer acceptance, complaint and chargeback rates, and wrong-action rate. Validate each tool result against the billing system and test date-calculation edge cases such as month-end and time zones.

**MVP build path**
Implement skip, pause and frequency change first. Add product swaps and pre-renewal reminders, then cancellation with offers, then dunning recovery.

## 15. Loyalty and rewards assistant

**Purpose and user journey**
Helps members understand and use loyalty programs. They ask about points, tier progress and expiry, get suggestions for redeeming rewards, and receive nudges to earn more in ways that fit their shopping habits.

**Reference architecture**
Member query/event -> identity -> loyalty agent -> [points ledger | tier engine | rewards catalog | offers] -> explanation or redemption -> ledger update

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
    A15_0["Member query/event"]
    class A15_0 frontend
    A15_1["identity"]
    class A15_1 tool
    A15_2["loyalty agent"]
    class A15_2 agent
    A15_3["points ledger"]
    class A15_3 data
    A15_4["tier engine"]
    class A15_4 agent
    A15_5["rewards catalog"]
    class A15_5 tool
    A15_6["offers"]
    class A15_6 tool
    A15_7["explanation or redemption"]
    class A15_7 tool
    A15_8["ledger update"]
    class A15_8 data
    A15_0 --> A15_1
    A15_1 --> A15_2
    A15_2 --> A15_3
    A15_2 --> A15_4
    A15_2 --> A15_5
    A15_2 --> A15_6
    A15_3 --> A15_7
    A15_4 --> A15_7
    A15_5 --> A15_7
    A15_6 --> A15_7
    A15_7 --> A15_8
    ID15["Entra ID + managed identity"]
    SAFE15["Policy, validation + approval gates"]
    OBS15["Tracing, metrics + evaluation"]
    class ID15,SAFE15,OBS15 control
    ID15 -. authentication .-> A15_1
    SAFE15 -. enforcement .-> A15_1
    OBS15 -. telemetry .-> A15_1
```

**Core components**
- Loyalty platform or ledger service (immutable transactions).
- Tier and rules engine.
- Rewards catalog.
- Assistant with read and redeem tools.
- Member profile and segmentation.
- Notification service for expiry and tier events.

**Agent/workflow design**
The agent answers account questions from ledger tools, never from memory. It explains how points were earned, how close the member is to the next tier, and which redemption gives the best value. Redemption is a two-step confirm action. Earn-more suggestions are generated from purchase history and ranked by member benefit and program cost.

**Data and integrations**
Point transactions, tier status, rewards inventory, purchase history, partner earn data, consent preferences. Integrations: POS and e-commerce order feed, CRM/CDP, rewards fulfillment, partners, email and push.

**Security and safety**
Protect against account takeover, since points have monetary value: use step-up authentication for redemptions and transfers, velocity limits, and anomaly detection. Keep the ledger append-only with reconciliation. Respect consent and privacy laws for profiling. Disclose terms and expiry clearly.

**Reliability, observability and evaluation**
Track balance-query accuracy, redemption success, active-member rate, breakage rate, support contacts about points and fraud losses. Reconcile earn events daily, test tier calculations with fixed scenarios, and monitor event-processing lag.

**MVP build path**
Start with balance, history and tier-progress Q&A. Add expiry reminders, then guided redemption, then personalized earn suggestions and partner offers.

## 16. Personalized promotion assistant

**Purpose and user journey**
Delivers relevant offers to the right customer at the right time within margin and fairness limits. A shopper sees tailored coupons or bundles in the app, email or on-site, and merchants control budgets and measure true incremental lift.

**Reference architecture**
Customer events -> feature store -> eligibility and propensity models -> offer optimizer (budget/margin rules) -> message generator -> channel delivery -> holdout measurement

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
    A16_0["Customer events"]
    class A16_0 frontend
    A16_1["feature store"]
    class A16_1 data
    A16_2["eligibility and propensity models"]
    class A16_2 tool
    A16_3["offer optimizer (budget/margin rules)"]
    class A16_3 tool
    A16_4["message generator"]
    class A16_4 tool
    A16_5["channel delivery"]
    class A16_5 tool
    A16_6["holdout measurement"]
    class A16_6 backend
    A16_0 --> A16_1
    A16_1 --> A16_2
    A16_2 --> A16_3
    A16_3 --> A16_4
    A16_4 --> A16_5
    A16_5 --> A16_6
    ID16["Entra ID + managed identity"]
    SAFE16["Policy, validation + approval gates"]
    OBS16["Tracing, metrics + evaluation"]
    class ID16,SAFE16,OBS16 control
    ID16 -. authentication .-> A16_1
    SAFE16 -. enforcement .-> A16_1
    OBS16 -. telemetry .-> A16_1
```

**Core components**
- Customer data platform and feature store (Azure Synapse or Fabric, Azure ML).
- Propensity and uplift models.
- Promotion rules engine and budget controller.
- LLM copy generator with brand-voice constraints.
- Channel orchestration (email, push, on-site).
- Experimentation platform.

**Agent/workflow design**
Models and rules decide who gets which offer; the LLM only writes the message copy and variants from a controlled template and offer data. Planner agents help marketers draft campaigns and simulate budget, but publishing requires approval. Every send is assigned to a treatment or holdout group to measure uplift rather than raw conversion.

**Data and integrations**
Order history, browsing events, consent flags, margin and inventory data, promotion catalog, past offer responses. Integrations: commerce platform promo codes, CDP, email/push providers, ad platforms, BI.

**Security and safety**
Honor consent, suppression lists and regional marketing laws (GDPR, ePrivacy). Do not target using sensitive traits or exploit vulnerability. Check for discriminatory pricing, limit discount abuse with single-use signed codes, and cap contact frequency. Use human approval for new campaigns and copy claims.

**Reliability, observability and evaluation**
Track incremental revenue, margin after discount, redemption rate, unsubscribe rate, budget burn and model drift. Run continuous holdout tests, offline policy evaluation before launch, and a kill switch per campaign. Monitor fairness across customer segments.

**MVP build path**
Begin with rule-based segments and holdout-measured campaigns. Add propensity scoring, then LLM-generated copy variants, then uplift-based optimization with budget control.
