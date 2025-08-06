# services/bollinger_service.py
from utils.fetch_data import fetch_ohlcv_data

async def get_bollinger_bands(from_date: str, to_date: str, period=20, num_std_dev=2):
    df = await fetch_ohlcv_data(from_date, to_date)
    df["SMA"] = df["close"].rolling(window=period).mean()
    df["STD"] = df["close"].rolling(window=period).std()

    df["Upper"] = df["SMA"] + (num_std_dev * df["STD"])
    df["Lower"] = df["SMA"] - (num_std_dev * df["STD"])

    return {
        "values": df[["timestamp", "Upper", "Lower"]].dropna().to_dict(orient="records")
    }
