"""
Core data models for multi-agent architecture
"""

from enum import Enum
from typing import List, Dict, Optional, Set
from pydantic import BaseModel, Field


class AgentType(str, Enum):
    """Types of agents based on their roles"""
    COORDINATOR = "coordinator"  # Orchestrates other agents
    SPECIALIST = "specialist"    # Domain-specific expert
    EXECUTOR = "executor"        # Performs concrete tasks
    ANALYZER = "analyzer"        # Analyzes data/requirements
    VALIDATOR = "validator"      # Validates outputs/decisions


class LLMTier(str, Enum):
    """LLM capability tiers"""
    FLAGSHIP = "flagship"      # GPT-4, Claude Opus - Complex reasoning
    ADVANCED = "advanced"      # GPT-4-turbo, Claude Sonnet - Balanced
    EFFICIENT = "efficient"    # GPT-3.5, Claude Haiku - Fast & cheap
    SPECIALIZED = "specialized" # Fine-tuned models for specific tasks


class LLMConfig(BaseModel):
    """LLM configuration for an agent"""
    provider: str = Field(description="LLM provider (openai, anthropic, etc)")
    model: str = Field(description="Specific model name")
    tier: LLMTier = Field(description="Capability tier")
    context_window: int = Field(description="Token context window")
    cost_per_1k_tokens: float = Field(description="Cost per 1K tokens")
    strengths: List[str] = Field(default_factory=list, description="Model strengths")

    class Config:
        use_enum_values = True


class Agent(BaseModel):
    """Agent definition"""
    id: str = Field(description="Unique agent identifier")
    name: str = Field(description="Human-readable name")
    type: AgentType = Field(description="Agent type")
    description: str = Field(description="What this agent does")
    capabilities: List[str] = Field(description="Specific capabilities")
    llm_config: LLMConfig = Field(description="LLM configuration")
    dependencies: List[str] = Field(default_factory=list, description="Agent IDs this depends on")
    reusability_score: float = Field(default=0.5, description="How reusable (0-1)")

    class Config:
        use_enum_values = True


class Communication(BaseModel):
    """Communication between agents"""
    from_agent: str = Field(description="Source agent ID")
    to_agent: str = Field(description="Target agent ID")
    message_type: str = Field(description="Type of communication")
    description: str = Field(description="What is communicated")


class Architecture(BaseModel):
    """Complete multi-agent architecture"""
    problem_statement: str = Field(description="Original problem")
    agents: List[Agent] = Field(description="All agents in the system")
    communications: List[Communication] = Field(default_factory=list)
    metadata: Dict = Field(default_factory=dict, description="Additional metadata")

    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """Get agent by ID"""
        for agent in self.agents:
            if agent.id == agent_id:
                return agent
        return None

    def get_agents_by_type(self, agent_type: AgentType) -> List[Agent]:
        """Get all agents of a specific type"""
        return [a for a in self.agents if a.type == agent_type]

    def estimate_cost(self, monthly_requests: int = 10000, avg_tokens_per_request: int = 1000) -> float:
        """Estimate monthly cost"""
        total_cost = 0.0
        for agent in self.agents:
            agent_cost = (monthly_requests * avg_tokens_per_request / 1000) * agent.llm_config.cost_per_1k_tokens
            total_cost += agent_cost
        return round(total_cost, 2)

    def get_dependency_tree(self) -> Dict[str, List[str]]:
        """Get dependency tree"""
        tree = {}
        for agent in self.agents:
            tree[agent.id] = agent.dependencies
        return tree

    def validate_architecture(self) -> tuple[bool, List[str]]:
        """Validate architecture for common issues"""
        errors = []

        # Check for circular dependencies
        visited = set()
        rec_stack = set()

        def has_cycle(agent_id: str) -> bool:
            visited.add(agent_id)
            rec_stack.add(agent_id)

            agent = self.get_agent(agent_id)
            if agent:
                for dep in agent.dependencies:
                    if dep not in visited:
                        if has_cycle(dep):
                            return True
                    elif dep in rec_stack:
                        return True

            rec_stack.remove(agent_id)
            return False

        for agent in self.agents:
            if agent.id not in visited:
                if has_cycle(agent.id):
                    errors.append(f"Circular dependency detected involving {agent.id}")

        # Check for missing dependencies
        agent_ids = {a.id for a in self.agents}
        for agent in self.agents:
            for dep in agent.dependencies:
                if dep not in agent_ids:
                    errors.append(f"Agent {agent.id} depends on non-existent agent {dep}")

        # Check for orphaned agents (except coordinators)
        coordinators = self.get_agents_by_type(AgentType.COORDINATOR)
        if coordinators:
            referenced = set()
            for agent in self.agents:
                referenced.update(agent.dependencies)

            for agent in self.agents:
                if agent.type != AgentType.COORDINATOR and agent.id not in referenced:
                    errors.append(f"Agent {agent.id} is not referenced by any other agent")

        return len(errors) == 0, errors
