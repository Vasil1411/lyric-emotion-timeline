// src/App.tsx
import { useState } from "react"
import { Routes, Route, Navigate, useNavigate } from "react-router-dom"
import { FloatingNav } from "./components/FloatingNav"
import { IngestSongModal } from "./components/IngestSongModal"
import { LoginPage } from "./pages/Login"
import { RegisterPage } from "./pages/Register"
import { DashboardPage } from "./pages/DashboardPage"
import { SongDetailsPage } from "./pages/SongDetailsPage"
import { ArtistAnalyticsPage } from "./pages/ArtistAnalyticsPage"
import { songs } from "./data"
import type { Song } from "./types"

// Вътрешен компонент за логнат потребител, за да може безопасно да ползва useNavigate()
function AuthenticatedLayout({
  username,
  logout,
  requestSong,
}: {
  username: string
  logout: () => void
  requestSong: (title: string) => void
}) {
  const [selectedSong, setSelectedSong] = useState<Song>(songs[0])
  const navigate = useNavigate()

  return (
    <div className="min-h-screen bg-slate-950 text-slate-300">
      <FloatingNav
        requestSong={() => requestSong("")}
        logout={logout}
      />

      <main>
        <Routes>
          <Route
            path="/"
            element={
              <DashboardPage
                username={username}
                requestSong={requestSong}
                openSong={(song) => {
                  setSelectedSong(song)
                  navigate("/song")
                }}
              />
            }
          />
          <Route
            path="/song"
            element={
              <SongDetailsPage
                song={selectedSong}
                back={() => navigate("/")}
                openArtist={() => navigate("/artist")}
              />
            }
          />
          <Route
            path="/artist"
            element={<ArtistAnalyticsPage back={() => navigate("/song")} />}
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  )
}

export default function App() {
  const [authenticated, setAuthenticated] = useState(() =>
    Boolean(localStorage.getItem("lyra_token")),
  )
  const [username, setUsername] = useState(
    () => localStorage.getItem("lyra_username") || "Listener",
  )
  const [ingestRequest, setIngestRequest] = useState<{ title: string } | null>(
    null,
  )

  function logout() {
    localStorage.removeItem("lyra_token")
    localStorage.removeItem("lyra_username")
    setAuthenticated(false)
  }

  return (
    <>
      {/* Модалният прозорец може да стои тук за цялото приложение */}
      {ingestRequest && (
        <IngestSongModal
          initialTitle={ingestRequest.title}
          close={() => setIngestRequest(null)}
        />
      )}

      <Routes>
        {!authenticated ? (
          <>
            <Route
              path="/login"
              element={
                <LoginPage
                  onSuccess={(name) => {
                    setUsername(name)
                    setAuthenticated(true)
                  }}
                />
              }
            />
            <Route
              path="/register"
              element={
                <RegisterPage
                  onSuccess={(name) => {
                    setUsername(name)
                    setAuthenticated(true)
                  }}
                />
              }
            />
            <Route path="*" element={<Navigate to="/login" replace />} />
          </>
        ) : (
          <Route
            path="/*"
            element={
              <AuthenticatedLayout
                username={username}
                logout={logout}
                requestSong={(title) => setIngestRequest({ title })}
              />
            }
          />
        )}
      </Routes>
    </>
  )
}