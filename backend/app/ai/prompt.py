from typing import List, Optional
from app.models.input import ArchLensEvaluationRequest


def build_system_prompt() -> str:
    return """
You are a senior software engineer performing a system design review.

Your role is to evaluate an existing system design, not to propose a perfect architecture.
You focus on trade-offs, scalability limits, reliability risks, failure modes, and cost implications.

You must follow these rules at all times:
- Always reason explicitly and step-by-step.
- State assumptions whenever information is missing or unclear.
- Avoid vague language and avoid false precision.
- Do not recommend a single “best” solution; discuss trade-offs instead.
- Always identify what would break first under load or partial failure.
- Cost estimates must be directional and assumption-driven.
- Never invent exact prices, benchmarks, or guarantees.
"""


def build_user_prompt(
    request: ArchLensEvaluationRequest,
    rag_context: Optional[str] = None,
) -> str:
    prompt = f"""
SYSTEM DESIGN TO EVALUATE
========================
{request.design_text}
"""

    if request.context:
        prompt += "\nEVALUATION CONTEXT\n==================\n"

        if request.context.system_type:
            prompt += f"- System type: {request.context.system_type}\n"

        if request.context.expected_scale:
            prompt += f"- Expected scale: {request.context.expected_scale}\n"

        if request.context.constraints:
            prompt += "- Constraints:\n"
            for constraint in request.context.constraints:
                prompt += f"  - {constraint}\n"

    if request.rag_config.enabled and rag_context:
        prompt += f"""
REFERENCE CONTEXT (FOR GROUNDING ONLY)
=====================================
{rag_context}

Rules for using reference context:
- Use this context only for factual grounding (pricing ranges, latency orders, known patterns).
- Do NOT invent facts beyond the provided context.
- If information is missing, state assumptions explicitly.
"""
    else:
        prompt += """
REFERENCE CONTEXT
=================
No external reference context is available.

Rules:
- Use architectural heuristics and first-principles reasoning.
- Increase uncertainty ranges where applicable.
- Explicitly list assumptions for cost and scalability analysis.
"""

    if request.focus_areas:
        prompt += "\nFOCUS AREAS\n===========\n"
        prompt += "Emphasize the following areas during evaluation:\n"
        for area in request.focus_areas:
            prompt += f"- {area}\n"

    prompt += """
OUTPUT REQUIREMENTS
===================
Return the evaluation strictly using the following structured format:

- architecture_breakdown
- data_flow
- scalability_analysis
- reliability_analysis
  - Must explicitly include "what_breaks_first"
- cost_tradeoffs
- infra_cost_estimates
- assumptions
- overall_summary

Rules:
- Do NOT omit any section.
- Do NOT add extra sections.
- Do NOT include explanatory text outside the structured output.
- All lists must be returned as lists, even if empty.
"""

    return prompt


def build_full_prompt(
    request: ArchLensEvaluationRequest,
    rag_context: Optional[str] = None,
) -> dict:
    return {
        "system": build_system_prompt(),
        "user": build_user_prompt(request, rag_context),
    }