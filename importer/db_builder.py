#!/usr/bin/env python3
"""
Syariah App — Database Builder
Builds syariah.db from parsed Al Quran and Hadis data
"""

import sqlite3
import sys
import logging
from pathlib import Path
from tqdm import tqdm

log = logging.getLogger(__name__)

SCHEMA_PATH = Path(__file__).parent.parent / 'database' / 'schema.sql'
DEFAULT_DB = Path(__file__).parent.parent / 'database' / 'syariah.db'


def init_database(db_path: str) -> sqlite3.Connection:
    """Initialize database with schema"""
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA cache_size=-64000")

    with open(SCHEMA_PATH, encoding='utf-8') as f:
        conn.executescript(f.read())

    log.info(f"Database initialized: {db_path}")
    return conn


def insert_surah_metadata(conn: sqlite3.Connection, surah_meta: dict):
    """Insert surah metadata"""
    rows = []
    for sid, (nama_arab, nama_latin, nama_indo, jumlah_ayat, jenis, juz_awal) in surah_meta.items():
        rows.append((sid, nama_arab, nama_latin, nama_indo, jumlah_ayat, jenis, juz_awal, sid))

    conn.executemany("""
        INSERT OR REPLACE INTO surah (id, nama_arab, nama_latin, nama_indo, jumlah_ayat, jenis, juz_awal, urutan)
        VALUES (?,?,?,?,?,?,?,?)
    """, rows)
    conn.commit()
    log.info(f"Inserted {len(rows)} surah metadata")


def insert_quran(conn: sqlite3.Connection, ayat_list: list):
    """Insert Al Quran ayat in batches"""
    BATCH = 200
    total = 0
    existing = set(
        (r[0], r[1]) for r in conn.execute("SELECT surah, ayat FROM quran")
    )

    batch = []
    for ayat in tqdm(ayat_list, desc="Inserting Quran", ncols=80):
        key = (ayat['surah'], ayat['ayat'])
        if key in existing:
            continue
        batch.append((
            ayat['surah'], ayat['ayat'], ayat['arab'], ayat['terjemahan'],
            ayat.get('tafsir'), ayat['juz'], None,
            ayat['nama_surah'], ayat['nama_latin']
        ))
        existing.add(key)

        if len(batch) >= BATCH:
            conn.executemany("""
                INSERT OR IGNORE INTO quran
                (surah, ayat, arab, terjemahan, tafsir, juz, halaman, nama_surah, nama_latin)
                VALUES (?,?,?,?,?,?,?,?,?)
            """, batch)
            conn.commit()
            total += len(batch)
            batch = []

    if batch:
        conn.executemany("""
            INSERT OR IGNORE INTO quran
            (surah, ayat, arab, terjemahan, tafsir, juz, halaman, nama_surah, nama_latin)
            VALUES (?,?,?,?,?,?,?,?,?)
        """, batch)
        conn.commit()
        total += len(batch)

    log.info(f"Total Quran ayat inserted: {total}")
    return total


def build_fts_index(conn: sqlite3.Connection):
    """Rebuild FTS5 indexes"""
    log.info("Rebuilding FTS5 indexes...")
    conn.execute("INSERT INTO quran_fts(quran_fts) VALUES('rebuild')")
    conn.execute("INSERT INTO hadis_fts(hadis_fts) VALUES('rebuild')")
    conn.commit()
    log.info("FTS5 rebuild complete")


def print_stats(conn: sqlite3.Connection):
    """Print database statistics"""
    quran_count = conn.execute("SELECT COUNT(*) FROM quran").fetchone()[0]
    hadis_count = conn.execute("SELECT COUNT(*) FROM hadis").fetchone()[0]
    surah_count = conn.execute("SELECT COUNT(*) FROM surah").fetchone()[0]
    print(f"\n{'='*50}")
    print(f"Database Statistics:")
    print(f"  Surah metadata : {surah_count}")
    print(f"  Al Quran ayat  : {quran_count:,}")
    print(f"  Hadis          : {hadis_count:,}")
    print(f"{'='*50}\n")


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Build Syariah App database')
    parser.add_argument('--db', default=str(DEFAULT_DB))
    parser.add_argument('--quran-dir', default=r"e:\Syariah Apps\AL - QUR'AN\SURAT")
    parser.add_argument('--hadis-src', default=r"e:\Syariah Apps\HADITS\HaditsSoft.db")
    parser.add_argument('--skip-quran', action='store_true')
    parser.add_argument('--skip-hadis', action='store_true')
    parser.add_argument('--rebuild-fts', action='store_true')
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler('import.log', encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )

    conn = init_database(args.db)

    if not args.skip_quran:
        from docx_parser import parse_all_quran, SURAH_META
        insert_surah_metadata(conn, SURAH_META)
        ayat_list = parse_all_quran(args.quran_dir)
        insert_quran(conn, ayat_list)

    if not args.skip_hadis:
        from haditssoft_extractor import extract_hadis
        extract_hadis(args.hadis_src, args.db)

    if args.rebuild_fts:
        build_fts_index(conn)

    print_stats(conn)
    conn.close()
    log.info("✅ Database build complete!")


if __name__ == '__main__':
    main()
