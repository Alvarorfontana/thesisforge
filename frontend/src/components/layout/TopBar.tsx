"use client";

import { Search, Sparkles } from "lucide-react";
import { Input } from "@/components/ui/input";

export default function TopBar() {
  return (
    <header className="glass mb-6 flex items-center justify-between px-6 py-4">
      <div className="flex items-center gap-2">
        <Sparkles className="text-blue-400" size={22} />
        <h1 className="gradient-text text-lg font-bold">ThesisForge</h1>
      </div>
      <div className="relative w-96">
        <Search
          size={16}
          className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-500"
        />
        <Input placeholder="Buscar en 300M+ documentos…" className="pl-9" />
      </div>
    </header>
  );
}
