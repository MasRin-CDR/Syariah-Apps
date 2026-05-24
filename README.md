Buatkan aplikasi modern bernama “Syariah App” yang mendukung platform:
- Desktop / Laptop
- Android

Gunakan arsitektur scalable, clean architecture, modular, dan production-ready.

==================================================
KONSEP UTAMA
==================================================

Aplikasi islami modern untuk:
- Membaca Al Quran
- Membaca Hadis
- Tools pencarian cerdas
- Kalkulator waris

Design UI:
- Modern
- Minimalis
- Elegan
- Islamic futuristic
- Smooth animation
- Responsive
- Dark mode support
- Mobile friendly
- Desktop friendly

Gunakan:
Frontend:
- React / Next.js / React Native / Electron (sesuaikan agar support Android + Desktop)

Backend:
- Python FastAPI

Database:
- SQLite / PostgreSQL

Search Engine:
- FTS5
- BM25
- FAISS semantic search

==================================================
HALAMAN AWAL / WELCOME SCREEN
==================================================

Saat aplikasi dibuka tampilkan halaman welcome modern dengan:
- Logo Syariah App
- Background islami futuristik
- Animasi lembut
- Tombol masuk menu utama

Tampilkan 4 menu utama berbentuk card/grid modern:

1. Al Quran
2. Hadis
3. Tools Pencarian
4. Kalkulator Waris

==================================================
MENU 1 : AL QURAN
==================================================

Di dalam menu Al Quran terdapat:

- Surah
- Juz
- Riwayat

Fitur:
- List seluruh surah
- Detail ayat
- Arabic text
- Terjemahan Indonesia
- Tafsir Lengkap Kemenag
- Bookmark
- Last read ( masukkan ke Riwayat )
- Pencarian ayat
- Copy Ayat
- Share Ayat

Kategori:
- Berdasarkan Surah
- Berdasarkan Juz

UI:
- Nyaman dibaca
- Typography arab bagus
- Smooth scrolling
- Responsive

==================================================
MENU 2 : HADIS
==================================================

Menu Hadis berisi:
- 9 Kitab Hadis

Contoh:
- Shahih Bukhari
- Shahih Muslim
- Sunan Abu Dawud
- Tirmidzi
- Nasai
- Ibnu Majah
- Malik
- Ahmad
- Darimi

Fitur:
- List kitab
- Bab hadis ( Di Dalam File Tiap hadis, Heading 1 )
- Isi hadis arab
- Terjemahan Indonesia
- Bookmark
- Copy hadis
- Share hadis

==================================================
MENU 3 : TOOLS PENCARIAN
==================================================

Buat sistem pencarian islami pintar.

Tampilan:
- Search bar besar di atas
- Modern search experience
- Real-time search
- Debounce search
- Loading indicator

User dapat mengetik:
contoh:
- sholat
- sabar
- zakat
- riba
- puasa

==================================================
HASIL PENCARIAN
==================================================

Pisahkan hasil menjadi 2 tabel:

1. Hasil Al Quran
2. Hasil Hadis

----------------------------------------
TABEL AL QURAN
----------------------------------------

Kolom:
- No
- Ayat
- Terjemah Singkat
- Relevansi
- Direktori

Direktori:
- Tombol menuju ayat terkait

Contoh:
| No | Ayat | Terjemah Singkat | Relevansi | Direktori |

----------------------------------------
TABEL HADIS
----------------------------------------

Kolom:
- No
- Hadis
- Terjemahan Singkat
- Relevansi
- Direktori

Direktori:
- Tombol menuju hadis terkait

==================================================
FITUR SEARCH ENGINE
==================================================

Gunakan kombinasi:
- SQLite FTS5
- BM25 ranking
- FAISS vector similarity

Tujuan:
- Search cepat
- Search relevan
- Semantic search
- Mendukung typo ringan
- Mendukung pencarian konteks

Sistem:
1. FTS5 untuk full text search
2. BM25 untuk ranking relevansi
3. FAISS untuk semantic similarity embedding

