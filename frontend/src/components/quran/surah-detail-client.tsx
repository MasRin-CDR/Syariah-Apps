'use client';

import Link from 'next/link';
import { AnimatePresence, motion } from 'framer-motion';
import {
  ArrowLeft,
  Bookmark,
  BookmarkCheck,
  Check,
  Clipboard,
  ScrollText,
  Share2,
} from 'lucide-react';
import { useEffect, useMemo, useState, type ReactNode } from 'react';

interface Ayat {
  id: number;
  surah: number;
  ayat: number;
  arab: string;
  terjemahan: string;
  tafsir?: string;
  juz: number;
  nama_surah: string;
  nama_latin: string;
}

interface SurahMeta {
  id: number;
  nama_arab: string;
  nama_latin: string;
  nama_indo: string;
  jumlah_ayat: number;
  jenis: string;
  juz_awal: number;
}

interface SurahDetailClientProps {
  surahId: number;
}

const API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const fontSizes = {
  sm: 'text-arabic-sm',
  md: 'text-arabic-md',
  lg: 'text-arabic-xl',
} as const;

type FontSize = keyof typeof fontSizes;

function formatAyatText(ayat: Ayat) {
  return `${ayat.arab}\n\n${ayat.terjemahan}\n\n(${ayat.nama_latin}: ${ayat.ayat})`;
}

