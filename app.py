import streamlit as st
from research_agent import fetch_articles, format_articles, generate_briefing

def parse_sections(text):
    sections = {
        "AI Business Insight": "",
        "Market Impact": "",
        "Conversation Topics": "",
        "Trend Score": "",
        "Top News": ""
    }

    current_section = None

    for line in text.split("\n"):
        if "AI Business Insight" in line:
            current_section = "AI Business Insight"
        elif "Market Impact" in line:
            current_section = "Market Impact"
        elif "Conversation Topic" in line:
            current_section = "Conversation Topics"
        elif "Trend Score" in line:
            current_section = "Trend Score"
        elif "Top News" in line:
            current_section = "Top News"
        elif current_section:
            sections[current_section] += line + "\n"

    return sections

st.title("🧠 AI Research Agent")

if st.button("Generate Daily Briefing"):
    with st.spinner("🧠 Analyzing news and generating insights..."):
        articles = fetch_articles()
        formatted = format_articles(articles)
        briefing = generate_briefing(formatted)

        sections = parse_sections(briefing)

    st.subheader("🧠 AI Business Insight")
    st.write(sections["AI Business Insight"])

    st.subheader("📊 Market Impact")
    st.write(sections["Market Impact"])

    st.subheader("🍸 Conversation Topics")
    st.write(sections["Conversation Topics"])

    st.subheader("📈 Trend Score")
    st.write(sections["Trend Score"])

    st.subheader("📰 Top News")
    st.write(sections["Top News"])
