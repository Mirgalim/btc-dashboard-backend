from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from routes.dashboard import router as dashboard_router
import os  # ⬅️ PORT environment variable авахад хэрэгтэй

# .env файлыг ачааллах
load_dotenv()

# FastAPI апп үүсгэх
app = FastAPI(title="Bitcoin Analytics API")

# Frontend-ийн зөвшөөрөгдсөн origin-ууд
origins = [
    "http://localhost:3000",
    "https://btc-dashboard-frontend-evcv.vercel.app",
    "https://btc-dashboard-backend-1.onrender.com",
    "https://btc-dashboard-frontend.vercel.app"
]

# CORS тохиргоо
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router нэмэх
app.include_router(dashboard_router, prefix="/dashboard")

# ⬅️ Render-д зориулж зөв PORT дээр ажиллуулах
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))  # Render өгсөн PORT-оос авах, эсвэл local-д 8000
    uvicorn.run("main:app", host="0.0.0.0", port=port)
