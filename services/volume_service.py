# services/volume_service.py
from utils.fetch_data import fetch_ohlcv_data

async def get_volume_data(from_date: str, to_date: str):
    df = await fetch_ohlcv_data(from_date, to_date)
    return {
        "total_volume": round(df["volume"].sum(), 2),
        "average_volume": round(df["volume"].mean(), 2),
        "values": df[["timestamp", "volume"]].to_dict(orient="records")
    }
