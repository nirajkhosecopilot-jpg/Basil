"""
Simple Example: Basic Usage

This example shows the simplest way to use Basil.
"""

from basil import ArchitectureDesigner


def main():
    # Simple problem statement
    problem = """
    Create a blog platform with user authentication,
    post creation and editing, comments, and search functionality.
    """

    # Create designer and generate architecture
    designer = ArchitectureDesigner()
    architecture = designer.design(problem)

    # Print results
    print(designer.visualize_architecture(architecture))

    # Access individual agents
    print("\nAgent Details:")
    for agent in architecture.agents:
        print(f"\n{agent.name}:")
        print(f"  - Type: {agent.type}")
        print(f"  - LLM: {agent.llm_config.model}")
        print(f"  - Capabilities: {len(agent.capabilities)}")


if __name__ == "__main__":
    main()
