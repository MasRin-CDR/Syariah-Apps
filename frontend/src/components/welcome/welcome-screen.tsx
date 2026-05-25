'use client';

import Link from 'next/link';
import { motion, type Variants } from 'framer-motion';
import {
  ArrowRight,
  BookOpen,
  Globe2,
  Monitor,
  Moon,
  Scale,
  ScrollText,
  Search,
  ShieldCheck,
  Smartphone,
  Sun,
  type LucideIcon,
} from 'lucide-react';
import { useEffect, useState } from 'react';

type Theme = 'dark' | 'light';

interface MenuItem {
  href: string;
  title: string;
  arabicTitle: string;
  meta: string;
  description: string;
  icon: LucideIcon;
  accent: string;
}

const menuItems: MenuItem[] = [
  {
    href: '/quran',
    title: 'Al Quran',
    arabicTitle: 'القرآن الكريم',
    meta: '114 surah',
    description: 'Teks Arab, terjemahan, tafsir, bookmark, dan riwayat baca.',
    icon: BookOpen,
    accent: 'from-emerald-400 via-teal-300 to-emerald-500',
  },
  {
    href: '/hadis',
    title: 'Hadis',
    arabicTitle: 'الحديث الشريف',
    meta: '9 kitab',
    description: 'Bukhari, Muslim, Abu Dawud, Tirmidzi, Nasai, dan lainnya.',
    icon: ScrollText,
    accent: 'from-amber-300 via-orange-300 to-amber-500',
  },
  {
    href: '/search',
    title: 'Pencarian',
    arabicTitle: 'البحث الذكي',
    meta: 'FTS5 + BM25 + FAISS',
    description: 'Temukan ayat dan hadis lewat kata kunci atau makna.',
    icon: Search,
    accent: 'from-sky-300 via-cyan-300 to-emerald-400',
  },
  {
    href: '/waris',
    title: 'Kalkulator Waris',
    arabicTitle: 'حساب الميراث',
    meta: 'Faraid',
    description: 'Hitung bagian ahli waris dengan dasar hukum ringkas.',
    icon: Scale,
    accent: 'from-rose-300 via-amber-300 to-emerald-400',
  },
];

const platformItems: Array<{ label: string; icon: LucideIcon }> = [
  { label: 'Android', icon: Smartphone },
  { label: 'Desktop', icon: Monitor },
  { label: 'Web', icon: Globe2 },
];

const containerVariants: Variants = {
  hidden: {},
  visible: {
    transition: {
      staggerChildren: 0.08,
    },
  },
};

const cardVariants: Variants = {
  hidden: {
    opacity: 0,
    y: 24,
  },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.45,
      ease: 'easeOut',
    },
  },
};

function applyTheme(theme: Theme) {
  const root = document.documentElement;
  root.classList.toggle('dark', theme === 'dark');
  root.dataset.theme = theme;
  localStorage.setItem('syariah-theme', theme);
}

