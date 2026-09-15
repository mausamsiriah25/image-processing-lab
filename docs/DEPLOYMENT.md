# Deployment Guide

This project deploys as two independent services: the frontend to **Vercel**
and the backend to **Render**. Neither has been deployed yet — these are the
exact steps to do so; the site is not live until you complete them.

## 1. Backend → Render

1. Push this repository to GitHub.
2. In Render, create a **New Web Service** and connect the repository.
3. Configure:
   - **Root directory:** `backend`
   - **Runtime:** Python 3
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment variables:**
     - `ENVIRONMENT=production`
     - `CORS_ORIGINS=https://<your-vercel-domain>.vercel.app`
     - `CONTENT_DIR=/opt/render/project/src/content/practicals` (adjust to
       Render's actual checkout path, or leave the default relative path if
       the working directory matches the repo root layout)
4. Alternatively, deploy the provided `backend/Dockerfile` as a Render
   **Docker** web service — it already installs the OpenCV system
   dependencies (`libgl1`, `libglib2.0-0`) that the slim Python image is
   missing.
5. Once deployed, note the public URL, e.g. `https://image-processing-lab-api.onrender.com`.
6. Confirm `GET https://<render-url>/api/health` returns `{"status": "ok"}`.

## 2. Frontend → Vercel

1. In Vercel, import the same GitHub repository as a new project.
2. Configure:
   - **Root directory:** `frontend`
   - **Framework preset:** Vite
   - **Build command:** `npm run build`
   - **Output directory:** `dist`
   - **Environment variable:** `VITE_API_URL=https://<your-render-backend-url>`
3. Deploy. Vercel will give you a `https://<project>.vercel.app` domain.

## 3. Close the loop on CORS

Once both are deployed:

1. Update the backend's `CORS_ORIGINS` environment variable on Render to
   include the exact Vercel domain from step 2 (and redeploy/restart the
   service so the new value takes effect).
2. Reload the Vercel-hosted frontend and confirm the Practicals dashboard
   loads (i.e. `GET /api/practicals` succeeds without a CORS error in the
   browser console).

## 4. Production vs development differences

| Setting | Development | Production |
|---|---|---|
| `ENVIRONMENT` | `development` | `production` |
| `CORS_ORIGINS` | `http://localhost:5173` | Your Vercel domain(s) |
| `VITE_API_URL` | `http://localhost:8000` | Your Render backend URL |
| Backend reload | `uvicorn --reload` | No `--reload` in production start command |

## 5. Post-deployment checklist

- [ ] `GET /api/health` returns `200`.
- [ ] `GET /api/practicals` returns all 11 practicals.
- [ ] A practical page loads its theory/code from the deployed backend.
- [ ] Running an experiment on the deployed site returns real results (not
      a CORS or network error).
- [ ] PDF report generation succeeds and downloads correctly.
- [ ] No `.env` files or secrets were committed to the repository.

Do not consider the project "deployed" until every item above has actually
been verified against the live URLs — a successful local build is not the
same as a working deployment.
