from fastapi import APIRouter, Query, HTTPException
from datetime import datetime, date, timedelta
from typing import Optional

from services.price_service import get_price_data
from services.ma_service import get_ma_data
from services.rsi_service import get_rsi_data
from services.macd_service import get_macd_data
from services.summary_service import get_summary, get_current_price
from services.volume_service import get_volume_data
from services.bollinger_service import get_bollinger_bands
from services.mvrv_service import get_mvrv_data
from services.macro_service import get_macro_indicators
from services.ai_insight_service import generate_bitcoin_insight

router = APIRouter()


@router.get("")
async def get_dashboard(
    days: Optional[int] = Query(
        None, description="Number of days before today"),
    from_date: Optional[date] = Query(
        None, description="Start date in YYYY-MM-DD format"),
    to_date: Optional[date] = Query(
        None, description="End date in YYYY-MM-DD format"),
):
    if days is not None:
        to_date = date.today()
        from_date = to_date - timedelta(days=days)

    if not from_date or not to_date:
        raise HTTPException(
            status_code=400, detail="Either days or both from_date & to_date are required.")
    if from_date > to_date:
        raise HTTPException(
            status_code=400, detail="from_date cannot be after to_date")

    summary = await get_summary(str(from_date), str(to_date))
    price_data = await get_price_data(str(from_date), str(to_date))

    try:
        insight = await generate_bitcoin_insight(summary)
    except Exception as e:
        print("AI insight error:", str(e))
        insight = "AI insight unavailable at the moment."


    def get_price_on(days_ago: int):
        target_date = (datetime.utcnow().date() - timedelta(days=days_ago))
        target_str = target_date.strftime("%Y-%m-%d")

        same_day_candles = [p for p in price_data if p["label"].startswith(target_str)]

        if not same_day_candles:
            sorted_prices = sorted(price_data, key=lambda x: x["label"])
            prev_candle = None
            for p in reversed(sorted_prices):
                if p["label"] < target_str:
                    prev_candle = p
                    break
            return prev_candle["value"] if prev_candle else None

        return same_day_candles[-1]["value"]

    today_price = await get_current_price()  
    history_ranges = [30, 60, 90] 
    price_history = [
        {
            "label": "Today",
            "amountChange": 0.0,
            "percentChange": 0.0
        }
    ]

    for r in history_ranges:
        base_price = get_price_on(r)
        if base_price is None:
            continue
        amount_change = today_price - base_price
        percent_change = (amount_change / base_price) * 100
        price_history.append({
            "label": f"{r} Days",
            "amountChange": round(amount_change, 2),
            "percentChange": round(percent_change, 2)
        })

    return {
        "status": "success",
        "summary": summary,
        "chart": price_data,
        "insight": insight,
        "price": price_data,
        "price_history": price_history,
        "ma": await get_ma_data(str(from_date), str(to_date)),
        "rsi": await get_rsi_data(str(from_date), str(to_date)),
        "macd": await get_macd_data(str(from_date), str(to_date)),
        "volume": await get_volume_data(str(from_date), str(to_date)),
        "bollinger": await get_bollinger_bands(str(from_date), str(to_date)),
        "mvrv": await get_mvrv_data(str(from_date), str(to_date)),
        "macro": await get_macro_indicators(),
    }