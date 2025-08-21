# AxionOS – Alpha

Tagline: The Operating System of Reality. From Alpha to Infinity.

AxionOS – Alpha is a personal operating system that learns continuously, orchestrates daily life, and forms the kernel for civilization‑scale intelligence. This repository hosts the MVP documentation and initial scaffolding.

## MVP focus
- Smart reminders, scheduling, task automation, expense tracking
- Private, secure personal data graph ("Personal Reality Graph")
- WhatsApp chat interface first; web dashboard next
- Integrations: Google Calendar, Gmail (read), Baileys (WhatsApp), Slack (optional), expense imports; MongoDB + Redis

## Architecture (alpha)
- Sensing & Integration Layer → Ingests external data (APIs, webhooks) into MongoDB; Redis for queues/caching
- Personal Reality Graph → User-centric knowledge graph (MongoDB collections + optional Neo4j relations; embeddings for recall)
- AI Core (Reality Kernel – Alpha) → LLM reasoning, lightweight multi‑agent orchestration (Scheduler, Finance, Health placeholder), tool calling
- Execution Engine → Calls API actions (schedule meeting, set reminders, track expenses) via adapters
- Interfaces → WhatsApp bot (Baileys), Web dashboard (React/MERN)

See `docs/System-Architecture.md` and `docs/MVP-PRD.md`.

## Tech stack (provisional)
- Backend: Node.js (TypeScript), Express, MongoDB, Redis, BullMQ, Zod, OpenAI/Anthropic SDKs
- Data: MongoDB Atlas/local, optional Neo4j (beta), Redis
- Frontend: React + Vite (later), Tailwind
- Messaging: WhatsApp via Baileys; Slack app (optional)
- Infra: Docker (dev), pnpm/npm, dotenv, GitHub Actions (CI)

## Repo layout
- `backend/` – API, agents, integrations (to be scaffolded)
- `docs/` – Product and technical documentation

## Getting started (docs only for now)
- Read `docs/MVP-PRD.md` for scope and acceptance
- Read `docs/System-Architecture.md` for components and data flow
- Backend scaffolding is described in `backend/README.md`

## Security & privacy
- Local-first dev; least-privilege OAuth scopes; encryption at rest; audit logging
- Redaction + PII minimization in prompts; configurable data retention

## Roadmap
- Alpha (MVP): reminders/scheduling/tasks/expenses
- Beta: health tracking, finance optimization, multi‑agent orchestration
- Global → Prime: network effects, large‑scale orchestration

See `docs/Roadmap.md`.
