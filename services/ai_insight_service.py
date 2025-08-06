# services/ai_insight_service.py
import os
import httpx

GROQ_API_KEY = "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"
MODEL = "llama3-70b-8192"

async def get_ai_insight(summary: dict) -> str:
    prompt = (
        f"Bitcoin summary:\n"
        f"- Max: {summary['max']}, Min: {summary['min']}, "
        f"- Avg: {summary['average']}, Median: {summary['median']}, Volatility: {summary['volatility']}.\n"
        f"Write a short 2-sentence technical insight."
    )

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 120
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=10.0  # in seconds
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("⚠️ AI insight fetch failed:", e)
        return ""  # fallback: хоосон утга буцаах



"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"