# Backend – AxionOS Alpha

This folder will host the Node.js/TypeScript backend for the MVP.

## Planned structure
```
backend/
  src/
    app.ts            # Express app bootstrap
    routes/           # REST endpoints
    services/         # domain services (tasks, reminders, expenses, events)
    agents/           # scheduler, finance (v0)
    integrations/     # google, gmail, whatsapp, slack
    queues/           # BullMQ job definitions
    db/               # Mongo models, index setup
    utils/            # logging, validation, config
  test/
  package.json
  tsconfig.json
  .env.example
```

## Key dependencies (draft)
- express, zod, pino, dotenv
- mongodb, mongoose (or mongo driver)
- ioredis, bullmq
- openai, anthopic (choose one to start), langchain (optional lightweight tools)
- googleapis, baileys, @slack/web-api
- jest/uvu + ts-jest/esbuild-jest

## Dev tasks (next)
- Initialize Node/TS project
- Add health endpoint and basic route skeletons
- Wire MongoDB + Redis
- Add WhatsApp (Baileys) echo bot with persistent store
- Add Google Calendar read, then write

See `../docs` for PRD and architecture.
