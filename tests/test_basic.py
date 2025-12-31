"""
Basic tests for Basil framework
"""

import pytest
from basil import ArchitectureDesigner, AgentType
from basil.analyzers.problem_analyzer import ProblemAnalyzer
from basil.selectors.llm_selector import LLMSelector
from basil.core.models import LLMTier


class TestProblemAnalyzer:
    """Test problem analysis functionality"""

    def test_simple_analysis(self):
        analyzer = ProblemAnalyzer()
        problem = "Build an API with user authentication and database storage"

        analysis = analyzer.analyze(problem)

        assert len(analysis.capabilities) > 0
        assert len(analysis.domains) > 0
        assert "authentication" in analysis.domains or "api" in analysis.domains

    def test_complex_analysis(self):
        analyzer = ProblemAnalyzer()
        problem = """
        E-commerce platform with authentication, payment processing,
        inventory management, and machine learning recommendations
        """

        analysis = analyzer.analyze(problem)

        assert len(analysis.domains) >= 3
        assert analysis.requires_coordination is True
        assert analysis.estimated_agents >= 4

    def test_grouping(self):
        analyzer = ProblemAnalyzer()
        problem = "API with auth and database"

        analysis = analyzer.analyze(problem)
        groupings = analyzer.suggest_agent_groupings(analysis)

        assert len(groupings) > 0


class TestLLMSelector:
    """Test LLM selection logic"""

    def test_flagship_for_coordinator(self):
        selector = LLMSelector()

        llm = selector.select_llm(
            agent_type=AgentType.COORDINATOR,
            complexity="high"
        )

        assert llm.tier == LLMTier.FLAGSHIP

    def test_efficient_for_simple_executor(self):
        selector = LLMSelector()

        llm = selector.select_llm(
            agent_type=AgentType.EXECUTOR,
            complexity="low"
        )

        assert llm.tier == LLMTier.EFFICIENT

    def test_provider_preference(self):
        selector = LLMSelector(prefer_provider="anthropic")

        llm = selector.select_llm(
            agent_type=AgentType.SPECIALIST,
            complexity="medium"
        )

        assert llm.provider == "anthropic"

    def test_cost_optimization(self):
        selector = LLMSelector(cost_optimize=True)

        llm = selector.select_llm(
            agent_type=AgentType.SPECIALIST,
            complexity="high"
        )

        # Should prefer advanced over flagship when optimizing
        assert llm.tier in [LLMTier.ADVANCED, LLMTier.FLAGSHIP]
        assert llm.cost_per_1k_tokens <= 0.03  # Not the most expensive


class TestArchitectureDesigner:
    """Test architecture design"""

    def test_simple_design(self):
        designer = ArchitectureDesigner()
        problem = "Build a blog with authentication and posts"

        architecture = designer.design(problem)

        assert len(architecture.agents) >= 2
        assert architecture.problem_statement == problem

    def test_complex_design_with_coordinator(self):
        designer = ArchitectureDesigner()
        problem = """
        E-commerce platform with authentication, payments,
        inventory, search, and analytics
        """

        architecture = designer.design(problem)

        # Should have coordinator for complex system
        coordinators = architecture.get_agents_by_type(AgentType.COORDINATOR)
        assert len(coordinators) >= 1

        # Should have multiple specialists
        assert len(architecture.agents) >= 4

    def test_architecture_validation(self):
        designer = ArchitectureDesigner()
        problem = "Simple API with database"

        architecture = designer.design(problem)
        is_valid, errors = architecture.validate_architecture()

        assert is_valid is True
        assert len(errors) == 0

    def test_cost_estimation(self):
        designer = ArchitectureDesigner()
        problem = "API with auth"

        architecture = designer.design(problem)
        cost = architecture.estimate_cost(monthly_requests=10000)

        assert cost > 0
        assert isinstance(cost, float)

    def test_visualization(self):
        designer = ArchitectureDesigner()
        problem = "Task manager with auth"

        architecture = designer.design(problem)
        viz = designer.visualize_architecture(architecture)

        assert "MULTI-AGENT ARCHITECTURE" in viz
        assert "AGENTS" in viz
        assert len(viz) > 100  # Should be substantial output


class TestArchitecture:
    """Test Architecture model methods"""

    def test_get_agent(self):
        designer = ArchitectureDesigner()
        architecture = designer.design("API with auth")

        # Should be able to get agents by ID
        for agent in architecture.agents:
            found = architecture.get_agent(agent.id)
            assert found is not None
            assert found.id == agent.id

    def test_get_agents_by_type(self):
        designer = ArchitectureDesigner()
        architecture = designer.design("Complex system with auth, payments, ML")

        specialists = architecture.get_agents_by_type(AgentType.SPECIALIST)
        assert isinstance(specialists, list)

    def test_dependency_tree(self):
        designer = ArchitectureDesigner()
        architecture = designer.design("System with auth and database")

        tree = architecture.get_dependency_tree()
        assert isinstance(tree, dict)
        assert len(tree) == len(architecture.agents)


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
