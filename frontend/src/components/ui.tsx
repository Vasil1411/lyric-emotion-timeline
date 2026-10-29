import type {
  ButtonHTMLAttributes,
  HTMLAttributes,
  InputHTMLAttributes,
  ReactNode,
} from "react"
import { LoaderCircle } from "lucide-react"

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "primary" | "secondary" | "ghost"
  loading?: boolean
}

export function Button({
  variant = "secondary",
  loading,
  className = "",
  children,
  disabled,
  ...props
}: ButtonProps) {
  const variants = {
    primary:
      "bg-indigo-500 text-white shadow-lg shadow-indigo-950/40 hover:bg-indigo-400",
    secondary:
      "border border-white/10 bg-white/[0.045] text-slate-200 hover:border-indigo-400/40 hover:bg-white/[0.08]",
    ghost: "text-slate-400 hover:bg-white/[0.05] hover:text-white",
  }

  return (
    <button
      className={`inline-flex items-center justify-center gap-2 rounded-xl px-4 py-2.5 text-sm font-medium transition-all disabled:cursor-not-allowed disabled:opacity-60 ${variants[variant]} ${className}`}
      disabled={disabled || loading}
      {...props}
    >
      {loading ? <LoaderCircle className="size-4 animate-spin" /> : children}
    </button>
  )
}

export function Input({
  className = "",
  ...props
}: InputHTMLAttributes<HTMLInputElement>) {
  return (
    <input
      className={`w-full rounded-xl border border-white/10 bg-slate-950/60 px-4 py-3 text-sm text-white outline-none transition placeholder:text-slate-600 focus:border-indigo-400/70 focus:ring-4 focus:ring-indigo-500/10 ${className}`}
      {...props}
    />
  )
}

export function Card({
  className = "",
  children,
  ...props
}: HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={`rounded-2xl border border-white/[0.09] bg-slate-900/75 ${className}`}
      {...props}
    >
      {children}
    </div>
  )
}

export function Heading({
  as = "h2",
  className = "",
  children,
}: {
  as?: "h1" | "h2" | "h3"
  className?: string
  children: ReactNode
}) {
  const Tag = as
  return <Tag className={className}>{children}</Tag>
}
