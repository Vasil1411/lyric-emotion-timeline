import { API_BASE_URL } from "../services/api"
import { getAuthHeaders } from "../services/userService"
import { Emotion } from "../types/emotion"
import { Song, SongTimeline } from "../types/song"


// ==================== SONGS & ML SERVICES ====================

// Fetch all songs from database
export async function getSongs() {
  const response = await fetch(`${API_BASE_URL}/songs/`, {
    headers: getAuthHeaders(),
  })
  
  if (!response.ok) {
    throw new Error("Failed to fetch songs.")
  }
  
  return await response.json()
}

// Fetch single song details with emotion timeline stanzas
export async function getSongDetails(songId: number) {
  const response = await fetch(`${API_BASE_URL}/songs/${songId}`, {
    headers: getAuthHeaders(),
  })
  
  if (!response.ok) {
    throw new Error("Failed to fetch song details.")
  }
  
  return await response.json()
}

// Ingest a new song via Genius lyrics & PyTorch ML inference
export async function ingestSong(artist: string, title: string) {
  const userId = localStorage.getItem("lyra_user_id") 
    ? Number(localStorage.getItem("lyra_user_id")) 
    : null

  const response = await fetch(`${API_BASE_URL}/songs/ingest`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify({ artist, title, user_id: userId }),
  })

  if (!response.ok) {
    const err = await response.json().catch(() => ({}))
    throw new Error(err.detail || "Failed to ingest song and run ML analysis.")
  }

  return await response.json()
}

// Get emotion-based song recommendations
export async function getSongRecommendations(songId: number, topN: number = 5) {
  const response = await fetch(`${API_BASE_URL}/songs/recommendations/${songId}?top_n=${topN}`, {
    headers: getAuthHeaders(),
  })

  if (!response.ok) {
    throw new Error("Failed to fetch recommendations.")
  }

  return await response.json()
}

// Get aggregated artist emotional profile
export async function getArtistAnalytics(artistName: string) {
  const response = await fetch(`${API_BASE_URL}/songs/analytics/artist/${encodeURIComponent(artistName)}`, {
    headers: getAuthHeaders(),
  })

  if (!response.ok) {
    throw new Error("Failed to fetch artist analytics.")
  }

  return await response.json()
}

// ==================== FEEDBACK ====================

export async function sendFeedback(
  songId: number,
  stanzaId: number | null,
  interactionType: string,
  rating: number = 1.0
) {
  const userId = localStorage.getItem("lyra_user_id") 
    ? Number(localStorage.getItem("lyra_user_id")) 
    : 1

  const response = await fetch(`${API_BASE_URL}/feedback`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify({
      user_id: userId,
      song_id: songId,
      stanza_id: stanzaId,
      interaction_type: interactionType,
      rating: rating,
    }),
  })

  if (!response.ok) {
    console.warn("Backend feedback logging failed, running in fallback mode.")
    return null
  }

  return await response.json()
}