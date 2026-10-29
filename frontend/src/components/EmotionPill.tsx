import { Button } from "./ui"
import { emotionStyles } from "../data"
import type { Emotion } from "../types"

type EmotionPillProps = {
  emotion: Emotion
  active: boolean
  onClick: () => void
}

export function EmotionPill({
  emotion,
  active,
  onClick,
}: EmotionPillProps) {
  // Извличаме стила (с дефолтна стойност за сигурност, ако липсва в данните)
  const style = emotionStyles[emotion] || { dot: "bg-slate-400" }

  return (
    <Button
      onClick={onClick}
      className={`rounded-full px-4 py-2 text-xs flex items-center gap-2 ${
        active ? "border-indigo-400/50 bg-indigo-500/15 text-white" : ""
      }`}
    >
      <span className={`size-2 rounded-full ${style.dot}`} />
      {emotion}
    </Button>
  )
}