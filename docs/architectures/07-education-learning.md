# Education and Learning Assistants (Apps 66-71)

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
    TOOLS --> DOMAIN["Education and learning tools and partner APIs"]
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


## 66. Language-learning tutor

**Purpose and user journey:** Gives learners conversational practice, corrections and spaced review in a target language. A learner sets a goal and level, chats or speaks through a scenario, receives gentle feedback, then reviews personalized flashcards and weekly progress summaries.

**Reference architecture:** `Learner app (text/voice) -> Session API -> Tutor agent -> LLM + CEFR curriculum -> Feedback + SRS scheduler -> Progress DB`

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
    A66_0["Learner app (text/voice)"]
    class A66_0 frontend
    A66_1["Session API"]
    class A66_1 external
    A66_2["Tutor agent"]
    class A66_2 agent
    A66_3["LLM + CEFR curriculum"]
    class A66_3 tool
    A66_4["Feedback + SRS scheduler"]
    class A66_4 tool
    A66_5["Progress DB"]
    class A66_5 backend
    A66_0 --> A66_1
    A66_1 --> A66_2
    A66_2 --> A66_3
    A66_3 --> A66_4
    A66_4 --> A66_5
    ID66["Entra ID + managed identity"]
    SAFE66["Policy, validation + approval gates"]
    OBS66["Tracing, metrics + evaluation"]
    class ID66,SAFE66,OBS66 control
    ID66 -. authentication .-> A66_1
    SAFE66 -. enforcement .-> A66_1
    OBS66 -. telemetry .-> A66_1
```

**Core components:** Speech-to-text and text-to-speech, pronunciation scorer, CEFR-tagged lesson library, learner model, spaced-repetition scheduler, conversation planner, feedback renderer, optional teacher dashboard.

**Agent/workflow design:** A planner picks a scenario and target vocabulary. The tutor persona converses at the learner's level plus one. A corrector tool marks errors and explains them. A summarizer writes mistakes to the learner model, and the scheduler queues reviews. Teachers can override plans.

**Data and integrations:** Learner profile, error taxonomy, frequency word lists, licensed lesson content, speech APIs, LMS connection via LTI, reminder notifications. Audio is stored only with consent and a short retention period.

**Security and safety:** Child safety: age gating, parental consent where required, no open-ended companionship, moderated roleplays, and never soliciting personal details. Academic integrity: graded-writing help stays off unless a teacher enables it. Minimize voice data and avoid voiceprints.

**Reliability, observability and evaluation:** Set a voice-turn latency budget and fall back to text. Trace each turn and track correction acceptance, retention and completion. Evaluate with native-speaker-rated dialogues, CEFR drift tests, invalid grammar-rule checks and per-language regression suites.

**MVP build path:** Launch one language pair with text chat, corrections, a 200-item A1-A2 deck and spaced repetition. Then add voice, pronunciation scoring and a teacher dashboard. Add languages only after native-speaker review.

## 67. Study assistant

**Purpose and user journey:** Helps students turn their own notes, slides and readings into a study plan, summaries, flashcards and practice questions. A student uploads materials, picks a deadline, follows a daily plan and asks questions grounded in the sources.

**Reference architecture:** `Upload portal -> Parser/chunker -> Vector index -> Study agent (RAG + planner) -> Cards/summaries/plan -> Progress tracker`

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
    A67_0["Upload portal"]
    class A67_0 frontend
    A67_1["Parser/chunker"]
    class A67_1 tool
    A67_2["Vector index"]
    class A67_2 data
    A67_3["Study agent (RAG + planner)"]
    class A67_3 agent
    A67_4["Cards/summaries/plan"]
    class A67_4 tool
    A67_5["Progress tracker"]
    class A67_5 backend
    A67_0 --> A67_1
    A67_1 --> A67_2
    A67_2 --> A67_3
    A67_3 --> A67_4
    A67_4 --> A67_5
    ID67["Entra ID + managed identity"]
    SAFE67["Policy, validation + approval gates"]
    OBS67["Tracing, metrics + evaluation"]
    class ID67,SAFE67,OBS67 control
    ID67 -. authentication .-> A67_1
    SAFE67 -. enforcement .-> A67_1
    OBS67 -. telemetry .-> A67_1
```

