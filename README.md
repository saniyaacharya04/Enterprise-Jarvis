# Enterprise Jarvis

Enterprise Jarvis is a lightweight, enterprise-focused AI assistant designed to demonstrate **Retrieval-Augmented Generation (RAG)** for secure internal knowledge access. The system enables users to query internal documentation through a conversational interface while ensuring responses are grounded only in approved organizational data.

The project is built with a modular architecture suitable for enterprise SaaS environments and supports fast demos using a model-agnostic design.

---

## Project Objective

The goal of this project is to design and implement a personal AI assistant for the enterprise that:

* Understands natural language queries
* Retrieves relevant internal knowledge using vector search
* Responds with contextually grounded answers
* Provides a conversational chatbot interface
* Can be extended to use enterprise-approved LLMs

---

## Architecture Overview

The system follows a standard RAG architecture:

1. **User Query**
   User submits a question via a chat interface.

2. **Retrieval**
   The query is embedded and matched against internal documents stored in Pinecone.

3. **Context Assembly**
   Relevant document snippets are assembled into a prompt.

4. **Response Generation**
   A fast, model-agnostic response generator produces the final answer.

5. **Chat Interface**
   Responses are displayed to the user through a web-based UI.

---

## Tech Stack

### Backend

* Python
* FastAPI
* Pinecone (Vector Database)
* Sentence Transformers (Embeddings)

### Frontend

* Streamlit (Chat UI)

### Infrastructure

* Conda (Environment management)
* Docker / Docker Compose (Optional deployment)

---

## Project Structure

```
jarvis-enterprise-assistant/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   └── chat.py
│   │   ├── services/
│   │   │   ├── rag_pipeline.py
│   │   │   ├── retriever.py
│   │   │   ├── embedder.py
│   │   │   └── llm_service.py
│   │   ├── models/
│   │   │   └── chat_schema.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── logger.py
│   │   ├── data/
│   │   │   └── knowledge_base/
│   │   │       └── docs.txt
│   │   └── utils/
│   │       └── prompt_templates.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── streamlit_app.py
│   └── requirements.txt
│
├── scripts/
│   └── ingest_data.py
│
├── docker-compose.yml
├── README.md
└── .env
```

---

## Setup Instructions

### 1. Create and Activate Environment

```bash
conda create -n jarvis python=3.10
conda activate jarvis
```

---

### 2. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

---

### 3. Configure Environment Variables

Create a `.env` file at the project root:

```
PINECONE_API_KEY=your_api_key
PINECONE_INDEX=jarvis-knowledge
```

---

### 4. Add Knowledge Base

Place internal documentation into:

```
backend/app/data/knowledge_base/docs.txt
```

Each line or paragraph represents a knowledge chunk.

---

### 5. Ingest Data into Pinecone

```bash
python scripts/ingest_data.py
```

---

### 6. Run Backend API

```bash
cd backend
uvicorn app.main:app
```

API documentation will be available at:

```
http://127.0.0.1:8000/docs
```

---

### 7. Run Frontend Chat UI

```bash
cd frontend
streamlit run streamlit_app.py
```

---

## Example API Request

```
POST /api/chat
```

```json
{
  "query": "What information do you have access to?"
}
```

---

## Design Decisions

* **Model-Agnostic Architecture**
  The LLM layer is abstracted, allowing easy replacement with enterprise-approved models.

* **Fast Demo Mode**
  For responsiveness and local execution, the assistant returns grounded answers without large model downloads.

* **Secure-by-Design**
  The assistant only answers based on retrieved internal context, preventing hallucinations.

* **Separation of Concerns**
  API, services, ingestion, and UI layers are cleanly separated.

---

## Future Enhancements

* Plug-in enterprise LLMs (OpenAI, Azure OpenAI, private LLaMA)
* Role-based access control
* Conversation memory
* Multi-document ingestion formats
* Authentication and audit logging

---

## Conclusion

Enterprise Jarvis demonstrates a practical, enterprise-ready AI assistant using Retrieval-Augmented Generation. The project focuses on correctness, security, performance, and extensibility, making it suitable for SaaS environments and internal knowledge systems.

---

