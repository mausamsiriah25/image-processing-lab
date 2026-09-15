from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from ..reports.builder import build_report
from ..schemas.report import ReportRequest
from ..services.content_service import ContentNotFoundError, get_practical

router = APIRouter(tags=["reports"])


@router.post("/api/practicals/{practical_id}/report")
def generate_report(practical_id: str, payload: ReportRequest) -> Response:
    try:
        practical = get_practical(practical_id)
    except ContentNotFoundError as exc:
        raise HTTPException(status_code=404, detail={"error": {"code": "NOT_FOUND", "message": str(exc)}})

    try:
        pdf_bytes = build_report(
            practical=practical,
            result=payload.result,
            student_info=payload.studentInfo.model_dump(),
            input_images=payload.inputImages,
        )
    except Exception:
        import logging

        logging.getLogger("reports").exception("Report generation failed for %s", practical_id)
        raise HTTPException(
            status_code=500,
            detail={
                "error": {
                    "code": "REPORT_GENERATION_FAILED",
                    "message": "The report could not be generated. Please try again.",
                }
            },
        )

    filename = f"{practical_id}-report.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
