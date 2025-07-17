
import openai
import faiss
import numpy as np
import json
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def embed_query(query: str) -> np.ndarray:
    response = openai.Embedding.create(
        input=query,
        model="text-embedding-3-small"
    )
    embedding = response["data"][0]["embedding"]
    return np.array(embedding, dtype="float32")

def load_faiss_index(index_path="index.faiss"):
    return faiss.read_index(index_path)

def load_metadata(meta_path="chunk_texts.json"):
    with open(meta_path, "r") as f:
        return json.load(f)

def search(query: str, index, metadata, top_k=3):
    query_vector = embed_query(query).reshape(1, -1)
    distances, indices = index.search(query_vector, top_k)
    results = [metadata[i] for i in indices[0]]
    return results

def synthesize_answer(query, chunks):
    context = "\\n\\n".join([
        f"Section: {chunk.get('section', 'N/A')}\\n{chunk.get('text', '').strip()}"
        + (f"\\nEquation: {chunk.get('equation', '')}" if chunk.get('equation') else "")
        for chunk in chunks
    ])
    system_prompt = "You are a helpful AI assistant. Use the provided context to answer the question clearly and accurately."
    user_prompt = f"Context:\\n{context}\\n\\nQuestion: {query}\\nAnswer:"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response["choices"][0]["message"]["content"].strip()

def main():
    index = load_faiss_index("index.faiss")
    metadata = load_metadata("chunk_texts.json")

    while True:
        query = input("\\nAsk a question (or type 'exit'): ")
        if query.lower() == "exit":
            break

        results = search(query, index, metadata)
        print("\\nTop relevant sections:")
        for i, res in enumerate(results, 1):
            print(f"\\nResult {i}:")
            print(f"Section: {res.get('section', 'N/A')}")
            print(f"Text: {res.get('text', '').strip()}")
            if res.get("equation"):
                print(f"Equation: {res['equation']}")

        print("\\n\\033[1mSynthesized Answer:\\033[0m")
        print(synthesize_answer(query, results))

if __name__ == "__main__":
    main()

