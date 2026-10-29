// src/pages/RegisterPage.tsx
import { useState, type FormEvent } from "react"
import { ChevronRight } from "lucide-react"
import { Link, useNavigate } from "react-router-dom"
import { Button, Heading, Input } from "../components/ui"
import { Logo } from "../components/Logo"
import { AuthLayout } from "../components/AuthLayout"
import { authenticate } from "../lib/api"

export function RegisterPage({ onSuccess }: { onSuccess: (username: string) => void }) {
  const navigate = useNavigate()
  const [username, setUsername] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  async function submit(event: FormEvent) {
    event.preventDefault()
    setLoading(true)
    setError("")
    try {
      const result = await authenticate(email, password, "register", username)
      const displayName = result.username || username.trim() || email.split("@")[0]
      localStorage.setItem("lyra_token", result.access_token)
      localStorage.setItem("lyra_username", displayName)
      onSuccess(displayName)
      navigate("/")
    } catch {
      setError("Backend unavailable. You can continue with the interactive demo.")
    } finally {
      setLoading(false)
    }
  }

  function demo() {
    localStorage.setItem("lyra_token", "demo-session")
    localStorage.setItem("lyra_username", "Alex")
    onSuccess("Alex")
    navigate("/")
  }

  return (
    <AuthLayout
      tagline="Join the emotion engine"
      title="Start listening deeper."
      description="Create an account to save feedback, track emotional analytics, and get custom recommendations."
    >
      <div className="w-full max-w-md">
        <div className="mb-10 lg:hidden">
          <Logo />
        </div>
        <p className="mb-3 text-sm font-medium text-indigo-300">Join Lyra</p>
        <Heading as="h2" className="text-4xl font-semibold tracking-tight text-white">
          Create account.
        </Heading>
        <p className="mt-3 text-sm leading-6 text-slate-500">
          Enter your details to get started with Lyra.
        </p>

        <form className="mt-9 space-y-5" onSubmit={submit}>
          <label className="block">
            <span className="mb-2 block text-xs font-medium text-slate-400">Username</span>
            <Input
              value={username}
              onChange={(event) => setUsername(event.target.value)}
              placeholder="How should we call you?"
              required
            />
          </label>
          <label className="block">
            <span className="mb-2 block text-xs font-medium text-slate-400">Email address</span>
            <Input
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              required
            />
          </label>
          <label className="block">
            <span className="mb-2 block text-xs font-medium text-slate-400">Password</span>
            <Input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              required
            />
          </label>
          {error && (
            <p className="rounded-xl border border-amber-400/20 bg-amber-400/5 p-3 text-xs text-amber-200">
              {error}
            </p>
          )}
          <Button type="submit" variant="primary" loading={loading} className="w-full py-3.5">
            Create account
            <ChevronRight className="size-4" />
          </Button>
        </form>

        <Button onClick={demo} className="mt-3 w-full py-3.5">
          Explore interactive demo
        </Button>

        <p className="mt-7 text-center text-sm text-slate-500">
          Already have an account?{" "}
          <Link to="/login" className="font-medium text-indigo-300 transition hover:text-indigo-200">
            Sign in
          </Link>
        </p>
      </div>
    </AuthLayout>
  )
}