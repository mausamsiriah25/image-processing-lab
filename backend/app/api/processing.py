from __future__ import annotations

import json

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from ..processors.base import ProcessingError
from ..processors.registry import get_definition
from ..services.content_service import ContentNotFoundError, get_practical
from ..services.image_io import decode_upload

router = APIRouter(tags=["processing"])


@router.post("/api/practicals/{practical_id}/process")
async def process_practical(
    practical_id: str,
    params: str = Form(default="{}"),
    image: UploadFile | None = File(default=None),
    image2: UploadFile | None = File(default=None),
    template: UploadFile | None = File(default=None),
    target: UploadFile | None = File(default=None),
) -> dict:
    definition = get_definition(practical_id)
    if definition is None:
        raise HTTPException(
            status_code=404,
            detail={"error": {"code": "NOT_FOUND", "message": f"Unknown practical '{practical_id}'."}},
        )

    try:
        get_practical(practical_id)  # ensures content exists too
    except ContentNotFoundError as exc:
        raise HTTPException(status_code=404, detail={"error": {"code": "NOT_FOUND", "message": str(exc)}})

    try:
        parsed_params = json.loads(params) if params else {}
        if not isinstance(parsed_params, dict):
            raise ValueError
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail={"error": {"code": "INVALID_PARAMS", "message": "Parameters must be a valid JSON object."}},
        )

    uploads = {"image": image, "image2": image2, "template": template, "target": target}
    images = {}
    for role, upload in uploads.items():
        if upload is None:
            continue
        raw = await upload.read()
        try:
            images[role] = decode_upload(raw, upload.content_type)
        except ProcessingError as exc:
            raise HTTPException(
                status_code=422, detail={"error": {"code": "INVALID_IMAGE", "message": str(exc)}}
            )

    if definition.requires_image and "image" not in images and not definition.multi_image:
        raise HTTPException(
            status_code=422,
            detail={"error": {"code": "MISSING_IMAGE", "message": "This practical requires an uploaded image."}},
        )
    if definition.multi_image:
        missing = [role for role in definition.image_roles if role not in images]
        if missing:
            raise HTTPException(
                status_code=422,
                detail={
                    "error": {
                        "code": "MISSING_IMAGE",
                        "message": f"This practical requires images for: {', '.join(missing)}.",
                    }
                },
            )

    try:
        result = definition.processor(images, parsed_params)
    except ProcessingError as exc:
        raise HTTPException(status_code=422, detail={"error": {"code": "PROCESSING_ERROR", "message": str(exc)}})
    except Exception:
        # Never leak stack traces to the client; log server-side instead.
        import logging

        logging.getLogger("processing").exception("Unhandled processor error for %s", practical_id)
        raise HTTPException(
            status_code=500,
            detail={
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "Something went wrong while processing your image. Please try again.",
                }
            },
        )

    return result.to_dict()
