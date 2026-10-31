# Context OS Architecture

## Product intent

Context OS is a multi-tenant AI workspace for maintaining project knowledge, recording
decisions, and detecting conflicts between new information and existing project direction.
AI may propose and explain a conflict, but it must not silently rewrite an accepted decision.
Material changes enter a human review workflow with source evidence.

## Domain hierarchy

```text
User <-> WorkspaceMembership <-> Workspace
                                  |
                                  +-- Project
                                      |-- Document
                                      |-- Note
                                      |-- Decision
                                      |-- Conversation
                                      |-- ConflictReview
```

A user may belong to multiple workspaces. For the MVP, workspace membership grants access
to every project and document within that workspace. Project-specific membership and
document-specific sharing are intentionally deferred.

## Non-negotiable invariants

1. `workspace_id` is the tenant boundary. Every tenant-owned record must be traceable to one
   workspace, either directly or through a parent whose workspace is verified in the same
   operation.
2. Repository queries for tenant-owned data must include workspace scope. A resource ID by
   itself is not sufficient authorization.
3. Authentication identifies the user; workspace membership authorizes tenant access. These
   are separate checks.
4. Retrieval is scoped to a project within the authorized workspace. Evidence from another
   project or workspace must never enter a response.
5. AI output is untrusted application input. Structured output must be validated before it is
   persisted or shown as a detected conflict.
6. Accepted decisions are immutable history. A material change creates a review record and,
   after approval, a new decision revision or superseding decision.
7. Conflict findings retain evidence references, model/provider metadata, and review outcome
   so the result is auditable.

## Core modules

- **Identity and access**: users, authentication, workspace memberships, and roles.
- **Workspaces**: tenant settings and membership administration.
- **Projects**: retrieval and organization boundary inside a workspace.
- **Knowledge**: documents, notes, ingestion state, chunks, and source metadata.
- **Decisions**: accepted project decisions and their revision history.
- **Conversations**: user questions, assistant answers, and citations.
- **Conflict review**: candidate conflicts, evidence, severity, review state, and resolution.
- **AI services**: provider-neutral embedding, retrieval, generation, and conflict-detection
  interfaces. Domain services depend on these interfaces, not provider SDKs.

## Conflict-review lifecycle

```text
new content
    -> ingest and index
    -> retrieve relevant accepted decisions
    -> detect candidate contradiction
    -> validate structured finding and evidence
    -> pending human review
       -> dismissed
       -> accepted -> superseding decision/revision
```

The finding should explain the new claim, the existing decision it may contradict, why the
change is material, and the exact sources supporting both sides. Low-confidence or
insufficiently evidenced findings must not be represented as confirmed conflicts.

## Layer responsibilities

- `api`: HTTP transport, request parsing, dependency wiring, and response mapping.
- `schemas`: validated API and AI boundary objects.
- `services`: use cases and business rules; no FastAPI or provider-specific behavior.
- `repositories`: persistence interfaces and SQLAlchemy implementations.
- `models`: database mappings and persistence constraints.
- `core`: configuration and cross-cutting infrastructure.

Route handlers should remain thin. Services orchestrate use cases through injected
interfaces, repositories enforce scoped data access, and database constraints protect the
invariants that can be expressed relationally.

## Delivery sequence

1. Establish PostgreSQL migrations, UUID identifiers, timestamps, and test database support.
2. Implement users, workspaces, memberships, and tenant-scoped authorization tests.
3. Implement project CRUD through scoped repositories and services.
4. Add documents and notes with an explicit ingestion state machine.
5. Add accepted decisions and immutable decision revisions.
6. Add chunking, embeddings, and project-scoped retrieval with source citations.
7. Add conversations and evidence-grounded answers.
8. Add conflict detection and the pending/dismissed/accepted review workflow.
9. Add background jobs, observability, rate limits, and production deployment hardening.

Each slice should include tenant-isolation tests before the next tenant-owned resource is
introduced.

## Open product decisions

The supplied role definition currently specifies the Owner role only partially. Exact roles,
permissions, authentication mechanism, AI provider, vector store, and deployment target must
be recorded as explicit decisions before their dependent implementation is finalized.
