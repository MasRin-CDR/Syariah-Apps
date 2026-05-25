"""
Syariah App — Al Quran API Router
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from database import get_db
from models.quran import SurahListResponse, SurahDetailResponse, AyatResponse, JuzResponse, SurahMeta

router = APIRouter(prefix="/api/quran", tags=["Al Quran"])


def row_to_surah_meta(row) -> dict:
    return {
        "id": row["id"],
        "nama_arab": row["nama_arab"],
        "nama_latin": row["nama_latin"],
        "nama_indo": row["nama_indo"],
        "jumlah_ayat": row["jumlah_ayat"],
        "jenis": row["jenis"],
        "juz_awal": row["juz_awal"],
    }


def row_to_ayat(row) -> dict:
    return {
        "id": row["id"],
        "surah": row["surah"],
        "ayat": row["ayat"],
        "arab": row["arab"],
        "terjemahan": row["terjemahan"],
        "tafsir": row["tafsir"],
        "juz": row["juz"],
        "nama_surah": row["nama_surah"],
        "nama_latin": row["nama_latin"],
    }


@router.get("/surah", response_model=SurahListResponse)
def get_surah_list(q: Optional[str] = Query(None, description="Filter by name")):
    """Get list of all 114 surah"""
    with get_db() as db:
        if q:
            rows = db.execute("""
                SELECT * FROM surah
                WHERE nama_latin LIKE ? OR nama_arab LIKE ? OR nama_indo LIKE ?
                ORDER BY id
            """, (f"%{q}%", f"%{q}%", f"%{q}%")).fetchall()
        else:
            rows = db.execute("SELECT * FROM surah ORDER BY id").fetchall()

        data = [SurahMeta(**row_to_surah_meta(r)) for r in rows]
        return SurahListResponse(total=len(data), data=data)


@router.get("/surah/{surah_id}", response_model=SurahDetailResponse)
def get_surah_detail(surah_id: int):
    """Get surah detail with all ayat"""
    if surah_id < 1 or surah_id > 114:
        raise HTTPException(status_code=400, detail="Nomor surah harus antara 1-114")

    with get_db() as db:
        surah_row = db.execute("SELECT * FROM surah WHERE id=?", (surah_id,)).fetchone()
        if not surah_row:
            raise HTTPException(status_code=404, detail=f"Surah {surah_id} tidak ditemukan")

        ayat_rows = db.execute(
            "SELECT * FROM quran WHERE surah=? ORDER BY ayat", (surah_id,)
        ).fetchall()

        return SurahDetailResponse(
            surah=SurahMeta(**row_to_surah_meta(surah_row)),
            ayat=[AyatResponse(**row_to_ayat(r)) for r in ayat_rows]
        )


@router.get("/ayat/{surah_id}/{ayat_num}", response_model=AyatResponse)
def get_ayat(surah_id: int, ayat_num: int):
    """Get single ayat detail"""
    with get_db() as db:
        row = db.execute(
            "SELECT * FROM quran WHERE surah=? AND ayat=?", (surah_id, ayat_num)
        ).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail=f"Ayat {surah_id}:{ayat_num} tidak ditemukan")
        return AyatResponse(**row_to_ayat(row))


@router.get("/juz/{juz_num}", response_model=JuzResponse)
def get_juz(juz_num: int, page: int = 1, limit: int = 50):
    """Get ayat in a juz"""
    if juz_num < 1 or juz_num > 30:
        raise HTTPException(status_code=400, detail="Nomor juz harus antara 1-30")

    offset = (page - 1) * limit
    with get_db() as db:
        total = db.execute("SELECT COUNT(*) FROM quran WHERE juz=?", (juz_num,)).fetchone()[0]
        rows = db.execute(
            "SELECT * FROM quran WHERE juz=? ORDER BY surah, ayat LIMIT ? OFFSET ?",
            (juz_num, limit, offset)
        ).fetchall()
        return JuzResponse(
            juz=juz_num,
            total_ayat=total,
            ayat=[AyatResponse(**row_to_ayat(r)) for r in rows]
        )
