"""
Syariah App — FastAPI Configuration
"""
from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    DATABASE_URL: str = f"sqlite:///{BASE_DIR}/database/syariah.db"
    DB_PATH: str = str(BASE_DIR / "database" / "syariah.db")
    FAISS_INDEX_PATH: str = str(BASE_DIR / "search_engine" / "faiss" / "index.bin")
    FAISS_MAP_PATH: str = str(BASE_DIR / "search_engine" / "faiss" / "id_map.json")
    EMBEDDING_MODEL: str = "paraphrase-multilingual-MiniLM-L12-v2"
    ALLOWED_ORIGINS: list = ["http://localhost:3000", "http://127.0.0.1:3000", "app://.", "capacitor://localhost"]
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
