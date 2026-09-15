# Architecture — Image Processing Lab

## 1. System Overview

```
┌─────────────┐     HTTPS      ┌──────────────┐     calls      ┌────────────────────┐
│  React SPA  │ ─────────────► │   FastAPI    │ ─────────────► │ Practical Registry  │
│  (Vercel)   │ ◄───────────── │  (Render)    │ ◄───────────── │  + Processors        │
└─────────────┘   JSON/base64  └──────────────┘   ProcessingResult└───────────────────┘
                                                                          │
                                                                          ▼
                                                           OpenCV / NumPy / Pillow /
                                                           Matplotlib (in-memory, temp dir)
```

- Stateless request/response cycle. No session needed for core lab use.
- Images travel as `multipart/form-data` uploads in, base64-encoded PNG/JPEG
  data out (embedded in JSON), so the frontend can render `<img src="data:...">`
  directly and offer a client-side download without a second round trip.
- PDF report generation is a second endpoint that re-uses the same
  `ProcessingResult` shape (client sends back the last result reference or
  re-runs processing server-side — see §5).

## 2. Request Lifecycle (processing)

1. User opens a practical page → frontend fetches
   `GET /api/practicals/{id}` → renders content, parameter form derived
   from the practical's `parameters` schema.
2. User uploads image(s) (validated client-side: type, size).
3. User adjusts parameters (defaults pre-filled from content schema).
4. User clicks "Run Experiment" → frontend calls
   `POST /api/practicals/{id}/process` with `multipart/form-data`
   (image file(s) + JSON-encoded params field).
5. FastAPI route:
   - validates the practical id exists in the registry,
   - validates uploaded file(s) (type/size/dimensions),
   - decodes image(s) into `numpy.ndarray` via OpenCV/Pillow,
   - validates params against the practical's Pydantic parameter model,
   - calls `registry.get(id).process(images, params)`.
6. Processor returns a `ProcessingResult` (outputs, metadata, timing,
   warnings).
7. Route serializes outputs (images → base64 PNG, charts → base64 PNG from
   Matplotlib, numeric/table data → plain JSON) and returns the response.
8. Frontend renders a `ResultGrid`: one card per output, auto-choosing
   image/chart/value/table presentation based on `type`.
9. Any temp files created server-side are deleted before/after the response
   is sent.

## 3. Request Lifecycle (report)

1. User clicks "Generate Report" on a practical that has a completed result
   in the current session (kept in frontend component state — not persisted
   server-side in V1).
2. A dialog collects student info (name, roll no., USN, semester, section,
   date).
3. Frontend calls `POST /api/practicals/{id}/report` with: student info +
   the practical id + the last `ProcessingResult` payload (images as
   base64) + original input image(s) as base64.
   - Rationale: since V1 has no persistence, the report endpoint is
     stateless and takes everything it needs in the request rather than
     looking up a stored experiment. This keeps the backend simple and
     avoids inventing a database requirement.
4. Backend builds a PDF with ReportLab (`backend/app/reports/builder.py`),
   pulling static content (aim/objectives/theory/algorithm/code) from the
   content JSON for that practical and embedding the images/values passed
   in.
5. Response is the PDF binary (`application/pdf`) with a
   `Content-Disposition` filename like `practical-04-report.pdf`.
6. Frontend triggers a download.

## 4. Practical Registry Pattern

`backend/app/processors/registry.py` holds a dict:

```python
REGISTRY: dict[str, PracticalDefinition] = {
    "practical-04": PracticalDefinition(
        id="practical-04",
        processor=practical04.process,
        requires_image=True,
        multi_image=False,
        parameter_schema=Practical04Params,
    ),
    ...
}
```

The API layer never branches on practical id beyond `registry[id]` lookups.
Adding a practical means adding one entry here plus its processor module and
content JSON — nothing else in the API layer changes.

## 5. Why No Persistence in V1

Every "extra" the assignment could invite (accounts, saved experiment
history, dashboards) is future scope per `Image_Processing_lab.md`'s
"FUTURE-READY ARCHITECTURE" section. Keeping processing and reporting
stateless:
- avoids a database dependency for the core learning workflow,
- keeps deployment trivial (two stateless services),
- keeps the report flow simple (client already has everything needed right
  after running an experiment).

The registry/service boundaries are already shaped so that adding
`models/experiment.py` + a `POST /api/experiments` endpoint later doesn't
require touching processors or the report builder.

## 6. Special-Case Practicals (flagged during discovery)

| Practical | Special handling needed |
|---|---|
| practical-01 | No processing endpoint use — content-only page (setup guide). Registry entry has `requires_image=False` and the "Run Experiment" workspace is replaced with an environment-setup checklist UI. |
| practical-02 | Arithmetic/bitwise operations need **two** images for some sub-operations (add/subtract/AND/OR/XOR) but only one for grayscale/RGB conversion. UI conditionally shows a second uploader based on the selected operation. |
| practical-06 | Inpainting needs a *mask*. The Markdown code both auto-generates a mask (thresholding near-black damaged pixels) and uses a predefined mask file. V1 implements **automatic mask detection** (configurable threshold) as the primary path; manual mask drawing is out of scope for V1 (documented as a future extension point). |
| practical-07 | Output is not primarily a transformed image — it's file-size/compression-ratio numbers plus a verified lossless-reconstruction image. `ProcessingResult` uses `type: "table"`/`"value"` outputs alongside one `type: "image"` reconstruction check. |
| practical-09 | Requires **two** images: a template and a target/scene image (`multiImage: true`). Output includes the annotated target image and a numeric match score. |
| postlab-02 / postlab-03 | Registered as practicals with `type: "postlab"` so they appear in the dashboard under their own category but follow the identical processing contract. |

## 7. Extension Points (not built in V1, but kept clean)

- `models/` is present but empty until persistence is needed.
- Auth: routes are not coupled to a user concept; adding
  `Depends(get_current_user)` later doesn't require restructuring.
- Additional universities/curricula: `content/practicals/` is namespaced by
  practical id, not hardcoded into one giant file, so a second content set
  could live alongside it later (e.g. `content/curricula/<course>/`).