**Core components:** Document parser with OCR, chunk index with citations, summarizer, flashcard generator, planner with calendar logic, mastery tracker, source viewer, export tools.

**Agent/workflow design:** Ingest materials, extract topics, and build a concept map. The planner schedules sessions by deadline and weak areas. Each answer retrieves source passages, cites them and says when the materials lack support. Quizzes update mastery estimates.

**Data and integrations:** Student-owned files, LMS imports, calendar sync, reference-manager exports, optional Anki export. Keep each workspace isolated and let students delete sources and derived embeddings.

**Security and safety:** Child safety: age-appropriate settings, parent or school controls for minors, and no unnecessary personal data. Academic integrity: supports learning from the student's own materials, labels generated content, and does not produce submit-ready assignments. Scan uploads for malware and prompt injection.

**Reliability, observability and evaluation:** Log retrieval hits, citation coverage and unsupported-answer rate. Run faithfulness checks against source passages, flashcard accuracy sampling, and plan feasibility tests. Monitor parsing failures and report them to the user.

**MVP build path:** Start with PDF and text upload, cited chat, summaries and flashcards. Add the deadline planner and mastery tracking next. Pilot with one course, collect error reports, then add OCR, LMS import and shared teacher-approved decks.

## 68. Homework tutor

**Purpose and user journey:** Guides students through homework by asking questions, giving hints and checking reasoning rather than handing over answers. A student photographs or types a problem, chooses a hint level, works step by step and receives a reflection summary.

**Reference architecture:** `Student UI -> Safety filter -> Tutor agent (hint ladder) -> Solver/verifier tools -> Step checker -> Guardian/teacher report`

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
    A68_0["Student UI"]
    class A68_0 frontend
    A68_1["Safety filter"]
    class A68_1 tool
    A68_2["Tutor agent (hint ladder)"]
    class A68_2 agent
    A68_3["Solver/verifier tools"]
    class A68_3 agent
    A68_4["Step checker"]
    class A68_4 tool
    A68_5["Guardian/teacher report"]
    class A68_5 backend
    A68_0 --> A68_1
    A68_1 --> A68_2
    A68_2 --> A68_3
    A68_3 --> A68_4
    A68_4 --> A68_5
    ID68["Entra ID + managed identity"]
    SAFE68["Policy, validation + approval gates"]
    OBS68["Tracing, metrics + evaluation"]
    class ID68,SAFE68,OBS68 control
    ID68 -. authentication .-> A68_1
    SAFE68 -. enforcement .-> A68_1
    OBS68 -. telemetry .-> A68_1
