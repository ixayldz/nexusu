# Nexus

Nexus is a FastAPI-based platform that chains multiple LLM-powered agents (Planner → Builder → Tester) and orchestrates them with an asynchronous Job Manager & Server-Sent Events (SSE) event bus.

## Progress Log

_Last updated: 2025-08-06_

### Project Overview

The platform coordinates three agents and provides endpoints for planning, building, testing, and job tracking. The reference test suite acts as acceptance criteria.

### Timeline & Milestones

| Step | Tag   | Highlights | Tests |
|------|-------|------------|-------|
| 3.1 – Skeleton | v0.1.0 | Project scaffolding, settings & logging, health/version endpoints. | ✅ 11/11 |
| 3.2 – Builder Agent | v0.2.0 | BuilderAgent, artefact writing, `/tasks/build`, async job queue skeleton. | ✅ 13/13 |
| 3.3 – Model Selection & LLM Stub | v0.3.0 | Dynamic model map, stubbed provider layer, env switch (`ENABLE_LIVE_LLM`). | ✅ 14/14 |
| 3.4a – Planner Agent | v0.4.0 | PlannerAgent, plan cache (Redis), invalid JSON guard, `/tasks/plan`. | ✅ 17/17 |
| 3.4b – Tester Agent | v0.4.1 | TesterAgent, dynamic pytest generation, `/tasks/test`. | ✅ 17/17 |
| 3.4c – Job Manager & SSE | v0.5.0 | Job orchestration, in-memory store, background tasks, Jobs API + SSE stream. | ✅ 18/18 |

**Current status:** All reference tests pass locally (`pytest -q → 18 passed`).

### Implemented Components

1. **Core**
   - `settings.py` – Pydantic-based config with `.env` overrides.
   - `logging.py` – Colourised structured logs.
   - `model_selector.py` – Central map to `select_model(AgentType)`.
   - `job_manager.py` – Job scheduling, in-memory registry, and SSE pub/sub bus.

2. **Agents**
   - `PlannerAgent` – Converts natural-language specs into ordered JSON plans.
   - `BuilderAgent` – Generates and writes code artefacts from plan steps.
   - `TesterAgent` – Produces pytest files and executes them in sandbox.

3. **Routers**
   - `/tasks` – Plan, build, and test endpoints that enqueue jobs.
   - `/jobs` – Fetch job status.
   - `/jobs/{id}/events` – SSE stream (byte-encoded lines).
   - `/health` & `/version` – Metadata endpoints.

4. **Providers**
   - Stubbed `call_openai`, `call_claude`, `call_gemini` with live toggle.

### Testing & Quality Gate

All acceptance tests located under `app/tests` currently succeed. A pydantic-core serialization bug was resolved by omitting the private `_task` field in job serialization. The event stream conforms to SSE expectations.

### Next Up

- Persistence layer – optional Redis/DB toggle instead of in-memory.
- Auth & rate-limit middleware for multi-tenant usage.
- LLM live mode – integrate real API keys.
- CI pipeline – GitHub Actions for lint and tests.
- Frontend – minimal React dashboard consuming the SSE.

## Development

To run the test suite:

```bash
pip install -r requirements-dev.txt
pytest -q
```

