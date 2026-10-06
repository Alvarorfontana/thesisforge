import { cn } from "@/lib/utils";
import { ButtonHTMLAttributes } from "react";

export function Button({ className, ...props }: ButtonHTMLAttributes<HTMLButtonElement>) {
  return (
    <button
      className={cn(
        "gradient-btn rounded-xl px-5 py-2.5 font-semibold text-white transition-transform",
        "hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50",
        className
      )}
      {...props}
    />
  );
}
