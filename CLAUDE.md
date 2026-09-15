# CLAUDE.md — Engineering Rulebook for Image Processing Lab

This file is the permanent source of truth for how this project is built and
maintained. Any developer or AI agent working on this repository — now or in
the future — must read this file first and follow it.

---

## 1. Project Purpose

**Image Processing Lab** is a public, long-lived educational web application
built around the practicals defined in `Image_Processing_lab.md` (course code
**N-PECCS502P**). It lets students:

- read the Aim / Objectives / Theory / Algorithm / Python code of each practical,
- upload an image (where applicable),
- configure real parameters,
- run the **actual** server-side OpenCV/NumPy/Pillow processing,
- see original + processed outputs (images, histograms, numeric results),
- download outputs, and
- generate a formatted PDF practical report.

The source Markdown (`Image_Processing_lab.md`) is the single source of truth
for course content. **Never invent, remove, or reinterpret practical content.**
UI copy may be reformatted for presentation, but meaning must be preserved.

---

## 2. Source Content Summary (do not contradict this)

The Markdown defines **11 practicals** under course N-PECCS502P:

| ID | Title | Needs Image Upload |
|----|-------|---------------------|
| practical-01 | Python & IDE Setup for Image Processing (Prelab) | No — informational only |
| practical-02 | Image I/O, Colour/Grayscale Conversion, Arithmetic & Bitwise Operations | Yes (1, or 2 for arithmetic/bitwise) |
| practical-03 | 2D Geometric Transformations (Translation, Reflection, Rotation, Scaling, Cropping, Shearing) | Yes |
| practical-04 | Spatial Domain Enhancement (Negative, Brightness/Contrast, Sharpening, Laplacian, Median, Histogram Equalization, Thresholding) | Yes |
| practical-05 | Spatial Domain Filters (Averaging, Box, Gaussian, Median, Bilateral) | Yes |
| practical-06 | Image Restoration — Inpainting (Telea / Navier-Stokes) & Denoising | Yes (optional synthetic damage generator) |
| practical-07 | Lossless Image Compression (JPEG vs PNG, RLE, LZW) | Yes |
| practical-08 | Morphological Operations (Erosion, Dilation, Opening, Closing) + area analysis | Yes |
| practical-09 | Object Detection Using Correlation (Template Matching) | Yes — **two images** (template + target) |
| postlab-02 | Colour Space Conversion (RGB, Grayscale, channels, YCrCb, HSV, Lab) | Yes |
| postlab-03 | Edge Detection — Canny vs Sobel vs Prewitt | Yes |

Full field-level extraction lives in `/docs/PRACTICALS.md`. That file, not this
one, is the canonical per-practical data map.

**Rule:** if a future edit to `Image_Processing_lab.md` changes a practical,
update `/docs/PRACTICALS.md` and the matching `content/practicals/*.json`
file and processor together, in the same change.

---

## 3. Technology Stack (do not swap without strong reason)

**Frontend:** React + Vite + TypeScript + Tailwind CSS + shadcn/ui + Lucide icons.
State: local component state / hooks only. No Redux/MobX/Zustand unless a
genuine cross-cutting need appears later.

**Backend:** Python + FastAPI + Pydantic. Image processing: OpenCV, NumPy,
Pillow, Matplotlib (SciPy only if a specific practical needs it — none
currently do).

**PDF:** ReportLab.

**Database:** SQLite via SQLAlchemy (or an equivalently thin abstraction),
used only where actually needed (see §9). Not required to run the core lab.

**Deployment:** Frontend → Vercel. Backend → Render (or equivalent Python/
FastAPI-capable host). Repo → GitHub.

Do not introduce Kubernetes, Redis, Kafka, GraphQL, microservices, or user
authentication in V1. See `Image_Processing_lab.md` "DO NOT OVERENGINEER".

---

## 4. Architecture

```
React UI → API client (services/) → FastAPI routes (api/) → Practical
Registry → Processor (processors/practicalNN.py) → OpenCV/NumPy/Pillow →
ProcessingResult → JSON response → React result renderer
```

