#!/usr/bin/env python3
"""
Syariah App — Al Quran .docx Parser
Parses 114 surah .docx files into structured data
"""

import re
import sys
import os
import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple

log = logging.getLogger(__name__)

# Surah metadata: id -> (nama_arab, nama_latin, nama_indo, jumlah_ayat, jenis, juz_awal)
SURAH_META = {
    1:  ("الفاتحة","Al-Fatihah","Pembukaan",7,"Makkiyah",1),
    2:  ("البقرة","Al-Baqarah","Sapi Betina",286,"Madaniyah",1),
    3:  ("آل عمران","Ali Imran","Keluarga Imran",200,"Madaniyah",3),
    4:  ("النساء","An-Nisa'","Wanita",176,"Madaniyah",4),
    5:  ("المائدة","Al-Ma'idah","Hidangan",120,"Madaniyah",6),
    6:  ("الأنعام","Al-An'am","Binatang Ternak",165,"Makkiyah",7),
    7:  ("الأعراف","Al-A'raf","Tempat Tertinggi",206,"Makkiyah",8),
    8:  ("الأنفال","Al-Anfal","Rampasan Perang",75,"Madaniyah",9),
    9:  ("التوبة","At-Taubah","Pengampunan",129,"Madaniyah",10),
    10: ("يونس","Yunus","Nabi Yunus",109,"Makkiyah",11),
    11: ("هود","Hud","Nabi Hud",123,"Makkiyah",11),
    12: ("يوسف","Yusuf","Nabi Yusuf",111,"Makkiyah",12),
    13: ("الرعد","Ar-Ra'd","Guruh",43,"Madaniyah",13),
    14: ("إبراهيم","Ibrahim","Nabi Ibrahim",52,"Makkiyah",13),
    15: ("الحجر","Al-Hijr","Batu",99,"Makkiyah",14),
    16: ("النحل","An-Nahl","Lebah",128,"Makkiyah",14),
    17: ("الإسراء","Al-Isra'","Perjalanan Malam",111,"Makkiyah",15),
    18: ("الكهف","Al-Kahf","Gua",110,"Makkiyah",15),
    19: ("مريم","Maryam","Maryam",98,"Makkiyah",16),
    20: ("طه","Taha","Ta Ha",135,"Makkiyah",16),
    21: ("الأنبياء","Al-Anbiya'","Para Nabi",112,"Makkiyah",17),
    22: ("الحج","Al-Hajj","Haji",78,"Madaniyah",17),
    23: ("المؤمنون","Al-Mu'minun","Orang Beriman",118,"Makkiyah",18),
    24: ("النور","An-Nur","Cahaya",64,"Madaniyah",18),
    25: ("الفرقان","Al-Furqan","Pembeda",77,"Makkiyah",18),
    26: ("الشعراء","Asy-Syu'ara","Para Penyair",227,"Makkiyah",19),
    27: ("النمل","An-Naml","Semut",93,"Makkiyah",19),
    28: ("القصص","Al-Qasas","Cerita",88,"Makkiyah",20),
    29: ("العنكبوت","Al-'Ankabut","Laba-laba",69,"Makkiyah",20),
    30: ("الروم","Ar-Rum","Bangsa Romawi",60,"Makkiyah",21),
    31: ("لقمان","Luqman","Luqman",34,"Makkiyah",21),
    32: ("السجدة","As-Sajdah","Sujud",30,"Makkiyah",21),
    33: ("الأحزاب","Al-Ahzab","Golongan Bersekutu",73,"Madaniyah",21),
    34: ("سبأ","Saba'","Kaum Saba",54,"Makkiyah",22),
    35: ("فاطر","Fatir","Pencipta",45,"Makkiyah",22),
    36: ("يس","Ya Sin","Ya Sin",83,"Makkiyah",22),
    37: ("الصافات","As-Saffat","Barisan",182,"Makkiyah",23),
    38: ("ص","Sad","Sad",88,"Makkiyah",23),
    39: ("الزمر","Az-Zumar","Rombongan",75,"Makkiyah",23),
    40: ("غافر","Gafir","Yang Maha Pengampun",85,"Makkiyah",24),
    41: ("فصلت","Fussilat","Yang Dijelaskan",54,"Makkiyah",24),
    42: ("الشورى","Asy-Syura","Musyawarah",53,"Makkiyah",25),
    43: ("الزخرف","Az-Zukhruf","Perhiasan",89,"Makkiyah",25),
    44: ("الدخان","Ad-Dukhan","Kabut",59,"Makkiyah",25),
    45: ("الجاثية","Al-Jasiyah","Yang Berlutut",37,"Makkiyah",25),
    46: ("الأحقاف","Al-Ahqaf","Bukit Pasir",35,"Makkiyah",26),
    47: ("محمد","Muhammad","Nabi Muhammad",38,"Madaniyah",26),
    48: ("الفتح","Al-Fath","Kemenangan",29,"Madaniyah",26),
    49: ("الحجرات","Al-Hujurat","Kamar",18,"Madaniyah",26),
    50: ("ق","Qaf","Qaf",45,"Makkiyah",26),
    51: ("الذاريات","Az-Zariyat","Angin Berputar",60,"Makkiyah",26),
    52: ("الطور","At-Tur","Bukit",49,"Makkiyah",27),
    53: ("النجم","An-Najm","Bintang",62,"Makkiyah",27),
    54: ("القمر","Al-Qamar","Bulan",55,"Makkiyah",27),
    55: ("الرحمن","Ar-Rahman","Yang Maha Pemurah",78,"Madaniyah",27),
    56: ("الواقعة","Al-Waqi'ah","Hari Kiamat",96,"Makkiyah",27),
    57: ("الحديد","Al-Hadid","Besi",29,"Madaniyah",27),
    58: ("المجادلة","Al-Mujadalah","Wanita yang Mengajukan Gugatan",22,"Madaniyah",28),
    59: ("الحشر","Al-Hasyr","Pengusiran",24,"Madaniyah",28),
    60: ("الممتحنة","Al-Mumtahanah","Wanita yang Diuji",13,"Madaniyah",28),
    61: ("الصف","As-Saff","Satu Barisan",14,"Madaniyah",28),
    62: ("الجمعة","Al-Jumu'ah","Hari Jumat",11,"Madaniyah",28),
    63: ("المنافقون","Al-Munafiqun","Orang Munafik",11,"Madaniyah",28),
    64: ("التغابن","At-Tagabun","Hari Ditampakkan Kesalahan",18,"Madaniyah",28),
    65: ("الطلاق","At-Talaq","Talak",12,"Madaniyah",28),
    66: ("التحريم","At-Tahrim","Mengharamkan",12,"Madaniyah",28),
    67: ("الملك","Al-Mulk","Kerajaan",30,"Makkiyah",29),
    68: ("القلم","Al-Qalam","Pena",52,"Makkiyah",29),
    69: ("الحاقة","Al-Haqqah","Hari Kiamat",52,"Makkiyah",29),
    70: ("المعارج","Al-Ma'arij","Tempat Naik",44,"Makkiyah",29),
    71: ("نوح","Nuh","Nabi Nuh",28,"Makkiyah",29),
    72: ("الجن","Al-Jin","Jin",28,"Makkiyah",29),
    73: ("المزمل","Al-Muzammil","Orang Berselimut",20,"Makkiyah",29),
    74: ("المدثر","Al-Mudassir","Orang Berkemul",56,"Makkiyah",29),
    75: ("القيامة","Al-Qiyamah","Hari Kiamat",40,"Makkiyah",29),
    76: ("الإنسان","Al-Insan","Manusia",31,"Madaniyah",29),
    77: ("المرسلات","Al-Mursalat","Malaikat yang Diutus",50,"Makkiyah",29),
    78: ("النبأ","An-Naba'","Berita Besar",40,"Makkiyah",30),
    79: ("النازعات","An-Nazi'at","Malaikat yang Mencabut",46,"Makkiyah",30),
    80: ("عبس","'Abasa","Ia Bermuka Masam",42,"Makkiyah",30),
    81: ("التكوير","At-Takwir","Menggulung",29,"Makkiyah",30),
    82: ("الإنفطار","Al-Infitar","Terbelah",19,"Makkiyah",30),
    83: ("المطففين","Al-Mutaffifin","Orang yang Curang",36,"Makkiyah",30),
    84: ("الإنشقاق","Al-Insyiqaq","Terbelah",25,"Makkiyah",30),
    85: ("البروج","Al-Buruj","Gugusan Bintang",22,"Makkiyah",30),
    86: ("الطارق","At-Tariq","Yang Datang di Malam Hari",17,"Makkiyah",30),
    87: ("الأعلى","Al-A'la","Yang Paling Tinggi",19,"Makkiyah",30),
    88: ("الغاشية","Al-Gasyiyah","Hari Pembalasan",26,"Makkiyah",30),
    89: ("الفجر","Al-Fajr","Fajar",30,"Makkiyah",30),
    90: ("البلد","Al-Balad","Negeri",20,"Makkiyah",30),
    91: ("الشمس","Asy-Syams","Matahari",15,"Makkiyah",30),
    92: ("الليل","Al-Lail","Malam",21,"Makkiyah",30),
    93: ("الضحى","Ad-Duha","Waktu Duha",11,"Makkiyah",30),
    94: ("الشرح","Al-Insyirah","Lapang Dada",8,"Makkiyah",30),
    95: ("التين","At-Tin","Buah Tin",8,"Makkiyah",30),
    96: ("العلق","Al-'Alaq","Segumpal Darah",19,"Makkiyah",30),
    97: ("القدر","Al-Qadr","Kemuliaan",5,"Makkiyah",30),
    98: ("البينة","Al-Bayyinah","Bukti Nyata",8,"Madaniyah",30),
    99: ("الزلزلة","Az-Zalzalah","Guncangan",8,"Madaniyah",30),
    100:("العاديات","Al-'Adiyat","Kuda Perang",11,"Makkiyah",30),
    101:("القارعة","Al-Qari'ah","Hari Kiamat",11,"Makkiyah",30),
    102:("التكاثر","At-Takasur","Bermegah-megahan",8,"Makkiyah",30),
    103:("العصر","Al-'Asr","Masa",3,"Makkiyah",30),
    104:("الهمزة","Al-Humazah","Pengumpat",9,"Makkiyah",30),
    105:("الفيل","Al-Fil","Gajah",5,"Makkiyah",30),
    106:("قريش","Al-Quraisy","Suku Quraisy",4,"Makkiyah",30),
    107:("الماعون","Al-Ma'un","Barang yang Berguna",7,"Makkiyah",30),
    108:("الكوثر","Al-Kausar","Nikmat yang Berlimpah",3,"Makkiyah",30),
    109:("الكافرون","Al-Kafirun","Orang Kafir",6,"Makkiyah",30),
    110:("النصر","An-Nasr","Pertolongan",3,"Madaniyah",30),
    111:("المسد","Al-Lahab","Gejolak Api",5,"Makkiyah",30),
    112:("الإخلاص","Al-Ikhlas","Ikhlas",4,"Makkiyah",30),
    113:("الفلق","Al-Falaq","Waktu Subuh",5,"Makkiyah",30),
    114:("الناس","An-Nas","Manusia",6,"Makkiyah",30),
}

