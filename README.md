# WorkTwin: The Digital Human Double 🧠

**Status:** MVP Phase | **Architecture:** Event-driven Microservices

WorkTwin is a "Digital Twin" system that mimics your professional persona. It doesn't just search; it analyzes your communication DNA (style, emoji use, technical vocabulary) to act as a high-fidelity proxy in Slack or Telegram.

---

## 🛠 Tech Stack

* FastAPI: Async entry point for the Perceiver API.
* PostgreSQL + PGVector: Unified storage for relational data and high-dimensional vectors (1536 dims).
* SQLAlchemy 2.0: Shared ORM models for data consistency across services.
* LangGraph: Orchestration of the agentic "Knowledge Gating" loop.
* RabbitMQ: Orchestrates the sync lifecycle (START_SYNC -> SYNC_COMPLETE).
* Redis: Caching "Style Profiles" for sub-100ms persona loading.
* Alembic: Single-point database migration management.

---

## 🏗 System Architecture

It's a microservice via **RabbitMQ** (Signals) and endpoint on **FastAPI**.

1. 📥 **Perceiver Service (The Student)**
* Role: Scans historical data, extracts "Style Markers," and populates the brain.
* Tech: Python, Celery, Redis, SQLAlchemy, FastAPI.
* Core Logic: 
    - Batch processing of message history -> Sentiment & Style Analysis -> Vector Indexing & Creating Profiles.
    - Receive request from inference service -> Find profile & Attach appropriate context -> Response.

---

## 🚦 Getting Started

1. **Clone & Setup**:
```bash
git clone https://github.com/AlBazaroff/work-twin
cd work-twin
uv sync

```


2. **Infrastructure**:
```bash
docker-compose up -d

```


3. **Database**:
```bash
alembic upgrade head

```
