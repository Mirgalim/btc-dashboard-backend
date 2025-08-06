# services/ma_service.py
from utils.fetch_data import fetch_ohlcv_data

async def get_ma_data(from_date: str, to_date: str):
    df = await fetch_ohlcv_data(from_date, to_date)
    df["SMA"] = df["close"].rolling(window=10).mean()
    df["EMA"] = df["close"].ewm(span=10, adjust=False).mean()
    df["WMA"] = df["close"].rolling(window=10).apply(
        lambda prices: sum((i + 1) * price for i, price in enumerate(prices)) / sum(range(1, 11)),
        raw=True
    )

    return {
        "values": df[["timestamp", "SMA", "EMA", "WMA"]].dropna().to_dict(orient="records")
    }
