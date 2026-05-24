Buatkan sistem parser ayat Al Quran untuk aplikasi “Syariah App” dengan format pembacaan, metadata ayat, dan footnote tafsir otomatis.

==================================================
FORMAT DATA
==================================================

Contoh input:

( البقرة/2:1)

Alif Lām Mīm. 4)

==================================================
RULE PARSING
==================================================

Format:

( NamaSurat/NomorSurat:NomorAyat )

Contoh:
( البقرة/2:1 )

Harus diparsing menjadi:

- Nama Surat:
  البقرة

- Nomor Surat:
  2

- Nomor Ayat:
  1

==================================================
OUTPUT TAMPILAN
==================================================

Tampilkan menjadi format modern:

Surat Al-Baqarah • Ayat 1

atau:

Al-Baqarah (2:1)

==================================================
FOOTNOTE SYSTEM
==================================================

Jika ditemukan angka dengan format:

4)

Maka:
- Angka tersebut adalah referensi footnote tafsir Kemenag
- Harus dijadikan superscript clickable
- Footnote tampil di bawah ayat

==================================================
CONTOH
==================================================

Input:

Alif Lām Mīm. 4)

Output render:

Alif Lām Mīm.<sup>4</sup>

==================================================
FOOTNOTE AREA
==================================================

Di bawah ayat tampilkan:

4. Tafsir Kemenag:
[isi tafsir]

Gunakan style:
- ukuran kecil
- border kiri lembut
- italic ringan
- warna secondary text
- mudah dibaca

==================================================
FITUR FOOTNOTE
==================================================

Tambahkan:
- Klik superscript scroll ke footnote
- Hover tooltip preview tafsir
- Expand/collapse tafsir
- Multiple footnote support
- Dark mode support

==================================================
STRUKTUR DATA
==================================================

Buat struktur data seperti:

{
  "surah_name_ar": "البقرة",
  "surah_number": 2,
  "ayah_number": 1,
  "text": "Alif Lām Mīm.",
  "footnotes": [
    {
      "id": 4,
      "source": "Tafsir Kemenag",
      "content": "..."
    }
  ]
}

==================================================
PARSING ENGINE
==================================================

Gunakan:
- Regex parsing
- Unicode Arabic support
- Footnote extraction
- Metadata extraction

Flow:
1. Deteksi metadata surat
2. Ekstrak nomor surat & ayat
3. Bersihkan footnote marker
4. Generate superscript
5. Render footnote section

==================================================
REGEX YANG DIBUTUHKAN
==================================================

Deteksi metadata ayat:

\(.*?\/\d+:\d+\)

Deteksi footnote:

\d+\)

==================================================
UI STYLE
==================================================

Style mengikuti:
- Quran NU Online
- Hadits NU Online

Karakter:
- Clean
- Reading focused
- Elegant
- Minimalis
- Typography nyaman

==================================================
TYPOGRAPHY
==================================================

Gunakan:
Arabic:
- Amiri
- Noto Naskh Arabic

Latin:
- Inter
- Source Sans Pro

==================================================
RENDER STYLE
==================================================

Ayat:
- font besar
- spacing lega
- line-height nyaman

Footnote:
- lebih kecil
- subtle color
- modern academic style

==================================================
FITUR TAMBAHAN
==================================================

Tambahkan:
- Copy ayat tanpa footnote
- Copy lengkap dengan footnote
- Toggle footnote
- Responsive mobile
- Sticky footnote navigation
- Lazy render footnote panjang

==================================================
TECH STACK
==================================================

Frontend:
- React / Next.js
- TailwindCSS

Backend:
- FastAPI

Parser:
- JavaScript regex
- Python regex

==================================================
OUTPUT YANG DIINGINKAN
==================================================

Generate:
- Ayat parser
- Footnote parser
- Metadata extractor
- React component
- Footnote component
- Tailwind styling
- Scroll interaction
- Tooltip tafsir
- Production-ready implementation