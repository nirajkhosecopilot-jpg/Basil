"""
Export architectures to various formats
"""

import json
import yaml
from typing import Dict, Any
from basil.core.models import Architecture


class ArchitectureExporter:
    """Export architectures to different formats"""

    @staticmethod
    def to_dict(architecture: Architecture) -> Dict[str, Any]:
        """Convert architecture to dictionary"""
        return {
            "problem_statement": architecture.problem_statement,
            "agents": [
                {
                    "id": agent.id,
                    "name": agent.name,
                    "type": agent.type,
                    "description": agent.description,
                    "capabilities": agent.capabilities,
                    "llm": {
                        "provider": agent.llm_config.provider,
                        "model": agent.llm_config.model,
                        "tier": agent.llm_config.tier,
                        "context_window": agent.llm_config.context_window,
                        "cost_per_1k_tokens": agent.llm_config.cost_per_1k_tokens,
                    },
                    "dependencies": agent.dependencies,
                    "reusability_score": agent.reusability_score,
                }
                for agent in architecture.agents
            ],
            "communications": [
                {
                    "from": comm.from_agent,
                    "to": comm.to_agent,
                    "type": comm.message_type,
                    "description": comm.description,
                }
                for comm in architecture.communications
            ],
            "metadata": architecture.metadata,
        }

    @staticmethod
    def to_json(architecture: Architecture, pretty: bool = True) -> str:
        """Export to JSON"""
        data = ArchitectureExporter.to_dict(architecture)
        if pretty:
            return json.dumps(data, indent=2)
        return json.dumps(data)

    @staticmethod
    def to_yaml(architecture: Architecture) -> str:
        """Export to YAML"""
        data = ArchitectureExporter.to_dict(architecture)
        return yaml.dump(data, default_flow_style=False, sort_keys=False)

    @staticmethod
    def to_mermaid(architecture: Architecture) -> str:
        """Export to Mermaid diagram format"""
        lines = ["graph TD"]

        # Add agents
        for agent in architecture.agents:
            node_shape = {
                "coordinator": f"[{agent.name}]",
                "specialist": f"({agent.name})",
                "executor": f"[{agent.name}]",
                "analyzer": f"{{{agent.name}}}",
                "validator": f"[/{agent.name}/]",
            }
            shape = node_shape.get(agent.type, f"({agent.name})")
            lines.append(f"    {agent.id}{shape}")

        # Add communications
        for comm in architecture.communications:
            lines.append(f"    {comm.from_agent} -->|{comm.message_type}| {comm.to_agent}")

        return "\n".join(lines)

    @staticmethod
    def to_markdown(architecture: Architecture) -> str:
        """Export to Markdown documentation"""
        lines = [f"# Architecture: {architecture.problem_statement[:50]}...\n"]

        # Overview
        lines.append("## Overview\n")
        lines.append(f"- **Total Agents**: {len(architecture.agents)}")
        lines.append(f"- **Estimated Cost**: ${architecture.estimate_cost()}/month (10K requests)")
        lines.append("")

        # Agents
        lines.append("## Agents\n")
        for agent in architecture.agents:
            lines.append(f"### {agent.name}\n")
            lines.append(f"**Type**: {agent.type}  ")
            lines.append(f"**LLM**: {agent.llm_config.model} ({agent.llm_config.tier})  ")
            lines.append(f"**Cost**: ${agent.llm_config.cost_per_1k_tokens}/1K tokens  ")
            lines.append(f"**Reusability**: {agent.reusability_score:.1%}\n")
            lines.append(f"{agent.description}\n")
            lines.append("**Capabilities**:")
            for cap in agent.capabilities:
                lines.append(f"- {cap}")
            if agent.dependencies:
                lines.append(f"\n**Dependencies**: {', '.join(agent.dependencies)}")
            lines.append("")

        # Communications
        if architecture.communications:
            lines.append("## Communication Flows\n")
            for comm in architecture.communications:
                lines.append(f"- **{comm.from_agent}** → **{comm.to_agent}**: {comm.description}")

        return "\n".join(lines)