```

**Core components:** Problem parser, subject solver tools, hidden reference solution, hint-ladder controller, step checker, misconception library, age-based tone settings, activity report.

**Agent/workflow design:** Classify the subject, solve privately, and verify with calculators or code. Reveal Socratic hints first, then worked parallel examples, and the full answer only under teacher policy. Detect frustration or repeated errors and recommend human help.

**Data and integrations:** Curriculum standards, textbook-aligned examples, math and science engines, LMS assignment context, optional guardian reports. Retain minimal history and avoid storing images beyond the session unless the user opts in.

**Security and safety:** Child safety: parental consent, age-appropriate language, private-information blocking, bullying and self-harm escalation paths, and no chat with strangers. Academic integrity: answer-reveal limits, assignment-mode policies, and activity logs visible to teachers. Guard against jailbreak attempts for answers.

**Reliability, observability and evaluation:** Verify solutions independently before hinting. Track hint depth, answer-leak rate, wrong-hint rate and escalation events. Evaluate on graded problem sets, adversarial answer-extraction prompts and teacher review of sampled sessions.

**MVP build path:** Begin with middle-school math text problems, a three-step hint ladder, a calculator and verifier. Add photo input and science subjects, then guardian reports and teacher policies. Expand only after pedagogy review.

## 69. Exam-preparation coach

**Purpose and user journey:** Prepares learners for a specific exam through a diagnostic test, a personalized plan, timed practice and review. The user selects an exam and date, receives a readiness estimate, practices weak topics and sits mock exams.

**Reference architecture:** `Exam profile -> Diagnostic engine -> Coach agent -> Question bank + generator -> Timed mock runner -> Readiness model -> Plan updater`

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
    A69_0["Exam profile"]
    class A69_0 frontend
    A69_1["Diagnostic engine"]
    class A69_1 agent
    A69_2["Coach agent"]
    class A69_2 agent
    A69_3["Question bank + generator"]
    class A69_3 tool
    A69_4["Timed mock runner"]
    class A69_4 tool
    A69_5["Readiness model"]
    class A69_5 tool
    A69_6["Plan updater"]
    class A69_6 backend
    A69_0 --> A69_1
    A69_1 --> A69_2
    A69_2 --> A69_3
    A69_3 --> A69_4
    A69_4 --> A69_5
    A69_5 --> A69_6
    ID69["Entra ID + managed identity"]
    SAFE69["Policy, validation + approval gates"]
    OBS69["Tracing, metrics + evaluation"]
    class ID69,SAFE69,OBS69 control
    ID69 -. authentication .-> A69_1
    SAFE69 -. enforcement .-> A69_1
    OBS69 -. telemetry .-> A69_1
```

**Core components:** Syllabus map, licensed question bank, item-difficulty model, mock exam runner, rubric-based marker, error analyzer, spaced review scheduler, readiness dashboard, reminders.

**Agent/workflow design:** Run a diagnostic, map errors to syllabus topics and build a backward-planned schedule. Select questions by difficulty and forgetting risk. The marker applies rubrics to open answers, and the coach explains misses and adjusts the plan after every session.

**Data and integrations:** Official syllabi, past-paper licensing, calendars, LMS or school-tutor connections, accessibility settings. Store scores as sensitive learning data and let users export or delete them.

**Security and safety:** Child safety: avoid pressure tactics, show wellbeing prompts for exam anxiety, and require guardian consent for minors. Academic integrity: no leaked or live exam content, no impersonation in proctored tests, and clear separation of practice from official assessment.

**Reliability, observability and evaluation:** Calibrate readiness predictions against real outcomes. Monitor item quality, marking disagreement with teachers, plan adherence and drop-off. Evaluate generated questions through expert review and test marker consistency with blind double-marking.

**MVP build path:** Choose one exam. Ship syllabus mapping, a diagnostic, multiple-choice practice and a spaced schedule. Add rubric marking for short answers and timed mocks, then calibrate readiness predictions with pilot cohort data.

## 70. Reading assistant

**Purpose and user journey:** Supports comprehension of texts for learners, including struggling readers and multilingual students. A reader opens a passage, gets leveled explanations, vocabulary help, read-aloud and comprehension questions, then reflects on understanding.

**Reference architecture:** `Reader UI -> Text processor -> Reading agent -> Readability + glossary tools -> TTS/translation -> Comprehension checks -> Progress log`

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
    A70_0["Reader UI"]
    class A70_0 frontend
    A70_1["Text processor"]
    class A70_1 tool
    A70_2["Reading agent"]
    class A70_2 agent
    A70_3["Readability + glossary tools"]
    class A70_3 tool
    A70_4["TTS/translation"]
    class A70_4 tool
    A70_5["Comprehension checks"]
    class A70_5 tool
    A70_6["Progress log"]
    class A70_6 backend
    A70_0 --> A70_1
    A70_1 --> A70_2
    A70_2 --> A70_3
    A70_3 --> A70_4
    A70_4 --> A70_5
    A70_5 --> A70_6
    ID70["Entra ID + managed identity"]
    SAFE70["Policy, validation + approval gates"]
    OBS70["Tracing, metrics + evaluation"]
    class ID70,SAFE70,OBS70 control
    ID70 -. authentication .-> A70_1
    SAFE70 -. enforcement .-> A70_1
    OBS70 -. telemetry .-> A70_1
