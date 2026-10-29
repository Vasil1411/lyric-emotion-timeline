// src/pages/ArtistAnalyticsPage.tsx
import { ArrowLeft, ChevronRight, Music2 } from "lucide-react"
import { Button, Card, Heading } from "../components/ui"
import { emotionStyles, emotions, songs } from "../data"
import type { Emotion } from "../types"

type ArtistAnalyticsPageProps = {
  back: () => void
}

export function ArtistAnalyticsPage({ back }: ArtistAnalyticsPageProps) {
  const profile: Record<Emotion, number> = {
    Joy: 18,
    Sadness: 46,
    Anger: 7,
    Fear: 12,
    Surprise: 9,
    Neutral: 8,
  }

  const stats = [
    { label: "Songs analyzed", value: "38" },
    { label: "Avg. confidence", value: "91%" },
    { label: "Emotional range", value: "Wide" },
  ]

  return (
    <div className="mx-auto max-w-7xl p-5 sm:p-8 lg:p-10">
      <Button variant="ghost" onClick={back} className="-ml-3 mb-7">
        <ArrowLeft className="size-4" /> Back to song
      </Button>

      <Card className="relative overflow-hidden p-7 sm:p-10">
        <div className="absolute right-0 top-0 h-full w-2/3 bg-[radial-gradient(circle_at_70%_30%,rgba(99,102,241,0.16),transparent_48%)]" />
        <div className="relative flex flex-col gap-7 sm:flex-row sm:items-center">
          <img
            src={songs[0]?.image}
            alt="Luna Vale"
            className="size-28 rounded-2xl object-cover grayscale-[15%] ring-1 ring-white/10"
          />
          <div>
            <p className="text-xs font-medium uppercase tracking-[0.18em] text-indigo-300">
              Artist intelligence
            </p>
            <Heading
              as="h1"
              className="mt-2 text-4xl font-semibold tracking-tight text-white"
            >
              Luna Vale
            </Heading>
            <p className="mt-2 text-sm text-slate-400">
              Alternative R&B · London, UK
            </p>
          </div>
        </div>
      </Card>

      <div className="mt-6 grid gap-4 sm:grid-cols-3">
        {stats.map((stat) => (
          <Card key={stat.label} className="p-5">
            <p className="text-2xl font-semibold text-white">{stat.value}</p>
            <p className="mt-1 text-xs text-slate-400">{stat.label}</p>
          </Card>
        ))}
      </div>

      <div className="mt-6 grid gap-6 lg:grid-cols-[1fr_0.9fr]">
        <Card className="p-6 sm:p-8">
          <Heading as="h2" className="font-semibold text-white">
            Emotional signature
          </Heading>
          <p className="mt-1 text-xs text-slate-400">
            Aggregated across all analyzed songs
          </p>
          <div className="mt-8 space-y-5">
            {emotions.map((emotion) => {
              const style = emotionStyles[emotion] || { text: "text-slate-400", bg: "bg-slate-400" }
              const percentage = profile[emotion] || 0

              return (
                <div key={emotion}>
                  <div className="mb-2 flex justify-between text-xs">
                    <span className={`font-semibold ${style.text}`}>
                      {emotion}
                    </span>
                    <span className="text-sm font-bold tabular-nums text-white">
                      {percentage}%
                    </span>
                  </div>
                  <div className="h-2 overflow-hidden rounded-full bg-white/[0.05]">
                    <div
                      className={`h-full rounded-full ${style.bg}`}
                      style={{ width: `${percentage}%` }}
                    />
                  </div>
                </div>
              )
            })}
          </div>
        </Card>

        <Card className="p-6 sm:p-8">
          <Heading as="h2" className="font-semibold text-white">
            Top emotional tracks
          </Heading>
          <p className="mt-1 text-xs text-slate-400">
            Ranked by signal strength
          </p>
          <div className="mt-6 space-y-3">
            {["Midnight Echoes", "Paper Moons", "Slow Orbit", "Afterimage"].map(
              (title, index) => (
                <div
                  key={title}
                  className="flex items-center gap-4 rounded-xl border border-white/[0.05] bg-white/[0.025] p-3"
                >
                  <span className="w-5 text-center text-xs text-slate-600">
                    0{index + 1}
                  </span>
                  <div className="grid size-9 place-items-center rounded-lg bg-indigo-500/10 text-indigo-300">
                    <Music2 className="size-4" />
                  </div>
                  <div className="min-w-0 flex-1">
                    <p className="truncate text-sm text-slate-200">{title}</p>
                    <p className="mt-0.5 text-[10px] text-slate-600">
                      {index % 2 ? "Reflective · 88%" : "Melancholic · 94%"}
                    </p>
                  </div>
                  <ChevronRight className="size-4 text-slate-700" />
                </div>
              ),
            )}
          </div>
        </Card>
      </div>
    </div>
  )
}