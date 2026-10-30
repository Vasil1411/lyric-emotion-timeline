export type User = {
  id: number
  username: string
  email: string
  created_at?: string | null
}

export type UserCreatePayload = {
  username: string
  email: string
  password: string
}

export type LoginPayload = {
  email: string
  password: string
}


export type FeedbackRequestPayload = {
  user_id: number
  song_id: number
  stanza_id?: number | null 
  interaction_type: string
  rating: number
}

export type UserFeedback = {
  id: number
  user_id: number
  song_id: number
  stanza_id?: number | null
  interaction_type: string
  rating: number
  is_processed_for_training: boolean
  timestamp?: string
}

export type UserActivity = {
  id: number
  user_id?: number | null
  action_type: string
  query_payload?: string | null
  song_id?: number | null
  timestamp?: string
}