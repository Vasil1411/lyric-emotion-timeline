import { z } from "zod"

// Validation schema for song ingestion (Genius search payload)
export const songIngestSchema = z.object({
  artist: z
    .string()
    .min(1, { message: "Artist name is required" }),
  title: z
    .string()
    .min(1, { message: "Song title is required" }),
})

// Validation schema for user feedback/rating log
export const feedbackSchema = z.object({
  songId: z.number().positive(),
  stanzaId: z.number().nullable().optional(),
  interactionType: z.string().min(1, { message: "Interaction type is required" }),
  rating: z.number().min(-1.0).max(1.0, { message: "Rating must be between -1.0 and 1.0" }),
})

export type SongIngestFormData = z.infer<typeof songIngestSchema>
export type FeedbackFormData = z.infer<typeof feedbackSchema>