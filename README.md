# Context OS Backend

Context OS is a multi-tenant AI workspace that helps teams organize project knowledge,
record important decisions, and ask questions across their documents and notes. Content is
organized by workspace and project, with each workspace acting as an isolated tenant boundary.

Its central feature is conflict-aware assistance. When new information may contradict an
existing project decision, the AI explains the potential conflict with supporting source
evidence and sends material changes for human review instead of silently changing the project
plan.

This backend is a production-minded FastAPI application supporting the Context OS API,
knowledge retrieval, decision tracking, conversations, and the conflict-review workflow.

## Development

```bash
uv sync --dev
uv run uvicorn app.main:app --reload
```

API documentation is available at `http://127.0.0.1:8000/docs`.

Copy `.env.example` to `.env` to override the default configuration.

See [docs/architecture.md](docs/architecture.md) for the product boundaries, tenant-safety
invariants, conflict-review lifecycle, and implementation sequence.
