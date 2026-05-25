"""
Syariah App — Search Service (FTS5 + FAISS Hybrid)
"""
import re
import time
import json
import logging
from pathlib import Path
from typing import List, Tuple, Dict, Optional

log = logging.getLogger(__name__)

# Global FAISS state (loaded at startup)
_faiss_index = None
_faiss_id_map: Dict[int, dict] = {}  # faiss_idx -> {id, tipe}
_embedding_model = None


def load_faiss(index_path: str, map_path: str):
    global _faiss_index, _faiss_id_map
    try:
        import faiss
        if Path(index_path).exists():
            _faiss_index = faiss.read_index(index_path)
            log.info(f"FAISS index loaded: {_faiss_index.ntotal} vectors")
        if Path(map_path).exists():
            with open(map_path, encoding='utf-8') as f:
                raw = json.load(f)
                _faiss_id_map = {int(k): v for k, v in raw.items()}
            log.info(f"FAISS map loaded: {len(_faiss_id_map)} entries")
    except Exception as e:
        log.warning(f"FAISS not loaded (normal if index not built yet): {e}")


def load_embedding_model(model_name: str):
    global _embedding_model
    try:
        from sentence_transformers import SentenceTransformer
        _embedding_model = SentenceTransformer(model_name)
        log.info(f"Embedding model loaded: {model_name}")
    except Exception as e:
        log.warning(f"Embedding model not loaded: {e}")


def highlight_text(text: str, query: str, max_len: int = 200) -> str:
    """Highlight query keywords in text, return snippet"""
    words = re.sub(r'[^\w\s]', '', query.lower()).split()
    snippet = text[:max_len]
    for word in words:
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        snippet = pattern.sub(f'<mark>{word}</mark>', snippet)
    if len(text) > max_len:
        snippet += '...'
    return snippet


def normalize_score(score: float, min_val: float = 0, max_val: float = 1) -> float:
    return max(0.0, min(1.0, (score - min_val) / (max_val - min_val + 1e-9)))


def fts5_search_quran(db, query: str, limit: int = 50) -> List[Tuple[int, float]]:
    """FTS5 search on quran table, returns (id, bm25_score)"""
    try:
        # Sanitize query for FTS5
        clean = re.sub(r'[^\w\s\u0600-\u06FF]', ' ', query).strip()
        if not clean:
            return []
        rows = db.execute("""
            SELECT q.id, bm25(quran_fts) as score
            FROM quran_fts
            JOIN quran q ON q.id = quran_fts.rowid
            WHERE quran_fts MATCH ?
            ORDER BY score
            LIMIT ?
        """, (clean, limit)).fetchall()
        return [(r[0], abs(float(r[1]))) for r in rows]
    except Exception as e:
        log.error(f"FTS5 quran error: {e}")
        return []


def fts5_search_hadis(db, query: str, limit: int = 50) -> List[Tuple[int, float]]:
    """FTS5 search on hadis table"""
    try:
        clean = re.sub(r'[^\w\s\u0600-\u06FF]', ' ', query).strip()
        if not clean:
            return []
        rows = db.execute("""
            SELECT h.id, bm25(hadis_fts) as score
            FROM hadis_fts
            JOIN hadis h ON h.id = hadis_fts.rowid
            WHERE hadis_fts MATCH ?
            ORDER BY score
            LIMIT ?
        """, (clean, limit)).fetchall()
        return [(r[0], abs(float(r[1]))) for r in rows]
    except Exception as e:
        log.error(f"FTS5 hadis error: {e}")
        return []


def faiss_search(query: str, limit: int = 50) -> Dict[int, float]:
    """FAISS semantic search, returns {db_id: similarity_score}"""
    if _faiss_index is None or _embedding_model is None:
        return {}
    try:
        import numpy as np
        emb = _embedding_model.encode([query], normalize_embeddings=True)
        emb = emb.astype('float32')
        scores, indices = _faiss_index.search(emb, limit)
        result = {}
        for score, idx in zip(scores[0], indices[0]):
            if idx >= 0 and idx in _faiss_id_map:
                entry = _faiss_id_map[idx]
                result[entry['id']] = float(score)
        return result
    except Exception as e:
        log.error(f"FAISS search error: {e}")
        return {}


