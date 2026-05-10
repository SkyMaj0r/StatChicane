<div align="center">

<br />

```
███████╗████████╗ █████╗ ████████╗ ██████╗██╗  ██╗██╗ ██████╗ █████╗ ███╗   ██╗███████╗
██╔════╝╚══██╔══╝██╔══██╗╚══██╔══╝██╔════╝██║  ██║██║██╔════╝██╔══██╗████╗  ██║██╔════╝
███████╗   ██║   ███████║   ██║   ██║     ███████║██║██║     ███████║██╔██╗ ██║█████╗  
╚════██║   ██║   ██╔══██║   ██║   ██║     ██╔══██║██║██║     ██╔══██║██║╚██╗██║██╔══╝  
███████║   ██║   ██║  ██║   ██║   ╚██████╗██║  ██║██║╚██████╗██║  ██║██║ ╚████║███████╗
╚══════╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝
```

### F1 Intelligence Platform

*Ask anything. Analyse everything. Predict the podium.*

<br />

![Version](https://img.shields.io/badge/version-2.0-FF4500?style=for-the-badge)
![Status](https://img.shields.io/badge/status-in_development-FFD60A?style=for-the-badge)
![FastF1](https://img.shields.io/badge/FastF1-powered-E8002D?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-30D158?style=for-the-badge)

<br />

</div>

---

## What is StatChicane?

StatChicane is a Formula 1 intelligence platform with two core experiences in a single web application:

**Ask F1** — A natural language statistics agent. Ask any question about F1 history in plain English and get a conversational, data-backed answer powered by the complete F1DB dataset.

> *"Who has the most wins at Monaco?"*
> *"Compare Hamilton and Verstappen's qualifying head-to-head in 2021."*
> *"Which constructor won the most championships in the turbo era?"*

**Race Lab** — An interactive telemetry analysis studio. Explore real session data from every GP weekend — lap times, tyre strategy, speed traces, sector breakdowns, qualifying gaps, and race pace analysis, all visualised interactively.

> *"Show me the speed trace delta between Verstappen and Hamilton at Silverstone 2021 Q3."*
> *"Plot the tyre strategies for the top 5 finishers at the 2023 Bahrain GP."*
> *"Based on practice pace and sector times, who should win Sunday?"*

---

## Screenshots

> 🚧 UI screenshots coming soon — currently in active development.

---

## Architecture

StatChicane v2 is a full-stack rebuild. The v1 prototype (Streamlit + LangChain) proved the concept; v2 is the real product.

```
┌─────────────────────────────────────────────────────────────┐
│                     Next.js Frontend                        │
│         /ask (Ask F1)          /racelab (Race Lab)          │
│     Plotly.js · Recharts · Tailwind CSS · Inter             │
└────────────────────────┬────────────────────────────────────┘
                         │ REST API
┌────────────────────────▼────────────────────────────────────┐
│                     FastAPI Backend                         │
│                                                             │
│   /api/auth        /api/ask          /api/racelab           │
│   JWT Auth         LLM Pipeline      FastF1 Engine          │
└──────┬─────────────────┬──────────────────┬────────────────┘
       │                 │                  │
┌──────▼──────┐  ┌───────▼──────┐  ┌───────▼───────┐
│    MySQL    │  │  Gemini API  │  │    FastF1     │
│   (F1DB)   │  │  (2 passes)  │  │  + Redis      │
└─────────────┘  └──────────────┘  └───────────────┘
```

### The Ask F1 Pipeline — Text-to-SQL-to-Text

```
User Question
     │
     ▼
Pass 1 — Gemini (temp: 0.0)
     │    Schema + question + history → SQL query
     ▼
MySQL Execution
     │    SQL → raw tabular results
     │    (retry loop with error context if SQL fails)
     ▼
Pass 2 — Gemini (temp: 0.3)
     │    Raw results → conversational answer + suggestions
     ▼
Response { answer, sql_used, suggestions, confidence }
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Next.js 14, React, Tailwind CSS v4 |
| **Charts** | Plotly.js (telemetry), Recharts (summary) |
| **Backend** | FastAPI, Python 3.12 |
| **LLM** | Google Gemini 2.0 Flash |
| **Historical Data** | MySQL + [F1DB](https://github.com/F1-SQL/f1-sql) |
| **Telemetry Data** | [FastF1](https://github.com/theOehrly/Fast-F1) |
| **Cache** | Redis |
| **Auth** | JWT (python-jose) |
| **UI Font** | Inter |

---

## Features

### Ask F1
- Natural language querying over all-time F1 statistics
- Multi-turn conversation with context memory
- Two-pass Gemini pipeline: SQL generation + conversational formatting
- SQL error retry loop for resilience
- Suggested follow-up questions after every answer
- Answer confidence indicator
- SQL query transparency toggle

### Race Lab
- **Session Selector** — Season → GP Weekend → FP1/FP2/FP3/Qualifying/Race
- **Lap Time Analysis** — Progression charts, fastest lap comparisons, stint breakdowns
- **Tyre Strategy Map** — Gantt-style compound visualisation for all drivers
- **Speed Trace** — Overlaid on circuit map with D3 colour gradient
- **Telemetry Traces** — Throttle, brake, gear, DRS on shared X axis
- **Qualifying Deep Dive** — Sector heatmaps, gap-to-pole, lap evolution
- **Race Analysis** — Position changes, safety car overlays, gap to leader
- **Who Will Win?** — Pre-weekend, post-qualifying, and mid-race predictor

### Platform
- Dieter Rams–inspired dark UI (`#1C1C1E` charcoal base, `#FF4500` accent)
- Frosted glass sidebar navigation
- Shareable chart URLs
- Mobile responsive
- 🥚 Hidden F1 red (`#FF1E00`) easter egg

---

## Project Structure

```
StatChicane/
├── v1/                          # Original prototype (Streamlit + LangChain)
│
└── v2/                          # Current rebuild
    ├── backend/                 # FastAPI
    │   ├── main.py
    │   ├── requirements.txt
    │   ├── .env.example
    │   └── app/
    │       ├── config.py
    │       ├── database.py
    │       ├── redis_client.py
    │       ├── models/
    │       │   └── ask.py
    │       ├── routers/
    │       │   ├── auth.py
    │       │   ├── ask.py
    │       │   ├── racelab.py
    │       │   └── health.py
    │       ├── services/
    │       │   ├── llm_service.py
    │       │   ├── query_service.py
    │       │   └── schema_service.py
    │       └── prompts/
    │           ├── sql_generation.py
    │           └── response_formatting.py
    │
    └── frontend/                # Next.js
        ├── app/
        │   ├── ask/page.tsx
        │   ├── racelab/page.tsx
        │   ├── layout.tsx
        │   └── globals.css
        ├── components/
        │   ├── layout/
        │   │   ├── AppShell.tsx
        │   │   ├── Sidebar.tsx
        │   │   └── SidebarItem.tsx
        │   └── ui/
        │       └── Logo.tsx
        └── lib/
            └── utils.ts
```

---

## Getting Started

### Prerequisites

| Tool | Version | Check |
|---|---|---|
| Python | 3.9+ | `python --version` |
| Node.js | 18+ | `node --version` |
| MySQL | 8.0+ | `mysql --version` |
| Redis | 7.0+ | `redis-cli ping` |

You also need:
- A [Google Gemini API key](https://aistudio.google.com/)
- The [F1DB dataset](https://github.com/F1-SQL/f1-sql/releases) imported into MySQL

---

### Backend Setup

```bash
# Clone the repo
git clone https://github.com/yourusername/StatChicane.git
cd StatChicane/v2/backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
# venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Fill in your values in .env

# Start the server
uvicorn main:app --reload
```

The API will be live at `http://127.0.0.1:8000`

Interactive API docs at `http://127.0.0.1:8000/docs`

---

### Frontend Setup

```bash
cd StatChicane/v2/frontend

# Install dependencies
npm install

# Start the dev server
npm run dev
```

The app will be live at `http://localhost:3000`

---

### Environment Variables

Copy `v2/backend/.env.example` to `v2/backend/.env` and fill in:

```env
# Database
DATABASE_URL=mysql+mysqlconnector://root:PASSWORD@localhost:3306/f1db

# Redis
REDIS_URL=redis://localhost:6379

# Gemini
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.0-flash

# Auth
JWT_SECRET=your_long_random_secret_string
JWT_ALGORITHM=HS256
JWT_EXPIRY_MINUTES=60

# App
CORS_ORIGINS=http://localhost:3000
FASTF1_CACHE_PATH=./fastf1_cache
```

> ⚠️ Never commit your `.env` file. It is already in `.gitignore`.

---

### Health Checks

With both servers running, verify everything is connected:

```bash
# All services
curl http://127.0.0.1:8000/api/health/all

# Individual checks
curl http://127.0.0.1:8000/api/health/db
curl http://127.0.0.1:8000/api/health/redis
```

Expected response:
```json
{
  "database": { "status": "ok", "database": "connected" },
  "redis": { "status": "ok", "redis": "connected" },
  "overall": "ok"
}
```

---

## Data Sources

### F1DB
[F1DB](https://github.com/F1-SQL/f1-sql) is an open-source MySQL database covering all-time Formula 1 statistics — every race result, qualifying time, championship standing, pit stop, and driver record since 1950. This powers the Ask F1 NLP pipeline.

### FastF1
[FastF1](https://github.com/theOehrly/Fast-F1) is a Python library that interfaces with the official F1 timing API, providing lap-by-lap and telemetry data (speed, throttle, brake, gear, DRS, tyre compounds, position) for every session from 2018 onwards. This powers Race Lab.

---

## Roadmap

### Phase 1 — Foundation ✅
- [x] FastAPI boilerplate + modular routers
- [x] MySQL + Redis connection layer with health checks
- [x] Next.js + Tailwind v4 design system (Dieter Rams palette)
- [x] Left sidebar shell with routing

### Phase 2 — Ask F1 🔄
- [x] Gemini LLM service layer (two-pass pipeline)
- [x] `/ask/query` endpoint with SQL retry loop
- [ ] Conversation history persistence
- [ ] Chat UI with message bubbles and suggestions

### Phase 3 — Race Lab Core ⬜
- [ ] FastF1 caching engine + session loader
- [ ] Session selector UI
- [ ] Lap time, tyre strategy, position charts

### Phase 4 — Advanced Telemetry ⬜
- [ ] Circuit map SVG with speed trace overlay
- [ ] Throttle/brake/gear subplots
- [ ] Who Will Win predictor
- [ ] AI Weekend Summary

### Phase 5 — Polish & Deploy ⬜
- [ ] JWT authentication
- [ ] Shareable chart URLs
- [ ] Docker + Vercel + Railway deployment

---

## Design Philosophy

StatChicane v2 is designed around **Dieter Rams' ten principles of good design**, applied to a data-heavy web application:

> *"Good design is as little design as possible."*

- **Charcoal base** `#1C1C1E` — easy on the eyes, never pure black
- **Rams orange accent** `#FF4500` — purposeful, not decorative
- **Inter typeface** — clean, readable at every size
- **Frosted glass sidebar** — depth without noise
- **No pure black. No pure white.** — everything is considered

---

## Acknowledgements

- [F1DB / F1-SQL](https://github.com/F1-SQL/f1-sql) — the all-time F1 dataset that makes Ask F1 possible
- [FastF1](https://github.com/theOehrly/Fast-F1) — the telemetry library that makes Race Lab possible
- [Formula 1](https://www.formula1.com) — the sport that makes all of this worth building

---

## v1 Reference

The original StatChicane (v1) prototype lives in the `/v1` directory. It was built with Streamlit, LangChain, and Gemini 1.5 Flash and proved the viability of the Text-to-SQL-to-Text pipeline. v2 is a complete rebuild expanding on that foundation.

---

<div align="center">

Built with 🏎️ and way too much coffee

*May the force be with you.*

</div>
