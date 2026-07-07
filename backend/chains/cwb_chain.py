"""
chains/cwb_chain.py
LangChain chains that generate per-module Configuration Workbook data.
Each module chain receives the relevant SDD sections and returns structured
configuration rows and setup tasks ready to be written to Excel.
"""
from __future__ import annotations
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from chains.model import llm

from config import get_settings
from models.sdd_models import SDDDocument

settings = get_settings()

CWB_SYSTEM = """You are an Oracle Fusion HCM technical architect generating
Configuration Workbooks (CWBs) – the definitive configuration blueprint used by
the implementation team to set up Oracle HCM.

Rules:
- Reference exact Oracle Setup and Maintenance task names
- Use correct Oracle terminology for field names and values
- Configuration values must be realistic and consistent across modules
- Mark every mandatory field clearly
- Return ONLY valid JSON"""


def _build_llm():
    # In future, could have module-specific LLM configurations here
    return llm


def _sdd_context(sdd: SDDDocument) -> str:
    """Summarise SDD into a concise context block."""
    ch3 = sdd.chapter3
    enterprise_section = next(
        (s for s in ch3.sections if s.section_id == "3.1"), None
    )
    return f"""Company: {sdd.config.company_name}
Industry: (from SDD)
Modules: {", ".join(sdd.modules)}
Enterprise decision: {enterprise_section.client_decision if enterprise_section else "Standard enterprise setup"}"""


# ──────────────────────────────────────────────────────────────────────────────
# Core HR CWB
# ──────────────────────────────────────────────────────────────────────────────

CORE_HR_CWB_PROMPT = """Generate a complete Core HR Configuration Workbook for {company}.

SDD context:
{context}

Return JSON with these exact keys:
{{
  "enterprise_structure": [
    {{"config_item": "Enterprise Name", "value": "...", "notes": "...", "mandatory": true, "oracle_default": ""}},
    ...
  ],
  "legal_entities": [
    {{"config_item": "Legal Entity Name", "value": "...", "notes": "...", "mandatory": true, "oracle_default": ""}},
    ...
  ],
  "business_units": [...],
  "departments": [
    // 8-10 sample departments based on industry
  ],
  "locations": [
    // 3-5 sample locations
  ],
  "jobs": [
    // 8-10 sample jobs typical for the industry
  ],
  "positions": [
    // "Yes - position-based" or "No - job-based" with rationale
    {{"config_item": "Position Management", "value": "...", "notes": "...", "mandatory": true, "oracle_default": "No"}}
  ],
  "grades": [
    // 5-8 grades typical for the industry
  ],
  "person_types": [
    {{"config_item": "Employee", "value": "System", "notes": "Oracle delivered", "mandatory": true, "oracle_default": "Employee"}},
    // add any custom person types needed
  ],
  "actions_reasons": [
    // 10-15 action/reason combinations covering hire, transfer, promote, terminate, change
  ],
  "lookups": [
    // 5-8 custom lookups needed for this client
  ],
  "security_roles": [
    // 6-8 key roles (use Oracle seeded role names)
  ],
  "setup_tasks": [
    {{
      "task_name": "Manage Enterprise HCM Information",
      "functional_area": "Workforce Structures",
      "offering": "Workforce Deployment",
      "scope": "Enterprise",
      "sequence": 1,
      "prerequisite_tasks": [],
      "configuration_data": [],
      "notes": "First task - configure enterprise settings"
    }},
    // 15-20 tasks in correct sequence
  ]
}}"""


async def generate_core_hr_cwb(sdd: SDDDocument) -> dict:
    llm = _build_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", CWB_SYSTEM),
        ("human", CORE_HR_CWB_PROMPT),
    ])
    chain = prompt | llm | JsonOutputParser()
    return await chain.ainvoke({
        "company": sdd.config.company_name,
        "context": _sdd_context(sdd),
    })


