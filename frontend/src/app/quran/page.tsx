'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';
import { ArrowLeft, BookOpen, Search } from 'lucide-react';
import { useEffect, useMemo, useState } from 'react';

interface SurahMeta {
  id: number;
  nama_arab: string;
  nama_latin: string;
  nama_indo: string;
  jumlah_ayat: number;
  jenis: string;
  juz_awal: number;
}

const API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function QuranPage() {
  const [surahList, setSurahList] = useState<SurahMeta[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [query, setQuery] = useState('');
  const [activeTab, setActiveTab] = useState<'surah' | 'juz'>('surah');

  useEffect(() => {
    let ignore = false;

    async function fetchSurahList() {
      try {
        setLoading(true);
        setError(null);

        const response = await fetch(`${API}/api/quran/surah`);

        if (!response.ok) {
          throw new Error('Gagal memuat daftar surah.');
        }

        const payload = await response.json();

        if (!ignore) {
          setSurahList(payload.data || []);
        }
      } catch (err) {
        if (!ignore) {
          setError(err instanceof Error ? err.message : 'Gagal memuat daftar surah.');
        }
      } finally {
        if (!ignore) {
          setLoading(false);
        }
      }
    }

    fetchSurahList();

    return () => {
      ignore = true;
    };
  }, []);

  const filtered = useMemo(() => {
    const normalizedQuery = query.trim().toLowerCase();

    if (!normalizedQuery) {
      return surahList;
    }

    return surahList.filter((surah) =>
      surah.nama_latin.toLowerCase().includes(normalizedQuery) ||
      surah.nama_indo.toLowerCase().includes(normalizedQuery) ||
      String(surah.id).includes(normalizedQuery),
    );
  }, [query, surahList]);

  return (
    <main className="min-h-screen bg-night-bg text-white">
      <header className="sticky top-0 z-30 border-b border-night-border bg-night-bg/86 backdrop-blur-xl">
        <div className="mx-auto max-w-4xl px-4 py-4">
          <div className="mb-4 flex items-center gap-3">
            <Link
              href="/"
              className="inline-flex h-9 w-9 items-center justify-center rounded-lg border border-white/10 text-night-muted transition hover:border-emerald-300 hover:text-emerald-200 focus:outline-none focus:ring-2 focus:ring-emerald-400"
              aria-label="Kembali ke beranda"
              title="Kembali ke beranda"
            >
              <ArrowLeft className="h-4 w-4" aria-hidden="true" />
            </Link>
            <div>
              <h1 className="text-xl font-bold text-white">Al Quran</h1>
              <p className="arabic text-right text-sm text-gold-light">القرآن الكريم</p>
            </div>
          </div>

          <label className="relative block">
            <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-night-muted" aria-hidden="true" />
            <input
              type="search"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Cari surah... contoh: Al-Baqarah, Maryam"
              className="w-full rounded-lg border border-night-border bg-night-surface py-2.5 pl-10 pr-4 text-sm text-white placeholder:text-night-muted focus:border-emerald-400 focus:outline-none"
            />
          </label>

          <div className="tab-bar mt-3">
            {(['surah', 'juz'] as const).map((tab) => (
              <button
                key={tab}
                type="button"
                onClick={() => setActiveTab(tab)}
                className={`tab-item capitalize ${activeTab === tab ? 'active' : ''}`}
              >
                {tab === 'surah' ? 'Surah' : 'Juz'}
              </button>
            ))}
          </div>
        </div>
      </header>

      <div className="mx-auto max-w-4xl px-4 py-6">
        {loading ? (
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
            {Array.from({ length: 12 }).map((_, index) => (
              <div key={index} className="skeleton h-20 rounded-lg" />
            ))}
          </div>
        ) : error ? (
          <div className="rounded-lg border border-amber-300/30 bg-amber-300/10 p-5 text-sm text-amber-100">
            {error} Pastikan backend FastAPI berjalan di {API}.
          </div>
        ) : activeTab === 'surah' ? (
          <motion.div
            className="grid grid-cols-1 gap-3 sm:grid-cols-2"
            initial="hidden"
            animate="visible"
            variants={{ visible: { transition: { staggerChildren: 0.03 } } }}
          >
            {filtered.map((surah) => (
              <motion.div
                key={surah.id}
                variants={{ hidden: { opacity: 0, y: 10 }, visible: { opacity: 1, y: 0 } }}
              >
                <Link
                  href={`/quran/${surah.id}`}
                  className="group flex min-h-24 items-center gap-4 rounded-lg border border-night-border bg-night-surface p-4 transition hover:border-emerald-400 hover:bg-night-surface/82 focus:outline-none focus:ring-2 focus:ring-emerald-400"
                >
                  <div className="ayat-number text-xs">{surah.id}</div>
                  <div className="min-w-0 flex-1">
                    <div className="flex items-start justify-between gap-3">
                      <div>
                        <p className="text-sm font-semibold text-white transition group-hover:text-emerald-300">
                          {surah.nama_latin}
                        </p>
                        <p className="text-xs text-night-muted">
                          {surah.nama_indo} - {surah.jumlah_ayat} ayat
                        </p>
                      </div>
                      <div className="text-right">
                        <p className="arabic text-lg leading-8 text-gold-light">{surah.nama_arab}</p>
                        <span className={`badge text-xs ${surah.jenis === 'Makkiyah' ? 'badge-gold' : 'badge-primary'}`}>
                          {surah.jenis}
                        </span>
                      </div>
                    </div>
                  </div>
                </Link>
              </motion.div>
            ))}
          </motion.div>
        ) : (
          <JuzGrid />
        )}

        {!loading && !error && activeTab === 'surah' && filtered.length === 0 ? (
          <div className="py-16 text-center text-night-muted">
            <BookOpen className="mx-auto mb-3 h-10 w-10" aria-hidden="true" />
            <p>Surah "{query}" tidak ditemukan.</p>
          </div>
        ) : null}
      </div>
    </main>
  );
}

function JuzGrid() {
  return (
    <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 md:grid-cols-5">
      {Array.from({ length: 30 }, (_, index) => index + 1).map((juz) => (
        <Link
          key={juz}
          href={`/quran/juz/${juz}`}
          className="flex min-h-28 flex-col items-center justify-center rounded-lg border border-night-border bg-night-surface p-5 transition hover:border-emerald-400 focus:outline-none focus:ring-2 focus:ring-emerald-400"
        >
          <span className="text-2xl font-bold text-white">{juz}</span>
          <span className="mt-1 text-xs text-night-muted">Juz {juz}</span>
        </Link>
      ))}
    </div>
  );
}
