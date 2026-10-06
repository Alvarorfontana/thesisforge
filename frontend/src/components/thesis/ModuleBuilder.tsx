"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { Card } from "@/components/ui/card";
import { streamGenerate, type ThesisRef } from "@/lib/api";

const MODULES = [
  { id: "problema", label: "Problema de Investigación" },
  { id: "marco_teorico", label: "Marco Teórico" },
  { id: "metodologia", label: "Metodología" },
  { id: "resultados", label: "Resultados" },
  { id: "discusion", label: "Discusión y Conclusiones" },
  { id: "referencias", label: "Referencias (APA 7)" },
];

export default function ModuleBuilder() {
  const [topic, setTopic] = useState("");
  const [ideas, setIdeas] = useState("");
  const [module, setModule] = useState("marco_teorico");
  const [content, setContent] = useState("");
  const [loading, setLoading] = useState(false);
  const [refs, setRefs] = useState<ThesisRef[]>([]);
  const [showRefs, setShowRefs] = useState(false);
  const [error, setError] = useState("");

  async function generate() {
    if (!topic.trim()) return;
    setLoading(true);
    setError("");
    setContent("");
    setRefs([]);
    try {
      await streamGenerate(topic, module, ideas, {
        onRefs: (r) => setRefs(r),
        onChunk: (chunk) => setContent((prev) => prev + chunk),
      });
    } catch (e: any) {
      setError(e?.message || "Error desconocido al generar.");
    } finally {
      setLoading(false);
    }
  }

  const progress = content ? ((MODULES.findIndex((m) => m.id === module) + 1) / MODULES.length) * 100 : 0;

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_380px]">
      {/* Panel principal */}
      <div className="space-y-6">
        <Card>
          <h2 className="gradient-text mb-1 text-xl font-bold">Nuevo informe de tesis</h2>
          <p className="mb-4 text-sm text-zinc-400">
            Rigor global + contexto argentino, con referencias reales.
          </p>
          <div className="space-y-3">
            <Input
              placeholder="Tema de investigación (ej: impacto de sequías en soja pampeana)"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
            />
            <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
              <Select value={module} onChange={(e) => setModule(e.target.value)}>
                {MODULES.map((m) => (
                  <option key={m.id} value={m.id} className="bg-zinc-900">
                    {m.label}
                  </option>
                ))}
              </Select>
              <Button onClick={generate} disabled={loading || !topic.trim()}>
                {loading ? "Generando…" : "✦ Generar módulo"}
              </Button>
            </div>
            <Textarea
              rows={3}
              placeholder="Ideas clave o datos propios (opcional)…"
              value={ideas}
              onChange={(e) => setIdeas(e.target.value)}
            />
          </div>

          {/* Barra de progreso */}
          <div className="mt-5">
            <div className="mb-1 flex justify-between text-xs text-zinc-500">
              <span>Progreso de la tesis</span>
              <span>{Math.round(progress)}%</span>
            </div>
            <div className="h-2 overflow-hidden rounded-full bg-white/5">
              <motion.div
                className="gradient-btn h-full rounded-full"
                animate={{ width: `${progress}%` }}
                transition={{ type: "spring", stiffness: 80 }}
              />
            </div>
          </div>
        </Card>

        {error && (
          <div className="rounded-xl border border-red-500/40 bg-red-500/10 p-4 text-sm text-red-200">
            ⚠️ {error}
          </div>
        )}

        {/* Editor con streaming */}
        <Card className="min-h-[420px]">
          {content ? (
            <div className="prose prose-invert max-w-none whitespace-pre-wrap text-zinc-200">
              {content}
              {loading && <span className="typing-cursor" />}
            </div>
          ) : (
            <div className="flex h-[380px] items-center justify-center text-zinc-600">
              {loading ? (
                <span className="typing-cursor text-zinc-400">
                  Consultando repositorios y redactando…
                </span>
              ) : (
                "El contenido generado aparecerá acá"
              )}
            </div>
          )}
        </Card>
      </div>

      {/* Panel de referencias */}
      <div>
        <button
          onClick={() => setShowRefs(!showRefs)}
          className="mb-3 text-sm text-blue-400 hover:text-blue-300"
        >
          {showRefs ? "▾ Ocultar" : "▸ Mostrar"} referencias recuperadas
          {refs.length > 0 && ` (${refs.length})`}
        </button>
        {showRefs && (
          <div className="space-y-3">
            {refs.length === 0 && (
              <p className="text-sm text-zinc-500">
                Generá un módulo para ver las tesis de referencia.
              </p>
            )}
            {refs.map((r, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.05 }}
                className={`glass p-4 text-sm ${
                  r.origin === "argentina" ? "border-l-4 border-l-sky-400" : "border-l-4 border-l-violet-400"
                }`}
              >
                <p className="font-semibold text-zinc-100">{r.title}</p>
                <p className="mt-1 text-xs text-zinc-400">
                  {[r.authors, r.institution, r.year].filter(Boolean).join(" · ")}
                </p>
                <span
                  className={`mt-2 inline-block rounded-full px-2 py-0.5 text-[10px] font-medium ${
                    r.origin === "argentina"
                      ? "bg-sky-400/10 text-sky-300"
                      : "bg-violet-400/10 text-violet-300"
                  }`}
                >
                  {r.origin === "argentina" ? "🇦🇷 " : "🌎 "}
                  {r.source}
                </span>
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
