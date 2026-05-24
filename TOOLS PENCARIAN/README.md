==================================================
ARSITEKTUR SEARCH ENGINE
==================================================

Buat hybrid intelligent search engine dengan flow berikut:

1. User memasukkan query
2. Query preprocessing:
   - tokenize
   - normalize
   - stemming
   - typo correction
3. Query dikirim ke:
   - SQLite FTS5
   - BM25 ranking
   - FAISS vector search
4. Hasil digabung menggunakan:
   - Reciprocal Rank Fusion (RRF)
5. Post-processing:
   - highlight keyword
   - filter Quran/Hadis
   - sorting relevansi
   - search history
6. Tampilkan hasil ranking terbaik

==================================================
SEARCH PIPELINE
==================================================

Flow arsitektur:

Query Input
↓
Query Preprocessing
↓
FTS5 + BM25 + FAISS
↓
Score Fusion (RRF)
↓
Highlight + Filter + Sorting
↓
Search Results

==================================================
STACK LIBRARY
==================================================

Gunakan stack berikut:

Python 3.10+

Full Text Search:
- sqlite3
- FTS5
- python-fts (opsional)

Konfigurasi:
- tokenizer unicode61
- porter stemmer

BM25 Ranking:
- rank-bm25
- alternatif: whoosh

Semantic Search:
- faiss-cpu
- sentence-transformers

Embedding model:
- paraphrase-multilingual-MiniLM-L6-v2

Karena harus support:
- Bahasa Indonesia
- Bahasa Arab

FAISS index:
- IndexFlatL2 untuk dataset kecil
- IndexIVFFlat untuk dataset besar

Typo tolerance:
- rapidfuzz

Keyword highlight:
- regex / re

==================================================
SCORE FUSION
==================================================

Gunakan:
Reciprocal Rank Fusion (RRF)

Formula:

score = Σ 1 / (k + rank_i)

Tujuan:
- Menggabungkan hasil:
  - FTS5
  - BM25
  - FAISS

Agar:
- hasil lebih relevan
- semantic search lebih akurat
- ranking lebih stabil

==================================================
FITUR SEARCH ENGINE
==================================================

Fitur wajib:

- Full text search
- Semantic search
- Typo correction
- Highlight keyword
- Search history
- Filter Quran/Hadis
- Relevance score
- Source label
- Ranking terbaik
- Real-time search
- Debounce input
- Infinite scroll
- Lazy loading

==================================================
DATABASE
==================================================

Gunakan SQLite/PostgreSQL.

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

Tabel Search History:
- id
- query
- created_at

==================================================
TOOLS PENCARIAN UI
==================================================

Halaman search memiliki:

- Search bar besar modern
- Glassmorphism search panel
- Tabs:
  - Quran
  - Hadis
  - Semua

==================================================
HASIL PENCARIAN
==================================================

Pisahkan hasil:

1. Hasil Quran
2. Hasil Hadis

Tabel Quran:
| No | Ayat | Terjemah Singkat | Relevansi | Direktori |

Tabel Hadis:
| No | Hadis | Terjemahan Singkat | Relevansi | Direktori |

Direktori:
- tombol menuju detail ayat/hadis

==================================================
POST PROCESSING
==================================================

Tambahkan:
- Keyword markup
- Snippet preview
- Highlight hasil
- Sorting:
   - relevansi
   - terbaru
- Filtering:
   - Quran
   - Hadis
- Search history

==================================================
DATA LAYER
==================================================

Gunakan:
- SQLite DB
- FTS5 tables
- FAISS vector index
- Embedding storage

==================================================
IMPORT DATA
==================================================

Database sumber berasal dari file Word (.docx).

Buat importer otomatis:
- Parsing docx
- Extract Arabic text
- Extract terjemahan
- Normalisasi unicode
- Generate FTS5 index
- Generate embedding FAISS

Gunakan:
- python-docx
- sqlalchemy
- sentence-transformers
- faiss-cpu

==================================================
UI/UX STYLE
==================================================

Desain:
- futuristic islamic dashboard
- dark elegant
- rounded 2xl
- smooth hover
- glow accent
- modern typography
- Arabic font support
- responsive mobile desktop

Gunakan:
- TailwindCSS
- Framer Motion
- clean spacing
- modern card system

==================================================
OUTPUT YANG DIINGINKAN
==================================================

Generate:
- Struktur project scalable
- Frontend modern
- Backend FastAPI
- Hybrid search engine
- FAISS integration
- BM25 integration
- FTS5 integration
- Importer script
- API endpoint
- Database schema
- Responsive UI
- Android + desktop support
- Clean architecture
- Production-ready codebase
