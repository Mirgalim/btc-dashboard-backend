# services/summary_service.py
import httpx
from utils.fetch_data import fetch_ohlcv_data


async def get_current_price():
    url = "https://api.binance.com/api/v3/ticker/price"
    params = {"symbol": "BTCUSDT"}
    async with httpx.AsyncClient() as client:
        r = await client.get(url, params=params)
        r.raise_for_status()
        data = r.json()
    return float(data["price"])

async def get_summary(from_date: str, to_date: str):
    df = await fetch_ohlcv_data(from_date, to_date)
    current_price = await get_current_price()
    return {
        "current_price": current_price,
        "max": round(df["close"].max(), 2),
        "min": round(df["close"].min(), 2),
        "average": round(df["close"].mean(), 2),
        "median": round(df["close"].median(), 2),
        "volatility": round(df["close"].std(), 2)
    }
