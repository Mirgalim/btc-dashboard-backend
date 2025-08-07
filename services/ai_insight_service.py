import os
import httpx
from xml.etree import ElementTree
from utils.sentiment_analysis import add_sentiment_to_news

CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
MODEL = "claude-3-haiku-20240307"

# 🔹 BTC News Headlines with Description & Source
async def get_latest_bitcoin_news(limit: int = 5) -> list[dict]:
    rss_url = "https://www.coindesk.com/arc/outboundfeeds/rss/"
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            r = await client.get(rss_url, timeout=10.0)
            r.raise_for_status()
            root = ElementTree.fromstring(r.content)
            items = root.findall(".//item")
            headlines = []
            for item in items[:limit]:
                title = item.find("title").text
                link = item.find("link").text
                desc = item.find("description").text if item.find("description") is not None else ""
                headlines.append({
                    "title": title,
                    "url": link,
                    "description": desc
                })
            return headlines
    except Exception as e:
        print("⚠️ Failed to fetch news (RSS):", e)
        return []

# 🧠 Claude Insight (дэлгэрэнгүй 3–4 өгүүлбэр)
async def get_ai_insight(summary: dict, latest_news: list[dict]) -> str:
    news_text = "\n".join(f"- {n['title']}: {n['description']}" for n in latest_news)
    prompt = (
        f"Bitcoin Summary:\n"
        f"- Max: {summary['max']}, Min: {summary['min']}, "
        f"Avg: {summary['average']}, Median: {summary['median']}, Volatility: {summary['volatility']}.\n\n"
        f"Latest News:\n{news_text}\n\n"
        f"Based on the Bitcoin market summary and recent news, provide a 3–4 sentence technical insight with context and reasoning."
    )

    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    payload = {
        "model": MODEL,
        "max_tokens": 500,
        "temperature": 0.7,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=payload,
                timeout=15.0
            )
            response.raise_for_status()
            result = response.json()
            return result["content"][0]["text"].strip()
    except Exception as e:
        print("⚠️ AI insight fetch failed:", e)
        return ""

# 🔗 Unified fetch
async def generate_bitcoin_insight(summary: dict) -> dict:
    news = await get_latest_bitcoin_news()
    news_with_sentiment = add_sentiment_to_news(news)
    insight = await get_ai_insight(summary, news_with_sentiment)
    return {
        "insight": insight,
        "news": news_with_sentiment
    }
