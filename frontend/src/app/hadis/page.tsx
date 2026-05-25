import { ModuleShell } from '@/components/modules/module-shell';
import { ScrollText } from 'lucide-react';

export default function HadisPage() {
  return (
    <ModuleShell
      title="Hadis"
      arabicTitle="الحديث الشريف"
      eyebrow="Modul Hadis"
      description="Navigasi 9 kitab hadis akan disusun dari Kitab ke Bab lalu ke detail hadis dengan teks Arab, terjemahan, bookmark, salin, dan bagikan."
      icon={ScrollText}
      highlights={[
        { label: 'Kitab', value: '9 sumber' },
        { label: 'Alur', value: 'Kitab > Bab > Hadis' },
        { label: 'Aksi', value: 'Bookmark, salin, bagikan' },
        { label: 'Data', value: 'SQLite + API Hadis' },
      ]}
    />
  );
}
