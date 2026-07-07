"""
chains/sdd_chain.py
LangChain chains for generating each chapter of the Solution Design Document.
Each chapter is invoked separately so we can stream progress updates to the
client and control token budget per section.
"""
from __future__ import annotations
import json
from typing import AsyncGenerator
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from chains.model import llm

from config import get_settings
from models.hla_models import HLAAnalysis
from models.sdd_models import SDDConfig

settings = get_settings()

# ──────────────────────────────────────────────────────────────────────────────
# Shared system prompt
# ──────────────────────────────────────────────────────────────────────────────

SDD_SYSTEM = """You are a senior Oracle Fusion HCM implementation consultant writing a
formal Solution Design Document (SDD). The SDD will be reviewed by the client's
senior stakeholders and the Oracle implementation team.

Writing style:
- Professional, precise, implementation-ready
- Use Oracle terminology correctly (e.g. "Legal Entity", "Business Unit", "HCM
  Experience Design Studio", "HDL – HCM Data Loader")
- Every configuration decision must reference the specific Oracle Setup and
  Maintenance task name
- Tables preferred over prose for configuration data

Return ONLY valid JSON matching the schema provided."""


def _build_llm(max_tokens: int = 4096):
    return llm


def _context(analysis: HLAAnalysis, config: SDDConfig) -> str:
    return f"""Company: {config.company_name}
Industry: {analysis.industry}
Modules in scope: {", ".join(analysis.modules)}
Employee count: {analysis.company_profile.employee_count}
Locations: {analysis.company_profile.locations}
Key complexity: {analysis.company_profile.key_complexity}

Key findings summary:
{chr(10).join(f"- {f}" for f in analysis.key_findings[:5])}

Key requirements:
{chr(10).join(f"- {r}" for r in analysis.requirements[:5])}"""


# ──────────────────────────────────────────────────────────────────────────────
# Chapter 2 – Introduction
# ──────────────────────────────────────────────────────────────────────────────

CHAPTER2_PROMPT = """Based on the following project context, generate Chapter 2 (Introduction)
of the Oracle Fusion HCM Solution Design Document.

{context}

Return JSON:
{{
  "purpose": "2-3 sentences describing document purpose",
  "scope": "Detailed scope statement covering modules, geographies, employee populations",
  "implementation_approach": "Overview of Oracle Cloud implementation approach being used",
  "document_overview": "Brief description of each chapter in this SDD"
}}"""


async def generate_chapter2(analysis: HLAAnalysis, config: SDDConfig) -> dict:
    llm = _build_llm(2048)
    prompt = ChatPromptTemplate.from_messages([
        ("system", SDD_SYSTEM),
        ("human", CHAPTER2_PROMPT),
    ])
    chain = prompt | llm | JsonOutputParser()
    return await chain.ainvoke({"context": _context(analysis, config)})


# ──────────────────────────────────────────────────────────────────────────────
# Chapter 3 – Business Structure (most important / longest chapter)
# ──────────────────────────────────────────────────────────────────────────────

BUSINESS_STRUCTURE_SECTIONS = [
    ("3.1",  "Enterprise",                    "Manage Enterprise HCM Information"),
    ("3.2",  "Employment Model",              "Manage Legal Entity HCM Information"),
    ("3.3",  "Department & Department Tree",  "Manage Departments"),
    ("3.4",  "Location",                      "Manage Locations"),
    ("3.5",  "Job Family",                    "Manage Job Families"),
    ("3.6",  "Job Structure",                 "Manage Jobs"),
    ("3.7",  "Position Structure",            "Manage Positions"),
    ("3.8",  "Grade Structure",               "Manage Grades"),
    ("3.9",  "Person Number Generation",      "Manage Person Number Generation"),
    ("3.10", "Application Defaults",          "Manage HCM System Options"),
    ("3.11", "Security Console Configuration","Security Console"),
    ("3.12", "User Roles",                    "Manage Role Provisioning Rules"),
    ("3.13", "Role Provisioning",             "Manage Role Provisioning Rules"),
    ("3.14", "Approvals",                     "Manage HCM Approval Transactions"),
    ("3.15", "Alerts",                        "Manage HCM Alerts"),
    ("3.16", "Reports and Analytics",         "Manage Business Intelligence"),
    ("3.17", "Person Types",                  "Manage Person Types"),
    ("3.18", "Assignment Statuses",           "Manage Assignment Statuses"),
    ("3.19", "Actions & Action Reasons",      "Manage Actions"),
    ("3.20", "HR Lookups",                    "Manage Common Lookups"),
    ("3.21", "Descriptive Flexfields",        "Manage Descriptive Flexfields"),
    ("3.22", "Extensible Flexfields",         "Manage Extensible Flexfields"),
    ("3.23", "Key Flexfields",                "Manage Key Flexfields"),
    ("3.24", "Responsive User Experience",    "HCM Experience Design Studio"),
    ("3.25", "Area of Responsibility",        "Manage Areas of Responsibility"),
    ("3.26", "Audit Policies",               "Manage Audit Policies"),
    ("3.27", "Dashboard Reporting",           "Configure Infolets"),
    ("3.28", "Document Records",             "Manage Document Types"),
]

