from dotenv import load_dotenv
import os
import requests
import feedparser
import re
import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.Client()
collection = client.get_or_create_collection("news_memory")

model = SentenceTransformer("all-MiniLM-L6-v2")

load_dotenv()
API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not API_KEY:
    raise ValueError("ANTHROPIC_API_KEY not found. Check your .env file.")

# -------------------------
# 1. Define RSS feeds
# -------------------------
feeds = {
    "ai": "https://news.google.com/rss/search?q=AI+business",
    "markets": "https://news.google.com/rss/search?q=middle+east+oil+market",
    "general": "https://news.google.com/rss",
    "fun": "https://news.google.com/rss/search?q=weird+news+OR+fun+facts+OR+surprising+news"
}

# -------------------------
# 2. Clean HTML from text
# -------------------------
def clean_html(text):
    return re.sub('<.*?>', '', text)

# -------------------------
# 3. Fetch articles
# -------------------------
def fetch_articles():
    articles = []
    for category, url in feeds.items():
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:
            summary = entry.summary if "summary" in entry else ""
            clean_summary = clean_html(summary)

            articles.append({
                "category": category,
                "title": entry.title,
                "summary": clean_summary
            })
    return articles

# -------------------------
# 4. Format articles
# -------------------------
def format_articles(articles):
    text = ""
    for a in articles:
        text += f"[{a['category'].upper()}]\n"
        text += f"Title: {a['title']}\n"
        text += f"Summary: {a['summary']}\n\n"
        if a['category'] == "fun":
            text += "(This is a fun or surprising story)\n"
    return text

# -------------------------
# 5. Generate briefing
# -------------------------
def retrieve_memory(query):
    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    return "\n".join(results["documents"][0])
    
def generate_briefing(text):
    url = "https://api.anthropic.com/v1/messages"

    headers = {
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    memory = retrieve_memory("AI trends and market changes")
    prompt = f"""
You are a senior strategy consultant writing a DAILY BRIEFING.
You have access to past briefings.

PAST CONTEXT (previous days):
{memory}

TASK:

📈 What Changed Since Yesterday
- Identify 2–3 key differences between past context and today's news
- Focus on:
  - new developments
  - shifts in direction
  - emerging risks or opportunities

Rules:
- Avoid generic statements
- Focus on specific, interesting insights
- Make conversation topics engaging and surprising
- Add the current date at the beginning of the output, so that I can easily identify the date

🧠 AI Business Insight
📊 Market Impact (US + Taiwan)

🍸 Conversation Topics (IMPORTANT)
- Provide 5 topics that are:
  - surprising OR counterintuitive OR fun
  - suitable for dinner conversation
  - NOT generic business statements

📰 Top News

📊 Trend Score (AI & Markets)

For each:
- AI trend: UP / DOWN / STABLE
- Market sentiment: UP / DOWN / STABLE

Also briefly explain WHY (1 line each)

ARTICLES:
{text}
"""

    data = {
        "model": "claude-sonnet-4-6",
        "max_tokens": 1500,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        raise RuntimeError(f"API error {response.status_code}: {response.text}")

    result = response.json()
    if "content" not in result:
        raise RuntimeError(f"Unexpected API response: {result}")

    return result["content"][0]["text"]

def store_memory(text):
    embedding = model.encode(text).tolist()

    collection.add(
        documents=[text],
        embeddings=[embedding],
        ids=[str(hash(text))]
    )

# -------------------------
# 6. Run everything
# -------------------------
if __name__ == "__main__":
    articles = fetch_articles()
    formatted = format_articles(articles)

    briefing = generate_briefing(formatted)

    print(briefing)

    # -------------------------
    # 7. Save history
    # -------------------------
    store_memory(briefing)