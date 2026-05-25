"""
Syariah App — Search & Bookmark API Routers
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from database import get_db
from models.bookmark import BookmarkCreate, BookmarkResponse, RiwayatCreate, RiwayatResponse, SearchResponse
from services.search_service import hybrid_search

# ── Search Router ───────────────────────────────────────────────────────────
search_router = APIRouter(prefix="/api/search", tags=["Pencarian"])


@search_router.get("", response_model=SearchResponse)
def search(
    q: str = Query(..., min_length=2, description="Kata kunci pencarian"),
    filter: Optional[str] = Query("all", pattern="^(all|quran|hadis)$"),
    limit: int = Query(20, ge=1, le=100)
):
    """Hybrid search: FTS5 + FAISS semantic search"""
    if not q.strip():
        raise HTTPException(status_code=400, detail="Query tidak boleh kosong")

    with get_db() as db:
        result = hybrid_search(db, q.strip(), filter_type=filter, limit=limit)

        # Save to search history
        try:
            db.execute("""
                INSERT INTO search_history (query, filter_type, result_count)
                VALUES (?, ?, ?)
            """, (q, filter, result['total_quran'] + result['total_hadis']))
        except Exception:
            pass

        return SearchResponse(**result)


@search_router.get("/history")
def get_search_history(limit: int = 10):
    """Get recent search history"""
    with get_db() as db:
        rows = db.execute("""
            SELECT query, filter_type, result_count, searched_at
            FROM search_history
            ORDER BY searched_at DESC
            LIMIT ?
        """, (limit,)).fetchall()
        return {"data": [dict(r) for r in rows]}


# ── Bookmark Router ─────────────────────────────────────────────────────────
bookmark_router = APIRouter(prefix="/api/bookmark", tags=["Bookmark"])


@bookmark_router.get("", response_model=list)
def get_bookmarks(tipe: Optional[str] = None):
    """Get all bookmarks"""
    with get_db() as db:
        if tipe:
            rows = db.execute(
                "SELECT * FROM bookmark WHERE tipe=? ORDER BY created_at DESC", (tipe,)
            ).fetchall()
        else:
            rows = db.execute(
                "SELECT * FROM bookmark ORDER BY created_at DESC"
            ).fetchall()
        return [dict(r) for r in rows]


@bookmark_router.post("", response_model=BookmarkResponse)
def add_bookmark(data: BookmarkCreate):
    """Add a bookmark"""
    with get_db() as db:
        try:
            cur = db.execute("""
                INSERT INTO bookmark (tipe, referensi, catatan)
                VALUES (?, ?, ?)
            """, (data.tipe, data.referensi, data.catatan))
            row = db.execute("SELECT * FROM bookmark WHERE id=?", (cur.lastrowid,)).fetchone()
            return BookmarkResponse(**dict(row))
        except Exception as e:
            if "UNIQUE" in str(e):
                raise HTTPException(status_code=409, detail="Sudah ada di bookmark")
            raise HTTPException(status_code=500, detail=str(e))


@bookmark_router.delete("/{bookmark_id}")
def delete_bookmark(bookmark_id: int):
    """Delete a bookmark"""
    with get_db() as db:
        cur = db.execute("DELETE FROM bookmark WHERE id=?", (bookmark_id,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Bookmark tidak ditemukan")
        return {"message": "Bookmark dihapus"}


# ── Riwayat Router ──────────────────────────────────────────────────────────
riwayat_router = APIRouter(prefix="/api/riwayat", tags=["Riwayat"])


@riwayat_router.get("")
def get_riwayat():
    """Get reading history"""
    with get_db() as db:
        rows = db.execute(
            "SELECT * FROM riwayat_baca ORDER BY updated_at DESC LIMIT 20"
        ).fetchall()
        return {"data": [dict(r) for r in rows]}


@riwayat_router.post("")
def upsert_riwayat(data: RiwayatCreate):
    """Upsert reading history"""
    with get_db() as db:
        db.execute("""
            INSERT INTO riwayat_baca (tipe, referensi, posisi, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(tipe, referensi) DO UPDATE SET
                posisi=excluded.posisi,
                updated_at=CURRENT_TIMESTAMP
        """, (data.tipe, data.referensi, data.posisi))
        return {"message": "Riwayat diperbarui"}
