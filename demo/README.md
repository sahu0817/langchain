## langsmith-frontend

Role: UI and HTTPS entrypoint for LangSmith.

- Serves the web UI (traces, datasets, evals, monitors, agent builder, etc.).
- Terminates user HTTP(S) and forwards API calls to the appropriate backends (langsmith-backend, langsmith-platform-backend, langsmith-playground, langsmith-ace-backend).
- Handles browser sessions, auth flows (in conjunction with the backends), and streaming connections for live trace views.

Think of this as “the thing behind your load balancer” that users directly hit.

## langsmith-backend

Role: Read / query API and general app logic. Primarily responsible for serving data back to the UI and SDKs:

- Implements most of the REST/GraphQL-ish API the UI calls to:
- List and fetch traces / runs (read path from ClickHouse via the queue pipeline’s writes).
- Manage projects, datasets, experiments, eval results, feedback, etc. (metadata from Postgres).

Powers dashboards, filters, search, and drill‑downs over stored traces and evaluation results. 
 
## langsmith-platform-backend

Role: Write / ingest API and platform‑level operations.

This is the main ingestion and control-plane service:

- Receives trace and event data from the LangSmith SDKs and integrations (Python/TypeScript).
- Implements organization / tenant, auth, licensing, and other platform‑level APIs. - 
- Accepts trace / run payloads from clients.
- Pushes them into Redis for asynchronous processing by the queue workers.
- This is the first hop in the trace ingestion pipeline before Redis and the queue workers. 

You can think of this as the “public write API + control plane.”

## langsmith-ingest-queue

Role: Specialized worker(s) for trace ingestion.

- platform-backend puts trace jobs into Redis.
- A queue service consumes those jobs and persists them to ClickHouse (traces) and Postgres (metadata). 
- langsmith-ingest-queue focuses on high‑volume ingest jobs (parsing, normalizing, and writing trace records and associated metadata).
- This keeps ingestion isolated from other background work so you can scale it independently (more replicas for heavy write traffic).
- This is “workers that turn raw trace events from Redis into stored rows in ClickHouse/Postgres.”

## langsmith-queue

Role: General-purpose background worker service.

- Implements the “queue service” that processes jobs from Redis and writes to storage. 
- andles asynchronous tasks beyond pure ingestion, for example:
  - Running evaluations / experiments in the background.
  - Aggregating metrics, computing rollups for dashboards.
  - Processing feedback, alerts, notifications, and other non‑interactive jobs. 

ℹ️  langsmith-ingest-queue is tuned for ingest, langsmith-queue is the more general async worker layer.

## langsmith-playground

Role: Backend for the LangSmith Playground experience.

- Powers the in‑browser playground for trying prompts, models, and settings interactively. 
- Talks to configured LLM providers / model backends and returns responses to the frontend.
- Can log playground runs into the same observability pipeline so they appear as traces.
- This is effectively a “sandbox LLM runner” that the UI calls when you use the playground tab.

## langsmith-ace-backend

Role: Secure Arbitrary Code Execution (ACE) service.

- Executes user-defined code in a controlled environment:
- Custom evaluators and scoring functions.
- Data preprocessing / postprocessing logic tied to evals or datasets.
- Other snippets exposed through the UI as “run this code as part of an evaluation or pipeline.” 
- Isolated from the main backend for security and stability—if user code crashes or misbehaves, it doesn’t take down the primary APIs.
- In short: this is the sandbox that runs “your code” for advanced evaluation and transformations.

# Storage Services

## langsmith-postgres

Role: Primary relational database.

- Stores transactional and metadata, not high‑volume traces:
  - Tenants, users, auth data.
  - Projects, datasets, experiments, eval definitions.
  - Thread/assistant metadata for the agent server, cron jobs, etc. 
  - Docs recommend using an external managed Postgres in production rather than the in‑cluster StatefulSet. 

## langsmith-redis

Role: Cache + job broker.

- Serves as the message broker between producers and workers:
  - langsmith-platform-backend (and possibly langsmith-backend or others) enqueue jobs.
  - langsmith-ingest-queue and langsmith-queue consume jobs.
- Also used as a cache for frequently accessed metadata and session‑like data to offload Postgres and speed up common queries. 
 
Serves as the message broker between producers and workers:
langsmith-platform-backend (and possibly langsmith-backend or others) enqueue jobs.
langsmith-ingest-queue and langsmith-queue consume jobs.
May also act as a cache for frequently accessed metadata, rate limiting, or ephemeral state, reducing load on Postgres and improving latency.

## langsmith-clickhouse

Role: Columnar analytics store for traces (OLAP).

- Primary storage for high‑volume, append‑heavy trace data:
  - Runs, spans, tokens, intermediate LLM calls, nested tools, etc.
  - Metrics related to latency, token counts, costs, error codes, etc.
- Optimized for analytical queries:
  - Filtering and aggregating traces for dashboards and insights.
  - Time‑series queries (latency over time, error rates, cost by model).
  - Drill‑downs into specific runs while still supporting large volumes.
- The write path:
  - langsmith-platform-backend → langsmith-redis → langsmith-ingest-queue / langsmith-queue → write to ClickHouse.
- The read path:
  - langsmith-backend queries ClickHouse to serve trace and metrics data to the frontend.

This is the observability warehouse for LangSmith.
