import { API_BASE_URL } from "./api"


export const getAuthHeaders = () => {
  const token = localStorage.getItem("lyra_token")
  return {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  }
}


export async function registerUser(username: string, email: string, password: string) {
  const response = await fetch(`${API_BASE_URL}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, email, password }),
  })
  
  if (!response.ok) {
    const errData = await response.json().catch(() => ({}))
    throw new Error(errData.detail || "Failed to register user.")
  }
  
  return await response.json()
}


export async function loginUser(emailOrUsername: string, password: string) {
  const formData = new URLSearchParams()
  formData.append("username", emailOrUsername) 
  formData.append("password", password)

  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: formData,
  })
  
  if (!response.ok) {
    throw new Error("Invalid email or password.")
  }
  
  const data = await response.json()
  if (data.access_token) {
    localStorage.setItem("lyra_token", data.access_token)
    localStorage.setItem("lyra_user_id", data.user_id)
  }
  
  return data
}