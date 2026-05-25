import Link from 'next/link';
import {
  ArrowLeft,
  ArrowRight,
  BookOpen,
  Clock,
  Database,
  type LucideIcon,
} from 'lucide-react';

interface ModuleHighlight {
  label: string;
  value: string;
}

interface ModuleAction {
  href: string;
  label: string;
}

interface ModuleShellProps {
  title: string;
  arabicTitle: string;
  eyebrow: string;
  description: string;
  icon: LucideIcon;
  highlights: ModuleHighlight[];
  primaryAction?: ModuleAction;
}

export function ModuleShell({
  title,
  arabicTitle,
  eyebrow,
  description,
  icon: Icon,
  highlights,
  primaryAction,
}: ModuleShellProps) {
  return (
    <main className="min-h-screen bg-islamic px-4 py-5 text-white sm:px-6 lg:px-8">
      <div className="mx-auto flex min-h-[calc(100vh-2.5rem)] max-w-5xl flex-col">
        <nav className="flex items-center justify-between">
          <Link
            href="/"
            className="inline-flex items-center gap-2 rounded-lg border border-white/10 bg-white/10 px-3 py-2 text-sm text-night-text transition hover:border-emerald-300 hover:text-emerald-200 focus:outline-none focus:ring-2 focus:ring-emerald-400"
          >
            <ArrowLeft className="h-4 w-4" aria-hidden="true" />
            Beranda
          </Link>
        </nav>

        <section className="grid flex-1 items-center gap-7 py-10 lg:grid-cols-[0.92fr_1.08fr]">
          <div>
            <div className="mb-5 inline-flex items-center gap-2 rounded-lg border border-emerald-300/30 bg-emerald-500/12 px-3 py-2 text-xs font-semibold text-emerald-200">
              <Clock className="h-4 w-4" aria-hidden="true" />
              {eyebrow}
            </div>
            <p className="arabic mb-4 text-right text-4xl leading-[4rem] text-gold-light">{arabicTitle}</p>
            <h1 className="text-4xl font-bold leading-tight sm:text-5xl">{title}</h1>
            <p className="mt-4 max-w-xl text-base leading-7 text-night-muted">{description}</p>

            {primaryAction ? (
              <Link
                href={primaryAction.href}
                className="mt-7 inline-flex items-center gap-2 rounded-lg bg-emerald-500 px-4 py-3 text-sm font-semibold text-white shadow-primary transition hover:bg-emerald-400 focus:outline-none focus:ring-2 focus:ring-emerald-300"
              >
                {primaryAction.label}
                <ArrowRight className="h-4 w-4" aria-hidden="true" />
              </Link>
            ) : null}
          </div>

          <div className="rounded-lg border border-white/10 bg-white/[0.075] p-5 shadow-glass backdrop-blur">
            <div className="flex items-center gap-4 border-b border-white/10 pb-5">
              <div className="flex h-14 w-14 items-center justify-center rounded-lg border border-emerald-300/30 bg-emerald-500/15 text-emerald-200">
                <Icon className="h-7 w-7" aria-hidden="true" />
              </div>
              <div>
                <p className="text-sm font-semibold text-white">{title}</p>
                <p className="text-xs text-night-muted">Presentation layer siap dihubungkan ke API.</p>
              </div>
            </div>

            <div className="mt-5 grid gap-3 sm:grid-cols-2">
              {highlights.map((highlight) => (
                <div key={highlight.label} className="rounded-lg border border-white/10 bg-night-bg/45 p-4">
                  <p className="text-xs text-night-muted">{highlight.label}</p>
                  <p className="mt-2 text-lg font-semibold text-white">{highlight.value}</p>
                </div>
              ))}
            </div>

            <div className="mt-5 flex items-center gap-3 rounded-lg border border-amber-300/25 bg-amber-300/10 p-4 text-sm text-amber-100">
              <Database className="h-5 w-5 flex-shrink-0" aria-hidden="true" />
              <p>Endpoint backend dan skema database sudah tersedia untuk integrasi data berikutnya.</p>
            </div>

            <div className="mt-5 flex items-center gap-3 rounded-lg border border-emerald-300/20 bg-emerald-400/10 p-4 text-sm text-emerald-100">
              <BookOpen className="h-5 w-5 flex-shrink-0" aria-hidden="true" />
              <p>Struktur komponen mengikuti pemisahan presentation, domain hook, dan data service.</p>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}
