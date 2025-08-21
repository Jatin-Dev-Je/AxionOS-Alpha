# System Architecture – AxionOS Alpha

## Overview
Alpha focuses on four pillars: sensing/integration, personal reality graph, AI core, and execution engine; surfaced via WhatsApp and a forthcoming web dashboard.

## Components
- API Gateway (Express, TypeScript)
- Ingestion services (webhooks, pollers): Gmail, Google Calendar, WhatsApp (Baileys), Slack (opt)
- Queues: Redis + BullMQ (jobs: ingest, classify, embed, act)
- Data stores: MongoDB (primary), Redis (cache/queue), optional Neo4j (relations)
- AI Core: LLM tools + lightweight agents (Scheduler, Finance); embeddings (OpenAI/Local)
- Execution Adapters: Google Calendar, Gmail drafts, Slack messages, WhatsApp replies
- Observability: structured logs (pino), metrics (basic), audit log

## Data model (MongoDB, draft)
- users: { _id, identity, oauth, prefs, timezone }
- messages: { _id, userId, source, text, ts, threadId, embeddings[], labels[] }
- tasks: { _id, userId, title, due, priority, status, sourceRef }
- reminders: { _id, userId, title, when, tz, location?, attendees?, sourceRef }
- expenses: { _id, userId, date, merchant, amount, currency, category, source }
- events: { _id, userId, providerId, attendees[], status, sourceRef }
- audit: { _id, userId, action, payloadHash, ts, status }

## Key flows
1) Message → Reminder  
   - Ingest message (WhatsApp/Gmail) → queue → classify (intent) → extract entities → create reminder/task → optional calendar event → notify user
2) Scheduling  
   - Gather availability → propose slots → confirm → create event → send invites → write back to chat
3) Expense CSV  
   - Upload → parse → normalize → categorize (model + rules) → store → summary

## Agent orchestration
- Orchestrator routes intents to tools/agents (scheduler, finance).  
- Tools return typed outputs validated by Zod; high‑risk actions require explicit user confirmation.

## Prompts & safety
- Use system prompts with explicit tool schemas; short context windows with retrieval (embeddings)
- Redact PII where possible; never echo secrets; store only hashes for auth tokens where feasible

## API surface (draft)
- REST: /health, /webhooks/*, /users/*, /tasks, /reminders, /expenses, /events
- Webhooks: WhatsApp, Gmail (watch/push or poller), Calendar events

## Configuration
- ENV: MONGODB_URI, REDIS_URL, OPENAI_API_KEY/ANTHROPIC_API_KEY, GOOGLE_OAUTH_*, WHATSAPP_STORE_PATH, JWT_SECRET
- Secrets via .env (dev) and secret manager (prod)

## Deployment (later)
- Containerized services; single service in Alpha, split as needed in Beta
- GitHub Actions for lint/test/build; Railway/Render/Vercel/Cloud Run for hosting

## Limitations (Alpha)
- Single‑user tenancy per workspace; simple RBAC later
- Optional Neo4j gated behind feature flag
