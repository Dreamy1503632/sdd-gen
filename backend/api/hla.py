"""
api/hla.py – HLA (High Level Assessment) endpoints
"""
from __future__ import annotations

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import Response

from models.hla_models import (
    GenerateQuestionnaireRequest,
    HLAAnalysis,
    Industry,
    HCMModule,
)
from services.excel_service import generate_questionnaire_excel
from services.hla_service import analyze_questionnaire, get_analysis

router = APIRouter()


# ── POST /rebuild-questions ───────────────────────────────────────────────────

@router.post("/rebuild-questions", summary="Rebuild ChromaDB from Excel files")
async def rebuild_questions() -> dict:
    """
    Re-ingests all Excel files from backend/files/ into ChromaDB.
    Call this whenever the Excel source files are updated.
    """
    from data.question_store import rebuild_store
    count = rebuild_store()
    return {"status": "ok", "documents_loaded": count}


# ── GET /industries ───────────────────────────────────────────────────────────

@router.get("/industries", summary="List available industries")
async def list_industries() -> list[str]:
    return [i.value for i in Industry]


# ── GET /modules ──────────────────────────────────────────────────────────────

@router.get("/modules", summary="List available HCM modules")
async def list_modules() -> list[str]:
    return [m.value for m in HCMModule]


# ── POST /generate-questionnaire ──────────────────────────────────────────────

@router.post("/generate-questionnaire", summary="Generate Excel questionnaire")
async def generate_questionnaire(req: GenerateQuestionnaireRequest) -> Response:
    """
    Returns an Excel (.xlsx) file containing the HLA questionnaire
    tailored to the selected industry and modules.
    """
    excel_bytes = generate_questionnaire_excel(
        industry=req.industry.value,
        modules=[m.value for m in req.modules],
    )
    filename = (
        f"Oracle_Fusion_HCM_Assessment_{req.industry.value.replace(' ', '_')}.xlsx"
    )
    return Response(
        content=excel_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# ── POST /upload-analyze ──────────────────────────────────────────────────────

@router.post("/upload-analyze", response_model=HLAAnalysis, summary="Upload & AI-analyze questionnaire")
async def upload_and_analyze(file: UploadFile = File(...)) -> HLAAnalysis:
    """
    Accepts a completed Excel questionnaire, parses it, runs it through the
    AI analysis chain, and returns a structured HLAAnalysis object.
    The session_id in the response can be used to generate an SDD.
    """
    if not file.filename or not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Only .xlsx / .xls files are accepted.")

    file_bytes = await file.read()
    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    analysis = await analyze_questionnaire(
        file_bytes=file_bytes,
        file_name=file.filename,
    )
    return analysis


# ── GET /{session_id} ─────────────────────────────────────────────────────────

@router.get("/{session_id}", response_model=HLAAnalysis, summary="Retrieve HLA analysis by session")
async def get_hla_analysis(session_id: str) -> HLAAnalysis:
    analysis = get_analysis(session_id)
    if not analysis:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found.")
    return analysis
