# B2C AI App Implementation Catalog

A curated catalog of **107 business-to-consumer AI application ideas**, each mapped to:

- an Azure / Microsoft Foundry implementation or reusable reference;
- a LangChain or LangGraph alternative;
- a Vercel AI SDK alternative where appropriate;
- an explicit match level: **Exact**, **Adjacent**, or **Base**.

Use this catalog for solution discovery, prototypes, Forward Deployed Engineer portfolio projects, workshops, and architecture comparisons.

## Comprehensive architecture overviews

The repository now includes implementation-oriented architecture guides for every catalog entry. Each guide covers the user journey, system flow, components, agent design, data, integrations, security, reliability, evaluation, and an MVP build path.

**[Browse all 107 architecture overviews](docs/architectures/README.md)**

## Important notes

- Links marked **Exact** implement the same scenario.
- Links marked **Adjacent** implement a closely related domain or workflow.
- Links marked **Base** provide reusable technical building blocks rather than a finished domain application.
- Archived repositories are explicitly labeled and should be treated as code references, not preferred new dependencies.
- Healthcare examples are for research and development. They are not medical devices and must not be used for diagnosis or treatment without appropriate validation and regulatory review.

---

**Azure match labels:** **Exact** = same scenario; **Adjacent** = same domain/workflow; **Base** = reusable Foundry implementation to adapt.

Every app also has a nearest reusable **LangChain or Vercel** implementation. Archived alternatives are labeled explicitly and are included only as code references.

> Healthcare Agent Orchestrator is research/development sample code and is not intended for clinical diagnosis or treatment.

## Commerce and retail

