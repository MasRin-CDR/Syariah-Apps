"""Pydantic models for Al Quran API"""
from pydantic import BaseModel
from typing import Optional, List


class AyatBase(BaseModel):
    id: int
    surah: int
    ayat: int
    arab: str
    terjemahan: str
    tafsir: Optional[str] = None
    juz: int
    nama_surah: str
    nama_latin: str


class AyatResponse(AyatBase):
    class Config:
        from_attributes = True


class SurahMeta(BaseModel):
    id: int
    nama_arab: str
    nama_latin: str
    nama_indo: str
    jumlah_ayat: int
    jenis: str
    juz_awal: int


class SurahListResponse(BaseModel):
    total: int
    data: List[SurahMeta]


class SurahDetailResponse(BaseModel):
    surah: SurahMeta
    ayat: List[AyatResponse]


class JuzResponse(BaseModel):
    juz: int
    total_ayat: int
    ayat: List[AyatResponse]
