// src/pages/SongDetailsPage.tsx
import { useState } from "react"
import { ArrowLeft, Check, ChevronRight, Clock3 } from "lucide-react"
import { Button, Card, Heading } from "../components/ui"
import { EmotionProfile } from "../components/EmotionProfile"
import { VerseReactions } from "../components/VerseReactions"
import { emotionStyles, stanzas } from "../data"
import { sendFeedback } from "../lib/api"
import type { Song } from "../types"

type SongDetailsPageProps = {
  song: Song
  back: () => void
  openArtist: () => void
}

export function SongDetailsPage({
  song,
  back,
  openArtist,
}: SongDetailsPageProps) {
  const [notice, setNotice] = useState("")

  async function feedback(stanzaId: number | null, type: string) {
    setNotice("Feedback saved — your recommendations will adapt.")
    try {
      await sendFeedback(song.id, stanzaId, type)
    } catch {
      // Keep optimistic feedback in demo mode when the API is not available.
    }
    window.setTimeout(() => setNotice(""), 2600)
  }

  // Защита за стиловете на доминиращата емоция
  const dominantStyle = emotionStyles[song.dominantEmotion] || { text: "text-slate-400" }

  return (
    <div className="mx-auto max-w-7xl p-5 sm:p-8 lg:p-10">
      {notice && (
        <div className="fixed bottom-6 right-6 z-50 flex items-center gap-2 rounded-xl border border-emerald-400/20 bg-slate-900 px-4 py-3 text-xs text-emerald-300 shadow-2xl">
          <Check className="size-4" /> {notice}
        </div>
      )}

      <Button variant="ghost" onClick={back} className="-ml-3 mb-7">
        <ArrowLeft className="size-4" /> Back to discover
      </Button>

      <div className="grid gap-7 lg:grid-cols-[1.2fr_0.8fr]">
        <Card className="relative min-h-80 overflow-hidden p-7 sm:p-10">
          <img
            src={song.image}
            alt={`${song.artist} portrait`}
            className="absolute inset-0 h-full w-full object-cover opacity-35"
          />
          <div className="absolute inset-0 bg-gradient-to-r from-slate-950 via-slate-950/85 to-slate-950/20" />
          
          <div className="relative flex h-full flex-col justify-between gap-8">
            <div className="flex flex-col items-start justify-between gap-4 sm:flex-row">
              <div className="flex items-center gap-2 text-xs font-medium text-slate-300">
                <span>{song.genre}</span>
                <span className="size-1 rounded-full bg-slate-500" />
                <span>2024</span>
              </div>
              <div className="sm:max-w-md">
                <p className="mb-2 text-[10px] font-semibold uppercase tracking-[0.16em] text-slate-400 sm:text-right">
                  Rate the overall song
                </p>
                <VerseReactions stanzaId={0} onFeedback={feedback} />
              </div>
            </div>

            <div>
              <p
                className={`mb-4 inline-flex rounded-full border border-current bg-slate-950/60 px-3 py-1.5 text-xs font-bold uppercase tracking-[0.18em] shadow-lg ${dominantStyle.text}`}
              >
                {song.dominantEmotion} dominant
              </p>
              <Heading
                as="h1"
                className="max-w-xl text-4xl font-semibold tracking-tight text-white sm:text-5xl"
              >
                {song.title}
              </Heading>
              <button
                type="button"
                onClick={openArtist}
                className="mt-3 text-left text-base text-slate-300 transition hover:text-indigo-300"
              >
                {song.artist} <ChevronRight className="inline size-4" />
              </button>
            </div>
          </div>
        </Card>

        <EmotionProfile song={song} />
      </div>

      <div className="mt-12 flex items-end justify-between">
        <div>
          <p className="text-xs font-medium uppercase tracking-[0.18em] text-indigo-300">
            Emotional arc
          </p>
          <Heading as="h2" className="mt-2 text-2xl font-semibold text-white">
            Inside the lyrics
          </Heading>
        </div>
        <div className="hidden items-center gap-2 text-xs text-slate-500 sm:flex">
          <Clock3 className="size-4" /> 4 sections analyzed
        </div>
      </div>

      <div className="relative mt-8 space-y-4 before:absolute before:bottom-10 before:left-[18px] before:top-10 before:w-px before:bg-gradient-to-b before:from-indigo-400/50 before:to-white/5 sm:before:left-[27px]">
        {stanzas.map((stanza, index) => {
          const style = emotionStyles[stanza.emotion] || { bg: "bg-slate-400", text: "text-slate-400" }
          
          return (
            <div
              key={stanza.id}
              className="relative grid grid-cols-[38px_1fr] gap-4 sm:grid-cols-[56px_1fr] sm:gap-6"
            >
              <div
                className={`relative z-10 mt-7 grid size-9 place-items-center rounded-full border-4 border-slate-950 ${style.bg} text-[10px] font-bold text-slate-950 sm:size-11`}
              >
                {index + 1}
              </div>
              
              <Card className="p-5 transition hover:border-white/[0.13] sm:p-7">
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <div className="flex items-center gap-3">
                    <span className="text-xs font-semibold uppercase tracking-[0.14em] text-slate-400">
                      {stanza.label}
                    </span>
                    <span
                      className={`rounded-full bg-white/[0.04] px-2.5 py-1 text-[10px] font-medium ${style.text}`}
                    >
                      {stanza.emotion}
                    </span>
                  </div>

                  <span
                    className={`inline-flex items-center gap-2 rounded-xl border px-3 py-2 text-sm font-bold tabular-nums shadow-lg ${
                      stanza.confidence > 90
                        ? "border-emerald-400/30 bg-emerald-400/10 text-emerald-300 shadow-emerald-950/30"
                        : stanza.confidence >= 70
                          ? "border-amber-400/30 bg-amber-400/10 text-amber-300 shadow-amber-950/30"
                          : "border-rose-400/30 bg-rose-400/10 text-rose-300 shadow-rose-950/30"
                    }`}
                  >
                    <span
                      className={`size-2 rounded-full ${
                        stanza.confidence > 90
                          ? "bg-emerald-300"
                          : stanza.confidence >= 70
                            ? "bg-amber-300"
                            : "bg-rose-300"
                      }`}
                    />
                    {stanza.confidence}% Confidence
                  </span>
                </div>

                <p className="mt-5 whitespace-pre-line text-sm leading-7 text-slate-300">
                  {stanza.lyric}
                </p>

                <div className="mt-5 flex justify-end border-t border-white/[0.08] pt-3">
                  <VerseReactions
                    stanzaId={stanza.id}
                    onFeedback={feedback}
                  />
                </div>
              </Card>
            </div>
          )
        })}
      </div>
    </div>
  )
}