// src/hooks/useSongDetails.ts

import { useState, useEffect } from "react"
import { getSongDetails, getSongRecommendations, sendFeedback } from "../services/songService"
import { Song } from "../types/song"

export function useSongDetails(songId: number) {
  const [song, setSong] = useState<Song | null>(null)
  const [recommendations, setRecommendations] = useState<Song[]>([])
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)

  // Fetch song details and ML-based recommendations concurrently
  useEffect(() => {
    if (!songId) return

    async function loadSongData() {
      try {
        setLoading(true)
        const [songData, recData] = await Promise.all([
          getSongDetails(songId),
          getSongRecommendations(songId, 5).catch(() => ({ recommended_songs: [] })),
        ])

        setSong(songData)
        setRecommendations(recData.recommended_songs || recData)
        setError(null)
      } catch (err: any) {
        setError(err.message || "Failed to load song details.")
      } finally {
        setLoading(false)
      }
    }

    loadSongData()
  }, [songId])

  // Handle user feedback rating for stanzas or whole songs
  const rateStanza = async (stanzaId: number | null, interactionType: string, rating: number = 1.0) => {
    try {
      await sendFeedback(songId, stanzaId, interactionType, rating)
    } catch (err) {
      console.error("Failed to submit feedback:", err)
    }
  }

  return {
    song,
    recommendations,
    loading,
    error,
    rateStanza,
  }
}