# Juz ranges: juz -> (surah_start, ayat_start, surah_end, ayat_end)
JUZ_AYAT_MAP = {
    1:(1,1,2,141), 2:(2,142,2,252), 3:(2,253,3,92), 4:(3,93,4,23),
    5:(4,24,4,147), 6:(4,148,5,81), 7:(5,82,6,110), 8:(6,111,7,87),
    9:(7,88,8,40), 10:(8,41,9,92), 11:(9,93,11,5), 12:(11,6,12,52),
    13:(12,53,14,52), 14:(15,1,16,128), 15:(17,1,18,74), 16:(18,75,20,135),
    17:(21,1,22,78), 18:(23,1,25,20), 19:(25,21,27,55), 20:(27,56,29,45),
    21:(29,46,33,30), 22:(33,31,36,27), 23:(36,28,39,31), 24:(39,32,41,46),
    25:(41,47,45,37), 26:(46,1,51,30), 27:(51,31,57,29), 28:(58,1,66,12),
    29:(67,1,77,50), 30:(78,1,114,6),
}


def get_juz(surah: int, ayat: int) -> int:
    """Determine juz number for a given surah:ayat"""
    for juz, (ss, sa, es, ea) in JUZ_AYAT_MAP.items():
        if surah > ss or (surah == ss and ayat >= sa):
            if surah < es or (surah == es and ayat <= ea):
                return juz
    return 30


