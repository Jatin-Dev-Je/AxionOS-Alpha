# AxionOS – Alpha MVP PRD

## Purpose
Deliver a personal operating system that automates daily life with smart reminders, scheduling, task automation, and expense tracking, laying the foundation for the Reality Kernel.

## Problem
People live in fragmented app silos (health, finance, productivity, travel, social). Current AI is reactive; people are data‑rich but insight‑poor.

## Solution (MVP)
- Build a Digital Twin via the Personal Reality Graph (MongoDB + embeddings; optional Neo4j later)
- Learn preferences to optimize decisions
- Automate real‑world actions via integrations (calendar, email, WhatsApp, expense sources)

## User personas
- Tech enthusiast / productivity hacker
- Busy professional (calendar heavy)
- Founder/SMB operator (expenses + coordination)

## Primary use cases (Alpha)
1) Smart reminders from messages/emails (“Follow up with Alex Friday 9am”)  
2) Scheduling assistant (find slot, create calendar event, send confirmation)  
3) Task automation (capture, prioritize, daily plan)  
4) Expense tracking (parse statements/CSV, categorize, summaries)

## Core features (in scope)
- WhatsApp chat interface (Baileys)
- Calendar integration (Google Calendar read/write)
- Gmail read + draft replies (no auto‑send in Alpha)
- Expense import (CSV/Email attachment) + categories + simple reports
- Personal Reality Graph stored in MongoDB; Redis for queues/caching
- LLM reasoning: OpenAI/Anthropic via tool‑use; Scheduler & Finance agents (v0)

## Out of scope (Alpha)
- Payments execution (e.g., pay bill) → plan only
- Health wearable ingestion (Beta)
- Multi‑user network effects (Global)
- AR/neural interfaces (future)

## Integrations & permissions
- Google: Calendar (read/write, principle of least privilege), Gmail (read + compose/draft)
- WhatsApp: Baileys client (phone session)
- Slack (optional): read channels + post
- Storage: MongoDB; Redis; optional Neo4j (pilot)

## Success metrics (first 4–6 weeks)
- T1: ≥70% of reminder extractions correct (manual audit)
- T2: ≥50% of auto‑scheduled meetings accepted without edit
- T3: ≥80% expense transactions categorized correctly after 1 week of learning
- Engagement: ≥3 sessions/week/user; Retention D14 ≥40%

## Acceptance criteria by feature
- Smart reminders:  
  - Extracts reminder intent from WhatsApp/Gmail; stores normalized reminder doc  
  - Creates calendar task/event with correct time zone  
  - Sends confirmation back to user
- Scheduling:  
  - Pulls availability from Google Calendar; proposes 2–3 slots  
  - On confirmation, creates event, invites participants, includes location/meet link
- Tasks:  
  - “Capture” command stores task with priority, due date inference  
  - Daily digest summarizes top 5 tasks
- Expenses:  
  - CSV upload parses ≥95% rows; auto‑categorization baseline ≥70%  
  - Monthly summary message and CSV export

## Non‑functional requirements
- Privacy: PII redaction in prompts; opt‑out data retention; export/delete my data
- Security: OAuth least scopes; encrypted secrets; audit log of actions
- Reliability: P95 API latency < 400ms (excluding LLM); retry with idempotency keys
- Observability: structured logs, request IDs, minimal metrics

## Risks & mitigations
- API rate limits → batch, cache, exponential backoff
- LLM hallucination → tool‑former prompts, constrained outputs (Zod), user confirmation for risky actions
- Session stability (Baileys) → persistent auth store, reconnect logic

## Launch checklist
- [ ] Security review (scopes, storage, logs)
- [ ] Basic load test (100 rps for non‑LLM routes)
- [ ] QA scripts for the 4 core user journeys
