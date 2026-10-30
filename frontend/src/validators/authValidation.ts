// src/validators/authValidation.ts

import { z } from "zod"

// Validation schema for user registration
export const registerSchema = z.object({
  username: z
    .string()
    .min(3, { message: "Username must be at least 3 characters long" })
    .max(30, { message: "Username cannot exceed 30 characters" }),
  email: z
    .string()
    .email({ message: "Invalid email address format" }),
  password: z
    .string()
    .min(6, { message: "Password must be at least 6 characters long" }),
})

// Validation schema for user login
export const loginSchema = z.object({
  email: z
    .string()
    .email({ message: "Invalid email address" }),
  password: z
    .string()
    .min(6, { message: "Password is required" }),
})

// Infer TypeScript types directly from Zod schemas
export type RegisterFormData = z.infer<typeof registerSchema>
export type LoginFormData = z.infer<typeof loginSchema>