SECTION_PROMPT = """Generate section {section_id} – {title} of the Oracle Fusion HCM SDD.

Project context:
{context}

Oracle Setup Task: {setup_task}

Return JSON:
{{
  "section_id": "{section_id}",
  "title": "{title}",
  "description": "What this section covers and why it matters for this client",
  "oracle_recommendation": "Oracle best-practice recommendation for this client's profile",
  "client_decision": "Recommended decision/design for {company} based on their requirements",
  "configuration_notes": "Specific Oracle Setup and Maintenance steps and configuration details",
  "table_data": [
    {{"column": "Configuration Item", "value": "Recommended Value", "notes": "Rationale"}},
    ...
  ]
}}"""


async def generate_business_structure_section(
    section_id: str,
    title: str,
    setup_task: str,
    analysis: HLAAnalysis,
    config: SDDConfig,
) -> dict:
    llm = _build_llm(2048)
    prompt = ChatPromptTemplate.from_messages([
        ("system", SDD_SYSTEM),
        ("human", SECTION_PROMPT),
    ])
    chain = prompt | llm | JsonOutputParser()
    return await chain.ainvoke({
        "section_id": section_id,
        "title": title,
        "setup_task": setup_task,
        "context": _context(analysis, config),
        "company": config.company_name,
    })


# ──────────────────────────────────────────────────────────────────────────────
# Chapter 4 – Process Flows
# ──────────────────────────────────────────────────────────────────────────────

# Maps module → list of (flow_id, title, oracle_transaction)
PROCESS_FLOW_CATALOGUE: dict[str, list[tuple[str, str, str]]] = {
    "Core HR": [
        ("4.1.1",  "New Worker – Pending Worker",           "Add Pending Worker"),
        ("4.1.2",  "Convert Pending Worker",                "Convert Pending Worker"),
        ("4.1.3",  "Hire Employee",                         "Add Worker"),
        ("4.1.4",  "Manage Person",                         "Manage Person"),
        ("4.1.5",  "Manage Work Relationship",              "Manage Work Relationship"),
        ("4.1.6",  "Change Assignment",                     "Change Assignment"),
        ("4.1.7",  "Change Manager",                        "Change Manager"),
        ("4.1.8",  "Change Location",                       "Change Location"),
        ("4.1.9",  "Transfer",                              "Transfer"),
        ("4.1.10", "Promote",                               "Promote"),
        ("4.1.11", "Terminate Work Relationship",           "Terminate"),
        ("4.1.12", "Mass Updates",                          "HCM Spreadsheet Data Loader"),
    ],
    "Talent Management": [
        ("4.2.1",  "Onboarding Journey",                   "New Worker Journeys"),
        ("4.2.2",  "Offboarding Journey",                  "Worker Journeys"),
        ("4.2.3",  "Create Job Requisition",               "Create Job Requisition"),
        ("4.2.4",  "Manage Candidate Pipeline",            "Search Candidates"),
        ("4.2.5",  "Make Offer",                           "Create Offer"),
        ("4.2.6",  "Goal Setting",                         "Manage Goals"),
        ("4.2.7",  "Performance Review",                   "Manage Performance Documents"),
        ("4.2.8",  "Talent Review",                        "Talent Review"),
        ("4.2.9",  "Succession Planning",                  "Manage Succession Plan"),
    ],
    "Workforce Management": [
        ("4.3.1",  "Change Working Hours",                  "Change Working Hours"),
        ("4.3.2",  "Work Schedule Assignment",              "Assign Work Schedule"),
        ("4.3.3",  "Time Entry",                            "My Time"),
        ("4.3.4",  "Absence Request",                       "Create Absence"),
        ("4.3.5",  "Absence Approval",                      "Manage Absence Records"),
        ("4.3.6",  "Accrual Balance Review",                "Manage Accrual Balances"),
    ],
    "Payroll": [
        ("4.4.1",  "Payroll Calculation",                   "Calculate Payroll"),
        ("4.4.2",  "Payroll Pre-Calculation Audit",         "Run Payroll Validation Report"),
        ("4.4.3",  "QuickPay",                              "QuickPay"),
        ("4.4.4",  "Payroll Costing",                       "Calculate Payroll Costing"),
        ("4.4.5",  "Payment Generation",                    "Generate Payments"),
        ("4.4.6",  "Off-cycle Payment",                     "Make EFT Payment"),
    ],
    "Compensation & Benefits": [
        ("4.5.1",  "Change Salary",                         "Change Salary"),
        ("4.5.2",  "Annual Compensation Review",            "Start Compensation Cycle"),
        ("4.5.3",  "Individual Compensation",               "Individual Compensation"),
        ("4.5.4",  "Benefits Open Enrollment",              "Self-Service Benefits"),
        ("4.5.5",  "Life Event Processing",                 "Manage Life Events"),
    ],
    "Workforce Analytics": [
        ("4.6.1",  "HR Dashboard Review",                   "Workforce Management Infolets"),
        ("4.6.2",  "Custom OTBI Report",                    "Oracle Transactional BI"),
        ("4.6.3",  "HCM Data Extracts",                     "HCM Extracts"),
    ],
    "Health & Safety": [
        ("4.7.1",  "Report Safety Incident",                "Report Incident"),
        ("4.7.2",  "Manage Incident Investigation",         "Manage Incidents"),
        ("4.7.3",  "Track Certifications",                  "Manage Worker Qualifications"),
    ],
    "Help Desk & Case Management": [
        ("4.8.1",  "Create HR Service Request",             "Create Service Request"),
        ("4.8.2",  "Manage HR Case",                        "Manage HR Cases"),
        ("4.8.3",  "Knowledge Article Search",              "Knowledge Management"),
    ],
}