| # | B2C app | Azure match | Azure implementation | LangChain / Vercel alternative |
|---:|---|---|---|---|
| 1 | Personal shopping assistant | Exact | [Fashion Assistant with Foundry agents](https://github.com/Azure-Samples/app-service-aspire-eshop-agents) | [Vercel AI Chatbot](https://github.com/vercel/chatbot) |
| 2 | Fashion and styling assistant | Exact | [Fashion Assistant with Foundry agents](https://github.com/Azure-Samples/app-service-aspire-eshop-agents) | [Vercel semantic image search](https://github.com/vercel-labs/semantic-image-search) |
| 3 | Personal wardrobe assistant | Exact | [Fashion Assistant with Foundry agents](https://github.com/Azure-Samples/app-service-aspire-eshop-agents) | [Vercel semantic image search](https://github.com/vercel-labs/semantic-image-search) |
| 4 | Product discovery assistant | Adjacent | [eShopLite reference apps](https://github.com/Azure-Samples/eShopLite) | [Vercel semantic image search](https://github.com/vercel-labs/semantic-image-search) |
| 5 | Product comparison assistant | Adjacent | [eShopLite reference apps](https://github.com/Azure-Samples/eShopLite) | [Vercel semantic image search](https://github.com/vercel-labs/semantic-image-search) |
| 6 | Gift recommendation assistant | Adjacent | [eShopLite reference apps](https://github.com/Azure-Samples/eShopLite) | [Vercel semantic image search](https://github.com/vercel-labs/semantic-image-search) |
| 7 | Visual product-search app | Adjacent | [eShopLite reference apps](https://github.com/Azure-Samples/eShopLite) | [Vercel semantic image search](https://github.com/vercel-labs/semantic-image-search) |
| 8 | Shopping-cart assistant | Adjacent | [Garden Shop AI Chat](https://github.com/dotnet/maui-labs/tree/main/samples/AIExtensions.Sample.Garden) | [LangGraph auth + payments app (archived reference)](https://github.com/langchain-ai/agent-auth-payments) |
| 9 | Checkout assistant | Adjacent | [Garden Shop AI Chat](https://github.com/dotnet/maui-labs/tree/main/samples/AIExtensions.Sample.Garden) | [LangGraph auth + payments app (archived reference)](https://github.com/langchain-ai/agent-auth-payments) |
| 10 | Order-tracking assistant | Adjacent | [eShopSupport](https://github.com/dotnet/eShopSupport) | [LangGraph customer-support workflow](https://github.com/langchain-ai/langgraph/tree/main/examples/customer-support) |
| 11 | Delivery-exception assistant | Adjacent | [eShopSupport](https://github.com/dotnet/eShopSupport) | [LangGraph customer-support workflow](https://github.com/langchain-ai/langgraph/tree/main/examples/customer-support) |
| 12 | Returns and refunds assistant | Adjacent | [eShopSupport](https://github.com/dotnet/eShopSupport) | [LangGraph customer-support workflow](https://github.com/langchain-ai/langgraph/tree/main/examples/customer-support) |
| 13 | E-commerce customer-support agent | Adjacent | [eShopSupport](https://github.com/dotnet/eShopSupport) | [LangGraph customer-support workflow](https://github.com/langchain-ai/langgraph/tree/main/examples/customer-support) |
| 14 | Subscription-management assistant | Base | [Agentic App Service CRUD and tool-calling app](https://github.com/Azure-Samples/app-service-agentic-semantic-kernel-ai-foundry-agent) | [LangGraph auth + payments app (archived reference)](https://github.com/langchain-ai/agent-auth-payments) |
| 15 | Loyalty and rewards assistant | Adjacent | [Garden Shop AI Chat](https://github.com/dotnet/maui-labs/tree/main/samples/AIExtensions.Sample.Garden) | [LangGraph auth + payments app (archived reference)](https://github.com/langchain-ai/agent-auth-payments) |
| 16 | Personalized promotion assistant | Adjacent | [Garden Shop AI Chat](https://github.com/dotnet/maui-labs/tree/main/samples/AIExtensions.Sample.Garden) | [LangGraph auth + payments app (archived reference)](https://github.com/langchain-ai/agent-auth-payments) |

## Food and dining

| # | B2C app | Azure match | Azure implementation | LangChain / Vercel alternative |
|---:|---|---|---|---|
| 17 | Grocery-shopping assistant | Adjacent | [Garden Shop AI Chat](https://github.com/dotnet/maui-labs/tree/main/samples/AIExtensions.Sample.Garden) | [Vercel AI Chatbot](https://github.com/vercel/chatbot) |
| 18 | Meal-planning coach | Base | [Getting Started with Foundry Agents and RAG](https://github.com/Azure-Samples/get-started-with-ai-agents) | [Vercel AI SDK RAG starter](https://github.com/vercel/ai-sdk-rag-starter) |
| 19 | Recipe assistant | Base | [Getting Started with Foundry Agents and RAG](https://github.com/Azure-Samples/get-started-with-ai-agents) | [Vercel AI SDK RAG starter](https://github.com/vercel/ai-sdk-rag-starter) |
| 20 | Nutrition coach | Base | [Getting Started with Foundry Agents and RAG](https://github.com/Azure-Samples/get-started-with-ai-agents) | [Vercel AI SDK RAG starter](https://github.com/vercel/ai-sdk-rag-starter) |
| 21 | Restaurant recommendation assistant | Adjacent | [Pizza Ordering Agent with Foundry and MCP](https://github.com/microsoft/ignite25-LAB571-build-a-pizza-ordering-agent-with-microsoft-foundry-and-mcp) | [LangGraph generative-UI agents (archived reference)](https://github.com/langchain-ai/langgraphjs-gen-ui-examples) |
| 22 | Restaurant reservation assistant | Adjacent | [Pizza Ordering Agent with Foundry and MCP](https://github.com/microsoft/ignite25-LAB571-build-a-pizza-ordering-agent-with-microsoft-foundry-and-mcp) | [LangGraph generative-UI agents (archived reference)](https://github.com/langchain-ai/langgraphjs-gen-ui-examples) |
| 23 | Food-ordering agent | Adjacent | [Pizza Ordering Agent with Foundry and MCP](https://github.com/microsoft/ignite25-LAB571-build-a-pizza-ordering-agent-with-microsoft-foundry-and-mcp) | [LangGraph generative-UI agents (archived reference)](https://github.com/langchain-ai/langgraphjs-gen-ui-examples) |

## Travel and events

| # | B2C app | Azure match | Azure implementation | LangChain / Vercel alternative |
|---:|---|---|---|---|
| 24 | Travel-planning assistant | Exact | [Multi-agent Travel Planner](https://github.com/Azure-Samples/app-service-maf-openai-travel-agent-dotnet) | [LangGraph generative-UI agents (archived reference)](https://github.com/langchain-ai/langgraphjs-gen-ui-examples) |
| 25 | Flight-search assistant | Exact | [Multi-agent Travel Planner](https://github.com/Azure-Samples/app-service-maf-openai-travel-agent-dotnet) | [LangGraph generative-UI agents (archived reference)](https://github.com/langchain-ai/langgraphjs-gen-ui-examples) |
| 26 | Hotel recommendation assistant | Exact | [Multi-agent Travel Planner](https://github.com/Azure-Samples/app-service-maf-openai-travel-agent-dotnet) | [LangGraph generative-UI agents (archived reference)](https://github.com/langchain-ai/langgraphjs-gen-ui-examples) |
| 27 | Trip-booking assistant | Exact | [Multi-agent Travel Planner](https://github.com/Azure-Samples/app-service-maf-openai-travel-agent-dotnet) | [LangGraph generative-UI agents (archived reference)](https://github.com/langchain-ai/langgraphjs-gen-ui-examples) |
| 28 | Itinerary generator | Exact | [Multi-agent Travel Planner](https://github.com/Azure-Samples/app-service-maf-openai-travel-agent-dotnet) | [LangGraph generative-UI agents (archived reference)](https://github.com/langchain-ai/langgraphjs-gen-ui-examples) |
| 29 | Travel-disruption assistant | Exact | [Multi-agent Travel Planner](https://github.com/Azure-Samples/app-service-maf-openai-travel-agent-dotnet) | [LangGraph generative-UI agents (archived reference)](https://github.com/langchain-ai/langgraphjs-gen-ui-examples) |
| 30 | Local activity concierge | Exact | [Multi-agent Travel Planner](https://github.com/Azure-Samples/app-service-maf-openai-travel-agent-dotnet) | [LangGraph generative-UI agents (archived reference)](https://github.com/langchain-ai/langgraphjs-gen-ui-examples) |
| 31 | Event-planning assistant | Base | [Multi-Agent Orchestration Workshop](https://github.com/Azure-Samples/multi-agent-orchestration-workshop) | [LangChain deployment cookbook](https://github.com/langchain-ai/deployment-cookbook) |
| 32 | Ticket-discovery assistant | Base | [Multi-Agent Orchestration Workshop](https://github.com/Azure-Samples/multi-agent-orchestration-workshop) | [LangChain deployment cookbook](https://github.com/langchain-ai/deployment-cookbook) |

## Home and property

| # | B2C app | Azure match | Azure implementation | LangChain / Vercel alternative |
|---:|---|---|---|---|
| 33 | Home-services booking assistant | Base | [Agentic App Service CRUD and tool-calling app](https://github.com/Azure-Samples/app-service-agentic-semantic-kernel-ai-foundry-agent) | [LangChain deployment cookbook](https://github.com/langchain-ai/deployment-cookbook) |
| 34 | Home-repair diagnostic assistant | Base | [C# vision chat application](https://github.com/Azure-Samples/ai-chat-vision-quickstart-csharp) | [Vercel AI Chatbot](https://github.com/vercel/chatbot) |
| 35 | Property-search assistant | Base | [Azure Search + OpenAI C# RAG app](https://github.com/Azure-Samples/azure-search-openai-demo-csharp) | [Vercel AI SDK RAG starter](https://github.com/vercel/ai-sdk-rag-starter) |
| 36 | Rental assistant | Base | [Agentic App Service CRUD and tool-calling app](https://github.com/Azure-Samples/app-service-agentic-semantic-kernel-ai-foundry-agent) | [Vercel AI Chatbot](https://github.com/vercel/chatbot) |
| 37 | Moving and relocation assistant | Base | [Azure Search + OpenAI C# RAG app](https://github.com/Azure-Samples/azure-search-openai-demo-csharp) | [Vercel AI SDK RAG starter](https://github.com/vercel/ai-sdk-rag-starter) |
| 38 | Interior-design assistant | Base | [C# vision chat application](https://github.com/Azure-Samples/ai-chat-vision-quickstart-csharp) | [Vercel AI SDK image generator](https://github.com/vercel-labs/ai-sdk-image-generator) |
| 39 | Smart-home support assistant | Adjacent | [eShopSupport](https://github.com/dotnet/eShopSupport) | [Vercel AI Chatbot](https://github.com/vercel/chatbot) |

## Finance, insurance, legal and automotive

| # | B2C app | Azure match | Azure implementation | LangChain / Vercel alternative |
|---:|---|---|---|---|
| 40 | Personal finance coach | Base | [Getting Started with Foundry Agents and RAG](https://github.com/Azure-Samples/get-started-with-ai-agents) | [Vercel AI SDK RAG starter](https://github.com/vercel/ai-sdk-rag-starter) |
| 41 | Budget-planning assistant | Base | [Getting Started with Foundry Agents and RAG](https://github.com/Azure-Samples/get-started-with-ai-agents) | [Vercel AI SDK RAG starter](https://github.com/vercel/ai-sdk-rag-starter) |
| 42 | Spending-analysis assistant | Base | [Getting Started with Foundry Agents and RAG](https://github.com/Azure-Samples/get-started-with-ai-agents) | [Vercel AI SDK RAG starter](https://github.com/vercel/ai-sdk-rag-starter) |
| 43 | Savings-goal coach | Base | [Getting Started with Foundry Agents and RAG](https://github.com/Azure-Samples/get-started-with-ai-agents) | [Vercel AI SDK RAG starter](https://github.com/vercel/ai-sdk-rag-starter) |
| 44 | Insurance-policy assistant | Base | [Azure Search + OpenAI C# RAG app](https://github.com/Azure-Samples/azure-search-openai-demo-csharp) | [Vercel AI SDK RAG starter](https://github.com/vercel/ai-sdk-rag-starter) |
| 45 | Insurance-claim assistant | Base | [Multi-Agent Orchestration Workshop](https://github.com/Azure-Samples/multi-agent-orchestration-workshop) | [LangChain deployment cookbook](https://github.com/langchain-ai/deployment-cookbook) |
| 46 | Consumer contract explainer | Base | [Azure Search + OpenAI C# RAG app](https://github.com/Azure-Samples/azure-search-openai-demo-csharp) | [Vercel AI SDK RAG starter](https://github.com/vercel/ai-sdk-rag-starter) |
| 47 | Tax-document organizer | Base | [Azure Search + OpenAI C# RAG app](https://github.com/Azure-Samples/azure-search-openai-demo-csharp) | [Vercel AI SDK RAG starter](https://github.com/vercel/ai-sdk-rag-starter) |
| 48 | Car-buying assistant | Adjacent | [eShopLite reference apps](https://github.com/Azure-Samples/eShopLite) | [Vercel semantic image search](https://github.com/vercel-labs/semantic-image-search) |
| 49 | Vehicle comparison assistant | Adjacent | [eShopLite reference apps](https://github.com/Azure-Samples/eShopLite) | [Vercel semantic image search](https://github.com/vercel-labs/semantic-image-search) |
| 50 | Vehicle-maintenance assistant | Adjacent | [eShopSupport](https://github.com/dotnet/eShopSupport) | [LangGraph customer-support workflow](https://github.com/langchain-ai/langgraph/tree/main/examples/customer-support) |

## Health, wellness and pets

| # | B2C app | Azure match | Azure implementation | LangChain / Vercel alternative |
|---:|---|---|---|---|
| 51 | Fitness coach | Adjacent | [Healthcare Agent Orchestrator](https://github.com/Azure-Samples/healthcare-agent-orchestrator) | [Vercel AI SDK RAG starter](https://github.com/vercel/ai-sdk-rag-starter) |
| 52 | Workout-planning assistant | Adjacent | [Healthcare Agent Orchestrator](https://github.com/Azure-Samples/healthcare-agent-orchestrator) | [Vercel AI SDK RAG starter](https://github.com/vercel/ai-sdk-rag-starter) |
| 53 | Wellness coach | Adjacent | [Healthcare Agent Orchestrator](https://github.com/Azure-Samples/healthcare-agent-orchestrator) | [Vercel AI SDK RAG starter](https://github.com/vercel/ai-sdk-rag-starter) |
| 54 | Sleep coach | Adjacent | [Healthcare Agent Orchestrator](https://github.com/Azure-Samples/healthcare-agent-orchestrator) | [Vercel AI SDK RAG starter](https://github.com/vercel/ai-sdk-rag-starter) |
| 55 | Habit-building assistant | Adjacent | [Healthcare Agent Orchestrator](https://github.com/Azure-Samples/healthcare-agent-orchestrator) | [Vercel AI Chatbot](https://github.com/vercel/chatbot) |
| 56 | Skincare advisor | Exact | [Fashion Assistant with Foundry agents](https://github.com/Azure-Samples/app-service-aspire-eshop-agents) | [Vercel AI Chatbot](https://github.com/vercel/chatbot) |
| 57 | Beauty-product assistant | Exact | [Fashion Assistant with Foundry agents](https://github.com/Azure-Samples/app-service-aspire-eshop-agents) | [Vercel semantic image search](https://github.com/vercel-labs/semantic-image-search) |
| 58 | Medication reminder | Adjacent | [Healthcare Agent Orchestrator](https://github.com/Azure-Samples/healthcare-agent-orchestrator) | [Vercel AI Chatbot](https://github.com/vercel/chatbot) |
| 59 | Healthcare navigation assistant | Adjacent | [Healthcare Agent Orchestrator](https://github.com/Azure-Samples/healthcare-agent-orchestrator) | [Vercel AI SDK RAG starter](https://github.com/vercel/ai-sdk-rag-starter) |
| 60 | Appointment-booking assistant | Base | [Agentic App Service CRUD and tool-calling app](https://github.com/Azure-Samples/app-service-agentic-semantic-kernel-ai-foundry-agent) | [LangChain deployment cookbook](https://github.com/langchain-ai/deployment-cookbook) |
| 61 | Symptom-intake assistant | Adjacent | [Healthcare Agent Orchestrator](https://github.com/Azure-Samples/healthcare-agent-orchestrator) | [Vercel AI SDK RAG starter](https://github.com/vercel/ai-sdk-rag-starter) |
| 62 | Mental-wellness journaling assistant | Adjacent | [Healthcare Agent Orchestrator](https://github.com/Azure-Samples/healthcare-agent-orchestrator) | [Vercel AI SDK RAG starter](https://github.com/vercel/ai-sdk-rag-starter) |
| 63 | Pet-care assistant | Base | [Agentic App Service CRUD and tool-calling app](https://github.com/Azure-Samples/app-service-agentic-semantic-kernel-ai-foundry-agent) | [Vercel AI Chatbot](https://github.com/vercel/chatbot) |
| 64 | Veterinary appointment assistant | Base | [Agentic App Service CRUD and tool-calling app](https://github.com/Azure-Samples/app-service-agentic-semantic-kernel-ai-foundry-agent) | [Vercel AI Chatbot](https://github.com/vercel/chatbot) |
| 65 | Pet-product recommendation assistant | Adjacent | [eShopLite reference apps](https://github.com/Azure-Samples/eShopLite) | [Vercel semantic image search](https://github.com/vercel-labs/semantic-image-search) |

## Education and learning

| # | B2C app | Azure match | Azure implementation | LangChain / Vercel alternative |
|---:|---|---|---|---|
| 66 | Language-learning tutor | Adjacent | [Student–Teacher agent workflow](https://github.com/microsoft/agent-framework/tree/main/python/samples/03-workflows/declarative/student_teacher) | [Vercel real-time voice fact checker](https://github.com/vercel-labs/ai-facts) |
| 67 | Study assistant | Adjacent | [Student–Teacher agent workflow](https://github.com/microsoft/agent-framework/tree/main/python/samples/03-workflows/declarative/student_teacher) | [Vercel AI SDK RAG starter](https://github.com/vercel/ai-sdk-rag-starter) |
| 68 | Homework tutor | Adjacent | [Student–Teacher agent workflow](https://github.com/microsoft/agent-framework/tree/main/python/samples/03-workflows/declarative/student_teacher) | [Vercel AI SDK RAG starter](https://github.com/vercel/ai-sdk-rag-starter) |
| 69 | Exam-preparation coach | Adjacent | [Student–Teacher agent workflow](https://github.com/microsoft/agent-framework/tree/main/python/samples/03-workflows/declarative/student_teacher) | [Vercel AI SDK RAG starter](https://github.com/vercel/ai-sdk-rag-starter) |
| 70 | Reading assistant | Adjacent | [Student–Teacher agent workflow](https://github.com/microsoft/agent-framework/tree/main/python/samples/03-workflows/declarative/student_teacher) | [Vercel real-time voice fact checker](https://github.com/vercel-labs/ai-facts) |
| 71 | Educational quiz generator | Adjacent | [Student–Teacher agent workflow](https://github.com/microsoft/agent-framework/tree/main/python/samples/03-workflows/declarative/student_teacher) | [Vercel AI Chatbot](https://github.com/vercel/chatbot) |

## Career, productivity and family

| # | B2C app | Azure match | Azure implementation | LangChain / Vercel alternative |
|---:|---|---|---|---|
| 72 | Career-planning assistant | Base | [Getting Started with Foundry Agents and RAG](https://github.com/Azure-Samples/get-started-with-ai-agents) | [Vercel AI SDK RAG starter](https://github.com/vercel/ai-sdk-rag-starter) |
| 73 | CV and résumé assistant | Base | [Getting Started with Foundry Agents and RAG](https://github.com/Azure-Samples/get-started-with-ai-agents) | [Vercel AI SDK RAG starter](https://github.com/vercel/ai-sdk-rag-starter) |
| 74 | Interview-practice coach | Base | [Getting Started with Foundry Agents and RAG](https://github.com/Azure-Samples/get-started-with-ai-agents) | [Vercel real-time voice fact checker](https://github.com/vercel-labs/ai-facts) |
| 75 | Job-search assistant | Base | [Getting Started with Foundry Agents and RAG](https://github.com/Azure-Samples/get-started-with-ai-agents) | [Vercel AI SDK RAG starter](https://github.com/vercel/ai-sdk-rag-starter) |
| 76 | Personal productivity assistant | Base | [Agentic App Service CRUD and tool-calling app](https://github.com/Azure-Samples/app-service-agentic-semantic-kernel-ai-foundry-agent) | [Vercel AI Chatbot](https://github.com/vercel/chatbot) |
| 77 | Daily-planning assistant | Base | [Agentic App Service CRUD and tool-calling app](https://github.com/Azure-Samples/app-service-agentic-semantic-kernel-ai-foundry-agent) | [LangChain deployment cookbook](https://github.com/langchain-ai/deployment-cookbook) |
| 78 | Email-writing assistant | Base | [Getting Started with Foundry Agents and RAG](https://github.com/Azure-Samples/get-started-with-ai-agents) | [Vercel AI SDK RAG starter](https://github.com/vercel/ai-sdk-rag-starter) |
| 79 | Personal knowledge assistant | Base | [Getting Started with Foundry Agents and RAG](https://github.com/Azure-Samples/get-started-with-ai-agents) | [Vercel real-time voice fact checker](https://github.com/vercel-labs/ai-facts) |
| 80 | Family schedule assistant | Base | [Agentic App Service CRUD and tool-calling app](https://github.com/Azure-Samples/app-service-agentic-semantic-kernel-ai-foundry-agent) | [LangChain deployment cookbook](https://github.com/langchain-ai/deployment-cookbook) |
| 81 | Parenting assistant | Base | [Agentic App Service CRUD and tool-calling app](https://github.com/Azure-Samples/app-service-agentic-semantic-kernel-ai-foundry-agent) | [Vercel AI Chatbot](https://github.com/vercel/chatbot) |
| 82 | Baby-care tracker | Base | [Agentic App Service CRUD and tool-calling app](https://github.com/Azure-Samples/app-service-agentic-semantic-kernel-ai-foundry-agent) | [Vercel AI Chatbot](https://github.com/vercel/chatbot) |
| 83 | Elder-care coordination assistant | Adjacent | [Healthcare Agent Orchestrator](https://github.com/Azure-Samples/healthcare-agent-orchestrator) | [Vercel AI Chatbot](https://github.com/vercel/chatbot) |
| 84 | Accessible-living assistant | Adjacent | [Healthcare Agent Orchestrator](https://github.com/Azure-Samples/healthcare-agent-orchestrator) | [Vercel AI Chatbot](https://github.com/vercel/chatbot) |

## Technology, utilities and sustainability

| # | B2C app | Azure match | Azure implementation | LangChain / Vercel alternative |
|---:|---|---|---|---|
| 85 | Consumer technical-support agent | Adjacent | [eShopSupport](https://github.com/dotnet/eShopSupport) | [LangGraph customer-support workflow](https://github.com/langchain-ai/langgraph/tree/main/examples/customer-support) |
| 86 | Device-setup assistant | Adjacent | [eShopSupport](https://github.com/dotnet/eShopSupport) | [LangGraph customer-support workflow](https://github.com/langchain-ai/langgraph/tree/main/examples/customer-support) |
| 87 | Troubleshooting assistant | Adjacent | [eShopSupport](https://github.com/dotnet/eShopSupport) | [LangGraph customer-support workflow](https://github.com/langchain-ai/langgraph/tree/main/examples/customer-support) |
| 88 | Telecom-plan assistant | Base | [Azure Search + OpenAI C# RAG app](https://github.com/Azure-Samples/azure-search-openai-demo-csharp) | [Vercel AI SDK RAG starter](https://github.com/vercel/ai-sdk-rag-starter) |
| 89 | Energy-plan comparison assistant | Base | [Azure Search + OpenAI C# RAG app](https://github.com/Azure-Samples/azure-search-openai-demo-csharp) | [Vercel AI SDK RAG starter](https://github.com/vercel/ai-sdk-rag-starter) |
| 90 | Sustainability coach | Base | [Getting Started with Foundry Agents and RAG](https://github.com/Azure-Samples/get-started-with-ai-agents) | [Vercel AI SDK RAG starter](https://github.com/vercel/ai-sdk-rag-starter) |
| 91 | Carbon-footprint assistant | Base | [Getting Started with Foundry Agents and RAG](https://github.com/Azure-Samples/get-started-with-ai-agents) | [Vercel AI SDK RAG starter](https://github.com/vercel/ai-sdk-rag-starter) |
| 92 | Gardening assistant | Adjacent | [Garden Shop AI Chat](https://github.com/dotnet/maui-labs/tree/main/samples/AIExtensions.Sample.Garden) | [Vercel AI Chatbot](https://github.com/vercel/chatbot) |
| 93 | Plant-diagnosis assistant | Base | [C# vision chat application](https://github.com/Azure-Samples/ai-chat-vision-quickstart-csharp) | [Vercel AI SDK image generator](https://github.com/vercel-labs/ai-sdk-image-generator) |

## Creative, social, safety and public services

| # | B2C app | Azure match | Azure implementation | LangChain / Vercel alternative |
|---:|---|---|---|---|
| 94 | Photography coach | Base | [C# vision chat application](https://github.com/Azure-Samples/ai-chat-vision-quickstart-csharp) | [Vercel AI SDK image generator](https://github.com/vercel-labs/ai-sdk-image-generator) |
| 95 | Creative-writing assistant | Base | [Getting Started with Foundry Agents and RAG](https://github.com/Azure-Samples/get-started-with-ai-agents) | [Vercel AI SDK image generator](https://github.com/vercel-labs/ai-sdk-image-generator) |
| 96 | Music-discovery assistant | Base | [Getting Started with Foundry Agents and RAG](https://github.com/Azure-Samples/get-started-with-ai-agents) | [Vercel AI SDK RAG starter](https://github.com/vercel/ai-sdk-rag-starter) |
| 97 | Book-recommendation assistant | Base | [Getting Started with Foundry Agents and RAG](https://github.com/Azure-Samples/get-started-with-ai-agents) | [Vercel AI SDK RAG starter](https://github.com/vercel/ai-sdk-rag-starter) |
| 98 | Movie and streaming assistant | Base | [Getting Started with Foundry Agents and RAG](https://github.com/Azure-Samples/get-started-with-ai-agents) | [Vercel AI SDK RAG starter](https://github.com/vercel/ai-sdk-rag-starter) |
| 99 | Gaming assistant | Base | [Getting Started with Foundry Agents and RAG](https://github.com/Azure-Samples/get-started-with-ai-agents) | [Vercel AI Chatbot](https://github.com/vercel/chatbot) |
| 100 | Social-event assistant | Base | [Multi-Agent Orchestration Workshop](https://github.com/Azure-Samples/multi-agent-orchestration-workshop) | [LangChain deployment cookbook](https://github.com/langchain-ai/deployment-cookbook) |
| 101 | Dating-planning assistant | Base | [Multi-Agent Orchestration Workshop](https://github.com/Azure-Samples/multi-agent-orchestration-workshop) | [LangChain deployment cookbook](https://github.com/langchain-ai/deployment-cookbook) |
| 102 | Wedding-planning assistant | Base | [Multi-Agent Orchestration Workshop](https://github.com/Azure-Samples/multi-agent-orchestration-workshop) | [LangChain deployment cookbook](https://github.com/langchain-ai/deployment-cookbook) |
| 103 | Personal safety assistant | Base | [Azure Search + OpenAI C# RAG app](https://github.com/Azure-Samples/azure-search-openai-demo-csharp) | [Vercel real-time voice fact checker](https://github.com/vercel-labs/ai-facts) |
| 104 | Emergency-preparedness assistant | Base | [Azure Search + OpenAI C# RAG app](https://github.com/Azure-Samples/azure-search-openai-demo-csharp) | [Vercel real-time voice fact checker](https://github.com/vercel-labs/ai-facts) |
| 105 | Citizen-services navigator | Base | [Azure Search + OpenAI C# RAG app](https://github.com/Azure-Samples/azure-search-openai-demo-csharp) | [Vercel AI SDK RAG starter](https://github.com/vercel/ai-sdk-rag-starter) |
| 106 | Immigration-document organizer | Base | [Azure Search + OpenAI C# RAG app](https://github.com/Azure-Samples/azure-search-openai-demo-csharp) | [Vercel AI SDK RAG starter](https://github.com/vercel/ai-sdk-rag-starter) |
| 107 | Consumer complaint assistant | Adjacent | [eShopSupport](https://github.com/dotnet/eShopSupport) | [LangGraph customer-support workflow](https://github.com/langchain-ai/langgraph/tree/main/examples/customer-support) |

## Additional LangChain and Vercel repositories used

- [LangChain deployment cookbook](https://github.com/langchain-ai/deployment-cookbook) — production full-stack agent deployment patterns with streaming, threads, subagents and persistence.
- [LangGraph customer-support workflow](https://github.com/langchain-ai/langgraph/tree/main/examples/customer-support) — support routing, tools and workflow patterns.
- [LangGraph generative-UI examples](https://github.com/langchain-ai/langgraphjs-gen-ui-examples) — travel, restaurant, stock and pizza UI examples; repository is archived, so use as a reference rather than a new dependency.
- [LangGraph auth and payments app](https://github.com/langchain-ai/agent-auth-payments) — authentication, Stripe subscriptions and request credits; repository is archived.
- [Vercel AI Chatbot](https://github.com/vercel/chatbot) — Next.js AI SDK application with authentication, persistence, files and multiple model providers.
- [Vercel AI SDK RAG starter](https://github.com/vercel/ai-sdk-rag-starter) — Next.js, Postgres/pgvector and knowledge-grounded chat.
- [Vercel semantic image search](https://github.com/vercel-labs/semantic-image-search) — multimodal metadata, embeddings, pgvector and image storage.
- [Vercel AI SDK image generator](https://github.com/vercel-labs/ai-sdk-image-generator) — multi-provider image generation application.
- [Vercel AI Facts](https://github.com/vercel-labs/ai-facts) — real-time voice transcription and fact checking.

## Core repositories used

- **Exact:** [Fashion Assistant with Foundry agents](https://github.com/Azure-Samples/app-service-aspire-eshop-agents)
- **Adjacent:** [eShopLite reference apps](https://github.com/Azure-Samples/eShopLite)
- **Adjacent:** [Garden Shop AI Chat](https://github.com/dotnet/maui-labs/tree/main/samples/AIExtensions.Sample.Garden)
- **Adjacent:** [eShopSupport](https://github.com/dotnet/eShopSupport)
- **Base:** [Agentic App Service CRUD and tool-calling app](https://github.com/Azure-Samples/app-service-agentic-semantic-kernel-ai-foundry-agent)
- **Base:** [Getting Started with Foundry Agents and RAG](https://github.com/Azure-Samples/get-started-with-ai-agents)
- **Adjacent:** [Pizza Ordering Agent with Foundry and MCP](https://github.com/microsoft/ignite25-LAB571-build-a-pizza-ordering-agent-with-microsoft-foundry-and-mcp)
- **Exact:** [Multi-agent Travel Planner](https://github.com/Azure-Samples/app-service-maf-openai-travel-agent-dotnet)
- **Base:** [Multi-Agent Orchestration Workshop](https://github.com/Azure-Samples/multi-agent-orchestration-workshop)
- **Base:** [C# vision chat application](https://github.com/Azure-Samples/ai-chat-vision-quickstart-csharp)
- **Base:** [Azure Search + OpenAI C# RAG app](https://github.com/Azure-Samples/azure-search-openai-demo-csharp)
- **Adjacent:** [Healthcare Agent Orchestrator](https://github.com/Azure-Samples/healthcare-agent-orchestrator)
- **Adjacent:** [Student–Teacher agent workflow](https://github.com/microsoft/agent-framework/tree/main/python/samples/03-workflows/declarative/student_teacher)
