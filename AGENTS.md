# Development instructions for LLM Agents

This document provides essential guidance for AI agents contributing to the Work Twin Perceiver Service.

---

## Purpose

This file is the primary operating manual for AI agents working in this repository.

It should give the agent enough context to:

- understand what the project does;
- follow the correct architecture and conventions;
- place code in the right directories;
- run the right commands for setup, validation, and testing;
- avoid unsafe or low-quality changes;
- know when to stop and ask a human.

If this file is vague, outdated, or contradictory, agent output will degrade. Keep it specific.

---

## Project Snapshot

- Project name: Work Twin Perceiver
- Project type: service
- One-line description: Perceive user's integrations, analyze and prepare data to use them in requests from inference service
- Primary users: Business clients like managers, who chatting, planning a lot of time
- Business/domain context: B2B/B2C
- Lifecycle stage: MVP
- Maintainers / owning team: Alexander Bazarov
- Default branch: main
- Repo status notes: none

---

## Agent Principles

Unless the user explicitly asks otherwise, the agent should:

- prefer the smallest safe change that solves the task;
- preserve existing architecture and naming conventions;
- update tests when behavior changes;
- update docs, config, or examples when they become stale because of the change;
- verify work before finishing;
- avoid speculative refactors;
- ask before destructive, irreversible, expensive, or production-affecting operations.

### Optimize For

1. Correctness
2. Maintainability
3. Speed

### Never Do These By Default

- Rewrite architecture without being asked.
- Introduce a new dependency when an existing project dependency can solve the problem.
- Manually edit generated files if the intended workflow is regeneration.
- Ignore failing checks related to the files or behavior you changed.
- Guess around security-sensitive, billing-sensitive, or compliance-sensitive behavior.

---

## Tech Stack

### Core Stack

- Language(s): Python 3.12
- Runtime(s): python:3.12-slim-trixie
- Framework(s): FastAPI 0.136, Pydantic 2.13, SQLAlchemy 2.0, Alembic 1.18, Langchain 1.2.15, Langgraph 1.1.9
- Package manager(s): uv 0.10.4
- Build tool(s): Docker Compose
- Database(s): PostgreSQL 18 + pgvector
- Messaging / queueing: RabbitMQ 3.13
- Cache / storage: Redis 7

### Key Libraries And Services

List the important tools the agent should recognize immediately:

| Area | Library / Service | Version | Purpose | Notes / Constraints |
| --- | --- | --- | --- | --- |
| Backend(Scraping) | Telethon | 1.43.2 | ASync connection to TelegramAPI | Prone to strict limit management |
| Data Validation | Pydantic | 2.13 | Validate incoming DTO, configuration and strict typing JSON-contracts between services | Use syntax V2, not compatible with V1 |
| Database | SQLAlchemy | 2.0 | Describe schemas and async interaction with PostgreSQL | Only AsyncIO Sessions |
| AI (Orchestration) | LangGraph | 1.1.9 | Build cycling graphs for cognitive ETL, parsing and generate AI answers | Graph state must be strictly serializable for saving in memory or Redis |
| Async Tasks | Celery | 5.6.3 | Background processing heavy tasks, chunking, send embedding, generate reports | Works with RabbitMQ. Tasks should be idempotent |
| Testing | Pytest | 9.0.3 | Automating testing business logic and integrative scenarios | Should pytest-asyncio for testing async endpoints and SQLAlchemy sessions |

### Version Policy

- Required versions: Strict ranges from pyproject.toml
- Version source of truth: pyproject.toml
- Dependency update policy: manual
- Compatibility requirements:
   - Runtime: CPython 3.12
   - DB Compatibility: Alembic schemas must be compatibility with PostgreSQL 18 and pgvector

---

## Architecture

- Architecture style: Event-driven microservice (ETL-focused)
- High-level description: Each domain operations owns its logic, routes, domain rules
- Main modules / bounded contexts: analyzer, ingestion, integrations
- Main data flow: 
   - Another service(Event) -> RabbitMQ -> Celery Task -> services work -> DB/Vector Store
   - Another service(Event) -> request -> services -> response
- Hard constraints: prevent leakage credentials into logs, avoid block EventLoop at work with heavy sync operations(use Celery instead)

---

## Environment Setup

### Required Tooling

- Required tools: python 3.12, uv 0.10, Docker Desktop
- Install dependencies: uv sync
- Start local environment: source .venv/bin/activate
- Start dependent services only: docker compose up -d
- Load environment variables from: .env
- Required local services: Postgres, RabbitMQ, Redis

