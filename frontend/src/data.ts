import type { Emotion, Song, Stanza } from "./types"

export const artistImage =
  "https://images.unsplash.com/photo-1653256485645-f49983825d6f?crop=faces&cs=tinysrgb&fit=crop&fm=jpg&q=85&w=900"

export const emotions: Emotion[] = [
  "Joy",
  "Sadness",
  "Anger",
  "Fear",
  "Surprise",
  "Neutral",
]

export const emotionStyles: Record<Emotion, {
  text: string
  bg: string
  dot: string
}> = {
  Joy: { text: "text-amber-300", bg: "bg-amber-300", dot: "bg-amber-300" },
  Sadness: { text: "text-blue-300", bg: "bg-blue-400", dot: "bg-blue-400" },
  Anger: { text: "text-rose-300", bg: "bg-rose-400", dot: "bg-rose-400" },
  Fear: { text: "text-violet-300", bg: "bg-violet-400", dot: "bg-violet-400" },
  Surprise: {
    text: "text-fuchsia-300",
    bg: "bg-fuchsia-400",
    dot: "bg-fuchsia-400",
  },
  Neutral: { text: "text-slate-300", bg: "bg-slate-400", dot: "bg-slate-400" },
}

export const songs: Song[] = [
  {
    id: 1,
    title: "Midnight Echoes",
    artist: "Luna Vale",
    genre: "Alternative R&B",
    match: 96,
    dominantEmotion: "Sadness",
    image: artistImage,
    accent: "from-indigo-500/40 to-violet-900/20",
    profile: {
      Joy: 12,
      Sadness: 68,
      Anger: 5,
      Fear: 9,
      Surprise: 3,
      Neutral: 3,
    },
  },
  {
    id: 2,
    title: "Golden Hour",
    artist: "The Daybreakers",
    genre: "Indie Pop",
    match: 92,
    dominantEmotion: "Joy",
    image:
      "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?crop=faces&cs=tinysrgb&fit=crop&fm=jpg&q=80&w=600",
    accent: "from-amber-400/35 to-orange-900/20",
    profile: {
      Joy: 76,
      Sadness: 6,
      Anger: 2,
      Fear: 3,
      Surprise: 9,
      Neutral: 4,
    },
  },
  {
    id: 3,
    title: "Static Hearts",
    artist: "Neon Palms",
    genre: "Synthwave",
    match: 89,
    dominantEmotion: "Surprise",
    image:
      "https://images.unsplash.com/photo-1524368535928-5b5e00ddc76b?cs=tinysrgb&fit=crop&fm=jpg&q=80&w=600",
    accent: "from-fuchsia-500/35 to-purple-900/20",
    profile: {
      Joy: 25,
      Sadness: 8,
      Anger: 4,
      Fear: 5,
      Surprise: 53,
      Neutral: 5,
    },
  },
  {
    id: 4,
    title: "Ash & Oxygen",
    artist: "Northbound",
    genre: "Alternative",
    match: 86,
    dominantEmotion: "Anger",
    image:
      "https://images.unsplash.com/photo-1501386761578-eac5c94b800a?cs=tinysrgb&fit=crop&fm=jpg&q=80&w=600",
    accent: "from-rose-500/30 to-red-950/20",
    profile: {
      Joy: 7,
      Sadness: 19,
      Anger: 55,
      Fear: 10,
      Surprise: 4,
      Neutral: 5,
    },
  },
]

export const stanzas: Stanza[] = [
  {
    id: 1,
    label: "Verse 1",
    lyric:
      "Streetlights flicker like a memory\nYour shadow moves across the hall\nI trace the shape of every silence\nWaiting for the night to call",
    emotion: "Sadness",
    confidence: 94,
  },
  {
    id: 2,
    label: "Pre-Chorus",
    lyric: "But somewhere underneath the static\nA quiet rhythm starts to rise",
    emotion: "Fear",
    confidence: 81,
  },
  {
    id: 3,
    label: "Chorus",
    lyric:
      "We are midnight echoes\nBouncing off the blue\nEvery broken frequency\nLeads me back to you",
    emotion: "Sadness",
    confidence: 97,
  },
  {
    id: 4,
    label: "Bridge",
    lyric:
      "Then morning breaks the spell in two\nAnd leaves a little light coming through",
    emotion: "Joy",
    confidence: 78,
  },
]
