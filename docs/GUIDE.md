# Basil User Guide

## Overview

Basil is a framework for automatically designing optimal multi-agent architectures from problem statements. It analyzes your requirements and creates a balanced architecture with appropriate LLM assignments.

## Core Concepts

### 1. Problem Analysis

Basil analyzes your problem statement to identify:
- **Capabilities**: Specific functionalities needed (auth, payments, search, etc.)
- **Domains**: Functional areas (authentication, database, API, etc.)
- **Complexity**: Low, medium, or high complexity for each capability
- **Coordination needs**: Whether a coordinator agent is required

### 2. Agent Types

Basil creates five types of agents:

| Type | Purpose | Example |
|------|---------|---------|
| **Coordinator** | Orchestrates other agents | Workflow manager |
| **Specialist** | Domain expert | Payment processor |
| **Executor** | Performs tasks | API handler |
| **Analyzer** | Analyzes data | Data validator |
| **Validator** | Validates outputs | Schema checker |

### 3. LLM Selection

Basil assigns LLMs based on:
- **Task complexity**: Simple tasks get efficient models, complex get flagship
- **Agent type**: Coordinators get powerful models, executors get efficient ones
- **Domain requirements**: Critical domains (payment, security) get powerful models
- **Cost optimization**: When enabled, prefers cheaper models when appropriate

### 4. LLM Tiers

| Tier | Models | Use Case | Cost |
|------|--------|----------|------|
| **Flagship** | GPT-4, Claude Opus | Complex reasoning, critical tasks | High |
| **Advanced** | GPT-4 Turbo, Claude Sonnet | Balanced performance | Medium |
| **Efficient** | GPT-3.5, Claude Haiku | Simple tasks, high volume | Low |

## Usage Guide

### Basic Usage

```python
from basil import ArchitectureDesigner

# Define your problem
problem = """
Build an e-commerce platform with user auth,
product catalog, shopping cart, and payments.
"""

# Create designer
designer = ArchitectureDesigner()

# Generate architecture
architecture = designer.design(problem)

# Visualize
print(designer.visualize_architecture(architecture))
```

### Advanced Options

```python
# Prefer Anthropic models
designer = ArchitectureDesigner(prefer_provider="anthropic")

# Optimize for cost
designer = ArchitectureDesigner(cost_optimize=True)

# Combine both
designer = ArchitectureDesigner(
    prefer_provider="openai",
    cost_optimize=True
)
```

### Accessing Architecture Details

```python
# Get all agents
for agent in architecture.agents:
    print(f"{agent.name}: {agent.llm_config.model}")

# Get agents by type
from basil import AgentType
coordinators = architecture.get_agents_by_type(AgentType.COORDINATOR)

# Get specific agent
auth_agent = architecture.get_agent("authentication_agent")

# Estimate costs
monthly_cost = architecture.estimate_cost(
    monthly_requests=100000,
    avg_tokens_per_request=1500
)

# Validate architecture
is_valid, errors = architecture.validate_architecture()
if not is_valid:
    for error in errors:
        print(f"Error: {error}")
```

## Design Principles

### 1. Optimal Granularity

Basil balances agent granularity:
- **Not too fine**: Avoids creating an agent for every tiny task
- **Not too coarse**: Separates concerns appropriately
- **Just right**: Groups related capabilities into focused agents

### 2. Reusability

Basil scores agents on reusability (0-1):
- **High (0.8-1.0)**: Generic agents (auth, API) reusable across projects
- **Medium (0.5-0.8)**: Somewhat customizable (analytics, workflows)
- **Low (0.3-0.5)**: Highly specific (custom ML models, business logic)

### 3. Cost Optimization

Basil optimizes costs by:
- Assigning efficient models to simple tasks
- Using powerful models only when needed
- Providing cost estimates for planning

### 4. Coordination

Basil adds a coordinator when:
- Multiple domains (3+) need orchestration
- Complex workflows require state management
- High-complexity tasks need oversight

## Examples

### Example 1: E-commerce Platform

See `examples/ecommerce_example.py` for a complete e-commerce architecture with:
- 6-8 specialized agents
- Coordinator for orchestration
- Mixed LLM tiers for cost optimization
- Estimated costs for different scales

### Example 2: Data Pipeline

See `examples/data_pipeline_example.py` for a data processing pipeline with:
- Stream and batch processing
- ML inference integration
- Security and compliance agents
- Monitoring and alerting

### Example 3: Simple Blog

See `examples/simple_example.py` for a minimal blog platform showing basic usage.

## Domain Coverage

Basil recognizes these domains out of the box:

- Authentication & Authorization
- API Development
- Database & Storage
- Payment Processing
- Machine Learning & AI
- Search & Indexing
- Notifications (email, SMS, push)
- Analytics & Reporting
- File Management
- Inventory Management
- Scheduling & Cron
- Security & Compliance
- Monitoring & Logging
- Workflow Orchestration

## Best Practices

### 1. Write Clear Problem Statements

✅ Good:
```
Build a task management app with user authentication,
task CRUD operations, real-time collaboration, and
email notifications.
```

❌ Bad:
```
Make an app
```

### 2. Include Implementation Details

✅ Good:
```
Payment processing with Stripe and PayPal support,
handling subscriptions and one-time payments.
```

❌ Bad:
```
Payments
```

### 3. Specify Scale Requirements

```
Platform supporting 100K daily active users with
real-time updates and sub-second response times.
```

### 4. Mention Critical Requirements

```
Healthcare platform requiring HIPAA compliance,
audit logging, and encrypted data storage.
```

## Customization

### Adding Custom Domains

Extend the problem analyzer:

```python
from basil.analyzers.problem_analyzer import ProblemAnalyzer

analyzer = ProblemAnalyzer()
analyzer.DOMAIN_PATTERNS["custom_domain"] = {
    "keywords": ["custom", "special"],
    "capabilities": ["custom_cap"],
    "complexity": "medium"
}
```

### Adding Custom LLMs

Extend the LLM registry:

```python
from basil.selectors.llm_selector import LLMSelector
from basil.core.models import LLMConfig, LLMTier

selector = LLMSelector()
selector.LLM_REGISTRY["custom-model"] = LLMConfig(
    provider="custom",
    model="custom-model-v1",
    tier=LLMTier.ADVANCED,
    context_window=32000,
    cost_per_1k_tokens=0.01,
    strengths=["custom_task"]
)
```

## FAQ

**Q: How many agents will be created?**
A: Typically 3-8 agents depending on problem complexity. Simple problems get 3-4 agents, complex ones get 6-8+.

**Q: Can I specify which LLM to use?**
A: Use `prefer_provider` to prefer a provider. For full control, modify the LLM selector.

**Q: How accurate are cost estimates?**
A: Estimates assume average token usage. Actual costs depend on prompt sizes and response lengths.

**Q: Can agents communicate with each other?**
A: Yes, Basil defines communication patterns. With a coordinator, agents report to it. Without one, peer-to-peer communication is used.

**Q: Is this production-ready?**
A: Basil generates architecture designs. You'll need to implement the actual agent logic and communication.

## Next Steps

1. Run the examples: `python examples/simple_example.py`
2. Try your own problem statement
3. Experiment with cost optimization
4. Extend with custom domains and LLMs

For more examples and advanced usage, see the `examples/` directory.
