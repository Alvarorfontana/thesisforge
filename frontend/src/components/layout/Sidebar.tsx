"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { BookOpen, FileText, Globe, Library, Settings } from "lucide-react";
import { cn } from "@/lib/utils";

const ITEMS = [
  { icon: FileText, label: "Nuevo informe" },
  { icon: Library, label: "Mis proyectos" },
  { icon: Globe, label: "Repositorios" },
  { icon: BookOpen, label: "Plantillas" },
  { icon: Settings, label: "Configuración" },
];

export default function Sidebar() {
  const [active, setActive] = useState(0);
  const [collapsed, setCollapsed] = useState(false);

  return (
    <motion.aside
      animate={{ width: collapsed ? 64 : 240 }}
      className="glass flex h-screen flex-col p-3"
    >
      <button
        onClick={() => setCollapsed(!collapsed)}
        className="mb-4 rounded-lg px-3 py-2 text-left text-xs text-zinc-500 hover:bg-white/5"
      >
        {collapsed ? "»" : "« Colapsar"}
      </button>
      {ITEMS.map((item, i) => (
        <button
          key={item.label}
          onClick={() => setActive(i)}
          className={cn(
            "mb-1 flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm transition-colors",
            active === i
              ? "gradient-btn font-semibold text-white"
              : "text-zinc-400 hover:bg-white/5 hover:text-zinc-200"
          )}
        >
          <item.icon size={18} />
          {!collapsed && <span>{item.label}</span>}
        </button>
      ))}
    </motion.aside>
  );
}
