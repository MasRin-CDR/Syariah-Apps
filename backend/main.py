"""
Syariah App — FastAPI Main Entry Point
"""
import sys
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Add parent dir to path
sys.path.insert(0, '.')

from config import settings
from api.quran import router as quran_router
from api.hadis import router as hadis_router
from api.search import search_router, bookmark_router, riwayat_router
from services.search_service import load_faiss, load_embedding_model

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s — %(message)s'
)
log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    log.info("🚀 Syariah App Backend starting...")
    log.info(f"Database: {settings.DB_PATH}")

    # Load FAISS index (non-blocking if not exists)
    load_faiss(settings.FAISS_INDEX_PATH, settings.FAISS_MAP_PATH)
    load_embedding_model(settings.EMBEDDING_MODEL)

    log.info("✅ Startup complete")
    yield
    # Shutdown
    log.info("👋 Shutting down...")


app = FastAPI(
    title="Syariah App API",
    description="API untuk Aplikasi Islami — Al Quran, Hadis, Pencarian Cerdas & Kalkulator Waris",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(quran_router)
app.include_router(hadis_router)
app.include_router(search_router)
app.include_router(bookmark_router)
app.include_router(riwayat_router)


@app.get("/", tags=["Root"])
def root():
    return {
        "app": "Syariah App API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "quran": "/api/quran/surah",
            "hadis": "/api/hadis/kitab",
            "search": "/api/search?q=sabar",
            "bookmark": "/api/bookmark",
        }
    }


@app.get("/health", tags=["Root"])
def health():
    from database import get_db
    try:
        with get_db() as db:
            q = db.execute("SELECT COUNT(*) FROM quran").fetchone()[0]
            h = db.execute("SELECT COUNT(*) FROM hadis").fetchone()[0]
        return {"status": "ok", "quran": q, "hadis": h}
    except Exception as e:
        return JSONResponse(status_code=503, content={"status": "error", "detail": str(e)})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
