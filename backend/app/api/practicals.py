from fastapi import APIRouter, HTTPException

from ..services.content_service import ContentNotFoundError, get_practical, list_practicals

router = APIRouter(tags=["practicals"])


@router.get("/api/practicals")
def get_practicals() -> dict:
    items = list_practicals()
    summaries = [
        {
            "id": p["id"],
            "number": p["number"],
            "type": p["type"],
            "title": p["title"],
            "category": p["category"],
            "aim": p["aim"],
            "requiresImage": p["requiresImage"],
            "multiImage": p.get("multiImage", False),
        }
        for p in items
    ]
    return {"practicals": summaries, "total": len(summaries)}


@router.get("/api/practicals/{practical_id}")
def get_practical_detail(practical_id: str) -> dict:
    try:
        return get_practical(practical_id)
    except ContentNotFoundError as exc:
        raise HTTPException(status_code=404, detail={"error": {"code": "NOT_FOUND", "message": str(exc)}})