def hybrid_search(db, query: str, filter_type: str = 'all', limit: int = 20):
    """
    Hybrid search combining FTS5 (BM25) + FAISS.
    Score = 0.4 * bm25_norm + 0.6 * faiss_sim
    """
    t0 = time.time()
    quran_results = []
    hadis_results = []

    # FTS5 search
    if filter_type in ('all', 'quran'):
        fts_quran = fts5_search_quran(db, query, limit=100)
    else:
        fts_quran = []

    if filter_type in ('all', 'hadis'):
        fts_hadis = fts5_search_hadis(db, query, limit=100)
    else:
        fts_hadis = []

    # FAISS semantic search
    faiss_scores = faiss_search(query, limit=100)

    # --- Merge Quran ---
    if filter_type in ('all', 'quran'):
        bm25_max = max((s for _, s in fts_quran), default=1.0)
        quran_score_map: Dict[int, float] = {}

        for qid, bm25 in fts_quran:
            bm25_norm = normalize_score(bm25, 0, bm25_max)
            fscore = faiss_scores.get(qid, 0.0)
            quran_score_map[qid] = 0.4 * bm25_norm + 0.6 * fscore

        # Add FAISS-only results
        for fid, fscore in faiss_scores.items():
            entry = _faiss_id_map.get(fid, {}) if _faiss_id_map else {}
            if entry.get('tipe') == 'quran' and fid not in quran_score_map:
                quran_score_map[fid] = 0.6 * fscore

        # Fetch top rows
        top_ids = sorted(quran_score_map, key=lambda x: -quran_score_map[x])[:limit]
        if top_ids:
            placeholders = ','.join('?' * len(top_ids))
            rows = db.execute(
                f"SELECT * FROM quran WHERE id IN ({placeholders})", top_ids
            ).fetchall()
            id_to_row = {r['id']: r for r in rows}
            for qid in top_ids:
                row = id_to_row.get(qid)
                if row:
                    quran_results.append({
                        'id': row['id'],
                        'surah': row['surah'],
                        'ayat': row['ayat'],
                        'nama_surah': row['nama_surah'],
                        'nama_latin': row['nama_latin'],
                        'arab': row['arab'],
                        'terjemahan': row['terjemahan'],
                        'highlight': highlight_text(row['terjemahan'], query),
                        'skor': round(quran_score_map[qid], 4),
                    })

    # --- Merge Hadis ---
    if filter_type in ('all', 'hadis'):
        bm25_max_h = max((s for _, s in fts_hadis), default=1.0)
        hadis_score_map: Dict[int, float] = {}

        for hid, bm25 in fts_hadis:
            bm25_norm = normalize_score(bm25, 0, bm25_max_h)
            fscore = faiss_scores.get(hid, 0.0)
            hadis_score_map[hid] = 0.4 * bm25_norm + 0.6 * fscore

        top_ids_h = sorted(hadis_score_map, key=lambda x: -hadis_score_map[x])[:limit]
        if top_ids_h:
            placeholders = ','.join('?' * len(top_ids_h))
            rows = db.execute(
                f"SELECT * FROM hadis WHERE id IN ({placeholders})", top_ids_h
            ).fetchall()
            id_to_row_h = {r['id']: r for r in rows}
            for hid in top_ids_h:
                row = id_to_row_h.get(hid)
                if row:
                    hadis_results.append({
                        'id': row['id'],
                        'kitab': row['kitab'],
                        'nomor': row['nomor'],
                        'bab': row['bab'],
                        'arab': row['arab'],
                        'terjemahan': row['terjemahan'],
                        'highlight': highlight_text(row['terjemahan'], query),
                        'skor': round(hadis_score_map[hid], 4),
                    })

    took_ms = round((time.time() - t0) * 1000, 2)
    return {
        'query': query,
        'filter': filter_type,
        'total_quran': len(quran_results),
        'total_hadis': len(hadis_results),
        'quran': quran_results,
        'hadis': hadis_results,
        'took_ms': took_ms,
    }
