import React, { createContext, useContext, useState, useEffect, ReactNode } from "react"
import { loginUser, registerUser } from "../services/userService"
import { User } from "../types/user"

interface AuthContextType {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  login: (email: string, pass: string) => Promise<void>
  register: (username: string, email: string, pass: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(localStorage.getItem("lyra_token"))

  // Initialize user session on mount if token exists
  useEffect(() => {
    const savedToken = localStorage.getItem("lyra_token")
    const savedUserId = localStorage.getItem("lyra_user_id")
    const savedUsername = localStorage.getItem("lyra_username")

    if (savedToken && savedUserId) {
      setToken(savedToken)
      setUser({
        id: Number(savedUserId),
        username: savedUsername || "User",
        email: localStorage.getItem("lyra_email") || "",
      })
    }
  }, [])

  // Handle user login
  const login = async (email: string, pass: string) => {
    try {
      const data = await loginUser(email, pass)
      
      // Save token and user details to localStorage
      localStorage.setItem("lyra_token", data.access_token)
      localStorage.setItem("lyra_user_id", data.user_id)
      if (data.email) localStorage.setItem("lyra_email", data.email)
      
      setToken(data.access_token)
      setUser({
        id: data.user_id,
        username: data.username || email.split("@")[0],
        email: email,
      })
    } catch (error) {
      console.error("Login failed:", error)
      throw error
    }
  }

  // Handle user registration
  const register = async (username: string, email: string, pass: string) => {
    try {
      await registerUser(username, email, pass)
      // Automatically log in after successful registration or redirect to login
      await login(email, pass)
    } catch (error) {
      console.error("Registration failed:", error)
      throw error
    }
  }

  // Handle user logout and clear session state
  const logout = () => {
    localStorage.removeItem("lyra_token")
    localStorage.removeItem("lyra_user_id")
    localStorage.removeItem("lyra_email")
    localStorage.removeItem("lyra_username")

    setToken(null)
    setUser(null)
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated: !!token,
        login,
        register,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

// Custom hook to use AuthContext easily across components
export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider")
  }
  return context
}