# services/mvrv_service.py

async def get_mvrv_data(from_date: str, to_date: str):
    # Энэ нь MOCK жишээ
    return {
        "values": [
            {"timestamp": from_date, "MVRV": 1.45},
            {"timestamp": to_date, "MVRV": 1.57}
        ],
        "latest": 1.57
    }
