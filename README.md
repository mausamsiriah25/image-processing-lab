# Image Processing Lab

An interactive, browser-based Image Processing Laboratory. Students read the
Aim/Objectives/Theory/Algorithm of each practical, view the real Python/OpenCV
implementation, upload an image, tune parameters, run the **actual** backend
processing, inspect the results, and generate a formatted PDF report.

Built around the practicals in `Image_Processing_lab.md` (Course N-PECCS502P).

## Features

- 11 practicals — image fundamentals, geometric transforms, spatial-domain
  enhancement, filtering, restoration/inpainting, lossless compression,
  morphological operations, correlation-based object detection, colour space
  conversion, and edge-detection comparison.
- Every experiment calls a real backend processor (OpenCV/NumPy/Pillow/
  Matplotlib) — nothing is a static/fake demo image.
- Reference Python code viewer with syntax highlighting, line numbers, copy,
  and fullscreen.
- Drag-and-drop image upload with validation.
- Practical-specific parameter controls (sliders, selects, etc.) with reset.
- Multi-output results: images, histograms/charts, numeric values, and
  tables, rendered generically.
- One-click PDF practical report generation (ReportLab), with a student-info
  form.
- Dark/light mode with persisted preference.
- Fully responsive, accessible UI.

## Screenshots

_Add screenshots of the Home page, Practicals dashboard, and a Practical
workspace here once the app has been run and captured._

## Architecture

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the full system design
and [`docs/PRACTICALS.md`](docs/PRACTICALS.md) for the field-level content
mapping. High level:

```
React (Vite/TS/Tailwind) → FastAPI → Practical Registry → Processor
                                                          (OpenCV/NumPy/Pillow/Matplotlib)
```

```
backend/    FastAPI app: api/, processors/, services/, schemas/, reports/
frontend/   React + Vite + TypeScript + Tailwind app
content/    Structured JSON content for all 11 practicals (single source of
            truth, shared by the API and the PDF report builder)
docs/       Architecture, practicals map, development & deployment guides
```

## Technology Stack

- **Frontend:** React, Vite, TypeScript, Tailwind CSS, React Router, lucide-react
- **Backend:** Python, FastAPI, Pydantic
- **Image processing:** OpenCV, NumPy, Pillow, Matplotlib
- **PDF reports:** ReportLab
- **Testing:** pytest (backend)

## Local Setup

### Prerequisites

- Python 3.11+
- Node.js 18+

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # adjust CORS_ORIGINS / paths if needed
uvicorn app.main:app --reload --port 8000
```

The API is now at `http://localhost:8000`. Interactive docs: `http://localhost:8000/docs`.

### Frontend

```bash
cd frontend
npm install
cp .env.example .env            # set VITE_API_URL if not localhost:8000
npm run dev
```

The app is now at `http://localhost:5173`.

## Environment Variables

**Backend** (`backend/.env`):

| Variable | Purpose | Default |
|---|---|---|
| `ENVIRONMENT` | `development` or `production` | `development` |
| `CORS_ORIGINS` | Comma-separated list of allowed frontend origins | `http://localhost:5173,http://127.0.0.1:5173` |
| `MAX_UPLOAD_SIZE_BYTES` | Max accepted upload size | `15728640` (15 MB) |
| `MAX_IMAGE_DIMENSION` | Max accepted image width/height in px | `6000` |
| `CONTENT_DIR` | Path to the practical content JSON directory | `../content/practicals` |

**Frontend** (`frontend/.env`):

| Variable | Purpose | Default |
|---|---|---|
| `VITE_API_URL` | Base URL of the backend API | `http://localhost:8000` |

## Running Tests

```bash
cd backend
pip install -r requirements.txt   # includes pytest
pytest
```

Every practical processor has a test asserting it returns a well-formed,
successful `ProcessingResult` for valid input, plus tests for the registry,
image-validation service, and error paths (missing images, bad params, etc.).

## Building for Production

```bash
cd frontend
npm run build      # outputs static assets to frontend/dist
```

The backend needs no build step — it runs directly via `uvicorn`.

## Adding a New Practical

1. Add a content JSON file to `content/practicals/<id>.json` following the
   schema in `CLAUDE.md` §6.
2. Add a processor module `backend/app/processors/<id>.py` implementing
   `process(images, params) -> ProcessingResult`.
3. Register it in `backend/app/processors/registry.py`.
4. Add a test in `backend/tests/test_processors.py`.
5. No frontend changes should be needed — the UI is driven entirely by the
   registry and content JSON.

Full rules: see [`CLAUDE.md`](CLAUDE.md) §12.

## Deployment

See [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) for step-by-step Vercel
(frontend) and Render (backend) deployment instructions.

## Contributing

- Follow the conventions in [`CLAUDE.md`](CLAUDE.md) — it's the engineering
  rulebook for this project and should be read before making changes.
- Keep `docs/PRACTICALS.md` in sync with `content/practicals/*.json`.
- Never invent or alter the underlying course content in
  `Image_Processing_lab.md`; it is the source of truth.

## License

MIT — see [`LICENSE`](LICENSE).
