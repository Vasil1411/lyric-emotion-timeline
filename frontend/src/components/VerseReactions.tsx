import { useState } from "react"
import { Flame, ThumbsDown, ThumbsUp } from "lucide-react"
import { Button } from "./ui"

type VerseReactionsProps = {
  stanzaId: number
  onFeedback: (id: number | null, type: string) => void
}

export function VerseReactions({ stanzaId, onFeedback }: VerseReactionsProps) {
  const [selected, setSelected] = useState("")
  
  const reactions = [
    { id: "liked", label: "Accurate emotion", icon: ThumbsUp },
    { id: "vibe", label: "Hits the vibe", icon: Flame },
    { id: "correction", label: "Needs correction", icon: ThumbsDown },
  ]

  return (
    <div className="flex items-center gap-1">
      <span className="mr-2 text-[10px] font-medium uppercase tracking-wider text-slate-500">
        React
      </span>
      {reactions.map((reaction) => {
        const IconComponent = reaction.icon
        const isSelected = selected === reaction.id

        return (
          <Button
            key={reaction.id}
            variant="ghost"
            className={`size-8 rounded-lg p-0 ${
              isSelected
                ? "bg-indigo-500/15 text-indigo-200 ring-1 ring-indigo-400/30"
                : ""
            }`}
            aria-label={reaction.label}
            title={reaction.label}
            onClick={() => {
              setSelected(reaction.id)
              onFeedback(stanzaId, reaction.id)
            }}
          >
            <IconComponent className="size-3.5" />
          </Button>
        )
      })}
    </div>
  )
}