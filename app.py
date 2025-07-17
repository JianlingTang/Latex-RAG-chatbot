import openai
import faiss
import numpy as np
import json
import os
import streamlit as st
from dotenv import load_dotenv

# Load API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

@st.cache_resource
def load_faiss_index(index_path="index.faiss"):
    return faiss.read_index(index_path)

@st.cache_data
def load_metadata(meta_path="chunk_texts.json"):
    with open(meta_path, "r") as f:
        return json.load(f)

def embed_query(query: str) -> np.ndarray:
    response = openai.Embedding.create(
        input=query,
        model="text-embedding-3-small"
    )
    embedding = response["data"][0]["embedding"]
    return np.array(embedding, dtype="float32")

def search(query: str, index, metadata, top_k=3):
    query_vector = embed_query(query).reshape(1, -1)
    distances, indices = index.search(query_vector, top_k)
    return [metadata[i] for i in indices[0]]

def synthesize_answer(query, chunks):
    context = "\n\n".join([
        f"Section: {chunk.get('section', 'N/A')}\n{chunk.get('text', '').strip()}"
        + (f"\nEquation: {chunk.get('equation', '')}" if chunk.get('equation') else "")
        for chunk in chunks
    ])
    system_prompt = "You are a helpful AI assistant. Use the provided context to answer the question clearly and accurately."
    user_prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response["choices"][0]["message"]["content"].strip()

# ========== Streamlit UI ==========
st.set_page_config(page_title="LaTeX RAG Assistant For Science", layout="wide")
st.title("📘 LaTeX Paper QA Assistant")
st.markdown("Ask a question about your LaTeX-based paper.")

query = st.text_input("🔍 Enter your question:")
if query:
    with st.spinner("Searching and synthesizing answer..."):
        index = load_faiss_index()
        metadata = load_metadata()
        results = search(query, index, metadata)
        answer = synthesize_answer(query, results)

    st.subheader("🧠 Synthesized Answer")
    st.markdown(answer)
    st.markdown("---")

    st.subheader("🔎 Top Relevant Chunks")
    for i, res in enumerate(results, 1):
        st.markdown(f"**Section:** {res.get('section', 'N/A')}")
        if res.get("text"):
            st.markdown(res["text"])
        if res.get("equation"):
            st.latex(res["equation"])


