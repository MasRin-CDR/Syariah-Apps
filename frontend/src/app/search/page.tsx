import { ModuleShell } from '@/components/modules/module-shell';
import { Search } from 'lucide-react';

export default function SearchPage() {
  return (
    <ModuleShell
      title="Pencarian"
      arabicTitle="البحث الذكي"
      eyebrow="Search Engine"
      description="Halaman pencarian akan menggabungkan hasil Al Quran dan Hadis dengan debounce, highlight keyword, riwayat lokal, serta skor relevansi."
      icon={Search}
      highlights={[
        { label: 'Keyword', value: 'FTS5' },
        { label: 'Ranking', value: 'BM25' },
        { label: 'Semantik', value: 'FAISS' },
        { label: 'Bahasa', value: 'Arab + Indonesia' },
      ]}
    />
  );
}
