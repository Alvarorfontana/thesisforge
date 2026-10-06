import { cn } from "@/lib/utils";
import { SelectHTMLAttributes } from "react";

export function Select({ className, children, ...props }: SelectHTMLAttributes<HTMLSelectElement>) {
  return (
    <select
      className={cn(
        "w-full rounded-xl border border-border bg-surface px-4 py-2.5",
        "focus:outline-none focus:ring-2 focus:ring-blue-500/50",
        className
      )}
      {...props}
    >
      {children}
    </select>
  );
}