# ──────────────────────────────────────────────────────────────────────────────
# Talent Management CWB
# ──────────────────────────────────────────────────────────────────────────────

TALENT_CWB_PROMPT = """Generate a Talent Management Configuration Workbook for {company}.

SDD context:
{context}

Return JSON:
{{
  "performance_templates": [
    // 3-5 performance document templates (e.g. Annual Review, Mid-Year, Probation)
    {{"config_item": "Template Name", "value": "...", "notes": "...", "mandatory": true, "oracle_default": ""}}
  ],
  "goal_plans": [
    // 2-3 goal plan configurations
  ],
  "talent_review_templates": [
    // 1-2 talent review configurations (9-box, etc.)
  ],
  "succession_plans": [
    {{"config_item": "Succession Plan Type", "value": "...", "notes": "...", "mandatory": false, "oracle_default": ""}}
  ],
  "recruiting_setup": [
    // 8-10 recruiting configuration items (posting types, offer letter templates, interview stages)
  ],
  "onboarding_checklists": [
    // 5-8 onboarding journey checklist items
  ],
  "setup_tasks": [
    // 12-15 Talent setup tasks in sequence
  ]
}}"""


async def generate_talent_cwb(sdd: SDDDocument) -> dict:
    llm = _build_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", CWB_SYSTEM),
        ("human", TALENT_CWB_PROMPT),
    ])
    chain = prompt | llm | JsonOutputParser()
    return await chain.ainvoke({
        "company": sdd.config.company_name,
        "context": _sdd_context(sdd),
    })


# ──────────────────────────────────────────────────────────────────────────────
# Workforce Management CWB
# ──────────────────────────────────────────────────────────────────────────────

WORKFORCE_CWB_PROMPT = """Generate a Workforce Management Configuration Workbook for {company}.

SDD context:
{context}

Return JSON:
{{
  "work_schedules": [
    // 4-6 work schedule definitions (pattern, hours, days)
    {{"config_item": "Schedule Name", "value": "...", "notes": "...", "mandatory": true, "oracle_default": ""}}
  ],
  "absence_types": [
    // 6-10 absence types (Annual Leave, Sick Leave, Parental Leave, etc.)
  ],
  "accrual_plans": [
    // 3-5 accrual plan configurations
  ],
  "time_entry_profiles": [
    // 3-5 time entry profile configurations
  ],
  "overtime_rules": [
    // 3-5 overtime rule configurations
  ],
  "setup_tasks": [
    // 10-12 Workforce Management setup tasks in sequence
  ]
}}"""


async def generate_workforce_cwb(sdd: SDDDocument) -> dict:
    llm = _build_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", CWB_SYSTEM),
        ("human", WORKFORCE_CWB_PROMPT),
    ])
    chain = prompt | llm | JsonOutputParser()
    return await chain.ainvoke({
        "company": sdd.config.company_name,
        "context": _sdd_context(sdd),
    })


# ──────────────────────────────────────────────────────────────────────────────
# Payroll CWB
# ──────────────────────────────────────────────────────────────────────────────

PAYROLL_CWB_PROMPT = """Generate a Payroll Configuration Workbook for {company}.

SDD context:
{context}

Return JSON:
{{
  "payroll_definitions": [
    // 2-4 payroll definitions (bi-weekly, monthly, etc.)
    {{"config_item": "Payroll Name", "value": "...", "notes": "Period dates, payment method", "mandatory": true, "oracle_default": ""}}
  ],
  "payroll_elements": [
    // 10-15 earnings elements (Regular, Overtime, Bonus, Commission, etc.)
  ],
  "deduction_elements": [
    // 8-12 deduction elements (Tax, NI/Social Security, Benefits, Pension, etc.)
  ],
  "payroll_flows": [
    // 5-8 payroll flow configurations
  ],
  "costing_setup": [
    // 4-6 costing configuration items
  ],
  "tax_config": [
    // country/region-specific tax configurations
  ],
  "setup_tasks": [
    // 15-18 Payroll setup tasks in correct sequence
  ]
}}"""


