# embed_index.py
import openai
import faiss
import numpy as np
import json
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
print(openai.api_key)

def embed_text(text: str) -> np.ndarray:
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-3-small"
    )
    embedding = response["data"][0]["embedding"]
    return np.array(embedding, dtype="float32")

def embed_chunks(chunks):
    texts = [f"{chunk['section']} {chunk['text']} {chunk['equation']}".strip() for chunk in chunks]
    embeddings = [embed_text(text) for text in texts]
    return np.stack(embeddings)

def build_faiss_index(embeddings):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index

def save_index(index, file_path="index.faiss"):
    faiss.write_index(index, file_path)

def main(chunks_path="chunks.json", index_path="index.faiss", meta_path="chunk_texts.json"):
    with open(chunks_path, "r") as f:
        chunks = json.load(f)

    # Use only the first 100 chunks for a lightweight demo
    chunks = chunks[:100]


    embeddings = embed_chunks(chunks)
    index = build_faiss_index(embeddings)
    save_index(index, index_path)

    with open(meta_path, "w") as f:
        json.dump(chunks, f)

if __name__ == "__main__":
    main()