def extract_surah_number_from_filename(filename: str) -> Optional[int]:
    """Extract surah number from filename like '2. Al - Baqarah.docx'"""
    m = re.match(r'^(\d+)\.', Path(filename).name)
    return int(m.group(1)) if m else None


def clean_text(text: str) -> str:
    """Clean text from extra whitespace"""
    if not text:
        return ''
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def parse_quran_docx(file_path: str) -> List[Dict]:
    """
    Parse a single surah .docx file.
    Returns list of dicts with: surah, ayat, arab, terjemahan, tafsir, juz, nama_surah, nama_latin
    """
    try:
        from docx import Document
    except ImportError:
        log.error("python-docx not installed. Run: pip install python-docx")
        return []

    surah_num = extract_surah_number_from_filename(file_path)
    if not surah_num:
        log.warning(f"Cannot determine surah number from: {file_path}")
        return []

    meta = SURAH_META.get(surah_num)
    if not meta:
        log.warning(f"No metadata for surah {surah_num}")
        return []

    nama_arab, nama_latin, nama_indo, jumlah_ayat, jenis, juz_awal = meta

    try:
        doc = Document(file_path)
    except Exception as e:
        log.error(f"Cannot open {file_path}: {e}")
        return []

    ayat_list = []
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

    # State machine parsing
    i = 0
    current_arab = ''
    current_terjemahan = ''
    current_tafsir_parts = []
    current_ayat_num = None
    in_tafsir = False

    # Pattern: ( SurahArab/surahNum:ayatNum )
    meta_pattern = re.compile(r'\(\s*[\u0600-\u06FF\s]+/\s*\d+\s*:\s*(\d+)\s*\)')
    # Pattern: Arabic text (contains Arabic chars)
    arabic_pattern = re.compile(r'[\u0600-\u06FF]')
    # Pattern: footnote marker like "4)"
    footnote_pattern = re.compile(r'\d+\)\s*$')

    def save_current():
        nonlocal current_arab, current_terjemahan, current_tafsir_parts, current_ayat_num, in_tafsir
        if current_ayat_num and current_terjemahan:
            tafsir = ' '.join(current_tafsir_parts).strip()
            tafsir = re.sub(r'\d+\)', '', tafsir).strip()
            juz = get_juz(surah_num, current_ayat_num)
            ayat_list.append({
                'surah': surah_num,
                'ayat': current_ayat_num,
                'arab': clean_text(current_arab),
                'terjemahan': clean_text(current_terjemahan),
                'tafsir': clean_text(tafsir) if tafsir else None,
                'juz': juz,
                'nama_surah': nama_arab,
                'nama_latin': nama_latin,
            })
        current_arab = ''
        current_terjemahan = ''
        current_tafsir_parts = []
        current_ayat_num = None
        in_tafsir = False

    for para in paragraphs:
        # Check for ayat metadata marker
        meta_match = meta_pattern.search(para)
        if meta_match:
            save_current()
            current_ayat_num = int(meta_match.group(1))
            in_tafsir = False
            continue

        if current_ayat_num is None:
            continue

        # If contains Arabic, likely Arabic text
        if arabic_pattern.search(para) and not current_arab:
            current_arab = para
            continue

        # Translation: typically the first non-arabic paragraph after arab
        if current_arab and not current_terjemahan and not arabic_pattern.search(para):
            # Remove footnote markers from translation
            terjemahan = re.sub(r'\s*\d+\)\s*', '', para).strip()
            if terjemahan:
                current_terjemahan = terjemahan
                continue

        # Rest is tafsir
        if current_terjemahan and para:
            current_tafsir_parts.append(para)

    # Save last
    save_current()

    log.info(f"  Surah {surah_num} ({nama_latin}): {len(ayat_list)} ayat parsed")
    return ayat_list


def parse_all_quran(surat_dir: str) -> List[Dict]:
    """Parse all 114 surah files"""
    surat_path = Path(surat_dir)
    files = sorted(surat_path.glob('*.docx'), key=lambda f: extract_surah_number_from_filename(f.name) or 999)

    all_ayat = []
    for docx_file in tqdm(files, desc="Parsing Quran", ncols=80):
        ayat = parse_quran_docx(str(docx_file))
        all_ayat.extend(ayat)

    log.info(f"Total ayat parsed: {len(all_ayat)}")
    return all_ayat


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
    surat_dir = r"e:\Syariah Apps\AL - QUR'AN\SURAT"
    results = parse_all_quran(surat_dir)
    print(f"Total: {len(results)} ayat")
    if results:
        print("Sample:", results[0])
