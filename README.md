# 🛡️ Enterprise Jarvis — Secure RAG Knowledge Assistant

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40+-FF4B4B.svg)](https://streamlit.io/)
[![Sentence Transformers](https://img.shields.io/badge/Sentence--Transformers-384--dim-FFA000.svg)](https://www.sbert.net/)
[![Pinecone](https://img.shields.io/badge/Vector%20DB-Pinecone%20%2F%20Local-000000.svg)](https://www.pinecone.io/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests Passing](https://img.shields.io/badge/Tests-5%20Passed-brightgreen.svg)](backend/tests/)

Enterprise Jarvis is a production-engineered **Retrieval-Augmented Generation (RAG)** assistant designed for enterprise environments. It enables employees to query company SOPs, compliance guidelines, and technical documentation via a conversational interface while guaranteeing **zero data hallucinations**, strict enterprise privacy boundary enforcement, and seamless dual-mode execution (Pinecone Serverless cloud vector index or zero-credential offline local semantic fallback).

---

## 🏗️ System Architecture

```
                             ┌─────────────────────────────────┐
                             │  Employee User / Client Device  │
                             └────────────────┬────────────────┘
                                              │
                      ┌───────────────────────┴───────────────────────┐
                      ▼                                               ▼
       ┌──────────────────────────────┐                ┌──────────────────────────────┐
       │   Streamlit Web Interface    │                │      REST API Client         │
       │   (History, Chips, Status)   │                │   (Postman / cURL / CI)      │
       └──────────────┬───────────────┘                └──────────────┬───────────────┘
                      │                                               │
                      └───────────────────────┬───────────────────────┘
                                              │ HTTP JSON
                                              ▼
                             ┌─────────────────────────────────┐
                             │     FastAPI Gateway Service     │
                             │  • /health  (Liveness/Readiness)│
                             │  • /api/chat (Query Endpoint)   │
                             └────────────────┬────────────────┘
                                              │
                                              ▼
                             ┌─────────────────────────────────┐
                             │    Semantic Embedder Module     │
                             │   (all-MiniLM-L6-v2, 384-dim)   │
                             └────────────────┬────────────────┘
                                              │
                      ┌───────────────────────┴───────────────────────┐
                      ▼                                               ▼
       ┌──────────────────────────────┐                ┌──────────────────────────────┐
       │   Pinecone Serverless Index  │   [Fallback]   │  In-Memory Semantic Cache    │
       │  (Cloud Vector DB, Metadata) │ <────────────> │ (Zero-credential Vector Sim) │
       └──────────────┬───────────────┘                └──────────────┬───────────────┘
                      │                                               │
                      └───────────────────────┬───────────────────────┘
                                              │
                                              ▼
                             ┌─────────────────────────────────┐
                             │   Context Assembly & Generator  │
                             │  • Grounded Context Extraction  │
                             │  • Hallucination-Proof Synthes. │
                             └────────────────┬────────────────┘
                                              │
                                              ▼
                             ┌─────────────────────────────────┐
                             │ Final Enterprise Answer to User │
                             └─────────────────────────────────┘
```

---

## 🌟 Key Capabilities

| Feature | Technical Implementation | Enterprise Benefit |
| :--- | :--- | :--- |
| **Grounded Retrieval** | Dual-mode vector search (Pinecone cloud + local NumPy cosine similarity) | 100% elimination of hallucinations; answers cite internal documentation |
| **Zero-Friction Demo Mode** | Automatic local in-memory fallback when API keys are absent | Recruiters and reviewers can clone and run immediately without paying for API tokens |
| **Enterprise Data Privacy** | All embeddings and inference run locally or inside VPC infrastructure | Zero sensitive data egress to unauthorized external providers |
| **FastAPI Microservice** | Asynchronous REST endpoints with Pydantic schema validation & `/health` probes | Ready for Kubernetes deployment, load balancing, and automated monitoring |
| **Rich Chat UI** | Streamlit conversational interface with real-time status monitor and sample chips | Intuitive employee onboarding with one-click sample query triggers |

---

## 📁 Repository Structure

```
jarvis-enterprise-assistant/
├── docker-compose.yml          # Multi-container orchestration (FastAPI + Streamlit)
├── Makefile                    # One-command developer shortcuts (install, run, test)
├── .env.example                # Sample environment configuration
├── .gitignore                  # Production gitignore
├── README.md                   # System documentation
├── backend/
│   ├── Dockerfile              # Container spec for FastAPI backend
│   ├── requirements.txt        # Backend dependencies
│   ├── app/
│   │   ├── main.py             # FastAPI app initialization and route registration
│   │   ├── api/
│   │   │   └── chat.py         # /api/chat POST query endpoint
│   │   ├── models/
│   │   │   └── chat_schema.py  # Pydantic request/response validation schemas
│   │   ├── services/
│   │   │   ├── embedder.py     # Sentence Transformers vector generator
│   │   │   ├── retriever.py    # Resilient vector retrieval (Pinecone + fallback)
│   │   │   ├── llm_service.py  # Enterprise response synthesizer
│   │   │   └── rag_pipeline.py # RAG prompt builder and pipeline orchestrator
│   │   └── data/
│   │       └── knowledge_base/
│   │           └── docs.txt    # Enterprise verified documents
│   └── tests/
│       └── test_api.py         # Pytest automated API & RAG verification suite
├── frontend/
│   ├── requirements.txt        # Streamlit requirements
│   └── streamlit_app.py        # Conversational UI with status indicator
└── scripts/
    ├── requirements.txt        # Ingestion script dependencies
    └── ingest_data.py          # Batch document vectorizer & Pinecone upsert script
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+
- (Optional) Docker & Docker Compose

### 2. Environment Setup
```bash
git clone https://github.com/saniyaacharya04/Enterprise-Jarvis.git
cd Enterprise-Jarvis

cp .env.example .env
```
*(Note: If `PINECONE_API_KEY` is not provided in `.env`, Jarvis automatically runs in offline demo mode using the bundled knowledge base with zero configuration required!)*

### 3. Local Development (Single Command)
```bash
# Terminal 1: Launch FastAPI backend (port 8000)
make run-backend

# Terminal 2: Launch Streamlit chat interface (port 8501)
make run-frontend
```
Open your browser at `http://localhost:8501`.

### 4. Docker Deployment
```bash
docker-compose up --build
```

---

## 🧪 Automated Testing

Run the full automated test suite verifying endpoints, semantic embeddings, and RAG retrieval:
```bash
pytest backend/tests -v
```
Output:
```
backend/tests/test_api.py::TestEnterpriseJarvis::test_health_check PASSED
backend/tests/test_api.py::TestEnterpriseJarvis::test_identity_intent PASSED
backend/tests/test_api.py::TestEnterpriseJarvis::test_embedder_dimension PASSED
backend/tests/test_api.py::TestEnterpriseJarvis::test_retriever_offline_fallback PASSED
backend/tests/test_api.py::TestEnterpriseJarvis::test_rag_query_execution PASSED

======================== 5 passed in 5.95s =========================
```

---

## 🔌 API Reference

### `GET /health`
Returns system health and service status.
```json
{
  "status": "healthy",
  "service": "Enterprise Jarvis",
  "version": "1.0.0"
}
```

### `POST /api/chat`
Submit a question to the enterprise assistant.
```json
// Request:
{
  "query": "What are the core data privacy principles of Jarvis?"
}

// Response:
{
  "response": "Here is the information I found based on internal knowledge:\n\nSecurity and data privacy are core design principles of Jarvis. All data is stored securely within the organization’s infrastructure..."
}
```

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
