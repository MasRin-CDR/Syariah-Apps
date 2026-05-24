# 🕌 Syariah App

> Aplikasi Islami Modern — Al Quran, Hadis, Pencarian Cerdas & Kalkulator Waris

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Android%20%7C%20Desktop-blue.svg)](#)
[![Stack](https://img.shields.io/badge/Stack-React%20%2B%20FastAPI%20%2B%20SQLite-brightgreen.svg)](#)
[![Status](https://img.shields.io/badge/Status-In%20Development-yellow.svg)](#)

---

## 📖 Tentang Aplikasi

**Syariah App** adalah aplikasi Islami modern yang dirancang untuk mendampingi ibadah dan kajian sehari-hari. Dibangun dengan arsitektur *clean*, *scalable*, dan *production-ready*, mendukung platform **Android** dan **Desktop (Windows/macOS/Linux)**.

### Fitur Utama

| Fitur | Deskripsi |
|-------|-----------|
| 📗 **Al Quran** | Baca Al Quran lengkap dengan teks Arab, terjemahan, dan tafsir Kemenag |
| 📙 **Hadis** | Akses 9 Kitab Hadis Shahih dengan terjemahan Indonesia |
| 🔍 **Pencarian Cerdas** | Mesin pencari semantik menggunakan FTS5 + BM25 + FAISS |
| ⚖️ **Kalkulator Waris** | Hitung pembagian warisan sesuai hukum faraid Islam |

---

## 🖥️ Platform yang Didukung

- ✅ **Desktop** — Windows, macOS, Linux (via Electron)
- ✅ **Android** — via Capacitor / React Native
- 🌐 **Web** — Berjalan di browser modern

---

## 🎨 Desain & UI

Tampilan **Islamic Futuristic** dengan nuansa:
- 🟢 Hijau Emerald sebagai warna utama
- 🟡 Gold accent untuk elemen premium
- 🌙 Dark mode elegan
- ✨ Glassmorphism & smooth animation
- 📱 Fully responsive (mobile-first)

---

## 🛠️ Teknologi

### Frontend
```
React + Next.js         → Web & SSR
TailwindCSS             → Styling utility-first
Framer Motion           → Animasi halus
Electron                → Desktop wrapper
Capacitor               → Android wrapper
```

### Backend
```
Python FastAPI          → REST API modern & cepat
SQLAlchemy              → ORM database
Pydantic                → Validasi data
Uvicorn                 → ASGI server
```

### Database & Search Engine
```
SQLite / PostgreSQL     → Penyimpanan utama
FTS5                    → Full-text search
BM25                    → Ranking relevansi
FAISS                   → Semantic vector search
Sentence Transformers   → Embedding teks
```

---

## 📁 Struktur Proyek

```
syariah-app/
├── frontend/                   # Antarmuka pengguna
│   ├── components/             # Komponen React reusable
│   │   ├── quran/              # Komponen Al Quran
│   │   ├── hadis/              # Komponen Hadis
│   │   ├── search/             # Komponen Pencarian
│   │   └── waris/              # Komponen Kalkulator Waris
│   ├── pages/                  # Halaman utama (Next.js)
│   ├── services/               # API service layer
│   ├── hooks/                  # Custom React hooks
│   ├── utils/                  # Helper functions
│   └── styles/                 # Global styles & Tailwind config
│
├── backend/                    # Server FastAPI
│   ├── api/                    # Endpoint API
│   │   ├── quran.py            # API Al Quran
│   │   ├── hadis.py            # API Hadis
│   │   ├── search.py           # API Pencarian
│   │   └── waris.py            # API Kalkulator Waris
│   ├── models/                 # Model database
│   ├── services/               # Business logic
│   ├── security/               # Auth & middleware
│   └── main.py                 # Entry point FastAPI
│
├── database/                   # Database & migrasi
│   ├── schema.sql              # Skema tabel
│   ├── migrations/             # Migrasi database
│   └── seeds/                  # Data awal
│
├── search_engine/              # Mesin pencari
│   ├── fts5/                   # Full-text search index
│   ├── bm25/                   # BM25 ranking
│   └── faiss/                  # Vector similarity index
│
├── importer/                   # Tools import data
│   ├── docx_parser.py          # Parser file Word
│   ├── db_builder.py           # Builder database
│   ├── indexer.py              # Generator search index
│   └── embedding_gen.py        # Generator FAISS embedding
│
├── assets/                     # Aset statis
│   ├── fonts/                  # Font Arab & Latin
│   ├── icons/                  # Ikon aplikasi
│   └── images/                 # Gambar & ilustrasi
│
├── electron/                   # Konfigurasi Electron (Desktop)
├── capacitor/                  # Konfigurasi Capacitor (Android)
├── docker/                     # Docker config
├── docs/                       # Dokumentasi
├── tests/                      # Unit & integration test
├── .env.example                # Contoh environment variable
├── docker-compose.yml          # Docker Compose
├── package.json                # Dependensi frontend
├── requirements.txt            # Dependensi backend Python
└── README.md
```

---

## 🗄️ Skema Database

### Tabel `quran`
```sql
CREATE TABLE quran (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    surah       INTEGER NOT NULL,           -- Nomor surah (1-114)
    ayat        INTEGER NOT NULL,           -- Nomor ayat
    arab        TEXT    NOT NULL,           -- Teks Arab (UTF-8)
    terjemahan  TEXT    NOT NULL,           -- Terjemahan Indonesia
    tafsir      TEXT,                       -- Tafsir Kemenag
    juz         INTEGER NOT NULL,           -- Juz (1-30)
    halaman     INTEGER,                    -- Halaman mushaf
    nama_surah  TEXT    NOT NULL,           -- Nama surah
    nama_latin  TEXT    NOT NULL            -- Nama latin surah
);

-- FTS5 Virtual Table
CREATE VIRTUAL TABLE quran_fts USING fts5(
    arab, terjemahan, tafsir,
    content='quran', content_rowid='id'
);
```

### Tabel `hadis`
```sql
CREATE TABLE hadis (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    kitab       TEXT    NOT NULL,           -- Nama kitab hadis
    bab         TEXT    NOT NULL,           -- Judul bab
    nomor       INTEGER NOT NULL,           -- Nomor hadis
    arab        TEXT    NOT NULL,           -- Teks Arab
    terjemahan  TEXT    NOT NULL,           -- Terjemahan Indonesia
    perawi      TEXT,                       -- Nama perawi
    kualitas    TEXT                        -- Shahih/Hasan/Dhaif
);

-- FTS5 Virtual Table
CREATE VIRTUAL TABLE hadis_fts USING fts5(
    arab, terjemahan, bab,
    content='hadis', content_rowid='id'
);
```

### Tabel `bookmark`
```sql
CREATE TABLE bookmark (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    tipe        TEXT NOT NULL,              -- 'quran' | 'hadis'
    referensi   INTEGER NOT NULL,          -- ID konten
    catatan     TEXT,                      -- Catatan pengguna
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Tabel `riwayat_baca`
```sql
CREATE TABLE riwayat_baca (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    tipe        TEXT NOT NULL,              -- 'quran' | 'hadis'
    referensi   INTEGER NOT NULL,
    posisi      TEXT,                       -- Posisi scroll
    updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔌 API Endpoint

### Al Quran
```
GET  /api/quran/surah               → Daftar semua surah
GET  /api/quran/surah/{id}          → Detail surah + ayat
GET  /api/quran/ayat/{surah}/{ayat} → Detail satu ayat
GET  /api/quran/juz/{nomor}         → Ayat berdasarkan juz
GET  /api/quran/tafsir/{surah}/{ayat} → Tafsir ayat
```

### Hadis
```
GET  /api/hadis/kitab               → Daftar kitab hadis
GET  /api/hadis/kitab/{nama}        → List bab dalam kitab
GET  /api/hadis/bab/{kitab}/{bab}   → List hadis dalam bab
GET  /api/hadis/{id}                → Detail satu hadis
```

### Pencarian
```
GET  /api/search?q={query}          → Pencarian semua
GET  /api/search/quran?q={query}    → Pencarian Al Quran saja
GET  /api/search/hadis?q={query}    → Pencarian Hadis saja
GET  /api/search/history            → Riwayat pencarian
```

### Bookmark & Riwayat
```
GET  /api/bookmark                  → Semua bookmark
POST /api/bookmark                  → Tambah bookmark
DELETE /api/bookmark/{id}           → Hapus bookmark
GET  /api/riwayat                   → Riwayat baca terakhir
POST /api/riwayat                   → Update riwayat baca
```

---

## 🚀 Cara Menjalankan

### Prasyarat
- Node.js >= 18
- Python >= 3.10
- Git

### 1. Clone Repositori
```bash
git clone https://github.com/MasRin-CDR/Syariah-Apps.git
cd syariah-app
```

### 2. Setup Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Salin konfigurasi environment
cp .env.example .env

# Jalankan server
uvicorn main:app --reload --port 8000
```

### 3. Import Database
```bash
cd importer

# Taruh file .docx di folder data/
mkdir data
# → Salin file Al Quran dan Hadis .docx ke sini

# Jalankan importer
python docx_parser.py
python db_builder.py
python indexer.py
python embedding_gen.py
```

> ⏳ Proses embedding FAISS membutuhkan waktu beberapa menit tergantung ukuran data.

### 4. Setup Frontend
```bash
cd frontend
npm install
npm run dev                     # Buka http://localhost:3000
```

### 5. Jalankan Desktop (Electron)
```bash
cd frontend
npm run electron:dev            # Mode development
npm run electron:build          # Build installer
```

### 6. Build Android (Capacitor)
```bash
cd frontend
npm run build
npx cap sync android
npx cap open android            # Buka di Android Studio
```

---

## ⚙️ Environment Variables

Buat file `.env` di folder `backend/`:
```env
# Database
DATABASE_URL=sqlite:///./syariah.db

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=true

# FAISS
FAISS_INDEX_PATH=./search_engine/faiss/index.bin
EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L12-v2

# Security
SECRET_KEY=ganti-dengan-secret-key-aman
ALLOWED_ORIGINS=http://localhost:3000
```

---

## 📦 Dependensi Utama

### Python (backend)
```
fastapi
uvicorn
sqlalchemy
python-docx
sentence-transformers
faiss-cpu
pydantic
python-multipart
aiofiles
```

### Node.js (frontend)
```
next
react
tailwindcss
framer-motion
electron
@capacitor/core
axios
zustand
```

---

## 🤝 Kontribusi

Kontribusi sangat disambut! Silakan:

1. **Fork** repositori ini
2. Buat **branch** fitur baru: `git checkout -b fitur/nama-fitur`
3. **Commit** perubahan: `git commit -m 'feat: tambah fitur X'`
4. **Push** ke branch: `git push origin fitur/nama-fitur`
5. Buka **Pull Request**

### Konvensi Commit
```
feat:     Fitur baru
fix:      Perbaikan bug
docs:     Perubahan dokumentasi
style:    Perubahan style/formatting
refactor: Refaktor kode
test:     Penambahan test
```

---

## 📄 Lisensi

Proyek ini dilisensikan di bawah **MIT License** — lihat file [LICENSE](LICENSE) untuk detail.

---

## 🙏 Ucapan Terima Kasih

- Data Al Quran & terjemahan: Kementerian Agama RI
- Tafsir: Tafsir Kemenag
- Hadis: Kitab-kitab hadis shahih
- Inspirasi UI: [quran.nu.or.id](https://quran.nu.or.id)

---

<div align="center">

**Bismillahirrahmanirrahim**

*Semoga aplikasi ini menjadi amal jariyah yang bermanfaat*

⭐ Jika bermanfaat, berikan bintang pada repositori ini ⭐

</div>
