# services/rsi_service.py
from utils.fetch_data import fetch_ohlcv_data

async def get_rsi_data(from_date: str, to_date: str, period=14):
    df = await fetch_ohlcv_data(from_date, to_date)
    delta = df["close"].diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    df["RSI"] = rsi
    return {
        "values": df[["timestamp", "RSI"]].dropna().to_dict(orient="records")
    }
