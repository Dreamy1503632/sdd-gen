"""
api/cwb.py – Configuration Workbook endpoints
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, StreamingResponse

from models.cwb_models import GenerateCWBRequest, CWBSummaryResponse
from services.cwb_service import generate_cwb_stream, get_cwb_file_path, _module_slug

router = APIRouter()

# In-memory store reference (populated by cwb_service)
from services.cwb_service import _CWB_STORE


# ── POST /generate ────────────────────────────────────────────────────────────

@router.post("/generate", summary="Generate CWBs (Server-Sent Events stream)")
async def generate_cwb(req: GenerateCWBRequest) -> StreamingResponse:
    """
    Streams CWB generation progress as Server-Sent Events.
    Each event is a JSON-encoded CWBGenerationProgress object.
    The final event has status="complete" and includes download_urls per module.
    """

    async def event_stream():
        async for progress in generate_cwb_stream(
            sdd_session_id=req.sdd_session_id,
            modules=req.modules,
            company_name=req.company_name,
        ):
            yield f"data: {progress.model_dump_json()}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


# ── GET /{session_id} ─────────────────────────────────────────────────────────

@router.get("/{session_id}", response_model=CWBSummaryResponse, summary="Get CWB summary")
async def get_cwb_summary(session_id: str) -> CWBSummaryResponse:
    data = _CWB_STORE.get(session_id)
    if not data:
        raise HTTPException(status_code=404, detail=f"CWB session '{session_id}' not found.")

    cwb = data["cwb"]
    download_urls = data.get("download_urls", {})

    return CWBSummaryResponse(
        session_id=session_id,
        company_name=cwb.get("company_name", ""),
        modules_generated=cwb.get("modules", []),
        total_setup_tasks=cwb.get("total_setup_tasks", 0),
        download_urls=download_urls,
    )


# ── GET /download/{session_id}/{module} ───────────────────────────────────────

@router.get(
    "/download/{session_id}/{module}",
    summary="Download specific module CWB as Excel",
)
async def download_cwb(session_id: str, module: str) -> FileResponse:
    """
    Downloads the Excel configuration workbook for a specific module.
    The `module` path parameter should be the URL-encoded module slug,
    e.g. `core_hr`, `talent_management`, `compensation_and_benefits`.
    """
    path = get_cwb_file_path(session_id, module)
    if not path:
        raise HTTPException(
            status_code=404,
            detail=f"CWB file for module '{module}' in session '{session_id}' not found.",
        )

    filename = path.name
    return FileResponse(
        path=str(path),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=filename,
    )


# ── POST /download/{module} ───────────────────────────────────────────────────
# Convenience alias matching the frontend's POST /api/cwb/download/{module}

@router.post("/download/{module}", summary="Download CWB (POST alias with session in body)")
async def download_cwb_post(module: str, body: dict) -> FileResponse:
    session_id = body.get("session_id", "")
    if not session_id:
        raise HTTPException(status_code=400, detail="session_id is required.")
    return await download_cwb(session_id, module)
