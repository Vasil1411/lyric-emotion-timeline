import { Emotion } from "./emotion"

export type Song = {
  id: number
  artist: string
  title: string
  genre?: string | null
  overall_profile?: string | Record<string, any> | null 
  created_at?: string | null
  stanzas?: SongTimeline[] 
}


export type SongTimeline = {
  id: number
  song_id: number
  stanza_index: number
  text: string
  emotion: Emotion
  confidence: number
}


export type SongIngestPayload = {
  artist: string
  title: string
  user_id?: number | null
}