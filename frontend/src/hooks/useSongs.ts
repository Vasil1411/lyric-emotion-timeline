

import { useState, useEffect, useCallback } from "react"
import { getSongs, ingestSong } from "../services/songService"
import { Song } from "../types/song"

export function useSongs() {
  const [songs, setSongs] = useState<Song[]>([])
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)

  // Fetch all songs from backend
  const fetchSongs = useCallback(async () => {
    try {
      setLoading(true)
      const data = await getSongs()
      setSongs(data)
      setError(null)
    } catch (err: any) {
      setError(err.message || "Failed to load songs.")
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchSongs()
  }, [fetchSongs])

  // Ingest a new song and update local state
  const addSong = async (artist: string, title: string) => {
    try {
      const newSong = await ingestSong(artist, title)
      setSongs((prev) => [newSong, ...prev])
      return newSong
    } catch (err: any) {
      throw err
    }
  }

  return {
    songs,
    loading,
    error,
    refetch: fetchSongs,
    addSong,
  }
}