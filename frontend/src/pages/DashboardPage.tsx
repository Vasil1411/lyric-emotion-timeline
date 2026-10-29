// src/pages/DashboardPage.tsx
import { useState, useMemo } from "react"
import { Headphones, Rocket, Search, Sparkles } from "lucide-react"
import { Button, Card, Heading, Input } from "../components/ui"
import { EmotionPill } from "../components/EmotionPill"
import { SongCard } from "../components/SongCard"
import { emotions, songs } from "../data"
import type { Emotion, Song } from "../types"

type DashboardPageProps = {
  openSong: (song: Song) => void
  requestSong: (title: string) => void
  username: string
}

export function DashboardPage({
  openSong,
  requestSong,
  username,
}: DashboardPageProps) {
  const [query, setQuery] = useState("")
  const [emotion, setEmotion] = useState<Emotion | null>(null)

  const filtered = useMemo(
    () =>
      songs.filter(
        (song) =>
          (!emotion || song.dominantEmotion === emotion) &&
          `${song.title} ${song.artist} ${song.genre}`
            .toLowerCase()
            .includes(query.toLowerCase()),
      ),
    [query, emotion],
  )

  const hasCatalogMatch = songs.some((song) =>
    `${song.title} ${song.artist} ${song.genre}`
      .toLowerCase()
      .includes(query.toLowerCase()),
  )

  return (
    <div className="mx-auto max-w-7xl p-5 sm:p-8 lg:p-10">
      <div className="grid items-end gap-8 xl:grid-cols-[1fr_auto]">
        <div>
          <p className="mb-3 flex items-center gap-2 text-xs font-medium uppercase tracking-[0.18em] text-indigo-300">
            <Sparkles className="size-4" /> Welcome back, {username}
          </p>
          <Heading
            as="h1"
            className="max-w-2xl text-4xl font-semibold tracking-[-0.035em] text-white sm:text-5xl"
          >
            What do you want to feel?
          </Heading>
          <p className="mt-4 max-w-2xl text-sm leading-6 text-slate-400">
            Search a song or choose an emotion. Lyra maps the emotional arc in
            lyrics to your listening taste.
          </p>
        </div>
        <Card className="hidden items-center gap-4 px-5 py-4 sm:flex">
          <div className="grid size-10 place-items-center rounded-xl bg-indigo-500/10 text-indigo-300">
            <Headphones className="size-5" />
          </div>
          <div>
            <p className="text-xl font-semibold text-white">18h</p>
            <p className="text-xs text-slate-500">felt this month</p>
          </div>
        </Card>
      </div>

      <div className="relative mt-10">
        <Search className="absolute left-4 top-1/2 size-5 -translate-y-1/2 text-slate-600" />
        <Input
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="Search by song, artist, or genre..."
          className="h-14 rounded-2xl pl-12 text-base shadow-xl shadow-slate-950/30"
        />
        <kbd className="absolute right-4 top-1/2 hidden -translate-y-1/2 rounded-md border border-white/10 bg-white/5 px-2 py-1 text-[10px] text-slate-600 sm:block">
          ⌘ K
        </kbd>
      </div>

      <div className="mt-5 flex gap-2 overflow-x-auto pb-2">
        <Button
          onClick={() => setEmotion(null)}
          className={`rounded-full px-4 py-2 text-xs ${
            !emotion ? "border-indigo-400/50 bg-indigo-500/15 text-white" : ""
          }`}
        >
          All moods
        </Button>
        {emotions.map((item) => (
          <EmotionPill
            key={item}
            emotion={item}
            active={emotion === item}
            onClick={() => setEmotion(item)}
          />
        ))}
      </div>

      <div className="mt-12 flex items-end justify-between">
        <div>
          <Heading as="h2" className="text-xl font-semibold text-white">
            Resonating now
          </Heading>
          <p className="mt-1 text-xs text-slate-400">
            Recommendations based on your emotional profile
          </p>
        </div>
        <p className="text-xs text-slate-600">{filtered.length} results</p>
      </div>

      <div className="mt-6 grid gap-5 sm:grid-cols-2 xl:grid-cols-4">
        {filtered.map((song) => (
          <SongCard key={song.id} song={song} open={() => openSong(song)} />
        ))}
      </div>

      {!filtered.length && (
        <Card className="mt-6 overflow-hidden p-8 text-center sm:p-12">
          {!hasCatalogMatch && query.trim() ? (
            <>
              <div className="mx-auto grid size-14 place-items-center rounded-2xl border border-indigo-400/20 bg-indigo-500/10 text-indigo-300 shadow-lg shadow-indigo-950/40">
                <Search className="size-6" />
              </div>
              <Heading as="h3" className="mt-5 text-lg font-semibold text-white">
                This track is a new frequency
              </Heading>
              <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-slate-400">
                We could not find “{query}” in the local catalog. Add the artist
                and Lyra will fetch the lyrics and map its emotional arc.
              </p>
              <Button
                variant="primary"
                onClick={() => requestSong(query)}
                className="mt-6 shadow-xl shadow-indigo-950/50"
              >
                <Rocket className="size-4" />
                Song not in database? Analyze with AI now
              </Button>
            </>
          ) : (
            <>
              <Search className="mx-auto size-8 text-slate-600" />
              <p className="mt-4 text-sm text-slate-300">
                No songs match this emotion filter.
              </p>
            </>
          )}
        </Card>
      )}
    </div>
  )
}