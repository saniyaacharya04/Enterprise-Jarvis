import streamlit as st
import requests

st.title("Enterprise Jarvis")

query = st.text_input("Ask your assistant")

if query:
    res = requests.post(
        "http://localhost:8000/api/chat",
        json={"query": query}
    )
    st.success(res.json()["response"])