export function SurahDetailClient({ surahId }: SurahDetailClientProps) {
  const [surah, setSurah] = useState<SurahMeta | null>(null);
  const [ayatList, setAyatList] = useState<Ayat[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showTafsir, setShowTafsir] = useState<number | null>(null);
  const [bookmarks, setBookmarks] = useState<Set<number>>(new Set());
  const [copied, setCopied] = useState<number | null>(null);
  const [shared, setShared] = useState<number | null>(null);
  const [fontSize, setFontSize] = useState<FontSize>('md');

  useEffect(() => {
    let ignore = false;

    async function fetchSurahDetail() {
      try {
        setLoading(true);
        setError(null);

        const response = await fetch(`${API}/api/quran/surah/${surahId}`);

        if (!response.ok) {
          throw new Error('Gagal memuat detail surah.');
        }

        const payload = await response.json();

        if (!ignore) {
          setSurah(payload.surah || null);
          setAyatList(payload.ayat || []);
        }
      } catch (err) {
        if (!ignore) {
          setError(err instanceof Error ? err.message : 'Gagal memuat detail surah.');
        }
      } finally {
        if (!ignore) {
          setLoading(false);
        }
      }
    }

    fetchSurahDetail();

    const savedBookmarks = JSON.parse(localStorage.getItem('bookmarks_quran') || '[]') as number[];
    setBookmarks(new Set(savedBookmarks));

    return () => {
      ignore = true;
    };
  }, [surahId]);

  const navigation = useMemo(
    () => ({
      previous: surahId > 1 ? surahId - 1 : null,
      next: surahId < 114 ? surahId + 1 : null,
    }),
    [surahId],
  );

  async function copyAyat(ayat: Ayat) {
    try {
      await navigator.clipboard.writeText(formatAyatText(ayat));
      setCopied(ayat.id);
      window.setTimeout(() => setCopied(null), 1800);
    } catch {
      setCopied(null);
    }
  }

  async function shareAyat(ayat: Ayat) {
    const text = formatAyatText(ayat);

    try {
      if (navigator.share) {
        await navigator.share({
          title: `${ayat.nama_latin}: ${ayat.ayat}`,
          text,
        });
      } else {
        await navigator.clipboard.writeText(text);
      }

      setShared(ayat.id);
      window.setTimeout(() => setShared(null), 1800);
    } catch {
      setShared(null);
    }
  }

  function toggleBookmark(ayatId: number) {
    setBookmarks((current) => {
      const next = new Set(current);

      if (next.has(ayatId)) {
        next.delete(ayatId);
      } else {
        next.add(ayatId);
      }

      localStorage.setItem('bookmarks_quran', JSON.stringify([...next]));
      return next;
    });
  }

  return (
    <main className="min-h-screen bg-night-bg text-white">
      <header className="sticky top-0 z-30 border-b border-night-border bg-night-bg/86 backdrop-blur-xl">
        <div className="mx-auto flex max-w-3xl items-center gap-3 px-4 py-3">
          <Link
            href="/quran"
            className="inline-flex h-9 w-9 items-center justify-center rounded-lg border border-white/10 text-night-muted transition hover:border-emerald-300 hover:text-emerald-200 focus:outline-none focus:ring-2 focus:ring-emerald-400"
            aria-label="Kembali ke daftar surah"
            title="Kembali ke daftar surah"
          >
            <ArrowLeft className="h-4 w-4" aria-hidden="true" />
          </Link>
          <div className="min-w-0 flex-1">
            <h1 className="truncate text-base font-bold text-white">{surah?.nama_latin || `Surah ${surahId}`}</h1>
            <p className="truncate text-xs text-night-muted">
              {surah ? `${surah.nama_indo} - ${surah.jumlah_ayat} ayat - ${surah.jenis}` : 'Memuat detail surah'}
            </p>
          </div>
          <div className="flex items-center gap-1">
            {(['sm', 'md', 'lg'] as const).map((size) => (
              <button
                key={size}
                type="button"
                onClick={() => setFontSize(size)}
                className={`h-8 w-8 rounded-lg text-center font-bold transition focus:outline-none focus:ring-2 focus:ring-emerald-400 ${
                  fontSize === size
                    ? 'bg-emerald-500 text-white'
                    : 'text-night-muted hover:bg-white/10 hover:text-white'
                } ${size === 'sm' ? 'text-xs' : size === 'md' ? 'text-sm' : 'text-base'}`}
                aria-label={`Ukuran font Arab ${size}`}
                title={`Ukuran font Arab ${size}`}
              >
                A
              </button>
            ))}
          </div>
        </div>
      </header>

      <div className="mx-auto max-w-3xl px-4 py-6">
        {!loading && surah ? (
          <motion.section
            initial={{ opacity: 0, y: -16 }}
            animate={{ opacity: 1, y: 0 }}
            className="relative mb-6 overflow-hidden rounded-lg bg-gradient-to-br from-emerald-800 to-night-surface p-6 text-center"
          >
            <div className="absolute inset-0 bg-geometric opacity-40" aria-hidden="true" />
            <div className="relative z-10">
              <p className="arabic mb-2 text-4xl font-bold leading-[4rem] text-white">{surah.nama_arab}</p>
              <p className="text-lg font-semibold text-emerald-100">{surah.nama_latin}</p>
              <p className="mt-1 text-sm text-emerald-200">
                {surah.nama_indo} - {surah.jumlah_ayat} ayat - {surah.jenis} - Juz {surah.juz_awal}
              </p>
            </div>
          </motion.section>
        ) : null}

        {!loading && surahId !== 1 && surahId !== 9 ? (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.15 }} className="bismillah">
            بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ
          </motion.div>
        ) : null}

        {loading ? (
          <div className="space-y-4">
            {Array.from({ length: 7 }).map((_, index) => (
              <div key={index} className="rounded-lg bg-night-surface p-5">
                <div className="skeleton mb-4 ml-auto h-10 w-3/4 rounded-lg" />
                <div className="skeleton mb-2 h-4 w-full rounded-lg" />
                <div className="skeleton h-4 w-4/5 rounded-lg" />
              </div>
            ))}
          </div>
        ) : error ? (
          <div className="rounded-lg border border-amber-300/30 bg-amber-300/10 p-5 text-sm text-amber-100">
            {error} Pastikan backend FastAPI berjalan di {API}.
          </div>
        ) : (
          <motion.div
            className="space-y-4"
            initial="hidden"
            animate="visible"
            variants={{ visible: { transition: { staggerChildren: 0.04 } } }}
          >
            {ayatList.map((ayat) => {
              const bookmarked = bookmarks.has(ayat.id);

              return (
                <motion.article
                  key={ayat.id}
                  variants={{ hidden: { opacity: 0, y: 12 }, visible: { opacity: 1, y: 0 } }}
                  className="rounded-lg border border-night-border bg-night-surface p-5 transition hover:border-emerald-600"
                >
                  <div className="mb-4 flex items-center justify-between gap-3">
                    <div className="ayat-number">{ayat.ayat}</div>
                    <div className="flex items-center gap-2">
                      <ActionButton
                        onClick={() => toggleBookmark(ayat.id)}
                        active={bookmarked}
                        label={bookmarked ? 'Hapus bookmark' : 'Bookmark'}
                      >
                        {bookmarked ? <BookmarkCheck className="h-4 w-4" /> : <Bookmark className="h-4 w-4" />}
                      </ActionButton>
                      <ActionButton
                        onClick={() => copyAyat(ayat)}
                        active={copied === ayat.id}
                        label="Salin ayat"
                      >
                        {copied === ayat.id ? <Check className="h-4 w-4" /> : <Clipboard className="h-4 w-4" />}
                      </ActionButton>
                      <ActionButton
                        onClick={() => shareAyat(ayat)}
                        active={shared === ayat.id}
                        label="Bagikan ayat"
                      >
                        {shared === ayat.id ? <Check className="h-4 w-4" /> : <Share2 className="h-4 w-4" />}
                      </ActionButton>
                      <ActionButton
                        onClick={() => setShowTafsir(showTafsir === ayat.id ? null : ayat.id)}
                        active={showTafsir === ayat.id}
                        label="Tampilkan tafsir"
                      >
                        <ScrollText className="h-4 w-4" />
                      </ActionButton>
                    </div>
                  </div>

                  <p className={`arabic mb-4 text-right leading-relaxed text-white ${fontSizes[fontSize]}`}>
                    {ayat.arab}
                  </p>

                  <p className="border-t border-night-border pt-3 text-sm leading-relaxed text-night-muted">
                    <span className="mr-2 font-medium text-emerald-300">{ayat.ayat}.</span>
                    {ayat.terjemahan}
                  </p>

                  <AnimatePresence>
                    {showTafsir === ayat.id && ayat.tafsir ? (
                      <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: 'auto', opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        className="overflow-hidden"
                      >
                        <div className="mt-3 border-l-2 border-l-emerald-400 border-t border-night-border pl-3 pt-3">
                          <p className="mb-1 text-xs font-semibold text-emerald-300">Tafsir Kemenag</p>
                          <p className="text-xs italic leading-relaxed text-night-muted">{ayat.tafsir}</p>
                        </div>
                      </motion.div>
                    ) : null}
                  </AnimatePresence>
                </motion.article>
              );
            })}
          </motion.div>
        )}

        <div className="mt-8 flex gap-3">
          {navigation.previous ? (
            <Link
              href={`/quran/${navigation.previous}`}
              className="flex-1 rounded-lg border border-night-border bg-night-surface p-4 text-center transition hover:border-emerald-400 hover:bg-emerald-900/20 focus:outline-none focus:ring-2 focus:ring-emerald-400"
            >
              <span className="text-xs text-night-muted">Sebelumnya</span>
              <p className="mt-1 text-sm font-medium text-white">Surah {navigation.previous}</p>
            </Link>
          ) : null}
          {navigation.next ? (
            <Link
              href={`/quran/${navigation.next}`}
              className="flex-1 rounded-lg border border-night-border bg-night-surface p-4 text-center transition hover:border-emerald-400 hover:bg-emerald-900/20 focus:outline-none focus:ring-2 focus:ring-emerald-400"
            >
              <span className="text-xs text-night-muted">Selanjutnya</span>
              <p className="mt-1 text-sm font-medium text-white">Surah {navigation.next}</p>
            </Link>
          ) : null}
        </div>
      </div>
    </main>
  );
}

function ActionButton({
  onClick,
  active,
  label,
  children,
}: {
  onClick: () => void;
  active: boolean;
  label: string;
  children: ReactNode;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      title={label}
      aria-label={label}
      className={`inline-flex h-8 w-8 items-center justify-center rounded-lg transition focus:outline-none focus:ring-2 focus:ring-emerald-400 ${
        active
          ? 'bg-emerald-500/20 text-emerald-300'
          : 'bg-night-border/55 text-night-muted hover:bg-night-border hover:text-white'
      }`}
    >
      {children}
    </button>
  );
}
