"""
chains/hla_chain.py
LangChain chain that analyses a completed HLA questionnaire and returns a
structured HLAAnalysis object.
"""
from __future__ import annotations
import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from chains.model import llm
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

from config import get_settings
from models.hla_models import (
    HLAAnalysis, CompanyProfile, GapItem, RiskItem, Timeline,
    EffortLevel, RiskSeverity,
)

settings = get_settings()

# ──────────────────────────────────────────────────────────────────────────────
# System prompt
# ──────────────────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a senior Oracle Fusion HCM Solution Architect with 15+ years of
implementation experience across industries. You have deep expertise in:
- Oracle Fusion Global HR, Talent Management, Workforce Management, Payroll,
  Compensation & Benefits, Workforce Analytics, Health & Safety, and HR Help Desk
- Oracle delivered vs. configurable vs. customisable functionality
- Industry-specific HCM best practices and compliance requirements
- Implementation methodology (AIM, OUM, Agile delivery)

Your analysis must be precise, implementation-ready, and grounded in Oracle HCM
delivered capability. Always distinguish clearly between what Oracle delivers
out-of-the-box vs. what requires configuration vs. what requires extension."""

# ──────────────────────────────────────────────────────────────────────────────
# Analysis prompt
# ──────────────────────────────────────────────────────────────────────────────

ANALYSIS_PROMPT = """Analyse the following Oracle Fusion HCM questionnaire responses and return a
structured JSON object exactly matching the schema below.

=== CLIENT CONTEXT ===
Industry: {industry}
Modules in scope: {modules}
Total questions answered: {answered_count} / {total_count}

=== QUESTIONNAIRE RESPONSES ===
{responses_text}

=== REQUIRED JSON SCHEMA ===
{{
  "company_profile": {{
    "employee_count": "string",
    "locations": "string",
    "countries": "string",
    "key_complexity": "string"
  }},
  "key_findings": ["string", ...],          // 6-8 specific, implementation-relevant findings
  "pain_points": ["string", ...],           // 5-7 current-state pain points
  "requirements": ["string", ...],          // 6-8 Oracle capability requirements
  "gap_analysis": [
    {{
      "module": "string",
      "requirement": "string",
      "oracle_capability": "string",        // what Oracle delivers OOTB
      "gap": "string",                      // "None" OR specific gap description
      "solution": "string",                 // implementation recommendation
      "effort": "Low|Medium|High"
    }}
  ],
  "recommendations": ["string", ...],       // 6-8 strategic recommendations
  "risks": [
    {{
      "risk": "string",
      "severity": "Low|Medium|High|Critical",
      "mitigation": "string"
    }}
  ],
  "timeline": {{
    "phase1": "string",     // e.g. "4-6 months – Core HR Foundation"
    "phase2": "string",
    "phase3": "string",     // "N/A" if not applicable
    "total_duration": "string",
    "critical_path": "string"
  }}
}}

Rules:
1. Base gap_analysis ONLY on Oracle Fusion HCM delivered functionality (as of 24C)
2. For every gap, suggest the Oracle-native solution first before recommending extensions
3. Be specific about Oracle transaction/setup task names where relevant
4. Consider {industry} industry compliance requirements
5. Return ONLY valid JSON – no markdown, no commentary before or after"""

# ──────────────────────────────────────────────────────────────────────────────
# LLM factory
# ──────────────────────────────────────────────────────────────────────────────

def _build_llm():
    """Factory for the LLM – allows centralised management of model choice and settings."""
    return llm


# ──────────────────────────────────────────────────────────────────────────────
# Response formatter
# ──────────────────────────────────────────────────────────────────────────────

def _format_responses(module_responses: dict) -> str:
    """Flatten module responses into a readable block for the prompt."""
    lines: list[str] = []
    for module, responses in module_responses.items():
        answered = [r for r in responses if r.get("response", "").strip()]
        if not answered:
            continue
        lines.append(f"\n### {module.upper()} ###")
        for r in answered:
            lines.append(
                f"[{r.get('priority', 'Medium')}] {r.get('category', '')}: "
                f"{r.get('question', '')}\n→ {r.get('response', '')}"
            )
    return "\n".join(lines)


def _parse_raw(raw: dict) -> dict:
    """Normalise LLM output to match our Pydantic models."""
    return raw


# ──────────────────────────────────────────────────────────────────────────────
# Public chain builder
# ──────────────────────────────────────────────────────────────────────────────

def build_hla_chain():
    """
    Returns a LangChain runnable that accepts:
        {
            "industry": str,
            "modules": list[str],
            "answered_count": int,
            "total_count": int,
            "module_responses": dict[str, list[dict]]
        }
    and returns a dict matching HLAAnalysis (minus session_id / completion_rate).
    """
    llm = _build_llm()

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", ANALYSIS_PROMPT),
        ]
    )

    format_step = RunnableLambda(
        lambda inputs: {
            **inputs,
            "modules": ", ".join(inputs["modules"]),
            "responses_text": _format_responses(inputs["module_responses"]),
        }
    )

    parser = JsonOutputParser()

    chain = format_step | prompt | llm | parser

    return chain


# ──────────────────────────────────────────────────────────────────────────────
# Convenience async wrapper
# ──────────────────────────────────────────────────────────────────────────────

async def run_hla_analysis(
    industry: str,
    modules: list[str],
    module_responses: dict,
    answered_count: int,
    total_count: int,
) -> dict:
    chain = build_hla_chain()
    raw = await chain.ainvoke(
        {
            "industry": industry,
            "modules": modules,
            "answered_count": answered_count,
            "total_count": total_count,
            "module_responses": module_responses,
        }
    )
    return raw