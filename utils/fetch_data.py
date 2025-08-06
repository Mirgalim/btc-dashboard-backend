# utils/fetch_data.py
import httpx
from datetime import datetime
import pandas as pd

async def fetch_ohlcv_data(from_date: str, to_date: str, interval=None):
    symbol = "BTCUSDT"
    start_dt = datetime.fromisoformat(from_date)
    end_dt = datetime.fromisoformat(to_date)

    # Interval автоматаар сонгох
    if interval is None:
        diff_days = (end_dt - start_dt).days
        if diff_days <= 1:
            interval = "5m"
        elif diff_days <= 7:
            interval = "1h"
        else:
            interval = "1d"

    start = int(start_dt.timestamp() * 1000)
    end = int(end_dt.timestamp() * 1000)

    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "startTime": start,
        "endTime": end,
        "limit": 1000,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        raw = response.json()

    df = pd.DataFrame(raw, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base", "taker_buy_quote", "ignore"
    ])

    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df["close"] = pd.to_numeric(df["close"])
    df["volume"] = pd.to_numeric(df["volume"])

    return df[["timestamp", "close", "volume"]]