Route handlers **never** contain image-processing logic. They:
1. validate the request (Pydantic schema),
2. look up the practical in the registry,
3. call `processor.process(image(s), parameters) -> ProcessingResult`,
4. serialize `ProcessingResult` to JSON (base64 images / numeric data),
5. return it.

### Backend layout

```
backend/
  app/
    main.py                 # FastAPI app, CORS, router mounting
    api/                     # route handlers only, no processing logic
      health.py
      practicals.py
      processing.py
      reports.py
    processors/               # one file per practical, pure functions
      base.py                 # ProcessingResult / Output dataclasses, shared interface
      practical01.py
      practical02.py
      ...
      postlab02.py
      postlab03.py
      registry.py              # maps practical id -> processor module + metadata
    services/                  # cross-cutting logic (image IO, temp file mgmt, validation)
    schemas/                   # Pydantic request/response models
    models/                    # SQLAlchemy models (only if/when persistence is added)
    utils/                     # small shared helpers (encode/decode base64, etc.)
    core/                      # settings, config, constants
    reports/                   # ReportLab PDF generation
  tests/
```

### Frontend layout

```
frontend/
  src/
    components/       # reusable UI: CodeViewer, ImageUploader, ParameterControls,
                       # ResultGrid, BeforeAfterSlider, ReportDialog, etc.
    pages/             # Home, PracticalsDashboard, PracticalDetail
    layouts/           # AppShell, Navbar, Footer
    hooks/              # useTheme, usePracticalContent, useProcessing
    services/           # api.ts, practicalService.ts, processingService.ts, reportService.ts
    types/               # shared TS types (mirrors backend Pydantic schemas)
    utils/
    data/                 # generated/copied practical content JSON (build-time import)
```

### Content layout

```
content/
  practicals/
    practical-01.json
    practical-02.json
    ...
    postlab-02.json
    postlab-03.json
```

Each JSON file is generated from `Image_Processing_lab.md` (or hand-authored
once from it) following the schema in §6. It is the single structured source
both frontend copy and backend report generation read from — **never
duplicate this content by hardcoding it a second time** in a React component
or a Python processor docstring.

---

## 5. Practical Processing Engine Rules

- **No giant if/elif dispatcher.** Every practical is its own module in
  `backend/app/processors/`, registered in `registry.py`.
- Every processor exposes the same interface:

  ```python
  def process(images: dict[str, np.ndarray], params: dict) -> ProcessingResult:
      ...
  ```

  `images` is keyed (e.g. `"image"`, `"template"`, `"target"`) because some
  practicals (09) need more than one image.

- `ProcessingResult` (defined once in `processors/base.py`) supports:
  - `success: bool`
  - `processing_time: float`
  - `outputs: list[Output]` — each with `name`, `type` (`"image" | "chart" |
    "value" | "table"`), `data`, optional `caption`
  - `metadata: dict`
  - `warnings: list[str]`

  Never force a practical into a single-output shape it doesn't have
  (compression and morphology practicals need numeric/table outputs
  alongside images).

- **Reference vs Web Execution code.** The classroom code (with
  `cv2.imshow`/`cv2.waitKey`/hardcoded local paths) is stored verbatim in the
  practical's content JSON as `"referenceCode"` and shown to students as-is.
  The actual server processor is separate, server-safe Python that
  implements the same algorithm — never silently replaces the taught
  algorithm with a different one. Where the two differ (e.g. no `imshow`,
  images passed as arrays instead of file paths), the UI must label them
  "Reference Python Implementation" and "Web Execution Implementation".

---

## 6. Content Schema

```jsonc
{
  "id": "practical-04",
  "number": 4,
  "type": "practical",          // "practical" | "postlab"
  "title": "Spatial Domain Image Enhancement",
  "category": "Image Enhancement",
  "requiresImage": true,
  "multiImage": false,           // true only for practical-09 (template + target)
  "aim": "...",
  "objectives": ["...", "..."],
  "theory": "... (markdown-safe string, may include ## subheadings)",
  "algorithm": ["step 1", "step 2"],
  "referenceCode": "```python\n...\n```",
  "syntax": ["cv2.threshold(...)", "..."],
  "parameters": [
    {
      "key": "threshold",
      "label": "Threshold value",
      "type": "slider",
      "min": 0, "max": 255, "default": 120, "step": 1
    }
  ],
  "expectedOutputs": ["Negative Image", "Histogram Equalized Image", "..."],
  "observation": "...",
  "conclusion": "...",
  "postLab": ["question 1", "question 2"]
}
```

