# WorkTwin: The Digital Human Double 🧠

**Status:** MVP Phase | **Architecture:** Event-driven Microservices

WorkTwin is a "Digital Twin" system that mimics your professional persona. It doesn't just search; it analyzes your communication DNA (style, emoji use, technical vocabulary) to act as a high-fidelity proxy in Slack or Telegram.

---

## 🛠 Tech Stack

* FastAPI: Async entry point for the Inference API.
* PostgreSQL + PGVector: Unified storage for relational data and high-dimensional vectors (1536 dims).
* SQLAlchemy 2.0: Shared ORM models for data consistency across services.
* LangGraph: Orchestration of the agentic "Knowledge Gating" loop.
* RabbitMQ: Orchestrates the sync lifecycle (START_SYNC -> SYNC_COMPLETE).
* Redis: Caching "Style Profiles" for sub-100ms persona loading.
* Alembic: Single-point database migration management.

---

## 🏗 System Architecture

The project is split into two independent services communicating via **RabbitMQ** (Signals) and **PostgreSQL** (Shared Knowledge).

1. 📥 **Perceiver Service (The Student)**
* Role: Scans historical data, extracts "Style Markers," and populates the brain.
* Tech: Python, Celery, Redis, SQLAlchemy.
* Core Logic: Batch processing of message history -> Sentiment & Style Analysis -> Vector Indexing.

2. 🧠 **Inference Engine (The Double)**
* Role: The real-time reasoning core. Decision-making via LangGraph.
* Tech: FastAPI, LangGraph, LangChain, PGVector.
* Core Logic: State-machine RAG (Retrieve -> Score -> Mimic -> Respond/Escalate).

---

## 🚦 Getting Started

1. **Clone & Setup**:
```bash
git clone https://github.com/AlBazaroff/work-twin
cd work-twin
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

```


2. **Infrastructure**:
```bash
docker-compose up -d

```


3. **Database**:
```bash
alembic upgrade head

```
