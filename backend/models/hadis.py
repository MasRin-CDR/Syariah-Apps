"""Pydantic models for Hadis API"""
from pydantic import BaseModel
from typing import Optional, List


class KitabMeta(BaseModel):
    nama: str
    nama_arab: Optional[str] = None
    jumlah_hadis: int
    jumlah_bab: int
    ikon: Optional[str] = None


class BabItem(BaseModel):
    bab_no: int
    bab: str
    bab_arab: Optional[str] = None
    jumlah_hadis: int


class HadisItem(BaseModel):
    id: int
    kitab: str
    kitab_arab: Optional[str] = None
    bab: str
    bab_arab: Optional[str] = None
    nomor: int
    arab: str
    terjemahan: str
    perawi: Optional[str] = None
    kualitas: Optional[str] = None


class KitabListResponse(BaseModel):
    total: int
    data: List[KitabMeta]


class BabListResponse(BaseModel):
    kitab: str
    total: int
    data: List[BabItem]


class HadisListResponse(BaseModel):
    kitab: str
    bab: Optional[str] = None
    total: int
    page: int
    limit: int
    data: List[HadisItem]
