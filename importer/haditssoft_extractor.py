#!/usr/bin/env python3
"""
Syariah App — HaditsSoft.db Extractor
Extracts hadis data from HaditsSoft.db into syariah.db
"""

import sqlite3
import sys
import os
import logging
from pathlib import Path
from tqdm import tqdm

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('import.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
log = logging.getLogger(__name__)

KITAB_MAP = {
    'Bukhari':  ('Shahih Bukhari',           'صحيح البخاري',  'BabBukhari',  'KitabBukhari'),
    'Muslim':   ('Shahih Muslim',            'صحيح مسلم',     'BabMuslim',   'KitabMuslim'),
    'AbuDawud': ('Sunan Abu Daud',           'سنن أبي داود',   'BabAbuDawud', 'KitabAbuDawud'),
    'Tirmidzi': ('Sunan Tirmidzi',           'سنن الترمذي',   'BabTirmidzi', 'KitabTirmidzi'),
    'AnNasai':  ('Sunan An-Nasai',           'سنن النسائي',   'BabAnNasai',  'KitabAnNasai'),
    'IbnuMajah':('Sunan Ibnu Majah',         'سنن ابن ماجة',  'BabIbnuMajah','KitabIbnuMajah'),
    'Malik':    ("Muwattha' Imam Malik",     'موطأ مالك',     'BabMalik',    'KitabMalik'),
    'Ahmad':    ('Musnad Ahmad',             'مسند أحمد',     'BabAhmad',    'KitabAhmad'),
    'AdDarimi': ('Sunan Ad-Darimi',          'سنن الدارمي',   'BabAdDarimi', 'KitabAdDarimi'),
}


def extract_hadis(src_db: str, dst_db: str):
    """Extract all hadis from HaditsSoft.db into syariah.db"""
    log.info(f"Opening source: {src_db}")
    src = sqlite3.connect(src_db)
    src.row_factory = sqlite3.Row
    src_cur = src.cursor()

    log.info(f"Opening destination: {dst_db}")
    dst = sqlite3.connect(dst_db)
    dst.execute("PRAGMA journal_mode=WAL")
    dst.execute("PRAGMA synchronous=NORMAL")

    # Apply schema
    schema_path = Path(__file__).parent.parent / 'database' / 'schema.sql'
    if schema_path.exists():
        with open(schema_path, encoding='utf-8') as f:
            dst.executescript(f.read())
        log.info("Schema applied")
    else:
        log.warning("Schema file not found, tables must exist already")

    total_inserted = 0

    for table_key, (kitab_name, kitab_arab, bab_table, kitab_table) in KITAB_MAP.items():
        log.info(f"\n--- Processing: {kitab_name} ---")

        # Load bab index: VMemberBab -> bab name
        bab_index = {}
        try:
            src_cur.execute(f'SELECT VMemberBab, NBab, NBabArab FROM "{bab_table}" ORDER BY VMemberBab')
            for row in src_cur.fetchall():
                bab_index[row[0]] = {
                    'name': row[1] or '',
                    'arab': row[2] or ''
                }
        except Exception as e:
            log.error(f"Failed to load bab for {kitab_name}: {e}")

        # Load kitab index: VMember -> kitab section name
        kitab_index = {}
        try:
            src_cur.execute(f'SELECT VMember, NKitab, NKitabArab FROM "{kitab_table}" ORDER BY VMember')
            for row in src_cur.fetchall():
                kitab_index[row[0]] = {
                    'name': row[1] or '',
                    'arab': row[2] or ''
                }
        except Exception as e:
            log.error(f"Failed to load kitab sections for {kitab_name}: {e}")

        # Load hadis rows
        try:
            src_cur.execute(f"""
                SELECT Nomer, Arabic, Indonesia, Albani, Darussalam, VSelectedK, VSelectedB
                FROM "{table_key}"
                ORDER BY Nomer
            """)
            rows = src_cur.fetchall()
        except Exception as e:
            log.error(f"Failed to fetch hadis from {table_key}: {e}")
            continue

        # Check existing
        existing = set()
        for row in dst.execute("SELECT kitab, nomor FROM hadis WHERE kitab=?", (kitab_name,)):
            existing.add(row[1])

        batch = []
        for row in tqdm(rows, desc=kitab_name, ncols=80):
            nomor = row[0]
            if nomor in existing:
                continue

            arabic = (row[1] or '').strip()
            terjemahan = (row[2] or '').strip()
            kualitas = None

            # Determine quality from Albani or Darussalam
            albani = str(row[3] or '')
            darussalam = str(row[4] or '')
            if albani:
                kualitas = albani
            elif darussalam:
                kualitas = darussalam

            vk = row[5] or 1
            vb = row[6] or 1

            bab_info = bab_index.get(vb, {'name': '', 'arab': ''})
            kitab_info = kitab_index.get(vk, {'name': kitab_name, 'arab': kitab_arab})

            batch.append((
                kitab_name,
                kitab_arab,
                bab_info['name'],
                bab_info['arab'],
                nomor,
                arabic,
                terjemahan,
                '',  # perawi
                kualitas,
                vk,
                vb
            ))

            if len(batch) >= 500:
                dst.executemany("""
                    INSERT OR IGNORE INTO hadis
                    (kitab, kitab_arab, bab, bab_arab, nomor, arab, terjemahan, perawi, kualitas, kitab_no, bab_no)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?)
                """, batch)
                dst.commit()
                total_inserted += len(batch)
                batch = []

        if batch:
            dst.executemany("""
                INSERT OR IGNORE INTO hadis
                (kitab, kitab_arab, bab, bab_arab, nomor, arab, terjemahan, perawi, kualitas, kitab_no, bab_no)
                VALUES (?,?,?,?,?,?,?,?,?,?,?)
            """, batch)
            dst.commit()
            total_inserted += len(batch)

        log.info(f"  Inserted for {kitab_name}: done")

    src.close()
    dst.close()
    log.info(f"\n✅ Total hadis inserted: {total_inserted}")
    return total_inserted


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Extract HaditsSoft.db -> syariah.db')
    parser.add_argument('--src', default=r'e:\Syariah Apps\HADITS\HaditsSoft.db')
    parser.add_argument('--dst', default=r'e:\Syariah Apps\database\syariah.db')
    args = parser.parse_args()
    extract_hadis(args.src, args.dst)
