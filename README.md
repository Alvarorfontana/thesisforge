# 🎓 ThesisForge

Generador de módulos de tesis con **rigor global y contexto argentino** (enfoque glocal).
Backend en FastAPI (asíncrono) + Frontend en Next.js 14 (dashboard premium).

## ✨ Características

- 🔎 Búsqueda paralela en 10 repositorios (globales + argentinos)
- 🆓 APIs 100% gratuitas (Semantic Scholar, OpenAlex, arXiv, Crossref, OAI-PMH)
- 🤖 Generación con Claude 3.5 Sonnet (streaming en tiempo real)
- 🇦🇷 Priorización de fuentes argentinas (SNRD, SEDICI/UNLP, FAUBA, CONICET)
- 🎨 Dashboard premium: glassmorphism, gradientes animados, Framer Motion

## 🚀 Inicio rápido

### Backend
```bash
cd backend
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # pegá tu ANTHROPIC_API_KEY
python -m app.db.init_db
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Abrí http://localhost:3000

## 📚 Repositorios conectados

| Origen | Fuente | Tipo |
|---|---|---|
| 🌎 Global | Semantic Scholar | 200M+ papers, sin key |
| 🌎 Global | OpenAlex | 250M+ obras, sin key |
| 🌎 Global | CORE | 300M+ docs (key gratuita) |
| 🌎 Global | arXiv / Crossref / LA Referencia | sin key |
| 🇦🇷 Argentina | SNRD (MinCyT) | federador nacional |
| 🇦🇷 Argentina | SEDICI (UNLP) / FAUBA / CONICET | OAI-PMH + DSpace |

## 📁 Estructura

```
thesisforge/
├── backend/            # FastAPI + conectores + LLM
│   ├── app/connectors/ # 10 fuentes (base + 9 implementaciones)
│   ├── app/services/   # aggregator, llm_service, thesis_engine
│   ├── app/routers/    # generate (SSE), search, projects
│   └── app/db/         # SQLAlchemy + init
└── frontend/           # Next.js 14 dashboard premium
    └── src/components/ # Sidebar, TopBar, ModuleBuilder, UI
```

## 🔑 API keys

- **Anthropic** (requerida): https://console.anthropic.com
- **CORE** (opcional, gratis): https://core.ac.uk/services/api
- El resto de las fuentes funcionan sin key.

## 📄 Licencia

MIT — Desarrollado por Álvaro
