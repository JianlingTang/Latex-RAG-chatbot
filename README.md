Here is your complete, production-ready `README.md` content that you can **copy and paste directly** into your repo's `README.md` file:

````markdown
# 🧠 LaTeX RAG Chatbot (Streamlit App)

This is a lightweight Retrieval-Augmented Generation (RAG) chatbot built with Streamlit, designed to parse LaTeX `.tex` documents and answer questions using OpenAI's GPT models.

---

## 🚀 Features

- 📄 Parses LaTeX files to extract clean text and equations  
- 🧹 Strips LaTeX noise to improve embedding quality  
- 🔍 FAISS-based semantic search over chunked LaTeX sections  
- 🤖 Synthesizes answers from relevant context using GPT-4  
- 🔁 Compares RAG-generated answers vs. direct LLM completions  

---

## 🧰 Tech Stack

- Python 3.11+
- [Streamlit](https://streamlit.io/)
- [FAISS](https://github.com/facebookresearch/faiss)
- [OpenAI API](https://platform.openai.com/)
- `python-dotenv` for API key management

---

## 🧪 Setup

```bash
git clone https://github.com/yourusername/latex-rag-chatbot.git
cd latex-rag-chatbot

# Set up environment
conda create -n texrag python=3.11 -y
conda activate texrag
pip install -r requirements.txt
````

### 🔑 API Key

Create a `.env` file in the root directory and add:

```dotenv
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 🚀 Run Locally

```bash
streamlit run app.py
```

Open the provided `localhost` URL in your browser to interact with the chatbot!

---

## ☁️ Deploy to Streamlit Cloud

1. Push your code to a **public GitHub repository**
2. Visit [Streamlit Community Cloud](https://streamlit.io/cloud)
3. Click **"New app"**, select your repo and branch
4. Add `OPENAI_API_KEY` as a **secret variable**
5. Click **Deploy** 🎉

---

## 📄 Example Workflow

1. Add your LaTeX `.tex` file to the repo
2. Run `tex_parser.py` to generate `chunks.json`
3. Run `embed_index.py` to build `index.faiss`
4. Launch `app.py` via Streamlit
5. Ask questions — the bot will retrieve context and generate accurate answers

---

## 📬 License

MIT License © 2025 Janet Tang