---

## Development Commands

Every command below should work as written.

| Task | Command | Scope | Notes |
| --- | --- | --- | --- |
| Install dependencies | `uv sync` | repo | Install dependencies using uv |
| Start development | `uv run fastapi dev main.py" | repo | Start service locally |
| Lint | `uv run ruff check` | repo | Runs linting code |
| Format | `uv run ruff format` | Repo | Runs formatting code |
| Typecheck | `uv run mypy perceiver_service/src` | repo | Check variable types |
| Run all tests | `uv run pytest` | repo | Run all existing test |
| Run one test file | `uv run pytest perceiver_service/tests/path/to/test_*.py` | package | Fastest local |
| Run one test case | `uv run pytest perceiver_service/tests/path/to/test_*.py::test_name` | case | Fastest check test case |

### Verification Strategy

The agent should usually validate changes in this order:

1. file-level or test-level checks;
2. nearest package or module checks;
3. full-repo checks when necessary;
4. release-grade checks before merge for risky or broad changes.

---

## Testing Guide

- Test framework(s): Pytest
- Test location(s): perceiver_service/tests/
- Naming pattern(s): test_*.py
- CI workflow location: .github/workflows/test.yml

### Testing Rules

- Every behavior change should be backed by tests unless there is a documented reason not to.
- Bug fixes should include a regression test when practical.
- Prefer focused tests during iteration.
- Run broader suites when changing shared code, persistence, contracts, infrastructure, or sensitive workflows.
- Snapshot or golden updates must be reviewed, not blindly accepted.

---

## Code Style And Naming

- Formatter: Ruff
- Linter: Ruff
- Type policy: Moderate
- Comments policy: In module-, class-, method-level and code's section, if something implicitly
- Import policy: Absolute and relative(if in one package)
- Error handling style: Exceptions
- Logging style: Tracing

### Naming Conventions We Prefer

| Item | Preferred | Avoid | Example |
| --- | --- | --- | --- |
| Files | snake_case | camelCase | balancing_loader.py |
| Directories | snake_case | camelCase | balancing_loader |
| Classes | UpperCamelCase | camelCase & snake_case | DocumentLoader |
| Functions / methods | snake_case | camelCase | get_id |
| Variables | snake_case | camelCase | max_price |
| Constants | UPPER_CASE | camelCase & snake_case | TIME_DELAY |
| Test methods | snake_case | camelCase | test_something |

### Style Do / Don't

Do:

- use names that reflect intent;
- keep modules cohesive and purpose-driven;
- follow established patterns already used nearby;
- prefer explicit business logic over clever abstractions.

Don't:

- create “utils” dumping grounds for unrelated logic;
- mix multiple naming styles in the same area;
- hide important side effects behind vague helper names;
- introduce broad abstractions before a second real use case exists.

---

## Security And Safety Boundaries

Treat this section as mandatory.

### Hard Rules

- Never commit secrets, private keys, access tokens, or production credentials.
- Never hardcode secrets in source code, tests, fixtures, or documentation.
- Redact sensitive values in logs and examples.
- Validate and sanitize untrusted input at the proper boundary.
- Use least privilege for database, cloud, and service credentials.
- Be extra careful in code touching auth, billing, PII, legal/compliance, infrastructure, or permissions.

### Human Approval Required Before

- deleting data or files;
- applying irreversible migrations;
- changing auth or permission logic;
- changing billing or payment flows;
- changing deployment or production infrastructure;
- installing or replacing major dependencies;
- rotating secrets or changing security configuration.

---

## Git, PR, And Definition Of Done

- Branch naming convention: feat/<short-description>
- Commit message convention: conventional commits

### Definition Of Done

A change is not complete until:

1. relevant checks pass;
2. tests are added or updated where needed;
3. docs/config/examples are updated if affected;
4. file placement and naming follow this document;
5. assumptions, risks, and follow-up work are documented.

---

## When The Agent Must Stop And Ask

The agent should pause and ask a human when:

- requirements are ambiguous and there are multiple valid implementations;
- a change may break API compatibility, data compatibility, or deployment safety;
- documentation and code materially disagree;
- tests fail for reasons unrelated to the task and the cause is unclear;
- the task requires secrets, production access, or product-policy decisions;
- the safest path depends on a tradeoff the user has not chosen.

---
