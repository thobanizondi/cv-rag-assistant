import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from retrieval_engine.rag_engine import load_all_cvs, build_vector_store, build_qa_chain

st.set_page_config(
    page_title="Thobani Zondi — CV Assistant",
    page_icon="📄",
    layout="centered"
)

st.title("📄 Thobani Zondi — CV Assistant")
st.markdown(
    "Ask me anything about Thobani's **experience**, **skills**, **certifications**, and **projects**."
)
st.divider()

@st.cache_resource(show_spinner=False)
def initialize_rag(version="llama-3.3-70b-versatile"):
    text = load_all_cvs("cv_data")
    vector_store = build_vector_store(text)
    qa_chain = build_qa_chain(vector_store)
    return qa_chain

with st.spinner("Loading CVs and building RAG pipeline — please wait..."):
    qa_chain = initialize_rag()

st.success("All CVs loaded and ready")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

suggested = [
    "What is Thobani's current role?",
    "What certifications does he hold?",
    "Describe his portfolio projects",
    "Is he a good fit for a Data Engineer role?",
    "What is his Python experience?",
    "What cloud platforms has he worked with?",
]

if not st.session_state.messages:
    st.markdown("#### Suggested Questions")
    cols = st.columns(2)
    for i, q in enumerate(suggested):
        if cols[i % 2].button(q, use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": q})
            with st.chat_message("user"):
                st.markdown(q)
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    answer = qa_chain(q)
                    st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()

if prompt := st.chat_input("Ask anything about Thobani's CV..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = qa_chain(prompt)
            st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()

st.divider()
st.markdown(
    "Built with LangChain · Groq LLaMA3 · FAISS · Streamlit | "
    "[GitHub](https://github.com/thobanizondi) · "
    "[Portfolio](https://datascienceportfol.io/thobanizondi)"
)