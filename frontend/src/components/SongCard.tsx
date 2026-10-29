import { ChevronRight, Play } from "lucide-react"
import { Button, Card, Heading } from "./ui"
import { emotionStyles } from "../data"
import type { Song } from "../types"

type SongCardProps = {
  song: Song
  open: () => void
}

export function SongCard({ song, open }: SongCardProps) {

  const style = emotionStyles[song.dominantEmotion] || { text: "text-slate-400" }

  return (
    <Card className="group overflow-hidden transition duration-300 hover:-translate-y-1 hover:border-indigo-400/30 hover:shadow-2xl hover:shadow-indigo-950/20">
      <div className={`relative h-40 overflow-hidden bg-gradient-to-br ${song.accent}`}>
        <img
          src={song.image}
          alt={`${song.artist} portrait`}
          className="h-full w-full object-cover opacity-55 grayscale-[20%] transition duration-500 group-hover:scale-105 group-hover:opacity-70"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-slate-900 via-transparent to-transparent" />
        
        <Button
          variant="primary"
          onClick={open}
          className="absolute bottom-4 right-4 size-10 rounded-full p-0 opacity-0 translate-y-2 group-hover:translate-y-0 group-hover:opacity-100 transition-all"
          aria-label={`Open ${song.title}`}
        >
          <Play className="size-4 fill-current" />
        </Button>

        <div className="absolute left-4 top-4 rounded-full border border-white/10 bg-slate-950/70 px-2.5 py-1 text-[10px] font-medium text-white backdrop-blur-md">
          {song.match}% match
        </div>
      </div>

      <div className="p-5">
        <div className="flex items-start justify-between gap-4">
          <div>
            <Heading as="h3" className="font-medium text-white">
              {song.title}
            </Heading>
            <p className="mt-1 text-xs text-slate-500">{song.artist}</p>
          </div>
          <span className={`mt-1 text-[10px] font-semibold uppercase tracking-wider ${style.text}`}>
            {song.dominantEmotion}
          </span>
        </div>

        <div className="mt-5 flex items-center justify-between border-t border-white/[0.06] pt-4">
          <span className="text-[11px] text-slate-600">{song.genre}</span>
          <Button variant="ghost" className="p-1 text-xs" onClick={open}>
            Analyze <ChevronRight className="size-3.5" />
          </Button>
        </div>
      </div>
    </Card>
  )
}