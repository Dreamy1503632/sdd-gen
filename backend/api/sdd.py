"""
api/sdd.py – Solution Design Document endpoints
"""
from __future__ import annotations
import json

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, StreamingResponse

from models.sdd_models import (
    GenerateSDDRequest,
    SDDGenerationProgress,
    SDDDocument,
    SDDSummaryResponse,
)
from services.sdd_service import generate_sdd_stream, get_sdd, get_sdd_docx_path

router = APIRouter()


# ── POST /generate ────────────────────────────────────────────────────────────

@router.post("/generate", summary="Generate SDD (Server-Sent Events stream)")
async def generate_sdd(req: GenerateSDDRequest) -> StreamingResponse:
    """
    Streams SDD generation progress as Server-Sent Events (SSE).
    Each event is a JSON-encoded SDDGenerationProgress object.

    The final event has status="complete" and includes the session_id
    which can be used to download the DOCX.

    Frontend usage:
        const es = new EventSource('/api/v1/sdd/generate');
    """

    async def event_stream():
        async for progress in generate_sdd_stream(
            hla_session_id=req.hla_session_id,
            config=req.config,
        ):
            data = progress.model_dump_json()
            yield f"data: {data}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",  # disable nginx buffering
        },
    )


# ── GET /{session_id} ─────────────────────────────────────────────────────────

@router.get("/{session_id}", response_model=SDDSummaryResponse, summary="Get SDD summary")
async def get_sdd_summary(session_id: str) -> SDDSummaryResponse:
    sdd = get_sdd(session_id)
    if not sdd:
        raise HTTPException(status_code=404, detail=f"SDD session '{session_id}' not found.")

    return SDDSummaryResponse(
        session_id=sdd.session_id,
        company_name=sdd.config.company_name,
        industry="(see HLA session)",
        modules=sdd.modules if hasattr(sdd, "modules") else [],
        estimated_pages=sdd.estimated_pages,
        section_count=sdd.section_count,
        process_flow_count=sdd.process_flow_count,
        download_url=f"/api/v1/sdd/download/{session_id}",
    )


# ── GET /download/{session_id} ────────────────────────────────────────────────

@router.get("/download/{session_id}", summary="Download SDD as DOCX")
async def download_sdd(session_id: str) -> FileResponse:
    path = get_sdd_docx_path(session_id)
    if not path:
        raise HTTPException(
            status_code=404,
            detail=f"DOCX for session '{session_id}' not found. Generate the SDD first.",
        )

    sdd = get_sdd(session_id)
    company = sdd.config.company_name.replace(" ", "_") if sdd else "Client"
    filename = f"SDD_{company}_{session_id[:8]}.docx"

    return FileResponse(
        path=str(path),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=filename,
    )


# ── POST /download ────────────────────────────────────────────────────────────
# Convenience alias used by the frontend (accepts JSON body with session_id)

@router.post("/download", summary="Download SDD as DOCX (POST alias)")
async def download_sdd_post(body: dict) -> FileResponse:
    session_id = body.get("session_id", "")
    if not session_id:
        raise HTTPException(status_code=400, detail="session_id is required.")
    return await download_sdd(session_id)
