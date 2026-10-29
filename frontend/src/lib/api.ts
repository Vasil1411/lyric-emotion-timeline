const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"

function getToken() {
  return localStorage.getItem("lyra_token")
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = getToken()
  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  })

  if (!response.ok)
    throw new Error(`Request failed with status ${response.status}`)
  return response.json() as Promise<T>
}

export async function authenticate(
  email: string,
  password: string,
  mode: "login" | "register",
  username?: string,
) {
  return request<{ access_token: string; username?: string }>(
    mode === "login" ? "/auth/login" : "/auth/register",
    {
      method: "POST",
      body: JSON.stringify({
        email,
        password,
        ...(mode === "register" ? { username } : {}),
      }),
    },
  )
}

export async function sendFeedback(
  songId: number,
  stanzaId: number | null,
  type: string,
) {
  return request("/feedback", {
    method: "POST",
    body: JSON.stringify({
      song_id: songId,
      stanza_id: stanzaId,
      feedback_type: type,
    }),
  })
}

export async function ingestSong(artist: string, title: string) {
  return request<{ id?: number; status?: string; message?: string }>(
    "/api/songs/ingest",
    {
      method: "POST",
      body: JSON.stringify({ artist, title }),
    },
  )
}