Tambahkan:
- Highlight keyword
- Search history
- Recent search
- Filter Quran/Hadis
- Sorting relevansi

==================================================
MENU 4 : KALKULATOR WARIS
==================================================

Sudah tersedia:
- HTML
- CSS
- JavaScript

Integrasikan ke aplikasi utama.

==================================================
TEKNOLOGI YANG DIHARAPKAN
==================================================

Frontend:
- React
- TailwindCSS
- Framer Motion

Backend:
- FastAPI

Database:
- SQLite/PostgreSQL

Search:
- FTS5
- BM25
- Sentence Transformer
- FAISS

Mobile/Desktop:
- Electron untuk desktop
- React Native / Capacitor untuk Android

==================================================
STRUKTUR PROJECT
==================================================

Gunakan struktur scalable:

/frontend
/backend
/database
/search_engine
/assets
/components
/services
/utils
/security
/api

==================================================
FITUR TAMBAHAN
==================================================

Tambahkan:
- Offline mode
- Cache database lokal
- Dark mode
- Bookmark
- Last read
- Riwayat pencarian
- Copy/share ayat & hadis
- Loading skeleton
- Error handling
- Security basic
- Clean code
- API modular
- Reusable component

==================================================
DESAIN
==================================================

Nuansa:
- Hijau emerald
- Gold accent
- Dark elegant
- Glassmorphism
- Islamic modern tech

Gunakan:
- Rounded modern UI
- Smooth transition
- Elegant typography
- Soft shadow
- Futuristic dashboard feel

==================================================
OUTPUT YANG DIINGINKAN
==================================================

Generate:
- Struktur project lengkap
- Arsitektur aplikasi
- UI modern
- Backend API
- Sistem search engine
- Integrasi FAISS + BM25 + FTS5
- Responsive Android/Desktop
- Contoh database schema
- Contoh endpoint API
- Contoh implementasi pencarian
- Contoh UI hasil pencarian
- Best practice production-ready
==================================================
SUMBER DATABASE
==================================================

Database konten sudah tersedia dalam bentuk file Word (.docx).

Isi database meliputi:
- Al Quran
- Terjemahan
- Hadis
- Terjemahan hadis

Tugas sistem:
- Parsing data dari file Word
- Konversi otomatis ke SQLite/PostgreSQL
- Membuat struktur tabel yang rapi
- Membersihkan formatting
- Menyesuaikan encoding arab & unicode
- Membuat indexing search

==================================================
PROSES IMPORT DATA
==================================================

Buat module import data otomatis:

Fitur:
- Import .docx
- Extract text arab & indonesia
- Mapping struktur ayat/hadis
- Simpan ke database
- Generate FTS5 index
- Generate embedding FAISS

Gunakan Python:
- python-docx
- sqlite3 / sqlalchemy
- sentence-transformers
- faiss-cpu

==================================================
STRUKTUR DATABASE YANG DIHARAPKAN
==================================================

Tabel Quran:
- id
- surah
- ayat
- arab
- terjemahan
- tafsir
- juz
- halaman

Tabel Hadis:
- id
- kitab
- bab
- nomor
- arab
- terjemahan

==================================================
SEARCH INDEXING
==================================================

Setelah import selesai:
- Generate FTS5 table
- Generate BM25 ranking
- Generate vector embedding FAISS

Tujuan:
- Search cepat
- Search relevan
- Semantic search
- Support typo ringan
- Support pencarian konteks

==================================================
PARSING RULE
==================================================

Pastikan:
- Unicode arab aman
- Harakat tidak rusak
- RTL support
- Ayat dan hadis tidak terpotong
- Nomor ayat/hadis terdeteksi otomatis
- Encoding UTF-8

==================================================
OUTPUT IMPORTER
==================================================

Generate:
- Script importer Python
- Auto database builder
- Auto indexing
- Error handling
- Logging import
- Duplicate detection
- Progress bar import
