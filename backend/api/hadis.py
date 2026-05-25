"""
Syariah App — Hadis API Router
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from database import get_db
from models.hadis import KitabListResponse, BabListResponse, HadisListResponse, KitabMeta, BabItem, HadisItem

router = APIRouter(prefix="/api/hadis", tags=["Hadis"])

KITAB_INFO = {
    "Shahih Bukhari":       {"arab": "صحيح البخاري",  "ikon": "bukhari"},
    "Shahih Muslim":        {"arab": "صحيح مسلم",     "ikon": "muslim"},
    "Sunan Abu Daud":       {"arab": "سنن أبي داود",   "ikon": "abudaud"},
    "Sunan Tirmidzi":       {"arab": "سنن الترمذي",   "ikon": "tirmidzi"},
    "Sunan An-Nasai":       {"arab": "سنن النسائي",   "ikon": "nasai"},
    "Sunan Ibnu Majah":     {"arab": "سنن ابن ماجة",  "ikon": "ibnumajah"},
    "Muwattha' Imam Malik": {"arab": "موطأ مالك",     "ikon": "malik"},
    "Musnad Ahmad":         {"arab": "مسند أحمد",     "ikon": "ahmad"},
    "Sunan Ad-Darimi":      {"arab": "سنن الدارمي",   "ikon": "darimi"},
}


@router.get("/kitab", response_model=KitabListResponse)
def get_kitab_list():
    """Get list of all 9 hadis books"""
    with get_db() as db:
        rows = db.execute("""
            SELECT kitab,
                   COUNT(*) as jumlah_hadis,
                   COUNT(DISTINCT bab_no) as jumlah_bab
            FROM hadis
            GROUP BY kitab
            ORDER BY MIN(id)
        """).fetchall()

        data = []
        for r in rows:
            info = KITAB_INFO.get(r["kitab"], {})
            data.append(KitabMeta(
                nama=r["kitab"],
                nama_arab=info.get("arab"),
                jumlah_hadis=r["jumlah_hadis"],
                jumlah_bab=r["jumlah_bab"],
                ikon=info.get("ikon"),
            ))
        return KitabListResponse(total=len(data), data=data)


@router.get("/kitab/{kitab_nama}", response_model=BabListResponse)
def get_bab_list(kitab_nama: str):
    """Get list of bab in a kitab"""
    with get_db() as db:
        rows = db.execute("""
            SELECT bab_no, bab, bab_arab, COUNT(*) as jumlah_hadis
            FROM hadis
            WHERE kitab=?
            GROUP BY bab_no
            ORDER BY bab_no
        """, (kitab_nama,)).fetchall()

        if not rows:
            raise HTTPException(status_code=404, detail=f"Kitab '{kitab_nama}' tidak ditemukan")

        data = [BabItem(
            bab_no=r["bab_no"] or 0,
            bab=r["bab"],
            bab_arab=r["bab_arab"],
            jumlah_hadis=r["jumlah_hadis"]
        ) for r in rows]

        return BabListResponse(kitab=kitab_nama, total=len(data), data=data)


@router.get("/bab/{kitab_nama}/{bab_no}", response_model=HadisListResponse)
def get_hadis_by_bab(kitab_nama: str, bab_no: int, page: int = 1, limit: int = 20):
    """Get hadis in a specific bab"""
    offset = (page - 1) * limit
    with get_db() as db:
        total = db.execute(
            "SELECT COUNT(*) FROM hadis WHERE kitab=? AND bab_no=?",
            (kitab_nama, bab_no)
        ).fetchone()[0]

        rows = db.execute("""
            SELECT * FROM hadis WHERE kitab=? AND bab_no=?
            ORDER BY nomor LIMIT ? OFFSET ?
        """, (kitab_nama, bab_no, limit, offset)).fetchall()

        if not rows and total == 0:
            raise HTTPException(status_code=404, detail="Bab tidak ditemukan")

        bab_name = rows[0]["bab"] if rows else ""
        return HadisListResponse(
            kitab=kitab_nama,
            bab=bab_name,
            total=total,
            page=page,
            limit=limit,
            data=[HadisItem(**dict(r)) for r in rows]
        )


@router.get("/{hadis_id}", response_model=HadisItem)
def get_hadis_detail(hadis_id: int):
    """Get single hadis by ID"""
    with get_db() as db:
        row = db.execute("SELECT * FROM hadis WHERE id=?", (hadis_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail=f"Hadis ID {hadis_id} tidak ditemukan")
        return HadisItem(**dict(row))
