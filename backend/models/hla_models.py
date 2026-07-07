"""
models/hla_models.py – request / response schemas for High-Level Assessment
"""
from __future__ import annotations
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


# ──────────────────────────────────────────────────────────────────────────────
# Enumerations
# ──────────────────────────────────────────────────────────────────────────────

class Industry(str, Enum):
    MANUFACTURING_DISCRETE  = "Manufacturing - Discrete"
    MANUFACTURING_PROCESS   = "Manufacturing - Process"
    FINANCIAL_BANKING       = "Financial Services - Banking"
    FINANCIAL_INSURANCE     = "Financial Services - Insurance"
    HEALTHCARE_HOSPITALS    = "Healthcare - Hospitals"
    HEALTHCARE_PHARMA       = "Healthcare - Pharmaceutical"
    RETAIL                  = "Retail & Consumer Goods"
    TECHNOLOGY              = "Technology & Software"
    PROFESSIONAL_SERVICES   = "Professional Services"
    ENERGY_UTILITIES        = "Energy & Utilities"
    PUBLIC_SECTOR           = "Public Sector"
    TELECOM                 = "Telecommunications"
    TRANSPORT               = "Transportation & Logistics"
    HOSPITALITY             = "Hospitality & Tourism"
    CONSTRUCTION            = "Construction & Engineering"


class HCMModule(str, Enum):
    CORE_HR             = "Core HR"
    TALENT              = "Talent Management"
    WORKFORCE           = "Workforce Management"
    PAYROLL             = "Payroll"
    COMP_BENEFITS       = "Compensation & Benefits"
    ANALYTICS           = "Workforce Analytics"
    HEALTH_SAFETY       = "Health & Safety"
    HELP_DESK           = "Help Desk & Case Management"


class Priority(str, Enum):
    CRITICAL = "Critical"
    HIGH     = "High"
    MEDIUM   = "Medium"
    LOW      = "Low"


class EffortLevel(str, Enum):
    LOW    = "Low"
    MEDIUM = "Medium"
    HIGH   = "High"


class RiskSeverity(str, Enum):
    LOW      = "Low"
    MEDIUM   = "Medium"
    HIGH     = "High"
    CRITICAL = "Critical"


# ──────────────────────────────────────────────────────────────────────────────
# Requests
# ──────────────────────────────────────────────────────────────────────────────

class GenerateQuestionnaireRequest(BaseModel):
    industry: Industry
    modules: list[HCMModule] = Field(..., min_length=1)


# ──────────────────────────────────────────────────────────────────────────────
# Internal parsing structures
# ──────────────────────────────────────────────────────────────────────────────

class QuestionResponse(BaseModel):
    category: str
    question: str
    response: str = ""
    priority: Priority = Priority.MEDIUM
    guidance: str = ""


class ModuleResponses(BaseModel):
    module: HCMModule
    responses: list[QuestionResponse]
    answered_count: int = 0
    total_count: int = 0


class ParsedQuestionnaire(BaseModel):
    file_name: str
    industry: str
    modules: list[str]
    module_responses: dict[str, list[QuestionResponse]]
    total_questions: int
    answered_questions: int
    completion_rate: float


# ──────────────────────────────────────────────────────────────────────────────
# AI Analysis output structures
# ──────────────────────────────────────────────────────────────────────────────

class CompanyProfile(BaseModel):
    company_name: Optional[str] = None
    employee_count: str = "Not specified"
    locations: str = "Not specified"
    countries: str = "Not specified"
    key_complexity: str = ""


class GapItem(BaseModel):
    module: str
    requirement: str
    oracle_capability: str
    gap: str                  # "None" if fully delivered
    solution: str
    effort: EffortLevel


class RiskItem(BaseModel):
    risk: str
    severity: RiskSeverity
    mitigation: str


class Timeline(BaseModel):
    phase1: str
    phase2: str = "N/A"
    phase3: str = "N/A"
    total_duration: str
    critical_path: str


class HLAAnalysis(BaseModel):
    session_id: str
    industry: str
    modules: list[str]
    company_profile: CompanyProfile
    key_findings: list[str]
    pain_points: list[str]
    requirements: list[str]
    gap_analysis: list[GapItem]
    recommendations: list[str]
    risks: list[RiskItem]
    timeline: Timeline
    completion_rate: float
    answered_questions: int
    total_questions: int


# ──────────────────────────────────────────────────────────────────────────────
# Response wrappers
# ──────────────────────────────────────────────────────────────────────────────

class QuestionnaireGeneratedResponse(BaseModel):
    download_url: str
    file_name: str
    total_questions: int
    sheet_count: int
    industry: str
    modules: list[str]


class AnalysisStatusResponse(BaseModel):
    session_id: str
    status: str               # "processing" | "complete" | "failed"
    progress: int             # 0-100
    message: str
    result: Optional[HLAAnalysis] = None