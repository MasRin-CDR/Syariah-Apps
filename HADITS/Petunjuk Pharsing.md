Buatkan sistem parser metadata Hadis untuk aplikasi “Syariah App” agar dapat membaca struktur kitab, nomor hadis, dan heading bab secara otomatis.

==================================================
FORMAT DATA HADIS
==================================================

Contoh input:

صحيح البخاري ١:
Shahih Bukhari 1:

Permulaan Wahyu

==================================================
RULE PARSING
==================================================

Format:

[Nama Kitab Arab] [Nomor Hadis]:
[Nama Kitab Latin] [Nomor Hadis]:

Contoh:

صحيح البخاري ١:
Shahih Bukhari 1:

Harus diparsing menjadi:

- Nama Kitab Arab:
  صحيح البخاري

- Nama Kitab Latin:
  Shahih Bukhari

- Nomor Hadis:
  1

==================================================
HEADING SYSTEM
==================================================

Heading 1 setelah metadata adalah:
Nama Bab Kitab Hadis

Contoh:

Permulaan Wahyu

Maka parser harus mendeteksi:
- Heading level 1
- Judul Bab Hadis

==================================================
OUTPUT TAMPILAN
==================================================

Tampilkan metadata hadis modern seperti:

Shahih Bukhari • Hadis No. 1

atau:

Shahih Bukhari (1)

Tampilkan heading bab:

# Permulaan Wahyu

==================================================
STRUKTUR DATA
==================================================

Gunakan struktur:

{
  "kitab_ar": "صحيح البخاري",
  "kitab_latin": "Shahih Bukhari",
  "hadith_number": 1,
  "bab_title": "Permulaan Wahyu"
}

==================================================
PARSER ENGINE
==================================================

Gunakan:
- Regex parser
- Unicode Arabic support
- Metadata extraction
- Heading detection

Flow:
1. Deteksi nama kitab arab
2. Deteksi nama kitab latin
3. Ekstrak nomor hadis
4. Deteksi heading bab
5. Simpan metadata
6. Render UI otomatis

==================================================
REGEX YANG DIBUTUHKAN
==================================================

Deteksi metadata hadis:

^.+?\d+:

Deteksi heading:
- line setelah metadata
- heading pertama dianggap nama bab

==================================================
UI STYLE
==================================================

Style mengikuti:
- Hadits NU Online
- Quran NU Online

Karakter:
- Minimalis
- Reading-focused
- Bersih
- Elegant
- Nyaman dibaca lama

==================================================
LAYOUT HADIS
==================================================

Tampilkan:

- Nama kitab
- Nomor hadis
- Nama bab
- Teks arab hadis
- Terjemahan Indonesia
- Footnote jika ada

Gunakan:
- Card reading layout
- Soft border
- Modern spacing
- Responsive typography

==================================================
TYPOGRAPHY
==================================================

Arabic:
- Amiri
- Noto Naskh Arabic
- Scheherazade New

Latin:
- Inter
- Source Sans Pro

==================================================
FITUR TAMBAHAN
==================================================

Tambahkan:
- Bookmark hadis
- Copy hadis
- Share hadis
- Sticky bab navigation
- Quick jump nomor hadis
- Search dalam kitab
- Related hadis

==================================================
SEARCH SUPPORT
==================================================

Metadata harus terintegrasi dengan:
- FTS5
- BM25
- FAISS

Agar user dapat mencari:
- nomor hadis
- nama kitab
- nama bab
- isi hadis
- semantic meaning

==================================================
DATABASE STRUCTURE
==================================================

Tabel Hadis:

- id
- kitab_ar
- kitab_latin
- bab
- nomor
- arab
- terjemahan
- footnote
- embedding

==================================================
RESPONSIVE DESIGN
==================================================

Aplikasi harus:
- Nyaman di Android
- Nyaman di desktop
- Reading optimized
- Smooth scrolling

==================================================
OUTPUT YANG DIINGINKAN
==================================================

Generate:
- Hadis metadata parser
- Bab heading parser
- Regex extraction
- React component
- Tailwind styling
- Metadata renderer
- Responsive hadis page
- Production-ready architecture