import { ModuleShell } from '@/components/modules/module-shell';
import { Scale } from 'lucide-react';

export default function WarisPage() {
  return (
    <ModuleShell
      title="Kalkulator Waris"
      arabicTitle="حساب الميراث"
      eyebrow="Faraid"
      description="Kalkulator waris akan menghitung bagian suami, istri, ayah, ibu, anak, cucu, dan saudara dengan tabel persentase, nominal, dan dasar hukum."
      icon={Scale}
      highlights={[
        { label: 'Input', value: 'Harta + ahli waris' },
        { label: 'Aturan', value: 'Faraid dasar' },
        { label: 'Output', value: 'Persentase + Rupiah' },
        { label: 'Dokumen', value: 'Print atau PDF' },
      ]}
    />
  );
}
