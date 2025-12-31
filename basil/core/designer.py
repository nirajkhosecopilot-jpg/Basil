"""
Main architecture designer that orchestrates the design process
"""

from typing import Optional, Dict
from basil.core.models import Agent, AgentType, Architecture, Communication
from basil.analyzers.problem_analyzer import ProblemAnalyzer
from basil.selectors.llm_selector import LLMSelector


class ArchitectureDesigner:
    """Main class for designing multi-agent architectures"""

    def __init__(
        self,
        prefer_provider: Optional[str] = None,
        cost_optimize: bool = False
    ):
        """
        Initialize the architecture designer

        Args:
            prefer_provider: Preferred LLM provider ("openai" or "anthropic")
            cost_optimize: If True, optimize for lower costs
        """
        self.analyzer = ProblemAnalyzer()
        self.llm_selector = LLMSelector(
            prefer_provider=prefer_provider,
            cost_optimize=cost_optimize
        )

    def design(self, problem_statement: str) -> Architecture:
        """
        Design a multi-agent architecture from a problem statement

        Args:
            problem_statement: Detailed description of the problem

        Returns:
            Complete Architecture with agents and their LLM configs
        """
        # Step 1: Analyze the problem
        analysis = self.analyzer.analyze(problem_statement)

        # Step 2: Get suggested groupings
        groupings = self.analyzer.suggest_agent_groupings(analysis)

        # Step 3: Create agents
        agents = []
        agent_id_map = {}

        # Create coordinator if needed
        if analysis.requires_coordination:
            coordinator = self._create_coordinator(analysis)
            agents.append(coordinator)
            agent_id_map["coordinator"] = coordinator.id

        # Create specialist agents for each domain
        for domain, capabilities in groupings.items():
            agent = self._create_specialist_agent(domain, capabilities, analysis)
            agents.append(agent)
            agent_id_map[domain] = agent.id

            # If we have a coordinator, make specialist depend on it for orchestration
            if analysis.requires_coordination and domain != "coordinator":
                # Note: coordinator doesn't depend on specialists, specialists report to coordinator
                pass

        # Step 4: Create communications
        communications = self._create_communications(agents, analysis.requires_coordination)

        # Step 5: Build architecture
        architecture = Architecture(
            problem_statement=problem_statement,
            agents=agents,
            communications=communications,
            metadata={
                "num_domains": len(analysis.domains),
                "num_capabilities": len(analysis.capabilities),
                "complexity_distribution": analysis.complexity_distribution,
                "requires_coordination": analysis.requires_coordination
            }
        )

        return architecture

    def _create_coordinator(self, analysis) -> Agent:
        """Create a coordinator agent"""
        # Coordinators need strong reasoning - use flagship model
        llm_config = self.llm_selector.select_llm(
            agent_type=AgentType.COORDINATOR,
            complexity="high",
            required_strengths=["complex_reasoning"]
        )

        return Agent(
            id="coordinator",
            name="Orchestrator Agent",
            type=AgentType.COORDINATOR,
            description="Coordinates and orchestrates all specialist agents, manages workflow and decision-making",
            capabilities=[
                "workflow_orchestration",
                "decision_making",
                "task_delegation",
                "result_aggregation"
            ],
            llm_config=llm_config,
            dependencies=[],
            reusability_score=0.9  # Coordinators are highly reusable
        )

    def _create_specialist_agent(self, domain: str, capabilities, analysis) -> Agent:
        """Create a specialist agent for a domain"""
        # Determine complexity for this domain
        complexities = [cap.complexity for cap in capabilities]
        max_complexity = "low"
        if "high" in complexities:
            max_complexity = "high"
        elif "medium" in complexities:
            max_complexity = "medium"

        # Determine agent type based on domain and complexity
        agent_type = AgentType.SPECIALIST
        if domain in ["api", "file_management", "notification"]:
            agent_type = AgentType.EXECUTOR
        elif domain in ["analytics", "data_processing"]:
            agent_type = AgentType.ANALYZER

        # Select LLM
        llm_config = self.llm_selector.select_llm(
            agent_type=agent_type,
            complexity=max_complexity,
            domain=domain
        )

        # Calculate reusability score
        reusability = self._calculate_reusability(domain, capabilities)

        # Format domain name
        domain_name = domain.replace("_", " ").title()

        return Agent(
            id=f"{domain}_agent",
            name=f"{domain_name} Agent",
            type=agent_type,
            description=f"Handles {domain_name.lower()} related tasks and operations",
            capabilities=[cap.name for cap in capabilities],
            llm_config=llm_config,
            dependencies=["coordinator"] if analysis.requires_coordination else [],
            reusability_score=reusability
        )

    def _calculate_reusability(self, domain: str, capabilities) -> float:
        """Calculate reusability score for an agent"""
        # Common domains are more reusable
        common_domains = {
            "authentication": 0.95,
            "api": 0.9,
            "database": 0.85,
            "notification": 0.85,
            "file_management": 0.8,
            "analytics": 0.75,
            "payment": 0.7,  # Less reusable due to business logic
            "inventory": 0.6,
            "ml_ai": 0.5,    # Often highly customized
        }

        base_score = common_domains.get(domain, 0.5)

        # Adjust based on number of capabilities (more capabilities = less focused = less reusable)
        num_caps = len(capabilities)
        if num_caps <= 2:
            adjustment = 0.1
        elif num_caps <= 4:
            adjustment = 0.0
        else:
            adjustment = -0.1

        return min(0.95, max(0.3, base_score + adjustment))

    def _create_communications(self, agents, has_coordinator: bool) -> list:
        """Create communication links between agents"""
        communications = []

        if has_coordinator:
            coordinator_id = "coordinator"

            # Coordinator communicates with all specialists
            for agent in agents:
                if agent.id != coordinator_id:
                    # Coordinator delegates to specialist
                    communications.append(Communication(
                        from_agent=coordinator_id,
                        to_agent=agent.id,
                        message_type="task_delegation",
                        description=f"Delegates tasks to {agent.name}"
                    ))

                    # Specialist reports back to coordinator
                    communications.append(Communication(
                        from_agent=agent.id,
                        to_agent=coordinator_id,
                        message_type="result_report",
                        description=f"Reports results back to coordinator"
                    ))

        else:
            # Peer-to-peer communication between agents
            for i, agent1 in enumerate(agents):
                for agent2 in agents[i+1:]:
                    communications.append(Communication(
                        from_agent=agent1.id,
                        to_agent=agent2.id,
                        message_type="data_exchange",
                        description=f"Exchanges data with {agent2.name}"
                    ))

        return communications

    def visualize_architecture(self, architecture: Architecture) -> str:
        """
        Create a text-based visualization of the architecture

        Args:
            architecture: Architecture to visualize

        Returns:
            Text visualization
        """
        lines = []
        lines.append("=" * 80)
        lines.append("MULTI-AGENT ARCHITECTURE")
        lines.append("=" * 80)
        lines.append("")
        lines.append(f"Problem: {architecture.problem_statement[:100]}...")
        lines.append("")
        lines.append(f"Total Agents: {len(architecture.agents)}")
        lines.append(f"Estimated Cost: ${architecture.estimate_cost()}/month (10K requests)")
        lines.append("")

        # Validate architecture
        is_valid, errors = architecture.validate_architecture()
        if is_valid:
            lines.append("✓ Architecture is valid")
        else:
            lines.append("⚠ Architecture has issues:")
            for error in errors:
                lines.append(f"  - {error}")
        lines.append("")

        lines.append("-" * 80)
        lines.append("AGENTS")
        lines.append("-" * 80)

        # Group by type
        by_type = {}
        for agent in architecture.agents:
            if agent.type not in by_type:
                by_type[agent.type] = []
            by_type[agent.type].append(agent)

        for agent_type, agents in sorted(by_type.items()):
            lines.append(f"\n{agent_type.upper()} AGENTS:")
            for agent in agents:
                lines.append(f"\n  [{agent.id}] {agent.name}")
                lines.append(f"  Description: {agent.description}")
                lines.append(f"  LLM: {agent.llm_config.model} ({agent.llm_config.tier})")
                lines.append(f"  Cost: ${agent.llm_config.cost_per_1k_tokens}/1K tokens")
                lines.append(f"  Capabilities: {', '.join(agent.capabilities[:3])}...")
                lines.append(f"  Reusability: {agent.reusability_score:.1%}")
                if agent.dependencies:
                    lines.append(f"  Dependencies: {', '.join(agent.dependencies)}")

        lines.append("\n" + "-" * 80)
        lines.append("COMMUNICATION FLOWS")
        lines.append("-" * 80)

        for comm in architecture.communications[:10]:  # Show first 10
            lines.append(f"\n  {comm.from_agent} → {comm.to_agent}")
            lines.append(f"    Type: {comm.message_type}")
            lines.append(f"    {comm.description}")

        if len(architecture.communications) > 10:
            lines.append(f"\n  ... and {len(architecture.communications) - 10} more")

        lines.append("\n" + "=" * 80)

        return "\n".join(lines)
