import { Activity } from 'lucide-react'

export function Logo() {
  return (
    <div className="flex items-center gap-3">
      <div className="grid size-9 place-items-center rounded-xl bg-gradient-to-br from-indigo-400 to-violet-600 shadow-lg shadow-indigo-950/60">
        <Activity className="size-5 text-white" />
      </div>
      <div>
        <p className="font-semibold tracking-tight text-white">Lyra</p>
        <p className="text-[10px] font-semibold uppercase tracking-[0.2em] text-indigo-300">
          Emotion engine
        </p>
      </div>
    </div>
  )
}