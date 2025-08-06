# services/macd_service.py
from utils.fetch_data import fetch_ohlcv_data

async def get_macd_data(from_date: str, to_date: str):
    df = await fetch_ohlcv_data(from_date, to_date)

    ema_12 = df["close"].ewm(span=12, adjust=False).mean()
    ema_26 = df["close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = ema_12 - ema_26
    df["Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()

    return {
        "values": df[["timestamp", "MACD", "Signal"]].dropna().to_dict(orient="records")
    }