Rules:
- `parameters` only lists controls that are genuinely exposed for that
  practical (per `Image_Processing_lab.md`'s own operations) — do not invent
  sliders for fixed classroom values.
- `referenceCode` must be copied faithfully from the Markdown, fenced as
  Python, unmodified.
- This schema is authoritative for both frontend rendering and PDF report
  generation. Do not create a second content representation.

---

## 7. API Conventions

```
GET  /api/health
GET  /api/practicals
GET  /api/practicals/{id}
POST /api/practicals/{id}/process     # multipart: image(s) + JSON params
POST /api/practicals/{id}/report      # JSON: student info + last result reference
```

- Request/response bodies are Pydantic models in `schemas/`.
- Errors return a consistent JSON shape: `{"error": {"code": "...",
  "message": "human-readable"}}`. Never leak stack traces.
- OpenAPI docs are generated automatically by FastAPI — keep route
  docstrings accurate.

---

## 8. Report Generation Rules

- Built with ReportLab in `backend/app/reports/`.
- One report template function per report "kind" is unnecessary — build one
  general report builder that takes the practical content JSON + the last
  `ProcessingResult` + student info, and lays out sections generically
  (title, aim, objectives, theory, algorithm, code block, input/output
  images, observation, conclusion).
- Must never overflow images off the page; scale to a max content width.
- If a practical has many outputs (e.g. practical-04's 5 threshold types),
  lay them out in a grid, not one-per-page.
- Report generation failures return a clear error; never a partially-broken
  PDF silently marked successful.

---

## 9. Data / Persistence Rules

- No login/accounts in V1.
- SQLite is optional infrastructure, not a requirement — only add a table
  when there's a concrete need (e.g. later: experiment history). Do not
  pre-build `users`/`experiments`/`reports` tables speculatively.
- Uploaded images and generated outputs live in a request-scoped temp
  directory and are deleted after the response is sent (or on a cleanup
  timer as a safety net).

---

## 10. Security Rules

- Never execute user-supplied Python. The backend only ever calls the fixed,
  registered processor functions.
- Validate uploaded file type (JPG/JPEG/PNG/WEBP), size, and decoded image
  dimensions before processing.
- Use unique generated filenames for any temp file; never trust the
  client-provided filename for a path.
- Configure CORS explicitly (frontend origin only, per environment).

---

## 11. Coding Conventions

**Python:** PEP 8, type hints on all processor/service functions, docstrings
on public functions, small single-purpose functions.

**TypeScript:** strict mode, no `any`, typed API responses (types mirror
backend Pydantic schemas), components split when they exceed roughly one
clear responsibility.

**General:** no duplicated logic between frontend and backend content
sources; no dead/commented-out code committed; no placeholder text
("Lorem ipsum", "Coming soon", "Dummy output") in shipped features — mark
unfinished features as TODO in code comments and keep them out of the nav
until real.

---

## 12. Rules for Adding a New Practical

1. Add/update the structured content JSON in `content/practicals/`.
2. Add a processor module in `backend/app/processors/`.
3. Register it in `backend/app/processors/registry.py`.
4. Add/extend Pydantic parameter schema if new parameter shapes are needed.
5. Add a processor test in `backend/tests/`.
6. No frontend code changes should be required beyond what the registry-driven
   UI already renders generically — if a new *kind* of output or parameter
   control is needed, extend the generic renderers, not one-off UI.

---

## 13. Rules for Future Developers / AI Agents

- Inspect existing files before modifying them; prefer the smallest correct
  diff.
- Never delete working functionality to "clean up" without replacing it with
  something that preserves behavior.
- Do not change an algorithm's behavior without a documented reason tied to
  the source Markdown.
- If a requirement is ambiguous, resolve it by re-reading
  `Image_Processing_lab.md` and this file before guessing.
- Keep `/docs/PRACTICALS.md` in sync with `content/practicals/*.json` — they
  must never diverge.
- Log significant architectural decisions in `/docs/ARCHITECTURE.md`.
