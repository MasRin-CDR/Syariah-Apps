import type { Metadata } from 'next';
import Script from 'next/script';
import './globals.css';

export const metadata: Metadata = {
  title: 'Syariah App - Al Quran, Hadis, Pencarian, dan Kalkulator Waris',
  description:
    'Aplikasi Islami modern untuk Al Quran, 9 kitab Hadis, pencarian cerdas, dan kalkulator waris faraid.',
  keywords: ['Al Quran', 'Hadis', 'Tafsir', 'Kalkulator Waris', 'Faraid', 'Syariah App'],
};

const themeScript = `
(() => {
  try {
    const saved = localStorage.getItem('syariah-theme');
    const theme = saved === 'light' ? 'light' : 'dark';
    document.documentElement.classList.toggle('dark', theme === 'dark');
    document.documentElement.dataset.theme = theme;
  } catch (_) {
    document.documentElement.classList.add('dark');
    document.documentElement.dataset.theme = 'dark';
  }
})();
`;

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="id" className="dark" suppressHydrationWarning>
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Noto+Naskh+Arabic:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap"
          rel="stylesheet"
        />
        <Script id="syariah-theme" strategy="beforeInteractive" dangerouslySetInnerHTML={{ __html: themeScript }} />
      </head>
      <body className="min-h-screen bg-slate-50 font-sans text-slate-950 antialiased dark:bg-night-bg dark:text-night-text">
        {children}
      </body>
    </html>
  );
}
