export type Emotion = "Joy" | "Sadness" | "Anger" | "Fear" | "Surprise" | "Neutral"

export type Song = {
  id: number
  title: string
  artist: string
  genre: string
  match: number
  dominantEmotion: Emotion
  image: string
  accent: string
  profile: Record<Emotion, number>
}

export type Stanza = {
  id: number
  label: string
  lyric: string
  emotion: Emotion
  confidence: number
}

export type View = "home" | "song" | "artist"
