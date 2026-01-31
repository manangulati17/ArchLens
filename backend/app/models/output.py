from pydantic import BaseModel, Field
from typing import List, Optional


class ArchitectureComponent(BaseModel):
    name: str = Field(..., description="Name of the component (e.g., User Services, Redis Cache)")
    type: str = Field(..., description="Component Type (API, DB, Cache, Queue, CDN, External)")
    responsibility: str = Field(..., description="Primary Responsibility of the Component")


class ArchitectureBreakdown(BaseModel):
    components: List[ArchitectureComponent]
    assumptions: List[str] = Field(..., description="Explicit assumptions made due to missing or unclear information")


class DataFlow(BaseModel):
    read_path: List[str] = Field(..., description="Step-by-step read request flow")
    write_path: List[str] = Field(..., description="Step-by-step write request flow")
    synchronous_operations: List[str] = Field(..., description="Operations performed synchronously in the request path")
    asynchronous_operations: List[str] = Field(..., description="Operations handled asynchronously")


class ScalabilityRisk(BaseModel):
    component: str = Field(...,description="Component under risk")
    risk: str = Field(..., description="Nature of the scalability risk")
    reason: str = Field(..., description="Why this risk emerges under scale")


class ScalabilityAnalysis(BaseModel):
    scalable_components: List[str] = Field(...,description="components that scale horizontally with minimal friction")
    bottlenecks: List[ScalabilityRisk]


class FailureMode(BaseModel):
    scenario: str = Field(...,description="Failure or stress scenario")
    impacted_components: List[str]
    failure_behavior: str = Field(..., description="Observed system behavior under this failure")


class ReliabilityAnalysis(BaseModel):
    single_points_of_failure: List[str]
    what_breaks_first: str = Field(...,description="The first component or interaction expected to fail under load or partial outage")
    failure_modes: List[FailureMode]


class CostTradeoff(BaseModel):
    decision: str = Field(..., description="Architectural decision impacting cost")
    option_a : str
    option_b : str
    cost_impact: str = Field(..., description="Relative cost impact between options")
    scalability_impact: str = Field(..., description = "How each option affects scalability")
    risk: str = Field(...,description="Operational or technical risk introduced")


class InfraCostEstimate(BaseModel):
    user_scale: str = Field(...,description="Traffic level (e.g., 1K, 10K, 100K, 1M users)")
    assumptions: List[str]
    estimated_monthly_cost_INR : str = Field(..., description="Directional monthly cost range, not exact pricing")


class ArchLensEvaluation(BaseModel):
    architecture_breakdown: ArchitectureBreakdown
    data_flow: DataFlow
    scalability_analysis: ScalabilityAnalysis
    reliability_analysis: ReliabilityAnalysis
    cost_tradeoffs: List[CostTradeoff]
    infra_cost_estimates: List[InfraCostEstimate]
    assumptions: Optional[List[str]]  = Field(default_factory= list, description="Global assumptions applied across the evaluation")
    overall_summary: str = Field(...,description="High-level assessment of the architecture and key risks")

