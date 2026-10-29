// src/components/IngestSongModal.tsx
import { useState, type FormEvent } from "react"
import { Check, LoaderCircle, Plus, Rocket } from "lucide-react"
import { Button, Card, Heading, Input } from "./ui"
import { ingestSong } from "../lib/api"


type IngestSongModalProps = {
  initialTitle: string
  close: () => void
}

export function IngestSongModal({ initialTitle, close }: IngestSongModalProps) {
  const [title, setTitle] = useState(initialTitle)
  const [artist, setArtist] = useState("")
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">(
    "idle",
  )

  async function submit(event: FormEvent) {
    event.preventDefault()
    setStatus("loading")
    try {
      await ingestSong(artist, title)
      setStatus("success")
    } catch {
      setStatus("error")
    }
  }

  return (
    <div
      className="fixed inset-0 z-50 grid place-items-center bg-slate-950/80 p-4 backdrop-blur-md"
      onClick={close}
    >
      <Card
        className="relative w-full max-w-lg overflow-hidden p-6 shadow-2xl shadow-indigo-950/60 sm:p-8"
        onClick={(event) => event.stopPropagation()}
      >
        <div
          className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-indigo-400 to-transparent"
          aria-hidden="true"
        />
        <div>
          <div className="flex items-start justify-between gap-4">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-indigo-300">
                AI song ingestion
              </p>
              <Heading as="h2" className="mt-2 text-2xl font-semibold text-white">
                Analyze a new song
              </Heading>
              <p className="mt-2 text-sm leading-6 text-slate-400">
                Add the exact song and artist so Lyra can build a new emotion
                timeline.
              </p>
            </div>
            <Button
              variant="ghost"
              className="size-9 shrink-0 p-0"
              onClick={close}
              aria-label="Close request"
            >
              <Plus className="size-4 rotate-45" />
            </Button>
          </div>

          {status === "loading" ? (
            <div className="py-12 text-center">
              <div className="mx-auto grid size-16 place-items-center rounded-2xl border border-indigo-400/20 bg-indigo-500/10 text-indigo-300">
                <LoaderCircle className="size-8 animate-spin" />
              </div>
              <p className="mt-6 font-semibold text-white">
                Building the emotional arc
              </p>
              <p className="mx-auto mt-2 max-w-sm text-sm leading-6 text-slate-400">
                Fetching lyrics from Genius & analyzing emotional arc with
                XLM-RoBERTa...
              </p>
            </div>
          ) : status === "success" ? (
            <div className="py-10 text-center">
              <div className="mx-auto grid size-16 place-items-center rounded-2xl border border-emerald-400/25 bg-emerald-400/10 text-emerald-300">
                <Check className="size-8" />
              </div>
              <p className="mt-6 text-lg font-semibold text-white">
                Analysis request received
              </p>
              <p className="mt-2 text-sm text-slate-400">
                {title} by {artist} is being added to your catalog.
              </p>
              <Button variant="primary" onClick={close} className="mt-6">
                Return to discover
              </Button>
            </div>
          ) : (
            <form className="mt-7 space-y-4" onSubmit={submit}>
              <label className="block">
                <span className="mb-2 block text-xs font-medium text-slate-300">
                  Song title
                </span>
                <Input
                  value={title}
                  onChange={(event) => setTitle(event.target.value)}
                  placeholder="e.g. Midnight Echoes"
                  required
                />
              </label>
              <label className="block">
                <span className="mb-2 block text-xs font-medium text-slate-300">
                  Artist
                </span>
                <Input
                  value={artist}
                  onChange={(event) => setArtist(event.target.value)}
                  placeholder="e.g. Luna Vale"
                  required
                />
              </label>
              {status === "error" && (
                <p className="rounded-xl border border-rose-400/20 bg-rose-400/[0.06] p-3 text-xs text-rose-200">
                  The ingestion service could not be reached. Check the FastAPI
                  connection and try again.
                </p>
              )}
              <Button
                type="submit"
                variant="primary"
                className="w-full py-3.5"
              >
                <Rocket className="size-4" />
                Fetch lyrics & analyze
              </Button>
            </form>
          )}
        </div>
      </Card>
    </div>
  )
}