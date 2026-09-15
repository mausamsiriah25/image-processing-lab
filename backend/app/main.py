"""FastAPI application entrypoint for the Image Processing Lab backend."""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .api import health, practicals, processing, reports
from .core.config import settings
from .processors.base import ProcessingError

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(practicals.router)
app.include_router(processing.router)
app.include_router(reports.router)


@app.exception_handler(ProcessingError)
async def processing_error_handler(request: Request, exc: ProcessingError) -> JSONResponse:
    return JSONResponse(status_code=422, content={"error": {"code": "PROCESSING_ERROR", "message": str(exc)}})
