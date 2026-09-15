# Implementation Roadmap — Image Processing Lab

Phases map to the development sequence in the original brief. Each phase
ends with something runnable; nothing is torn down in a later phase.

- **Phase 1 — Discovery.** Analyze `Image_Processing_lab.md`, produce
  `CLAUDE.md`, `docs/ARCHITECTURE.md`, `docs/PRACTICALS.md`, this roadmap.
  ✅ Done.
- **Phase 2 — Content schema + data.** All 11 `content/practicals/*.json`
  files generated programmatically from `Image_Processing_lab.md`
  (verbatim reference code preserved), validated against the schema in
  `CLAUDE.md` §6. ✅ Done.
- **Phase 3 — Backend foundation.** FastAPI app (`app/main.py`), CORS,
  `core/config.py`, health/practicals/processing/reports routers,
  `content_service.py` loading the JSON content with caching. ✅ Done.
- **Phase 4 — Frontend foundation.** Vite+React+TS+Tailwind scaffold,
  routing (Home / Practicals / Practical Detail / About), centralized API
  client (`services/`), theme hook with persisted dark/light preference,
  practicals dashboard with search + category filter. ✅ Done.
- **Phase 5 — Processing engine + all 11 processors.** Modular
  `processors/practicalNN.py` + `postlabNN.py` files, a shared
  `ProcessingResult`/`Output` contract (`processors/base.py`), and a
  central registry (`processors/registry.py`). All 11 processors
  implemented with real OpenCV/NumPy/Matplotlib logic and verified against
  68 assertions run directly in this environment (no mocked/fake outputs).
  ✅ Done.
- **Phase 6 — Interactive workspace UI.** `ImageUploader`,
  `ParameterControls`, `CodeViewer`, `ResultGrid`, `BeforeAfterSlider`
  components; `PracticalDetailPage` wiring upload → parameters → run →
  results → report, generically for every practical (no per-practical
  React components). ✅ Done.
- **Phase 7 — Report generation.** ReportLab `reports/builder.py` generic
  report layout (works across image-heavy, table-heavy, and multi-image
  practicals), `ReportDialog` student-info form, `/api/practicals/{id}/report`
  route. Verified end-to-end against practical-04, -07, and -09 output
  shapes, producing valid multi-page PDFs. ✅ Done.
- **Phase 8 — Testing.** `backend/tests/` pytest suite (processors,
  registry, image validation) — 68 equivalent assertions manually verified
  passing against the real processors in this sandbox (pytest itself
  couldn't be installed offline; the suite is ready to run with
  `pip install -r requirements.txt && pytest`). ✅ Done (verification method
  documented in the implementation summary).
- **Phase 9 — Documentation & deployment prep.** `README.md`, `LICENSE`,
  `.gitignore`, `backend/.env.example`, `frontend/.env.example`,
  `backend/Dockerfile`, `docs/DEVELOPMENT.md`, `docs/DEPLOYMENT.md`. ✅ Done.

## Not yet done / explicitly deferred

- **Live deployment.** Vercel/Render deployment has **not** been performed —
  `docs/DEPLOYMENT.md` gives exact steps, but no live URL exists yet.
- **`npm install` / frontend build verification.** This sandbox has no
  network access, so `npm install` and `vite build` could not be executed
  here. All `.ts`/`.tsx` files were syntax/type-checked with a locally
  available `tsc` (ignoring only the expected "package not installed"
  errors); a real `npm install && npm run build` should be run once before
  deploying.
- **Manual mask drawing** for practical-06 inpainting (documented as a
  deferred feature in `docs/ARCHITECTURE.md` §6 — automatic mask detection
  is implemented instead).
- **Frontend component tests** — the backend has a full pytest suite;
  frontend interaction tests (upload validation, parameter form behavior)
  are not yet written.

**Immediate next step:** run `npm install` in `frontend/` and
`pip install -r requirements.txt` in `backend/` in an environment with
network access, then run both dev servers together and do a manual
click-through pass before deploying per `docs/DEPLOYMENT.md`.
