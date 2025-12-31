# Basil - Multi-Agent Architecture Design Framework

> **Design-time architecture planner for multi-agent AI systems**

Basil is an intelligent **architecture design tool** that helps you plan optimal multi-agent systems. Given a problem statement, it analyzes requirements, recommends specialized agents, and assigns appropriate LLMs based on task complexity—all **before you write a single line of code**.

## 🎯 What Basil Does

Basil is a **meta-tool** for the design phase:
- ✅ Analyzes problem statements to identify required capabilities
- ✅ Designs optimal agent architectures (not too granular, not too coarse)
- ✅ Recommends which LLM to use for each agent (GPT-4, Claude, etc.)
- ✅ Estimates costs before you build anything
- ✅ Generates architecture documentation and diagrams
- ❌ Does **NOT** execute agents or make LLM calls (that's what runtime frameworks do)

## 🔄 Basil vs Runtime Frameworks

**Basil is NOT like Semantic Kernel, LangChain, or AutoGen**—it works at a different phase:

| Phase | Tool | What It Does |
|-------|------|--------------|
| **Design** | **Basil** ← You are here | Plans architecture, recommends LLMs |
| **Runtime** | Semantic Kernel, LangChain, AutoGen, CrewAI | Executes agents, makes LLM calls |

**Think of it this way**: Basil is the architect who designs the blueprint; runtime frameworks are the construction crew that builds and operates the building.

**See [docs/COMPARISON.md](docs/COMPARISON.md) for detailed comparisons.**

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

- **[Quick Start Guide](QUICKSTART.md)**: Get started in 5 minutes
- **[User Guide](docs/GUIDE.md)**: Comprehensive guide with examples
- **[Architecture Deep Dive](docs/ARCHITECTURE.md)**: How Basil works internally
- **[Framework Comparison](docs/COMPARISON.md)**: Basil vs Semantic Kernel, LangChain, etc.

## Use Cases

### ✅ When to Use Basil

- Planning a new multi-agent system from scratch
- Deciding how many agents you need and what they should do
- Choosing which LLM to use for each agent
- Estimating costs before building
- Optimizing architecture for cost vs performance
- Presenting architecture to stakeholders
- Avoiding costly refactoring later

### ❌ When NOT to Use Basil

- You just need to make a single LLM call
- Your architecture is already decided
- You're building a simple single-agent chatbot
- You're looking for a runtime execution framework (use Semantic Kernel, LangChain, etc.)

## Workflow: Design with Basil, Build with Others

```
┌─────────────────────────────────────┐
│  1. DESIGN with Basil               │
│     Input: Problem statement        │
│     Output: Architecture blueprint  │
│                                     │
│     "You need 5 agents:             │
│      - Coordinator (GPT-4)          │
│      - API Handler (GPT-3.5)        │
│      - Database Agent (Claude)..."  │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  2. BUILD with runtime frameworks   │
│     - Semantic Kernel (.NET)        │
│     - LangChain (Python)            │
│     - AutoGen (Microsoft)           │
│     - CrewAI                        │
│                                     │
│     Implement the agents Basil      │
│     recommended using the LLMs      │
│     Basil suggested                 │
└─────────────────────────────────────┘
```

## License

MIT
