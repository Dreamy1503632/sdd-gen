"""
models/sdd_models.py – request / response schemas for Solution Design Document
"""
from __future__ import annotations
from typing import Optional, Any
from pydantic import BaseModel, Field


# ──────────────────────────────────────────────────────────────────────────────
# Document metadata
# ──────────────────────────────────────────────────────────────────────────────

class SDDConfig(BaseModel):
    company_name: str
    project_name: str = "Oracle Fusion HCM Implementation"
    doc_reference: str = "SDD_V1.0"
    author: str = "Implementation Team"
    version: str = "1.0"
    confidentiality: str = "Confidential"


# ──────────────────────────────────────────────────────────────────────────────
# Chapter content models (what the AI fills in)
# ──────────────────────────────────────────────────────────────────────────────

class DocumentControlEntry(BaseModel):
    version: str
    date: str
    author: str
    description: str


class SDDChapter1(BaseModel):
    """Document Control & Change History"""
    change_history: list[DocumentControlEntry]
    distribution_list: list[str]
    abbreviations: dict[str, str]


class SDDChapter2(BaseModel):
    """Introduction"""
    purpose: str
    scope: str
    implementation_approach: str
    document_overview: str


class BusinessStructureSection(BaseModel):
    section_id: str           # e.g. "3.1"
    title: str
    description: str
    oracle_recommendation: str
    client_decision: str
    configuration_notes: str
    table_data: list[dict[str, Any]] = Field(default_factory=list)


class SDDChapter3(BaseModel):
    """Business Structure – all ~28 subsections"""
    sections: list[BusinessStructureSection]


class ProcessStep(BaseModel):
    step_number: int
    actor: str                # e.g. "HR Specialist", "Manager", "Employee"
    action: str
    system: str               # e.g. "Oracle HCM", "Email"
    outcome: str
    notes: str = ""


class ProcessFlow(BaseModel):
    flow_id: str              # e.g. "4.1"
    title: str
    module: str
    trigger: str
    steps: list[ProcessStep]
    approval_required: bool
    approvers: list[str]
    oracle_transaction: str   # Oracle delivered transaction name
    notes: str = ""


class SDDChapter4(BaseModel):
    """Process Flows"""
    flows: list[ProcessFlow]


class GapEntry(BaseModel):
    gap_id: str
    module: str
    requirement: str
    oracle_capability: str
    gap_description: str
    recommended_solution: str
    effort: str
    workaround: str = ""


class SDDChapter6(BaseModel):
    """Gap Analysis"""
    gaps: list[GapEntry]
    summary: str


class Assumption(BaseModel):
    assumption_id: str
    category: str
    description: str
    impact_if_incorrect: str


class SDDChapter9(BaseModel):
    """Assumptions & Dependencies"""
    assumptions: list[Assumption]
    dependencies: list[str]
    exclusions: list[str]


# ──────────────────────────────────────────────────────────────────────────────
# Full SDD document
# ──────────────────────────────────────────────────────────────────────────────

class SDDDocument(BaseModel):
    session_id: str
    hla_session_id: str
    config: SDDConfig
    modules: list[str] = Field(default_factory=list)
    chapter1: SDDChapter1
    chapter2: SDDChapter2
    chapter3: SDDChapter3
    chapter4: SDDChapter4
    chapter6: SDDChapter6
    chapter9: SDDChapter9
    estimated_pages: int = 0
    section_count: int = 0
    process_flow_count: int = 0
    generation_time_seconds: float = 0


# ──────────────────────────────────────────────────────────────────────────────
# Requests / Responses
# ──────────────────────────────────────────────────────────────────────────────

class GenerateSDDRequest(BaseModel):
    hla_session_id: str
    config: SDDConfig


class SDDGenerationProgress(BaseModel):
    session_id: str
    status: str              # "generating" | "complete" | "failed"
    progress: int
    current_chapter: str
    log_entries: list[str]
    download_url: Optional[str] = None
    document: Optional[SDDDocument] = None


class SDDSummaryResponse(BaseModel):
    session_id: str
    company_name: str
    industry: str
    modules: list[str]
    estimated_pages: int
    section_count: int
    process_flow_count: int
    download_url: str