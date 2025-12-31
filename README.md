# Basil - Multi-Agent Architecture Framework

Basil is an intelligent framework for designing optimal multi-agent architectures from problem statements. It analyzes complex problems, identifies required specialized agents, and assigns appropriate LLMs based on task expertise.

## Features

- **Problem Analysis**: Automatically analyzes problem statements to identify required capabilities
- **Optimal Agent Design**: Balances granularity and reusability to create efficient agent hierarchies
- **LLM Selection**: Assigns appropriate LLM models based on task complexity and domain expertise
- **Architecture Visualization**: Generates clear architecture flows and diagrams
- **Reusability**: Promotes agent reuse across different problem domains

## Architecture Principles

1. **Optimal Granularity**: Agents are neither too fine-grained nor too coarse
2. **Domain Expertise**: Each agent is specialized for specific tasks
3. **LLM Matching**: Assign powerful models for complex tasks, efficient models for simple ones
4. **Reusability**: Design agents that can be reused across multiple problems
5. **Clear Communication**: Well-defined interfaces and communication patterns

## Quick Start

```python
from basil import ArchitectureDesigner

# Define your problem
problem_statement = """
Build an e-commerce platform with product catalog, user authentication,
shopping cart, payment processing, inventory management, and recommendation engine.
"""

# Generate architecture
designer = ArchitectureDesigner()
architecture = designer.design(problem_statement)

# View the architecture
print(architecture.visualize())
print(f"Agents: {len(architecture.agents)}")
print(f"Estimated cost: ${architecture.estimate_cost()}/month")
```

## Installation

```bash
pip install -r requirements.txt
```

## Project Structure

```
basil/
├── core/           # Core framework components
├── agents/         # Agent implementations
├── analyzers/      # Problem analysis tools
├── selectors/      # LLM selection logic
├── generators/     # Architecture generators
├── examples/       # Example use cases
└── tests/          # Test suite
```

## Documentation

See [docs/](docs/) for detailed documentation.

## License

MIT