async def generate_payroll_cwb(sdd: SDDDocument) -> dict:
    llm = _build_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", CWB_SYSTEM),
        ("human", PAYROLL_CWB_PROMPT),
    ])
    chain = prompt | llm | JsonOutputParser()
    return await chain.ainvoke({
        "company": sdd.config.company_name,
        "context": _sdd_context(sdd),
    })


# ──────────────────────────────────────────────────────────────────────────────
# Compensation & Benefits CWB
# ──────────────────────────────────────────────────────────────────────────────

COMP_BENEFITS_CWB_PROMPT = """Generate a Compensation & Benefits Configuration Workbook for {company}.

SDD context:
{context}

Return JSON:
{{
  "salary_basis": [
    {{"config_item": "Salary Basis Name", "value": "...", "notes": "Annual/Monthly/Hourly", "mandatory": true, "oracle_default": ""}}
  ],
  "grade_rates": [
    // 4-6 grade rate tables with min/mid/max
  ],
  "compensation_plans": [
    // 4-6 compensation plans (Merit, Bonus, Equity, etc.)
  ],
  "benefit_plans": [
    // 6-10 benefit plans (Medical, Dental, Vision, Life, Pension, etc.)
  ],
  "benefit_programs": [
    // 2-3 benefit program groupings
  ],
  "eligibility_profiles": [
    // 3-5 eligibility profile definitions
  ],
  "enrollment_periods": [
    // Open enrollment and life event period definitions
  ],
  "setup_tasks": [
    // 12-16 Compensation & Benefits setup tasks
  ]
}}"""


async def generate_comp_benefits_cwb(sdd: SDDDocument) -> dict:
    llm = _build_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", CWB_SYSTEM),
        ("human", COMP_BENEFITS_CWB_PROMPT),
    ])
    chain = prompt | llm | JsonOutputParser()
    return await chain.ainvoke({
        "company": sdd.config.company_name,
        "context": _sdd_context(sdd),
    })


# ──────────────────────────────────────────────────────────────────────────────
# Analytics CWB
# ──────────────────────────────────────────────────────────────────────────────

ANALYTICS_CWB_PROMPT = """Generate a Workforce Analytics Configuration Workbook for {company}.

SDD context:
{context}

Return JSON:
{{
  "subject_areas": [
    {{"config_item": "Subject Area", "value": "...", "notes": "OTBI subject area name", "mandatory": true, "oracle_default": ""}}
  ],
  "dashboard_configs": [
    // 4-6 dashboard configurations
  ],
  "standard_reports": [
    // 8-10 Oracle delivered reports to be configured
  ],
  "custom_reports": [
    // 4-6 custom OTBI/BIP reports to be built
  ],
  "setup_tasks": [
    // 6-8 Analytics setup tasks
  ]
}}"""


async def generate_analytics_cwb(sdd: SDDDocument) -> dict:
    llm = _build_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", CWB_SYSTEM),
        ("human", ANALYTICS_CWB_PROMPT),
    ])
    chain = prompt | llm | JsonOutputParser()
    return await chain.ainvoke({
        "company": sdd.config.company_name,
        "context": _sdd_context(sdd),
    })


# ──────────────────────────────────────────────────────────────────────────────
# Module dispatcher
# ──────────────────────────────────────────────────────────────────────────────

MODULE_GENERATORS = {
    "Core HR":               generate_core_hr_cwb,
    "Talent Management":     generate_talent_cwb,
    "Workforce Management":  generate_workforce_cwb,
    "Payroll":               generate_payroll_cwb,
    "Compensation & Benefits": generate_comp_benefits_cwb,
    "Workforce Analytics":   generate_analytics_cwb,
}


async def generate_cwb_for_module(module: str, sdd: SDDDocument) -> dict | None:
    generator = MODULE_GENERATORS.get(module)
    if generator is None:
        return None
    return await generator(sdd)