FLOW_PROMPT = """Generate a detailed process flow for section {flow_id} – {title}.

Project context:
{context}

Oracle transaction: {oracle_transaction}

Return JSON:
{{
  "flow_id": "{flow_id}",
  "title": "{title}",
  "module": "{module}",
  "trigger": "What event/action initiates this process",
  "steps": [
    {{
      "step_number": 1,
      "actor": "Role performing this step",
      "action": "Specific action taken",
      "system": "Oracle HCM | Email | External System",
      "outcome": "Result of this step",
      "notes": "Configuration consideration or tip"
    }}
  ],
  "approval_required": true,
  "approvers": ["list of approver roles"],
  "oracle_transaction": "{oracle_transaction}",
  "notes": "Client-specific notes or configuration decisions"
}}"""


async def generate_process_flow(
    flow_id: str,
    title: str,
    module: str,
    oracle_transaction: str,
    analysis: HLAAnalysis,
    config: SDDConfig,
) -> dict:
    llm = _build_llm(2048)
    prompt = ChatPromptTemplate.from_messages([
        ("system", SDD_SYSTEM),
        ("human", FLOW_PROMPT),
    ])
    chain = prompt | llm | JsonOutputParser()
    return await chain.ainvoke({
        "flow_id": flow_id,
        "title": title,
        "module": module,
        "oracle_transaction": oracle_transaction,
        "context": _context(analysis, config),
    })


# ──────────────────────────────────────────────────────────────────────────────
# Chapter 6 – Gap Analysis
# ──────────────────────────────────────────────────────────────────────────────

GAP_PROMPT = """Generate Chapter 6 (Gap Analysis) of the SDD based on the HLA analysis.

Project context:
{context}

Gaps identified in HLA:
{gaps_text}

Return JSON:
{{
  "gaps": [
    {{
      "gap_id": "G001",
      "module": "module name",
      "requirement": "client requirement",
      "oracle_capability": "what Oracle HCM delivers OOTB",
      "gap_description": "None OR specific gap",
      "recommended_solution": "implementation approach",
      "effort": "Low|Medium|High",
      "workaround": "Oracle-native workaround if a gap exists"
    }}
  ],
  "summary": "Executive summary of overall gap posture (2-3 sentences)"
}}"""


async def generate_chapter6(analysis: HLAAnalysis, config: SDDConfig) -> dict:
    llm = _build_llm(4096)
    prompt = ChatPromptTemplate.from_messages([
        ("system", SDD_SYSTEM),
        ("human", GAP_PROMPT),
    ])
    chain = prompt | llm | JsonOutputParser()
    gaps_text = "\n".join(
        f"- [{g.module}] {g.requirement} → Gap: {g.gap} (Effort: {g.effort})"
        for g in analysis.gap_analysis
    )
    return await chain.ainvoke({
        "context": _context(analysis, config),
        "gaps_text": gaps_text,
    })


# ──────────────────────────────────────────────────────────────────────────────
# Chapter 9 – Assumptions
# ──────────────────────────────────────────────────────────────────────────────

ASSUMPTIONS_PROMPT = """Generate Chapter 9 (Assumptions & Dependencies) of the SDD.

Project context:
{context}

Risks identified:
{risks_text}

Return JSON:
{{
  "assumptions": [
    {{
      "assumption_id": "A001",
      "category": "Data|Integration|Organisational|Technical|Process",
      "description": "Clear, specific assumption statement",
      "impact_if_incorrect": "What breaks if this assumption is wrong"
    }}
  ],
  "dependencies": ["External dependency description"],
  "exclusions": ["What is explicitly out of scope"]
}}

Include 12-15 assumptions covering: data migration, integrations, access, testing, decisions, go-live."""


async def generate_chapter9(analysis: HLAAnalysis, config: SDDConfig) -> dict:
    llm = _build_llm(3000)
    prompt = ChatPromptTemplate.from_messages([
        ("system", SDD_SYSTEM),
        ("human", ASSUMPTIONS_PROMPT),
    ])
    chain = prompt | llm | JsonOutputParser()
    risks_text = "\n".join(
        f"- [{r.severity}] {r.risk}" for r in analysis.risks
    )
    return await chain.ainvoke({
        "context": _context(analysis, config),
        "risks_text": risks_text,
    })