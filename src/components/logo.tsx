import { cn } from "@/lib/utils"
import type { SVGProps } from "react"

export const Logo = ({ className, ...props }: SVGProps<SVGSVGElement>) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="1.5"
    strokeLinecap="round"
    strokeLinejoin="round"
    className={cn(className)}
    {...props}
  >
    <path d="M12 2a10 10 0 0 0-7.5 16.5A10 10 0 0 0 12 22a10 10 0 0 0 7.5-3.5A10 10 0 0 0 12 2z" />
    <path d="M12 6c-2 0-4 1-5 2.5" />
    <path d="M12 6c2 0 4 1 5 2.5" />
    <path d="M12 12c-2 0-4-1-5-2.5" />
    <path d="M12 12c2 0 4-1 5-2.5" />
    <path d="M12 18c-2 0-4-1-5-2.5" />
    <path d="M12 18c2 0 4-1 5-2.5" />
  </svg>
)
