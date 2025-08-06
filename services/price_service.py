import httpx
import datetime

async def get_price_data(from_date: str, to_date: str):
    url = "https://api.binance.com/api/v3/klines"
    symbol = "BTCUSDT"

    # from_date → UTC 00:00
    start_dt = datetime.datetime.strptime(from_date, "%Y-%m-%d").replace(
        tzinfo=datetime.timezone.utc,
        hour=0, minute=0, second=0, microsecond=0
    )

    # to_date → UTC 23:59:59
    end_dt = datetime.datetime.strptime(to_date, "%Y-%m-%d").replace(
        tzinfo=datetime.timezone.utc,
        hour=23, minute=59, second=59, microsecond=0
    )

    diff_days = (end_dt - start_dt).days

    # Interval автоматаар сонгох
    if diff_days <= 1:
        interval = "5m"
    elif diff_days <= 7:
        interval = "1h"
    else:
        interval = "1d"

    start_ts = int(start_dt.timestamp() * 1000)
    end_ts = int(end_dt.timestamp() * 1000)

    params = {
        "symbol": symbol,
        "interval": interval,
        "startTime": start_ts,
        "endTime": end_ts,
        "limit": 1000
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        kline_data = response.json()

    # Label формат
    if interval in ["5m", "15m", "30m", "1h"]:
        label_format = "%Y-%m-%d %H:%M"
    else:
        label_format = "%Y-%m-%d"

    return [
        {
            "label": datetime.datetime.utcfromtimestamp(k[0] / 1000).strftime(label_format),
            "value": float(k[4])
        }
        for k in kline_data
    ]