```

**Core components:** Text segmenter, readability scorer, glossary and definition service, text-to-speech with highlighting, translation module, question generator, annotation store, accessibility controls.

**Agent/workflow design:** Estimate reading level, chunk the text and offer optional support. When asked, explain in simpler words while preserving the original. Pose predictive and inferential questions, check answers against the passage, and recommend next texts.

**Data and integrations:** Public-domain and licensed libraries, school reading lists, dictionary APIs, OCR for scans, LMS integration, dyslexia-friendly fonts and display settings. Store annotations privately by default.

**Security and safety:** Child safety: curated or age-rated texts, blocked unsafe web content, no profile building for advertising, and guardian visibility. Academic integrity: summaries cannot replace assigned reading in teacher-controlled mode, and copyright limits are respected.

**Reliability, observability and evaluation:** Measure answer-grounding, readability accuracy, simplification fidelity, and TTS pronunciation errors. Compare question quality with teacher ratings. Use offline fallback for read-aloud and log accessibility-feature usage without storing sensitive text.

**MVP build path:** Start with pasted text and public-domain books, definitions, read-aloud and five comprehension questions. Add leveled simplification, annotation and progress tracking. Run pilots with teachers and readers with accessibility needs before translation and LMS features.

## 71. Educational quiz generator

**Purpose and user journey:** Lets teachers and learners create quizzes from lesson materials with chosen difficulty, standards and question types. A creator uploads content, reviews generated items, publishes a quiz and analyzes results.

**Reference architecture:** `Content input -> Standards mapper -> Quiz agent -> Item generator -> Validator/reviewer -> Quiz builder -> Delivery + analytics`

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
    A71_0["Content input"]
    class A71_0 frontend
    A71_1["Standards mapper"]
    class A71_1 frontend
    A71_2["Quiz agent"]
    class A71_2 frontend
    A71_3["Item generator"]
    class A71_3 tool
    A71_4["Validator/reviewer"]
    class A71_4 agent
    A71_5["Quiz builder"]
    class A71_5 frontend
    A71_6["Delivery + analytics"]
    class A71_6 backend
    A71_0 --> A71_1
    A71_1 --> A71_2
    A71_2 --> A71_3
    A71_3 --> A71_4
    A71_4 --> A71_5
    A71_5 --> A71_6
    ID71["Entra ID + managed identity"]
    SAFE71["Policy, validation + approval gates"]
    OBS71["Tracing, metrics + evaluation"]
    class ID71,SAFE71,OBS71 control
    ID71 -. authentication .-> A71_1
    SAFE71 -. enforcement .-> A71_1
    OBS71 -. telemetry .-> A71_1
```

**Core components:** Content ingestion, learning-objective extractor, item templates, distractor generator, answer verifier, bias and readability checker, review queue, quiz export, item analytics.

**Agent/workflow design:** Extract objectives, draft items for each objective and difficulty, and independently solve them to verify keys. Flag ambiguity, duplicates and bias. A human approves items before publishing, and later results retire poor questions.

**Data and integrations:** Teacher-supplied materials, curriculum standards, QTI export, Google Classroom or LMS gradebook, item-statistics store. Separate private banks from shared community banks with explicit permissions.

**Security and safety:** Child safety: no personal questions, age-appropriate wording, anonymized results for minors and aggregate reporting. Academic integrity: secure question banks, randomization, access controls, review before high-stakes use, and prohibition on copying copyrighted exam items.

**Reliability, observability and evaluation:** Track key-validation failure, teacher edit rate, item difficulty, discrimination and bias flags. Evaluate against expert-written benchmark items and regenerate failing items. Version every quiz so that results stay interpretable.

**MVP build path:** Build multiple-choice generation from pasted text with teacher approval, answer verification and CSV or QTI export. Add standards tagging, analytics and shared banks later. Pilot formative quizzes before any high-stakes assessment.
