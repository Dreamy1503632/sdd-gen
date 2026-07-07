"""
models/cwb_models.py – schemas for Configuration Workbooks (CWBs)
"""
from __future__ import annotations
from typing import Optional, Any
from pydantic import BaseModel, Field


# ──────────────────────────────────────────────────────────────────────────────
# Generic building blocks
# ──────────────────────────────────────────────────────────────────────────────

class ConfigRow(BaseModel):
    """One row in a configuration table (key-value + metadata)."""
    config_item: str
    value: str
    notes: str = ""
    mandatory: bool = True
    oracle_default: str = ""


class SetupTask(BaseModel):
    """Oracle HCM Setup and Maintenance task."""
    task_name: str
    functional_area: str
    offering: str
    scope: str          # "Enterprise" | "LegalEntity" | "BusinessUnit" | etc.
    sequence: int
    prerequisite_tasks: list[str] = Field(default_factory=list)
    configuration_data: list[ConfigRow] = Field(default_factory=list)
    notes: str = ""


# ──────────────────────────────────────────────────────────────────────────────
# Module-specific workbook structures
# ──────────────────────────────────────────────────────────────────────────────

class CoreHRWorkbook(BaseModel):
    enterprise_structure: list[ConfigRow]
    legal_entities: list[ConfigRow]
    business_units: list[ConfigRow]
    departments: list[ConfigRow]
    locations: list[ConfigRow]
    jobs: list[ConfigRow]
    positions: list[ConfigRow]
    grades: list[ConfigRow]
    person_types: list[ConfigRow]
    actions_reasons: list[ConfigRow]
    lookups: list[ConfigRow]
    security_roles: list[ConfigRow]
    setup_tasks: list[SetupTask]


class TalentWorkbook(BaseModel):
    performance_templates: list[ConfigRow]
    goal_plans: list[ConfigRow]
    talent_review_templates: list[ConfigRow]
    succession_plans: list[ConfigRow]
    recruiting_setup: list[ConfigRow]
    onboarding_checklists: list[ConfigRow]
    setup_tasks: list[SetupTask]


class WorkforceWorkbook(BaseModel):
    work_schedules: list[ConfigRow]
    absence_types: list[ConfigRow]
    accrual_plans: list[ConfigRow]
    time_entry_profiles: list[ConfigRow]
    overtime_rules: list[ConfigRow]
    setup_tasks: list[SetupTask]


class PayrollWorkbook(BaseModel):
    payroll_definitions: list[ConfigRow]
    payroll_elements: list[ConfigRow]
    deduction_elements: list[ConfigRow]
    payroll_flows: list[ConfigRow]
    costing_setup: list[ConfigRow]
    tax_config: list[ConfigRow]
    setup_tasks: list[SetupTask]


class CompBenefitsWorkbook(BaseModel):
    salary_basis: list[ConfigRow]
    grade_rates: list[ConfigRow]
    compensation_plans: list[ConfigRow]
    benefit_plans: list[ConfigRow]
    benefit_programs: list[ConfigRow]
    eligibility_profiles: list[ConfigRow]
    enrollment_periods: list[ConfigRow]
    setup_tasks: list[SetupTask]


class AnalyticsWorkbook(BaseModel):
    subject_areas: list[ConfigRow]
    dashboard_configs: list[ConfigRow]
    standard_reports: list[ConfigRow]
    custom_reports: list[ConfigRow]
    setup_tasks: list[SetupTask]


# ──────────────────────────────────────────────────────────────────────────────
# Top-level CWB container
# ──────────────────────────────────────────────────────────────────────────────

class CWBDocument(BaseModel):
    session_id: str
    sdd_session_id: str
    company_name: str
    modules: list[str]

    core_hr: Optional[CoreHRWorkbook] = None
    talent: Optional[TalentWorkbook] = None
    workforce: Optional[WorkforceWorkbook] = None
    payroll: Optional[PayrollWorkbook] = None
    comp_benefits: Optional[CompBenefitsWorkbook] = None
    analytics: Optional[AnalyticsWorkbook] = None

    total_setup_tasks: int = 0
    generation_time_seconds: float = 0


# ──────────────────────────────────────────────────────────────────────────────
# Requests / Responses
# ──────────────────────────────────────────────────────────────────────────────

class GenerateCWBRequest(BaseModel):
    sdd_session_id: str
    modules: list[str]        # subset of modules to generate CWBs for
    company_name: str


class CWBGenerationProgress(BaseModel):
    session_id: str
    status: str
    progress: int
    current_module: str
    log_entries: list[str]
    download_urls: dict[str, str] = Field(default_factory=dict)   # module → url


class CWBSummaryResponse(BaseModel):
    session_id: str
    company_name: str
    modules_generated: list[str]
    total_setup_tasks: int
    download_urls: dict[str, str]