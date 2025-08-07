import os
import httpx
from xml.etree import ElementTree

CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")  # Claude API token
MODEL = "claude-3-haiku-20240307"  # хурдан, хямд загвар

# 🔹 Token-гүй RSS суурьтай BTC мэдээ татах (CoinDesk)
async def get_latest_bitcoin_news(limit: int = 5) -> str:
    rss_url = "https://www.coindesk.com/arc/outboundfeeds/rss/"
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(rss_url, timeout=10.0)
            r.raise_for_status()
            root = ElementTree.fromstring(r.content)
            items = root.findall(".//item")
            headlines = [item.find("title").text for item in items[:limit]]
            return "\n".join(f"- {h}" for h in headlines)
    except Exception as e:
        print("⚠️ Failed to fetch news (RSS):", e)
        return "No recent news available."

# 🔹 Claude Insight үүсгэх
async def get_ai_insight(summary: dict, latest_news: str) -> str:
    prompt = (
        f"Bitcoin Summary:\n"
        f"- Max: {summary['max']}, Min: {summary['min']}, "
        f"Avg: {summary['average']}, Median: {summary['median']}, Volatility: {summary['volatility']}.\n\n"
        f"Latest News:\n{latest_news}\n\n"
        f"Based on this summary and news, provide a concise technical 2-sentence insight."
    )

    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    payload = {
        "model": MODEL,
        "max_tokens": 150,
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

# 🔹 Нэгтгэгч функц
async def generate_bitcoin_insight(summary: dict) -> str:
    latest_news = await get_latest_bitcoin_news()
    return await get_ai_insight(summary, latest_news)
