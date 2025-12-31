"""
FastAPI backend for Basil Architecture Designer
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import sys
from pathlib import Path

# Add parent directory to path to import basil
sys.path.append(str(Path(__file__).parent.parent))

from basil.core.designer import ArchitectureDesigner
from basil.core.models import AgentType, LLMTier
from basil.selectors.llm_selector import LLMSelector
from basil.utils.exporter import ArchitectureExporter

app = FastAPI(
    title="Basil API",
    description="Multi-Agent Architecture Design API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class DesignRequest(BaseModel):
    """Request to design an architecture"""
    problem_statement: str = Field(..., min_length=10, description="Problem statement")
    prefer_provider: Optional[str] = Field(None, description="Preferred LLM provider (openai/anthropic)")
    cost_optimize: bool = Field(False, description="Optimize for cost")
    max_agents: Optional[int] = Field(None, ge=1, le=20, description="Maximum number of agents")
    domains: Optional[List[str]] = Field(None, description="Specific domains to focus on")
    complexity_preference: Optional[str] = Field(None, description="Complexity preference (low/medium/high)")


class AgentResponse(BaseModel):
    """Agent information in response"""
    id: str
    name: str
    type: str
    description: str
    capabilities: List[str]
    llm_provider: str
    llm_model: str
    llm_tier: str
    llm_cost_per_1k: float
    dependencies: List[str]
    reusability_score: float


class CommunicationResponse(BaseModel):
    """Communication flow in response"""
    from_agent: str
    to_agent: str
    message_type: str
    description: str


class ArchitectureResponse(BaseModel):
    """Complete architecture response"""
    problem_statement: str
    agents: List[AgentResponse]
    communications: List[CommunicationResponse]
    metadata: Dict[str, Any]
    cost_estimates: Dict[str, float]
    validation: Dict[str, Any]
    visualization: str


class ExportRequest(BaseModel):
    """Request to export architecture"""
    architecture_id: str
    format: str = Field(..., description="Export format (json/yaml/markdown/mermaid)")


# In-memory storage for architectures (in production, use a database)
architectures_store: Dict[str, Any] = {}


@app.get("/")
def read_root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Basil Architecture Designer API",
        "version": "1.0.0"
    }


@app.get("/api/models")
def get_available_models():
    """Get all available LLM models"""
    selector = LLMSelector()
    models = selector.get_all_models()

    return {
        "models": [
            {
                "id": name,
                "provider": config.provider,
                "model": config.model,
                "tier": config.tier,
                "context_window": config.context_window,
                "cost_per_1k_tokens": config.cost_per_1k_tokens,
                "strengths": config.strengths
            }
            for name, config in models.items()
        ],
        "tiers": [tier.value for tier in LLMTier],
        "providers": list(set(config.provider for config in models.values()))
    }


@app.get("/api/agent-types")
def get_agent_types():
    """Get all agent types"""
    return {
        "agent_types": [
            {
                "value": agent_type.value,
                "description": _get_agent_type_description(agent_type)
            }
            for agent_type in AgentType
        ]
    }


@app.post("/api/design", response_model=ArchitectureResponse)
def design_architecture(request: DesignRequest):
    """
    Design a multi-agent architecture from a problem statement
    """
    try:
        # Create designer with preferences
        designer = ArchitectureDesigner(
            prefer_provider=request.prefer_provider,
            cost_optimize=request.cost_optimize
        )

        # Design the architecture
        architecture = designer.design(request.problem_statement)

        # Validate architecture
        is_valid, errors = architecture.validate_architecture()

        # Calculate cost estimates for different scales
        cost_estimates = {
            "10k_requests": architecture.estimate_cost(10000),
            "100k_requests": architecture.estimate_cost(100000),
            "1m_requests": architecture.estimate_cost(1000000),
        }

        # Generate visualization
        visualization = designer.visualize_architecture(architecture)

        # Convert to response format
        agents_response = [
            AgentResponse(
                id=agent.id,
                name=agent.name,
                type=agent.type,
                description=agent.description,
                capabilities=agent.capabilities,
                llm_provider=agent.llm_config.provider,
                llm_model=agent.llm_config.model,
                llm_tier=agent.llm_config.tier,
                llm_cost_per_1k=agent.llm_config.cost_per_1k_tokens,
                dependencies=agent.dependencies,
                reusability_score=agent.reusability_score
            )
            for agent in architecture.agents
        ]

        communications_response = [
            CommunicationResponse(
                from_agent=comm.from_agent,
                to_agent=comm.to_agent,
                message_type=comm.message_type,
                description=comm.description
            )
            for comm in architecture.communications
        ]

        response = ArchitectureResponse(
            problem_statement=architecture.problem_statement,
            agents=agents_response,
            communications=communications_response,
            metadata=architecture.metadata,
            cost_estimates=cost_estimates,
            validation={
                "is_valid": is_valid,
                "errors": errors
            },
            visualization=visualization
        )

        # Store architecture for later export (use architecture hash or ID)
        arch_id = str(hash(request.problem_statement))
        architectures_store[arch_id] = architecture

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/export")
def export_architecture(request: ExportRequest):
    """
    Export an architecture in various formats
    """
    if request.architecture_id not in architectures_store:
        raise HTTPException(status_code=404, detail="Architecture not found")

    architecture = architectures_store[request.architecture_id]
    exporter = ArchitectureExporter()

    try:
        if request.format == "json":
            content = exporter.to_json(architecture)
            media_type = "application/json"
        elif request.format == "yaml":
            content = exporter.to_yaml(architecture)
            media_type = "application/x-yaml"
        elif request.format == "markdown":
            content = exporter.to_markdown(architecture)
            media_type = "text/markdown"
        elif request.format == "mermaid":
            content = exporter.to_mermaid(architecture)
            media_type = "text/plain"
        else:
            raise HTTPException(status_code=400, detail="Invalid format")

        return {
            "format": request.format,
            "content": content,
            "media_type": media_type
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/domains")
def get_supported_domains():
    """Get all supported domains"""
    from basil.analyzers.problem_analyzer import ProblemAnalyzer

    analyzer = ProblemAnalyzer()
    domains = []

    for domain, config in analyzer.DOMAIN_PATTERNS.items():
        domains.append({
            "id": domain,
            "name": domain.replace("_", " ").title(),
            "keywords": config["keywords"][:5],  # First 5 keywords
            "capabilities": config["capabilities"],
            "complexity": config["complexity"]
        })

    return {"domains": domains}


def _get_agent_type_description(agent_type: AgentType) -> str:
    """Get description for agent type"""
    descriptions = {
        AgentType.COORDINATOR: "Orchestrates and coordinates other agents",
        AgentType.SPECIALIST: "Domain-specific expert agent",
        AgentType.EXECUTOR: "Performs concrete tasks and operations",
        AgentType.ANALYZER: "Analyzes data and requirements",
        AgentType.VALIDATOR: "Validates outputs and decisions"
    }
    return descriptions.get(agent_type, "")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
