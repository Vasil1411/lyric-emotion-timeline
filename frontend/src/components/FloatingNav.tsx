// src/components/FloatingNav.tsx
import { LogOut, Plus } from "lucide-react"
import { Button } from "./ui"
import { Logo } from "./Logo"

type FloatingNavProps = {
  requestSong: () => void
  logout: () => void
}

export function FloatingNav({ requestSong, logout }: FloatingNavProps) {
  return (
    <header className="sticky top-0 z-40 px-3 pt-3 sm:px-6 sm:pt-5">
      {/* Основна лента за десктоп */}
      <div className="mx-auto flex max-w-7xl items-center gap-3 rounded-2xl border border-white/10 bg-slate-900/75 p-2 shadow-2xl shadow-indigo-950/30 backdrop-blur-2xl">
        <div className="shrink-0 px-2 sm:px-3">
          <Logo />
        </div>
        
        {/* Бутони за навигация (статични засега) */}
        <nav className="hidden flex-1 items-center justify-center gap-1 md:flex">
          <Button variant="ghost" className="rounded-xl px-4 text-white bg-white/[0.08]">
            Discover
          </Button>
          <Button variant="ghost" className="rounded-xl px-4 text-slate-400">
            Song Timeline
          </Button>
          <Button variant="ghost" className="rounded-xl px-4 text-slate-400">
            Artist Analytics
          </Button>
        </nav>

        {/* Десни бутони */}
        <div className="ml-auto flex items-center gap-1.5">
          <Button
            variant="primary"
            onClick={requestSong}
            className="whitespace-nowrap rounded-xl px-3 sm:px-4"
          >
            <Plus className="size-4" />
            <span className="hidden sm:inline">
              Request / Analyze New Song
            </span>
            <span className="sm:hidden">Analyze</span>
          </Button>
          
          <Button
            variant="ghost"
            className="size-10 rounded-xl p-0"
            onClick={logout}
            aria-label="Sign out"
          >
            <LogOut className="size-4" />
          </Button>
        </div>
      </div>
    </header>
  )
}