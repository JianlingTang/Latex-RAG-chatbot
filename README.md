# 🧠 LaTeX RAG Chatbot (Streamlit App)

This is a lightweight Retrieval-Augmented Generation (RAG) chatbot built with Streamlit, designed to parse LaTeX `.tex` documents and answer questions using OpenAI's GPT models.

## 🚀 Features

- 📄 Parses LaTeX files to extract clean text and equations
- 🧹 Strips LaTeX noise to improve embedding quality
- 🔍 FAISS-based semantic search over chunked LaTeX sections
- 🤖 Synthesizes answers from relevant context using GPT-4
- 🔁 Compares RAG-generated answers vs. direct LLM completions

## 🧰 Tech Stack

- Python 3.11+
- [Streamlit](https://streamlit.io/)
- [FAISS](https://github.com/facebookresearch/faiss)
- [OpenAI API](https://platform.openai.com/)
- `dotenv` for API key management

## 🧪 Setup

```bash
git clone https://github.com/yourusername/latex-rag-chatbot.git
cd latex-rag-chatbot
conda create -n texrag python=3.11
conda activate texrag
pip install -r requirements.txt