export function WelcomeScreen() {
  const [theme, setTheme] = useState<Theme>('dark');

  useEffect(() => {
    const savedTheme = localStorage.getItem('syariah-theme');
    const initialTheme = savedTheme === 'light' ? 'light' : 'dark';

    setTheme(initialTheme);
    applyTheme(initialTheme);
  }, []);

  const nextTheme = theme === 'dark' ? 'light' : 'dark';
  const ThemeIcon = theme === 'dark' ? Moon : Sun;

  return (
    <main className="relative min-h-screen overflow-hidden bg-slate-50 text-slate-950 transition-colors dark:bg-night-bg dark:text-white">
      <div className="absolute inset-0 bg-islamic opacity-100" aria-hidden="true" />
      <div
        className="absolute inset-0 bg-[linear-gradient(135deg,rgba(16,185,129,0.14),transparent_34%,rgba(245,158,11,0.12)_72%,transparent)]"
        aria-hidden="true"
      />

      <section className="relative z-10 mx-auto flex min-h-screen w-full max-w-6xl flex-col px-4 py-5 sm:px-6 lg:px-8">
        <nav className="flex items-center justify-between gap-4">
          <motion.div
            className="flex items-center gap-3"
            initial={{ opacity: 0, y: -12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.45, ease: 'easeOut' }}
          >
            <div className="flex h-11 w-11 items-center justify-center rounded-lg border border-emerald-300/40 bg-emerald-500/15 text-emerald-300 shadow-primary">
              <BookOpen className="h-5 w-5" aria-hidden="true" />
            </div>
            <div>
              <p className="text-sm font-semibold text-slate-900 dark:text-white">Syariah App</p>
              <p className="text-xs text-slate-500 dark:text-night-muted">Android - Desktop - Web</p>
            </div>
          </motion.div>

          <motion.button
            type="button"
            className="inline-flex h-10 w-10 items-center justify-center rounded-lg border border-slate-300 bg-white text-slate-700 shadow-card transition hover:border-emerald-500 hover:text-emerald-600 focus:outline-none focus:ring-2 focus:ring-emerald-400 dark:border-white/10 dark:bg-white/10 dark:text-white dark:hover:border-emerald-300"
            onClick={() => {
              setTheme(nextTheme);
              applyTheme(nextTheme);
            }}
            title={`Aktifkan mode ${nextTheme === 'dark' ? 'gelap' : 'terang'}`}
            aria-label={`Aktifkan mode ${nextTheme === 'dark' ? 'gelap' : 'terang'}`}
            whileHover={{ y: -1 }}
            whileTap={{ scale: 0.96 }}
          >
            <ThemeIcon className="h-4 w-4" aria-hidden="true" />
          </motion.button>
        </nav>

        <div className="grid flex-1 items-center gap-8 py-9 lg:grid-cols-[0.88fr_1.12fr] lg:py-12">
          <motion.div
            className="max-w-xl"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.58, ease: 'easeOut' }}
          >
            <motion.div
              className="mb-6 inline-flex items-center gap-2 rounded-lg border border-emerald-400/30 bg-white/70 px-3 py-2 text-xs font-medium text-emerald-700 shadow-card backdrop-blur dark:bg-white/10 dark:text-emerald-200"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.12, duration: 0.4 }}
            >
              <ShieldCheck className="h-4 w-4" aria-hidden="true" />
              Ruang ibadah dan kajian
            </motion.div>

            <motion.p
              className="arabic mb-4 text-right text-3xl leading-[3.2rem] text-amber-500 dark:text-gold-light sm:text-4xl"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.2, duration: 0.5 }}
            >
              بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ
            </motion.p>

            <h1 className="text-4xl font-bold leading-tight text-slate-950 dark:text-white sm:text-5xl">
              Syariah <span className="text-emerald-500 dark:text-emerald-300">App</span>
            </h1>
            <p className="mt-4 max-w-lg text-base leading-7 text-slate-600 dark:text-night-muted">
              Aplikasi Islami modern untuk membaca Al Quran, menelusuri hadis, mencari dalil, dan menghitung faraid dalam satu ruang kerja yang tenang.
            </p>

            <div className="mt-7 grid grid-cols-2 gap-3 sm:grid-cols-3">
              {platformItems.map(({ label, icon: StatusIcon }) => {
                return (
                  <div
                    key={label}
                    className="flex h-11 items-center gap-2 rounded-lg border border-slate-200 bg-white/70 px-3 text-sm text-slate-700 shadow-card backdrop-blur dark:border-white/10 dark:bg-white/10 dark:text-night-text"
                  >
                    <StatusIcon className="h-4 w-4 text-emerald-500 dark:text-emerald-300" aria-hidden="true" />
                    <span>{label}</span>
                  </div>
                );
              })}
            </div>
          </motion.div>

          <motion.div
            className="grid gap-4 sm:grid-cols-2"
            variants={containerVariants}
            initial="hidden"
            animate="visible"
          >
            {menuItems.map((item) => {
              const Icon = item.icon;

              return (
                <motion.div key={item.href} variants={cardVariants}>
                  <Link
                    href={item.href}
                    className="group relative flex min-h-[190px] flex-col overflow-hidden rounded-lg border border-slate-200 bg-white/82 p-5 shadow-card backdrop-blur transition focus:outline-none focus:ring-2 focus:ring-emerald-400 dark:border-white/10 dark:bg-white/[0.075]"
                  >
                    <span className={`absolute inset-x-0 top-0 h-1 bg-gradient-to-r ${item.accent}`} aria-hidden="true" />
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex h-12 w-12 items-center justify-center rounded-lg border border-emerald-400/30 bg-emerald-500/12 text-emerald-600 dark:text-emerald-200">
                        <Icon className="h-5 w-5" aria-hidden="true" />
                      </div>
                      <ArrowRight className="mt-1 h-5 w-5 text-slate-400 transition group-hover:translate-x-1 group-hover:text-emerald-500 dark:text-white/45 dark:group-hover:text-gold-light" aria-hidden="true" />
                    </div>

                    <div className="mt-5 flex-1">
                      <p className="arabic text-right text-xl leading-9 text-amber-600 dark:text-gold-light">{item.arabicTitle}</p>
                      <h2 className="mt-2 text-xl font-semibold text-slate-950 dark:text-white">{item.title}</h2>
                      <p className="mt-2 text-sm leading-6 text-slate-600 dark:text-night-muted">{item.description}</p>
                    </div>

                    <div className="mt-5 inline-flex w-fit rounded-lg border border-slate-200 bg-slate-50 px-3 py-1.5 text-xs font-semibold text-slate-600 dark:border-white/10 dark:bg-white/10 dark:text-emerald-100">
                      {item.meta}
                    </div>
                  </Link>
                </motion.div>
              );
            })}
          </motion.div>
        </div>
      </section>
    </main>
  );
}
