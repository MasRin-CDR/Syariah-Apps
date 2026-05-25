"""Pydantic models for Bookmark & Search API"""
from pydantic import BaseModel
from typing import Optional, List, Literal
from datetime import datetime


class BookmarkCreate(BaseModel):
    tipe: Literal['quran', 'hadis']
    referensi: int
    catatan: Optional[str] = None


class BookmarkResponse(BaseModel):
    id: int
    tipe: str
    referensi: int
    catatan: Optional[str] = None
    created_at: Optional[str] = None


class RiwayatCreate(BaseModel):
    tipe: Literal['quran', 'hadis']
    referensi: int
    posisi: Optional[str] = None


class RiwayatResponse(BaseModel):
    id: int
    tipe: str
    referensi: int
    posisi: Optional[str] = None
    updated_at: Optional[str] = None


class QuranSearchResult(BaseModel):
    id: int
    surah: int
    ayat: int
    nama_surah: str
    nama_latin: str
    arab: str
    terjemahan: str
    highlight: Optional[str] = None
    skor: float = 0.0


class HadisSearchResult(BaseModel):
    id: int
    kitab: str
    nomor: int
    bab: str
    arab: str
    terjemahan: str
    highlight: Optional[str] = None
    skor: float = 0.0


class SearchResponse(BaseModel):
    query: str
    filter: str
    total_quran: int
    total_hadis: int
    quran: List[QuranSearchResult]
    hadis: List[HadisSearchResult]
    took_ms: float
