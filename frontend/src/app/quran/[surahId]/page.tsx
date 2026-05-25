import { SurahDetailClient } from '@/components/quran/surah-detail-client';

interface SurahDetailPageProps {
  params: Promise<{
    surahId: string;
  }>;
}

export default async function SurahDetailPage({ params }: SurahDetailPageProps) {
  const { surahId } = await params;

  return <SurahDetailClient surahId={Number(surahId)} />;
}
