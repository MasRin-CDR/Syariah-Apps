Buatkan sistem deteksi Tajwid otomatis untuk aplikasi “Syariah App”.

Tujuan:
- Mendeteksi hukum tajwid secara otomatis pada teks Al Quran
- Memberikan highlight warna sesuai hukum tajwid
- Real-time rendering
- Support Arabic Unicode
- Responsive Android & Desktop

==================================================
FITUR UTAMA
==================================================

Sistem harus mampu:
- Parsing huruf arab
- Mendeteksi Nun Sukun
- Mendeteksi Tanwin
- Mendeteksi Mim Sukun
- Mendeteksi Tasydid
- Mendeteksi Lam Ta’rif
- Memberikan warna otomatis sesuai hukum tajwid

Gunakan:
- JavaScript / TypeScript
- Regex Unicode Arabic
- Rule-based engine
- Modular tajwid parser

==================================================
RULE TAJWID
==================================================

A. HUKUM NUN SUKUN & TANWIN

Deteksi:
- نْ
- ً
- ٌ
- ٍ

--------------------------------------------------
1. IDZHAR
--------------------------------------------------

Warna:
#006633

Kondisi:
Nun sukun atau tanwin bertemu:
ء ه ح خ ع غ

Label:
Idzhar

--------------------------------------------------
2. IDGHAM BIGHUNNAH
--------------------------------------------------

Warna:
#009933

Kondisi:
Nun sukun atau tanwin bertemu:
ي و م ن

Label:
Idgham Bighunnah

--------------------------------------------------
3. IDGHAM BILAGHUNNAH
--------------------------------------------------

Warna:
#339966

Kondisi:
Nun sukun atau tanwin bertemu:
ل ر

Label:
Idgham Bilaghunnah

--------------------------------------------------
4. IQLAB
--------------------------------------------------

Warna:
#33CC66

Kondisi:
Nun sukun atau tanwin bertemu:
ب

Label:
Iqlab

--------------------------------------------------
5. IKHFA’
--------------------------------------------------

Warna:
#33CC33

Kondisi:
Nun sukun atau tanwin bertemu:
ت ث ج د ذ ز س ش ص ض ط ظ ف ق ك

Label:
Ikhfa’

==================================================
B. HUKUM MIM SUKUN
==================================================

Deteksi:
مْ

--------------------------------------------------
1. IKHFA’ SYAFAWI
--------------------------------------------------

Warna:
#990000

Kondisi:
Mim sukun bertemu:
ب

Label:
Ikhfa’ Syafawi

--------------------------------------------------
2. IDGHAM MIMI
--------------------------------------------------

Warna:
#CC3300

Kondisi:
Mim sukun bertemu:
م

Label:
Idgham Mimi

--------------------------------------------------
3. IDZHAR SYAFAWI
--------------------------------------------------

Warna:
#FF0000

Kondisi:
Mim sukun bertemu selain:
م dan ب

Label:
Idzhar Syafawi

==================================================
C. GHUNNAH
==================================================

Deteksi:
- مّ
- نّ

Warna:
#FF6600

Label:
Ghunnah

==================================================
D. LAM TA’RIF
==================================================

Deteksi:
ال

--------------------------------------------------
1. IDZHAR QOMARIYAH
--------------------------------------------------

Warna:
#666633

Kondisi:
Lam Ta’rif bertemu:
ء ب غ ح خ ك و ج ف ع ق ي م ه

Label:
Idzhar Qomariyah

--------------------------------------------------
2. IKHFA’ SYAMSIYAH
--------------------------------------------------

Warna:
#333333

Kondisi:
Lam Ta’rif bertemu:
ر ز د ذ ت ث س ش ص ض ط ظ ل ن

Label:
Ikhfa’ Syamsiyah

==================================================
FITUR RENDERING
==================================================

Tampilkan:
- Highlight warna langsung pada ayat
- Tooltip nama hukum tajwid
- Hover effect
- Klik untuk detail hukum
- Legend warna tajwid

Contoh:
- Hijau = Idzhar
- Merah = Ghunnah
- dll

==================================================
IMPLEMENTASI
==================================================

Gunakan:
- Unicode-aware regex
- Modular rule engine
- Parser pipeline
- Tokenization Arabic text

Flow:
1. Input ayat
2. Normalize unicode
3. Scan huruf per huruf
4. Deteksi pola tajwid
5. Render span berwarna
6. Tampilkan tooltip hukum

==================================================
CONTOH OUTPUT HTML
==================================================

Gunakan format:

<span class="tajwid-idzhar">مِنْ هَادٍ</span>

atau:

<span style="color:#006633">
مِنْ هَادٍ
</span>

==================================================
KOMPONEN UI
==================================================

Tambahkan:
- Tajwid legend panel
- Toggle on/off tajwid
- Responsive typography
- Arabic font support
- Dark mode support

Gunakan font:
- Amiri
- Noto Naskh Arabic
- Scheherazade New

==================================================
PERFORMA
==================================================

Optimasi:
- Real-time parsing
- Fast rendering
- Lazy processing
- Efficient regex
- Debounce update

Harus mampu:
- Render seluruh ayat panjang
- Tidak lag di Android
- Support ribuan ayat

==================================================
OUTPUT YANG DIINGINKAN
==================================================

Generate:
- Tajwid detection engine
- Regex tajwid lengkap
- Modular parser
- HTML renderer
- React component
- Tailwind styling
- Tooltip tajwid
- Color mapping
- Dark mode support
- Production-ready structure