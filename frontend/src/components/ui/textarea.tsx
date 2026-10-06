import { cn } from "@/lib/utils";
import { TextareaHTMLAttributes } from "react";

export function Textarea({ className, ...props }: TextareaHTMLAttributes<HTMLTextAreaElement>) {
  return (
    <textarea
      className={cn(
        "w-full rounded-xl border border-border bg-surface px-4 py-2.5",
        "placeholder:text-zinc-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50",
        className
      )}
      {...props}
    />
  );
}
