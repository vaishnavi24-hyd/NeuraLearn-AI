# 🧠 NeuroLearn AI

## Advanced Visual Learning Assistant Powered by RAG & Local LLMs

NeuroLearn AI is a futuristic AI-powered educational platform that combines Retrieval-Augmented Generation (RAG), semantic search, adaptive tutoring, visual explanations, quizzes, flashcards, and learning analytics into a single intelligent learning ecosystem.

Built using modern GenAI technologies such as Ollama, ChromaDB, LangChain, and Streamlit, NeuroLearn AI transforms static study materials into an interactive AI tutoring experience.

---

# 🚀 Key Features

## 📚 AI Tutor with RAG Architecture

* Ask questions directly from uploaded study materials
* Context-aware AI tutoring
* Semantic retrieval using ChromaDB
* Grounded responses with reduced hallucinations
* Source-aware contextual explanations
* Persistent conversational tutoring flow

---

## 🧩 Visual Learning System

* AI-generated Mermaid diagrams
* Flowcharts and concept maps
* Visual process explanations
* Side-by-side text and diagram rendering
* Interactive visual tutoring experience

---

## 📝 Quiz Generator

Generate:

* Multiple Choice Questions (MCQs)
* Short-answer questions
* True/False questions
* Revision-oriented assessments
* Topic-focused quizzes

Includes:

* Interactive quiz mode
* Instant scoring
* Progress tracking
* Difficulty customization

---

## 🎴 Flashcard Generator

* AI-generated flashcards
* Quick revision cards
* Interactive study mode
* Flip-card animations
* Concept recall system

---

## 📊 Learning Analytics Dashboard

Track:

* Study activity
* Quiz performance
* Weak topics
* Topic frequency
* Learning trends
* Study streaks
* AI-generated study insights

---

## 🧠 Adaptive AI Tutoring

Customize:

* Explanation depth
* Response length
* Teaching style
* Beginner / Intermediate / Advanced modes
* Storytelling explanations
* Step-by-step tutoring
* Exam-oriented responses

---

## ⚡ Semantic Search Engine

Powered by:

* Embeddings
* Vector similarity search
* ChromaDB retrieval
* Semantic chunk matching

Allows AI to retrieve conceptually relevant study material.

---

## 🌌 Premium Futuristic UI

* Dark neon cyberpunk theme
* Glassmorphism effects
* Responsive SaaS-style dashboard
* Animated glowing components
* Premium typography
* Modern AI platform styling

---

# 🏗️ System Architecture

```text
PDF Upload
    ↓
Text Extraction
    ↓
Document Chunking
    ↓
Embedding Generation
    ↓
ChromaDB Vector Storage
    ↓
Semantic Retrieval
    ↓
Ollama (Mistral)
    ↓
AI Tutor Responses
    ↓
Visual Explanations
    ↓
Quizzes & Flashcards
```

---

# 🧠 RAG Workflow

NeuroLearn AI uses Retrieval-Augmented Generation (RAG) architecture.

Workflow:

1. Users upload study materials.
2. PDFs are parsed and chunked.
3. Chunks are converted into embeddings.
4. Embeddings are stored inside ChromaDB.
5. User questions trigger semantic retrieval.
6. Relevant chunks are passed to Ollama.
7. AI generates grounded contextual answers.

This significantly reduces hallucinations and improves answer relevance.

---

# 🛠️ Tech Stack

| Layer             | Technology            |
| ----------------- | --------------------- |
| Frontend          | Streamlit             |
| LLM Engine        | Ollama                |
| AI Model          | Mistral               |
| RAG Framework     | LangChain             |
| Vector Database   | ChromaDB              |
| Embeddings        | sentence-transformers |
| PDF Parsing       | pdfplumber, PyPDF2    |
| Data Processing   | pandas                |
| Visualization     | Plotly                |
| Diagram Rendering | Mermaid.js            |
| Styling           | Custom CSS            |
| Storage           | SQLite                |

---

# 📂 Project Structure

```text
neurolearn-ai/
│
├── app.py
├── components/
├── services/
├── database/
├── uploads/
├── styles/
├── assets/
├── utils/
├── chromadb/
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation Guide

## 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/neurolearn-ai.git
cd neurolearn-ai
```

---

## 2️⃣ Create Virtual Environment

```bash
python3 -m venv venv
```

Activate environment:

### macOS/Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Install Ollama

Download Ollama:

[https://ollama.com](https://ollama.com)

---

## 5️⃣ Pull Mistral Model

```bash
ollama pull mistral
```

---

## 6️⃣ Start Ollama

```bash
ollama serve
```

---

## 7️⃣ Run NeuroLearn AI

```bash
streamlit run app.py
```

---

# 💡 Core AI Concepts Demonstrated

NeuroLearn AI demonstrates:

* Retrieval-Augmented Generation (RAG)
* Semantic Search
* Vector Databases
* Embeddings
* Local LLM Inference
* Adaptive Prompt Engineering
* Conversational AI
* Educational AI Systems
* Visual AI Explanations
* Learning Analytics

---

# 🎯 Key Capabilities

✅ Semantic document retrieval

✅ Grounded contextual AI tutoring

✅ AI-generated visual explanations

✅ Adaptive personalized learning

✅ AI-powered quiz generation

✅ Flashcard-based revision

✅ Interactive analytics dashboard

✅ Local LLM deployment using Ollama

✅ Fully modular AI architecture



# 📈 Why NeuroLearn AI Stands Out

Unlike generic chatbot-based educational systems, NeuroLearn AI combines:

* RAG architecture
* semantic retrieval
* visual tutoring
* adaptive explanations
* interactive learning systems
* analytics-driven insights

into a single AI-powered educational ecosystem.

---

Focused on:

* Generative AI
* RAG Systems
* Local LLM Applications
* AI-Powered Educational Platforms
* Multimodal AI Engineering


