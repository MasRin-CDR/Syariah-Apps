-- ============================================================
-- Syariah App — Database Schema
-- ============================================================

-- Al Quran
CREATE TABLE IF NOT EXISTS quran (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    surah       INTEGER NOT NULL,
    ayat        INTEGER NOT NULL,
    arab        TEXT    NOT NULL,
    terjemahan  TEXT    NOT NULL,
    tafsir      TEXT,
    juz         INTEGER NOT NULL DEFAULT 1,
    halaman     INTEGER,
    nama_surah  TEXT    NOT NULL,
    nama_latin  TEXT    NOT NULL,
    UNIQUE(surah, ayat)
);

CREATE INDEX IF NOT EXISTS idx_quran_surah ON quran(surah);
CREATE INDEX IF NOT EXISTS idx_quran_juz ON quran(juz);

-- FTS5 for Al Quran
CREATE VIRTUAL TABLE IF NOT EXISTS quran_fts USING fts5(
    arab, terjemahan, tafsir,
    content='quran', content_rowid='id'
);

-- Triggers to keep FTS in sync
CREATE TRIGGER IF NOT EXISTS quran_ai AFTER INSERT ON quran BEGIN
    INSERT INTO quran_fts(rowid, arab, terjemahan, tafsir) VALUES (new.id, new.arab, new.terjemahan, new.tafsir);
END;

CREATE TRIGGER IF NOT EXISTS quran_ad AFTER DELETE ON quran BEGIN
    INSERT INTO quran_fts(quran_fts, rowid, arab, terjemahan, tafsir) VALUES ('delete', old.id, old.arab, old.terjemahan, old.tafsir);
END;

CREATE TRIGGER IF NOT EXISTS quran_au AFTER UPDATE ON quran BEGIN
    INSERT INTO quran_fts(quran_fts, rowid, arab, terjemahan, tafsir) VALUES ('delete', old.id, old.arab, old.terjemahan, old.tafsir);
    INSERT INTO quran_fts(rowid, arab, terjemahan, tafsir) VALUES (new.id, new.arab, new.terjemahan, new.tafsir);
END;

-- ============================================================
-- Surah Metadata
-- ============================================================
CREATE TABLE IF NOT EXISTS surah (
    id          INTEGER PRIMARY KEY,
    nama_arab   TEXT NOT NULL,
    nama_latin  TEXT NOT NULL,
    nama_indo   TEXT NOT NULL,
    jumlah_ayat INTEGER NOT NULL,
    jenis       TEXT NOT NULL CHECK(jenis IN ('Makkiyah','Madaniyah')),
    juz_awal    INTEGER NOT NULL,
    urutan      INTEGER NOT NULL
);

-- ============================================================
-- Hadis
-- ============================================================
CREATE TABLE IF NOT EXISTS hadis (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    kitab       TEXT    NOT NULL,
    kitab_arab  TEXT,
    bab         TEXT    NOT NULL,
    bab_arab    TEXT,
    nomor       INTEGER NOT NULL,
    arab        TEXT    NOT NULL,
    terjemahan  TEXT    NOT NULL,
    perawi      TEXT,
    kualitas    TEXT,
    kitab_no    INTEGER,
    bab_no      INTEGER
);

CREATE INDEX IF NOT EXISTS idx_hadis_kitab ON hadis(kitab);
CREATE INDEX IF NOT EXISTS idx_hadis_kitab_bab ON hadis(kitab, bab_no);

-- FTS5 for Hadis
CREATE VIRTUAL TABLE IF NOT EXISTS hadis_fts USING fts5(
    arab, terjemahan, bab,
    content='hadis', content_rowid='id'
);

CREATE TRIGGER IF NOT EXISTS hadis_ai AFTER INSERT ON hadis BEGIN
    INSERT INTO hadis_fts(rowid, arab, terjemahan, bab) VALUES (new.id, new.arab, new.terjemahan, new.bab);
END;

CREATE TRIGGER IF NOT EXISTS hadis_ad AFTER DELETE ON hadis BEGIN
    INSERT INTO hadis_fts(hadis_fts, rowid, arab, terjemahan, bab) VALUES ('delete', old.id, old.arab, old.terjemahan, old.bab);
END;

-- ============================================================
-- Bookmark & Riwayat
-- ============================================================
CREATE TABLE IF NOT EXISTS bookmark (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    tipe        TEXT    NOT NULL CHECK(tipe IN ('quran','hadis')),
    referensi   INTEGER NOT NULL,
    catatan     TEXT,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(tipe, referensi)
);

CREATE TABLE IF NOT EXISTS riwayat_baca (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    tipe        TEXT    NOT NULL CHECK(tipe IN ('quran','hadis')),
    referensi   INTEGER NOT NULL,
    posisi      TEXT,
    updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(tipe, referensi)
);

CREATE TABLE IF NOT EXISTS search_history (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    query       TEXT NOT NULL,
    filter_type TEXT DEFAULT 'all',
    result_count INTEGER DEFAULT 0,
    searched_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
