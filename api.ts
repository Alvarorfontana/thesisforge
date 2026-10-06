const API_URL = (process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000").replace(/\/+$/, "");

export const API_BASE = API_URL;

export interface ThesisRef {
  title: string; authors: string; institution: string;
  country: string; year: string; source: string; origin: string; url: string;
}

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

// Render (plan gratis) duerme el servidor: mientras despierta responde con
// errores sin CORS. Probamos /api/health hasta que conteste bien (máx ~2 min).
export async function wakeBackend(onStatus?: (msg: string) => void): Promise<void> {
  for (let i = 0; i < 24; i++) {
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), 10000);
    try {
      const r = await fetch(`${API_URL}/api/health`, { signal: ctrl.signal });
      clearTimeout(timer);
      if (r.ok) return;
    } catch {
      clearTimeout(timer);
    }
    onStatus?.(`Despertando el servidor gratuito… (intento ${i + 1}/24, puede tardar 1-2 minutos)`);
    await sleep(5000);
  }
  throw new Error(
    `El backend (${API_URL}) no respondió después de 2 minutos. Revisá en Render que el servicio diga Live y mirá la pestaña Logs.`
  );
}

export async function streamGenerate(
  topic: string, module: string, ideas: string,
  handlers: {
    onChunk: (text: string) => void;
    onRefs: (refs: ThesisRef[]) => void;
  }
): Promise<void> {
  let res: Response;
  try {
    res = await fetch(`${API_URL}/api/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic, module, ideas }),
    });
  } catch {
    throw new Error(
      `No se pudo conectar con el backend (${API_URL}). ` +
      `Si dice localhost, falta configurar NEXT_PUBLIC_API_URL en Vercel y redeployar sin caché. ` +
      `Si es la URL de Render, puede estar despertando: esperá 1 minuto y probá de nuevo.`
    );
  }
  if (!res.ok || !res.body) {
    throw new Error(`El backend respondió con error HTTP ${res.status}.`);
  }

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const events = buffer.split("\n\n");
    buffer = events.pop() || "";
    for (const ev of events) {
      if (!ev.startsWith("data: ")) continue;
      let msg: { type: string; data: any };
      try { msg = JSON.parse(ev.slice(6)); } catch { continue; }
      if (msg.type === "refs") handlers.onRefs(msg.data);
      else if (msg.type === "chunk") handlers.onChunk(msg.data);
      else if (msg.type === "error") throw new Error(msg.data);
      else if (msg.type === "done") return;
    }
  }
}
