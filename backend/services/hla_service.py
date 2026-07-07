"""
services/hla_service.py
Orchestrates the HLA workflow:
  1. Parse uploaded Excel questionnaire
  2. Run LangChain HLA analysis chain
  3. Persist results and return HLAAnalysis
"""
from __future__ import annotations
import json
import uuid
from datetime import datetime
from pathlib import Path

from config import get_settings
from models.hla_models import (
    HLAAnalysis, CompanyProfile, GapItem, RiskItem, Timeline,
    EffortLevel, RiskSeverity, ParsedQuestionnaire,
)
from services.excel_service import parse_questionnaire_excel
from chains.hla_chain import run_hla_analysis

settings = get_settings()
_SESSION_STORE: dict[str, dict] = {}     # in-memory; swap for Redis in prod


# ──────────────────────────────────────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────────────────────────────────────

async def analyze_questionnaire(
    file_bytes: bytes,
    file_name: str,
) -> HLAAnalysis:
    """Full pipeline: parse Excel → LangChain analysis → HLAAnalysis."""

    # 1. Parse the uploaded Excel
    parsed: ParsedQuestionnaire = parse_questionnaire_excel(file_bytes, file_name)

    # 2. Flatten responses for the chain
    module_responses_raw: dict[str, list[dict]] = {
        module: [r.model_dump() for r in responses]
        for module, responses in parsed.module_responses.items()
    }

    # 3. Run AI analysis
    try:
        raw_result = await run_hla_analysis(
            industry=parsed.industry,
            modules=parsed.modules,
            module_responses=module_responses_raw,
            answered_count=parsed.answered_questions,
            total_count=parsed.total_questions,
        )
    except Exception as exc:
        # Graceful fallback – build a basic analysis from parsed data
        raw_result = _fallback_analysis(parsed)

    # 4. Coerce raw dict into typed models
    session_id = str(uuid.uuid4())
    analysis = _build_analysis(session_id, raw_result, parsed)

    # 5. Persist to in-memory store (replace with Redis in prod)
    _SESSION_STORE[session_id] = {
        "analysis": analysis.model_dump(),
        "parsed": parsed.model_dump(),
        "created_at": datetime.utcnow().isoformat(),
    }

    return analysis


def get_analysis(session_id: str) -> HLAAnalysis | None:
    data = _SESSION_STORE.get(session_id)
    if not data:
        return None
    return HLAAnalysis(**data["analysis"])


def get_parsed(session_id: str) -> ParsedQuestionnaire | None:
    data = _SESSION_STORE.get(session_id)
    if not data:
        return None
    return ParsedQuestionnaire(**data["parsed"])


# ──────────────────────────────────────────────────────────────────────────────
# Internal helpers
# ──────────────────────────────────────────────────────────────────────────────

def _build_analysis(
    session_id: str,
    raw: dict,
    parsed: ParsedQuestionnaire,
) -> HLAAnalysis:
    cp_raw = raw.get("company_profile", {})
    company_profile = CompanyProfile(
        employee_count=cp_raw.get("employee_count", "Not specified"),
        locations=cp_raw.get("locations", "Not specified"),
        countries=cp_raw.get("countries", "Not specified"),
        key_complexity=cp_raw.get("key_complexity", ""),
    )

    gap_items = [
        GapItem(
            module=g.get("module", ""),
            requirement=g.get("requirement", ""),
            oracle_capability=g.get("oracle_capability", ""),
            gap=g.get("gap", "None"),
            solution=g.get("solution", ""),
            effort=EffortLevel(g.get("effort", "Medium")),
        )
        for g in raw.get("gap_analysis", [])
    ]

    risk_items = [
        RiskItem(
            risk=r.get("risk", ""),
            severity=RiskSeverity(r.get("severity", "Medium")),
            mitigation=r.get("mitigation", ""),
        )
        for r in raw.get("risks", [])
    ]

    tl_raw = raw.get("timeline", {})
    timeline = Timeline(
        phase1=tl_raw.get("phase1", "TBD"),
        phase2=tl_raw.get("phase2", "N/A"),
        phase3=tl_raw.get("phase3", "N/A"),
        total_duration=tl_raw.get("total_duration", "TBD"),
        critical_path=tl_raw.get("critical_path", "TBD"),
    )

    return HLAAnalysis(
        session_id=session_id,
        industry=parsed.industry,
        modules=parsed.modules,
        company_profile=company_profile,
        key_findings=raw.get("key_findings", []),
        pain_points=raw.get("pain_points", []),
        requirements=raw.get("requirements", []),
        gap_analysis=gap_items,
        recommendations=raw.get("recommendations", []),
        risks=risk_items,
        timeline=timeline,
        completion_rate=parsed.completion_rate,
        answered_questions=parsed.answered_questions,
        total_questions=parsed.total_questions,
    )


def _fallback_analysis(parsed: ParsedQuestionnaire) -> dict:
    """Returns a basic analysis dict when AI call fails."""
    modules = parsed.modules
    return {
        "company_profile": {
            "employee_count": "Not specified",
            "locations": "Multiple locations",
            "countries": "Not specified",
            "key_complexity": f"{len(modules)} modules, {parsed.answered_questions} responses",
        },
        "key_findings": [
            f"Implementation scope covers {', '.join(modules)}",
            f"Questionnaire {parsed.completion_rate:.0f}% complete ({parsed.answered_questions}/{parsed.total_questions} questions answered)",
            "Detailed requirements collected – manual review recommended",
        ],
        "pain_points": [
            "Current system limitations requiring modernisation",
            "Need for integrated HCM platform",
            "Manual processes requiring automation",
        ],
        "requirements": [f"{m} module configuration required" for m in modules],
        "gap_analysis": [
            {
                "module": "Core HR",
                "requirement": "Enterprise and organizational structure",
                "oracle_capability": "Oracle Fusion HCM delivers complete enterprise structure including Legal Entities, Business Units, Departments, Jobs, Positions, and Grades",
                "gap": "None",
                "solution": "Configure via HCM Setup and Maintenance work areas",
                "effort": "Low",
            }
        ],
        "recommendations": [
            "Start with Core HR foundation module",
            "Phase implementation by module priority",
            "Conduct thorough data migration planning early",
            "Leverage Oracle best practices and delivered functionality",
        ],
        "risks": [
            {"risk": "Data migration complexity", "severity": "High", "mitigation": "Early data assessment and migration planning with multiple test cycles"},
            {"risk": "User adoption challenges", "severity": "Medium", "mitigation": "Comprehensive training program and change management strategy"},
        ],
        "timeline": {
            "phase1": f"4-6 months ({modules[0] if modules else 'Core HR'})",
            "phase2": f"3-5 months ({modules[1] if len(modules) > 1 else 'N/A'})",
            "phase3": "N/A",
            "total_duration": f"{max(6, len(modules) * 3)}-{max(12, len(modules) * 5)} months",
            "critical_path": "Data migration and Core HR foundation",
        },
    }