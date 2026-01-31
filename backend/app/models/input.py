from pydantic import BaseModel, Field
from typing import List, Optional, Literal


class RAGConfig(BaseModel):
    enabled: bool = Field(
        default=True,
        description="Whether retrieval-augmented generation (RAG) should be used"
    )
    sources: List[Literal["cloud_pricing", "latency_baselines", "architecture_patterns"]] = Field(
        default_factory=list,
        description="Knowledge sources to use for grounding the evaluation"
    )


class EvaluationContext(BaseModel):
    system_type: Optional[Literal["interview", "production", "startup", "enterprise"]] = Field(
        default=None,
        description="Nature of the system being evaluated"
    )
    expected_scale: Optional[str] = Field(
        default=None,
        description="Expected scale (e.g., 100k users, 10M requests/day)"
    )
    constraints: List[str] = Field(
        default_factory=list,
        description="Explicit constraints such as compliance, latency, budget, region, etc."
    )


class ArchLensEvaluationRequest(BaseModel):
    design_text: str = Field(
        ...,
        description="Textual description of the system design to be evaluated"
    )
    context: Optional[EvaluationContext] = Field(
        default=None,
        description="Optional context to guide evaluation depth and assumptions"
    )
    rag_config: RAGConfig = Field(
        default_factory=RAGConfig,
        description="Controls for retrieval-augmented generation (RAG) behavior"
    )
    focus_areas: List[Literal["scalability", "reliability", "cost", "security"]] = Field(
        default_factory=list,
        description="Specific architectural aspects to emphasize during evaluation"
    )