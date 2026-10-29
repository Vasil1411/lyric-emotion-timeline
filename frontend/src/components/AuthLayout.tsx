
import { type ReactNode } from "react"
import { Sparkles } from "lucide-react"
import { Logo } from "./Logo"
import { Heading } from "./ui"

type AuthLayoutProps = {
  children: ReactNode
  tagline?: string
  title?: string
  description?: string
}

export function AuthLayout({
  children,
  tagline = "Hear what the words are feeling",
  title = "Music, mapped to emotion.",
  description = "Explore the emotional arc inside every verse and discover songs that resonate with exactly how you feel.",
}: AuthLayoutProps) {
  return (
    <main className="relative grid min-h-screen overflow-hidden bg-slate-950 lg:grid-cols-[1.1fr_0.9fr]">
      
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_20%_15%,rgba(99,102,241,0.18),transparent_30%),radial-gradient(circle_at_75%_80%,rgba(168,85,247,0.12),transparent_28%)]" />

      {/* Left section (shared/common) */}
      <section className="relative hidden min-h-screen border-r border-white/[0.06] p-12 lg:flex lg:flex-col lg:justify-between">
        <Logo />
        <div className="max-w-xl">
          <div className="mb-8 flex items-center gap-2 text-xs font-medium uppercase tracking-[0.22em] text-indigo-300">
            <Sparkles className="size-4" />
            {tagline}
          </div>
          <Heading
            as="h1"
            className="text-6xl font-semibold leading-[1.04] tracking-[-0.045em] text-white"
          >
            {title}
          </Heading>
          <p className="mt-6 max-w-lg text-lg leading-8 text-slate-400">
            {description}
          </p>
          <div className="mt-12 flex items-center gap-8">
            <div>
              <p className="text-2xl font-semibold text-white">2.4M</p>
              <p className="mt-1 text-xs text-slate-500">lyrics analyzed</p>
            </div>
            <div className="h-10 w-px bg-white/10" />
            <div>
              <p className="text-2xl font-semibold text-white">94%</p>
              <p className="mt-1 text-xs text-slate-500">emotion accuracy</p>
            </div>
          </div>
        </div>
        <p className="text-xs text-slate-600">
          Powered by contextual lyric intelligence
        </p>
      </section>

      {/* Right section (different for each page - forms go here) */}
      <section className="relative flex min-h-screen items-center justify-center px-6 py-12">
        {children}
      </section>
    </main>
  )
}