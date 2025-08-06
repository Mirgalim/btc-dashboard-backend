# services/ai_insight_service.py
import os
import httpx

CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")  # Claude API token
MODEL = "claude-3-haiku-20240307"  # хурдан, хямд, real-time ойлголт

# Bitcoin мэдээ авах (CryptoPanic API)
CRYPTO_NEWS_API = "https://cryptopanic.com/api/v1/posts/"
CRYPTO_NEWS_TOKEN = os.getenv("CRYPTO_NEWS_TOKEN")  # CryptoPanic token

async def get_latest_bitcoin_news(limit: int = 5) -> str:
    params = {
        "auth_token": CRYPTO_NEWS_TOKEN,
        "currencies": "BTC",
        "public": "true"
    }
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(CRYPTO_NEWS_API, params=params, timeout=10.0)
            r.raise_for_status()
            data = r.json()
            headlines = [item["title"] for item in data["results"][:limit]]
            return "\n".join(f"- {h}" for h in headlines)
    except Exception as e:
        print("⚠️ Failed to fetch news:", e)
        return "No recent news available."

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

# Нэгтгэсэн функц
async def generate_bitcoin_insight(summary: dict) -> str:
    latest_news = await get_latest_bitcoin_news()
    return await get_ai_insight(summary, latest_news)
