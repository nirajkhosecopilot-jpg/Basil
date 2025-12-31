# Quick Start Guide

Get started with Basil in 5 minutes!

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd Basil

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## Your First Architecture

Create a file `my_architecture.py`:

```python
from basil import ArchitectureDesigner

# Define your problem
problem = """
Create a social media platform with user profiles,
posts and comments, real-time messaging, and content recommendations.
"""

# Design the architecture
designer = ArchitectureDesigner()
architecture = designer.design(problem)

# View the result
print(designer.visualize_architecture(architecture))
```

Run it:

```bash
python my_architecture.py
```

## What You'll See

```
================================================================================
MULTI-AGENT ARCHITECTURE
================================================================================

Problem: Create a social media platform with user profiles, posts and...

Total Agents: 5
Estimated Cost: $12.50/month (10K requests)

✓ Architecture is valid

--------------------------------------------------------------------------------
AGENTS
--------------------------------------------------------------------------------

COORDINATOR AGENTS:

  [coordinator] Orchestrator Agent
  Description: Coordinates and orchestrates all specialist agents
  LLM: claude-3-opus-20240229 (flagship)
  Cost: $0.075/1K tokens
  Capabilities: workflow_orchestration, decision_making, task_delegation...
  Reusability: 90.0%

SPECIALIST AGENTS:

  [authentication_agent] Authentication Agent
  Description: Handles authentication related tasks
  LLM: claude-3-5-sonnet-20241022 (advanced)
  Cost: $0.015/1K tokens
  Capabilities: user_authentication, session_management, access_control...
  Reusability: 95.0%

  ...

--------------------------------------------------------------------------------
COMMUNICATION FLOWS
--------------------------------------------------------------------------------

  coordinator → authentication_agent
    Type: task_delegation
    Delegates tasks to Authentication Agent

  ...
```

## Try the Examples

```bash
# E-commerce platform (comprehensive example)
python examples/ecommerce_example.py

# Data processing pipeline
python examples/data_pipeline_example.py

# Simple blog platform
python examples/simple_example.py
```

## Customize Your Design

### Prefer a Specific LLM Provider

```python
# Use Anthropic models
designer = ArchitectureDesigner(prefer_provider="anthropic")

# Use OpenAI models
designer = ArchitectureDesigner(prefer_provider="openai")
```

### Optimize for Cost

```python
# Minimize costs by using cheaper models when possible
designer = ArchitectureDesigner(cost_optimize=True)
```

### Combine Options

```python
designer = ArchitectureDesigner(
    prefer_provider="anthropic",
    cost_optimize=True
)
```

## Access Architecture Details

```python
# Get all agents
for agent in architecture.agents:
    print(f"{agent.name}: {agent.llm_config.model}")

# Filter by type
from basil import AgentType
specialists = architecture.get_agents_by_type(AgentType.SPECIALIST)

# Get cost estimates
cost_10k = architecture.estimate_cost(monthly_requests=10000)
cost_100k = architecture.estimate_cost(monthly_requests=100000)
print(f"10K requests: ${cost_10k}, 100K requests: ${cost_100k}")

# Validate architecture
is_valid, errors = architecture.validate_architecture()
if not is_valid:
    print("Validation errors:", errors)
```

## Write Better Problem Statements

❌ **Too vague:**
```python
problem = "Build a web app"
```

✅ **Clear and detailed:**
```python
problem = """
Build a project management web application with:
- User authentication and team management
- Project and task CRUD operations
- Real-time collaboration features
- File attachments and storage
- Email notifications
- Analytics dashboard
"""
```

## Next Steps

1. **Read the full guide**: `docs/GUIDE.md`
2. **Understand the architecture**: `docs/ARCHITECTURE.md`
3. **Run examples**: `examples/`
4. **Experiment** with your own problem statements

## Tips

- **Be specific**: More details = better architecture
- **Include integrations**: Mention specific services (Stripe, AWS, etc.)
- **State requirements**: Performance, scale, compliance needs
- **List features**: Break down functionality clearly

## Common Issues

**"Too few agents created"**
- Add more details to your problem statement
- Specify distinct functional areas

**"Too expensive"**
- Use `cost_optimize=True`
- Review agent LLM assignments
- Consider simplifying the problem

**"Architecture validation failed"**
- Check error messages
- Usually indicates circular dependencies
- Review agent relationships

## Getting Help

- Check `docs/GUIDE.md` for detailed documentation
- Review examples in `examples/`
- See architecture details in `docs/ARCHITECTURE.md`

Happy architecting! 🚀
