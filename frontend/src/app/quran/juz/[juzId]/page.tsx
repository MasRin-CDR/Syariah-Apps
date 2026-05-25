import { ModuleShell } from '@/components/modules/module-shell';
import { BookOpen } from 'lucide-react';

interface JuzPageProps {
  params: Promise<{
    juzId: string;
  }>;
}

export default async function JuzPage({ params }: JuzPageProps) {
  const { juzId } = await params;

  return (
    <ModuleShell
      title={`Juz ${juzId}`}
      arabicTitle="القرآن الكريم"
      eyebrow="Juz Al Quran"
      description="Tampilan ayat per juz akan mengambil data dari endpoint /api/quran/juz/{nomor} dan menjaga pengalaman baca yang sama dengan detail surah."
      icon={BookOpen}
      highlights={[
        { label: 'Nomor juz', value: juzId },
        { label: 'Sumber', value: 'API Quran Juz' },
        { label: 'Aksi', value: 'Bookmark, salin, tafsir' },
        { label: 'Mode baca', value: 'RTL Arab' },
      ]}
      primaryAction={{ href: '/quran', label: 'Kembali ke daftar surah' }}
    />
  );
}
