// src/components/FeedbackButtons.tsx
import { useState } from "react"
import { Check, Flame, Heart, PencilLine } from "lucide-react"
import { Button } from "./ui"

type FeedbackButtonsProps = {
  stanzaId: number | null
  onFeedback: (id: number | null, type: string) => void
}

export function FeedbackButtons({ stanzaId, onFeedback }: FeedbackButtonsProps) {
  const [selected, setSelected] = useState("")
  
  const options = [
    { id: "vibe", label: "Hit the vibe", icon: Flame },
    { id: "liked", label: "Liked", icon: Heart },
    { id: "correction", label: "Needs correction", icon: PencilLine },
  ]

  return (
    <div className="flex flex-wrap gap-2">
      {options.map((option) => {
        const IconComponent = option.icon
        const isSelected = selected === option.id

        return (
          <Button
            key={option.id}
            className={`px-3 py-2 text-[11px] ${
              isSelected
                ? "border-indigo-400/40 bg-indigo-500/15 text-indigo-200"
                : ""
            }`}
            onClick={() => {
              setSelected(option.id)
              onFeedback(stanzaId, option.id)
            }}
          >
            {isSelected ? (
              <Check className="size-3.5" />
            ) : (
              <IconComponent className="size-3.5" />
            )}
            {option.label}
          </Button>
        )
      })}
    </div>
  )
}