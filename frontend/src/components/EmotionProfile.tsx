// src/components/EmotionProfile.tsx
import { Card, Heading } from "./ui"
import { emotionStyles, emotions } from "../data"
import type { Song } from "../types"

type EmotionProfileProps = {
  song: Song
}

export function EmotionProfile({ song }: EmotionProfileProps) {
  return (
    <Card className="p-6">
      <div className="flex items-center justify-between">
        <div>
          <Heading as="h2" className="font-semibold text-white">
            Overall emotional profile
          </Heading>
          <p className="mt-1 text-xs text-slate-400">
            Context-weighted lyric analysis
          </p>
        </div>
        <span className="rounded-full border border-indigo-400/20 bg-indigo-500/10 px-3 py-1 text-[10px] font-medium text-indigo-200">
          High confidence
        </span>
      </div>
      <div className="mt-7 space-y-4">
        {emotions.map((emotion) => {
          const style = emotionStyles[emotion] || { text: "text-slate-400", bg: "bg-slate-400" }
          const percentage = song.profile?.[emotion] || 0

          return (
            <div
              key={emotion}
              className="grid grid-cols-[70px_1fr_36px] items-center gap-3"
            >
              <span className={`text-xs font-semibold ${style.text}`}>
                {emotion}
              </span>
              <div className="h-1.5 overflow-hidden rounded-full bg-white/[0.06]">
                <div
                  className={`h-full rounded-full ${style.bg} shadow-[0_0_12px_currentColor]`}
                  style={{ width: `${percentage}%` }}
                />
              </div>
              <span className="text-right text-sm font-bold tabular-nums text-white">
                {percentage}%
              </span>
            </div>
          )
        })}
      </div>
    </Card>
  )
}