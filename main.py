# main.py

from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from routes.dashboard import router as dashboard_router

# .env файлыг ачааллах
load_dotenv()

# FastAPI апп үүсгэх
app = FastAPI(title="Bitcoin Analytics API")

# Frontend-ийн зөвшөөрөгдсөн origin-ууд
origins = [
    "http://localhost:3000",  # Next.js dev server
    "http://127.0.0.1:3000",
    # production domain-ууд энд нэмнэ
]

# CORS тохиргоо нэмэх
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # зөвшөөрөгдсөн origin-ууд
    allow_credentials=True,
    allow_methods=["*"],              # бүх HTTP method зөвшөөрнө
    allow_headers=["*"],              # бүх header зөвшөөрнө
)

# Router нэмэх
app.include_router(dashboard_router, prefix="/dashboard")
