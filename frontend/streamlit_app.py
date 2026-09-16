import streamlit as st
import requests
import os

st.set_page_config(
    page_title="Enterprise Jarvis | AI Knowledge Assistant",
    page_icon="🛡️",
    layout="wide"
)

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Sidebar
with st.sidebar:
    st.title("🛡️ Enterprise Jarvis")
    st.markdown("**Internal Enterprise Knowledge Assistant**")
    st.markdown("---")

    # Backend health check
    try:
        health_resp = requests.get(f"{BACKEND_URL}/health", timeout=2)
        if health_resp.status_code == 200:
            st.success("🟢 Backend Connected (Healthy)")
        else:
            st.warning("🟡 Backend Degraded")
    except Exception:
        st.error("🔴 Backend Disconnected (Start API on port 8000)")

    st.markdown("---")
    st.subheader("System Information")
    st.markdown("""
    - **Architecture**: RAG (Retrieval-Augmented)
    - **Embeddings**: `all-MiniLM-L6-v2` (384-dim)
    - **Vector Store**: Pinecone Serverless / In-Memory Fallback
    - **Governance**: Zero Data Egress / RBAC
    """)

    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.title("🤖 Enterprise Jarvis Assistant")
st.caption("Ask questions grounded strictly in organizational knowledge bases and verified documentation.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am Enterprise Jarvis. How can I assist you with company policies, architecture, or internal documentation today?"}
    ]

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Quick prompt suggestions
col1, col2, col3 = st.columns(3)
quick_prompt = None
if col1.button("📋 What is Jarvis?", use_container_width=True):
    quick_prompt = "What is Jarvis and what is its primary objective?"
if col2.button("🔒 Data Privacy & Security", use_container_width=True):
    quick_prompt = "How does Jarvis ensure data privacy and prevent data egress?"
if col3.button("🧠 Hallucination Prevention", use_container_width=True):
    quick_prompt = "How does the retrieval-augmented generation pipeline eliminate hallucinations?"

user_query = st.chat_input("Type your question regarding enterprise knowledge...")
query_to_send = user_query or quick_prompt

if query_to_send:
    # Add user message to state
    st.session_state.messages.append({"role": "user", "content": query_to_send})
    with st.chat_message("user"):
        st.markdown(query_to_send)

    with st.chat_message("assistant"):
        with st.spinner("Retrieving verified enterprise context..."):
            try:
                res = requests.post(
                    f"{BACKEND_URL}/api/chat",
                    json={"query": query_to_send},
                    timeout=10
                )
                if res.status_code == 200:
                    answer = res.json().get("response", "No response received.")
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    err_msg = f"API Error ({res.status_code}): {res.text}"
                    st.error(err_msg)
            except Exception as e:
                st.error(f"Failed to communicate with Jarvis backend: {e}")
