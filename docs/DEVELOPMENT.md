# Development Guide

## Running both servers locally

Two terminals:

```bash
# Terminal 1 — backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000

# Terminal 2 — frontend
cd frontend
npm install
cp .env.example .env
npm run dev
```

Visit `http://localhost:5173`. The frontend calls the backend at
`VITE_API_URL` (default `http://localhost:8000`).

## Project conventions

Read [`CLAUDE.md`](../CLAUDE.md) first — it is the authoritative rulebook for
architecture, coding conventions, and how to add a practical. This file only
covers day-to-day workflow.

## Backend development

- All image-processing logic lives in `backend/app/processors/*.py`. Route
  handlers in `backend/app/api/` stay thin — they validate input and call the
  registry.
- `backend/app/processors/base.py` defines the shared `ProcessingResult` /
  `Output` types and the `image_output` / `chart_output` / `value_output` /
  `table_output` helpers — use these instead of hand-rolling output dicts.
- Content (aim/theory/code/parameters) lives in `content/practicals/*.json`,
  not in Python or React. `backend/app/services/content_service.py` loads it
  with an in-memory cache; call `reload_cache()` in tests if you mutate
  content on disk mid-test-run.

### Running the test suite

```bash
cd backend
pytest -v
```

`tests/test_processors.py` covers every one of the 11 processors; the bar
for a new processor is: given a valid image (and valid params), it returns
`success=True` with at least one well-formed output.

## Frontend development

- All backend calls go through `src/services/*.ts` — never call `fetch`
  directly from a component.
- Practical-specific UI (theory, code, parameter form, results) is entirely
  data-driven from the practical's content JSON and the processing result —
  there should be no per-practical React components. If a practical needs a
  new *kind* of parameter or output, extend `ParameterControls.tsx` /
  `ResultGrid.tsx` generically rather than special-casing a practical id.
- Theme preference persists to `localStorage` under the `ipl-theme` key via
  `useTheme.ts`.

## Adding a practical

See `CLAUDE.md` §12 and the README's "Adding a New Practical" section.

## Common issues

- **CORS errors in the browser console:** confirm `CORS_ORIGINS` in the
  backend `.env` includes the frontend's origin (e.g.
  `http://localhost:5173`).
- **"Could not reach the backend" in the UI:** confirm the backend is
  running and `VITE_API_URL` in the frontend `.env` points to it.
- **A practical's content 404s:** confirm
  `content/practicals/<id>.json` exists and its `id` field matches the
  practical id used in the URL and in `registry.py`.
