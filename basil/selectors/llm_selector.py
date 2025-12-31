"""
LLM selector that assigns appropriate models based on task requirements
"""

from typing import List, Dict, Optional
from basil.core.models import LLMConfig, LLMTier, AgentType


class LLMSelector:
    """Selects appropriate LLM based on task requirements"""

    # Available LLM configurations
    LLM_REGISTRY = {
        # Flagship models - for complex reasoning and critical tasks
        "gpt4": LLMConfig(
            provider="openai",
            model="gpt-4",
            tier=LLMTier.FLAGSHIP,
            context_window=8192,
            cost_per_1k_tokens=0.06,
            strengths=["complex_reasoning", "code_generation", "analysis"]
        ),
        "claude-opus": LLMConfig(
            provider="anthropic",
            model="claude-3-opus-20240229",
            tier=LLMTier.FLAGSHIP,
            context_window=200000,
            cost_per_1k_tokens=0.075,
            strengths=["complex_reasoning", "long_context", "analysis", "creative_writing"]
        ),

        # Advanced models - balanced performance and cost
        "gpt4-turbo": LLMConfig(
            provider="openai",
            model="gpt-4-turbo",
            tier=LLMTier.ADVANCED,
            context_window=128000,
            cost_per_1k_tokens=0.03,
            strengths=["reasoning", "code_generation", "json_mode"]
        ),
        "claude-sonnet": LLMConfig(
            provider="anthropic",
            model="claude-3-5-sonnet-20241022",
            tier=LLMTier.ADVANCED,
            context_window=200000,
            cost_per_1k_tokens=0.015,
            strengths=["balanced", "code_generation", "analysis", "long_context"]
        ),

        # Efficient models - fast and cost-effective
        "gpt3.5-turbo": LLMConfig(
            provider="openai",
            model="gpt-3.5-turbo",
            tier=LLMTier.EFFICIENT,
            context_window=16385,
            cost_per_1k_tokens=0.002,
            strengths=["speed", "efficiency", "simple_tasks"]
        ),
        "claude-haiku": LLMConfig(
            provider="anthropic",
            model="claude-3-5-haiku-20241022",
            tier=LLMTier.EFFICIENT,
            context_window=200000,
            cost_per_1k_tokens=0.004,
            strengths=["speed", "efficiency", "simple_tasks", "long_context"]
        ),
    }

    # Task complexity to LLM tier mapping
    COMPLEXITY_TO_TIER = {
        "low": LLMTier.EFFICIENT,
        "medium": LLMTier.ADVANCED,
        "high": LLMTier.FLAGSHIP
    }

    # Agent type preferences
    AGENT_TYPE_PREFERENCES = {
        AgentType.COORDINATOR: LLMTier.FLAGSHIP,     # Needs strong reasoning
        AgentType.SPECIALIST: LLMTier.ADVANCED,      # Domain expertise
        AgentType.EXECUTOR: LLMTier.EFFICIENT,       # Simple execution
        AgentType.ANALYZER: LLMTier.ADVANCED,        # Analysis capabilities
        AgentType.VALIDATOR: LLMTier.EFFICIENT,      # Pattern matching
    }

    # Domain-specific preferences
    DOMAIN_PREFERENCES = {
        "ml_ai": ["claude-opus", "gpt4"],            # Complex reasoning
        "security": ["gpt4", "claude-opus"],         # Critical accuracy
        "payment": ["gpt4", "claude-opus"],          # High stakes
        "workflow": ["claude-sonnet", "gpt4-turbo"], # State management
        "authentication": ["claude-sonnet", "gpt4-turbo"],
        "database": ["claude-sonnet", "gpt4-turbo"],
        "api": ["claude-haiku", "gpt3.5-turbo"],     # Simple tasks
        "notification": ["claude-haiku", "gpt3.5-turbo"],
        "file_management": ["claude-haiku", "gpt3.5-turbo"],
    }

    def __init__(self, prefer_provider: Optional[str] = None, cost_optimize: bool = False):
        """
        Initialize LLM selector

        Args:
            prefer_provider: Preferred LLM provider ("openai" or "anthropic")
            cost_optimize: If True, prefer cheaper models when possible
        """
        self.prefer_provider = prefer_provider
        self.cost_optimize = cost_optimize

    def select_llm(
        self,
        agent_type: AgentType,
        complexity: str,
        domain: Optional[str] = None,
        required_strengths: Optional[List[str]] = None
    ) -> LLMConfig:
        """
        Select appropriate LLM for an agent

        Args:
            agent_type: Type of agent
            complexity: Task complexity ("low", "medium", "high")
            domain: Optional domain for domain-specific selection
            required_strengths: Optional list of required capabilities

        Returns:
            Selected LLM configuration
        """
        # Start with base tier from complexity
        base_tier = self.COMPLEXITY_TO_TIER.get(complexity, LLMTier.ADVANCED)

        # Adjust for agent type
        type_tier = self.AGENT_TYPE_PREFERENCES.get(agent_type, LLMTier.ADVANCED)

        # Use the higher tier (more capable)
        selected_tier = max(base_tier, type_tier, key=lambda x: self._tier_rank(x))

        # Get domain preferences
        preferred_models = []
        if domain and domain in self.DOMAIN_PREFERENCES:
            preferred_models = self.DOMAIN_PREFERENCES[domain]

        # Filter by tier
        candidates = [
            (name, config) for name, config in self.LLM_REGISTRY.items()
            if config.tier == selected_tier
        ]

        # If cost optimization, downgrade if possible
        if self.cost_optimize and selected_tier == LLMTier.FLAGSHIP:
            advanced_candidates = [
                (name, config) for name, config in self.LLM_REGISTRY.items()
                if config.tier == LLMTier.ADVANCED
            ]
            if advanced_candidates:
                candidates = advanced_candidates

        # Apply provider preference
        if self.prefer_provider:
            provider_candidates = [
                (name, config) for name, config in candidates
                if config.provider == self.prefer_provider
            ]
            if provider_candidates:
                candidates = provider_candidates

        # Apply domain preferences
        if preferred_models:
            domain_candidates = [
                (name, config) for name, config in candidates
                if name in preferred_models
            ]
            if domain_candidates:
                candidates = domain_candidates

        # Check required strengths
        if required_strengths:
            strength_candidates = [
                (name, config) for name, config in candidates
                if any(s in config.strengths for s in required_strengths)
            ]
            if strength_candidates:
                candidates = strength_candidates

        # Select best candidate (prefer lower cost if multiple)
        if not candidates:
            # Fallback to any model of the tier
            candidates = [
                (name, config) for name, config in self.LLM_REGISTRY.items()
                if config.tier == selected_tier
            ]

        if not candidates:
            # Ultimate fallback
            return self.LLM_REGISTRY["claude-sonnet"]

        # Sort by cost and select cheapest
        candidates.sort(key=lambda x: x[1].cost_per_1k_tokens)
        return candidates[0][1]

    def _tier_rank(self, tier: LLMTier) -> int:
        """Get numeric rank of tier"""
        ranks = {
            LLMTier.EFFICIENT: 1,
            LLMTier.ADVANCED: 2,
            LLMTier.FLAGSHIP: 3,
            LLMTier.SPECIALIZED: 2,
        }
        return ranks.get(tier, 2)

    def get_all_models(self, tier: Optional[LLMTier] = None) -> Dict[str, LLMConfig]:
        """Get all available models, optionally filtered by tier"""
        if tier:
            return {
                name: config for name, config in self.LLM_REGISTRY.items()
                if config.tier == tier
            }
        return self.LLM_REGISTRY.copy()

    def compare_models(self, model_names: List[str]) -> Dict:
        """Compare multiple models"""
        comparison = {}
        for name in model_names:
            if name in self.LLM_REGISTRY:
                config = self.LLM_REGISTRY[name]
                comparison[name] = {
                    "provider": config.provider,
                    "tier": config.tier,
                    "cost_per_1k": config.cost_per_1k_tokens,
                    "context_window": config.context_window,
                    "strengths": config.strengths
                }
        return comparison
