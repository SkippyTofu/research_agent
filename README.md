# 🧠 AI Research Agent — Daily Strategic Briefing

An AI-powered research agent that automatically curates and synthesizes daily news into executive-level briefings.

🔗 **Live App:** https://your-app.streamlit.app *(replace with your link)*

---

## 💡 Overview

This project addresses a common problem:  
> Information is fragmented, time-consuming to scan, and difficult to turn into actionable insights.

The AI Research Agent transforms raw news into **structured, decision-ready intelligence** across AI, markets, and global trends.

---

## 🚀 Features

- 🧠 **AI Business Insights**  
  Extracts strategic signals from AI and technology news

- 📊 **Market Impact (US + Taiwan)**  
  Connects global events (e.g., geopolitics, energy) to financial implications

- 🍸 **Conversation Topics**  
  Generates engaging, non-obvious talking points for networking and discussions

- 📈 **Trend Scoring**  
  Identifies whether AI momentum is rising, stable, or declining

- 🔄 **Change Detection (RAG-enabled)**  
  Highlights what has changed vs previous days using memory

---

## 🧱 Architecture

The system is designed as a lightweight AI pipeline:

1. **Data Ingestion**  
   - RSS feeds (Google News)
   - Categories: AI, Markets, General, Fun

2. **Processing Layer**  
   - HTML cleaning
   - Structured formatting

3. **AI Reasoning (LLM)**  
   - Claude API generates insights
   - Prompt structured for strategic output (not generic summaries)

4. **Memory Layer (RAG)**  
   - Embeddings via Sentence Transformers
   - Stored in ChromaDB
   - Enables trend comparison over time

5. **Presentation Layer**  
   - Streamlit UI
   - Section-based dashboard for readability

---

## 🎯 Product Thinking

This project is not just a technical demo — it reflects **AI product design principles**:

- Translating raw data → actionable insights
- Structuring outputs for real user workflows (daily briefing)
- Designing for **decision-making**, not just summarization
- Combining automation + interpretability

---

## 📊 Impact

- ⏱️ Reduces daily news scanning time from ~30 minutes → <5 minutes  
- 🧠 Improves quality of insights vs generic summaries  
- 🔄 Enables trend tracking over time (via RAG memory)  
- 📈 Demonstrates scalable pattern for enterprise AI knowledge workflows  

---

## ⚙️ Tech Stack

- **Python**
- **Streamlit** — UI layer  
- **Anthropic Claude API** — LLM reasoning  
- **ChromaDB** — vector database (memory)  
- **Sentence Transformers** — embeddings  
- **RSS (feedparser)** — real-time data ingestion  

---

## 🖥️ Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py