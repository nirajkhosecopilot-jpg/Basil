# Basil Architecture Documentation

## System Overview

Basil is a multi-agent architecture design framework consisting of four main components:

```
┌─────────────────────────────────────────────────────────────┐
│                    ArchitectureDesigner                      │
│                    (Main Orchestrator)                       │
└────────────┬───────────────────────────────┬────────────────┘
             │                               │
             ▼                               ▼
    ┌────────────────┐              ┌────────────────┐
    │ ProblemAnalyzer│              │  LLMSelector   │
    │                │              │                │
    │ - Identifies   │              │ - Selects      │
    │   domains      │              │   appropriate  │
    │ - Extracts     │              │   LLM models   │
    │   capabilities │              │ - Optimizes    │
    │ - Determines   │              │   for cost     │
    │   complexity   │              │                │
    └────────────────┘              └────────────────┘
             │                               │
             └───────────┬───────────────────┘
                         ▼
              ┌─────────────────────┐
              │    Architecture     │
              │                     │
              │  - Agents           │
              │  - Communications   │
              │  - Metadata         │
              └─────────────────────┘
```

## Component Details

### 1. ArchitectureDesigner

**Purpose**: Main entry point that orchestrates the architecture design process.

**Key Methods**:
- `design(problem_statement)`: Generates complete architecture
- `visualize_architecture(architecture)`: Creates text visualization

**Process**:
1. Analyzes problem statement using ProblemAnalyzer
2. Groups capabilities into optimal agent clusters
3. Creates agents with appropriate types
4. Selects LLMs using LLMSelector
5. Defines communication patterns
6. Validates architecture

### 2. ProblemAnalyzer

**Purpose**: Analyzes problem statements to extract requirements.

**Key Methods**:
- `analyze(problem_statement)`: Returns ProblemAnalysis
- `suggest_agent_groupings(analysis)`: Groups capabilities into agents

**Pattern Matching**:
- Uses keyword-based domain detection
- 15+ pre-defined domain patterns
- Complexity scoring (low/medium/high)
- Capability extraction

**Grouping Strategy**:
- Groups related capabilities
- Merges small domains
- Balances granularity

### 3. LLMSelector

**Purpose**: Selects appropriate LLM models for agents.

**Key Methods**:
- `select_llm(agent_type, complexity, domain)`: Returns LLMConfig
- `get_all_models(tier)`: Lists available models
- `compare_models(names)`: Compares models

**Selection Criteria**:
1. **Complexity**: Low→Efficient, Medium→Advanced, High→Flagship
2. **Agent Type**: Coordinator→Flagship, Specialist→Advanced, Executor→Efficient
3. **Domain**: Critical domains (payment, security) → powerful models
4. **Provider Preference**: OpenAI or Anthropic
5. **Cost Optimization**: Downgrade when possible

**Available Models**:

| Model | Provider | Tier | Cost/1K | Best For |
|-------|----------|------|---------|----------|
| claude-opus | Anthropic | Flagship | $0.075 | Complex reasoning |
| gpt-4 | OpenAI | Flagship | $0.06 | Critical tasks |
| claude-sonnet | Anthropic | Advanced | $0.015 | Balanced workloads |
| gpt-4-turbo | OpenAI | Advanced | $0.03 | Code generation |
| claude-haiku | Anthropic | Efficient | $0.004 | Simple tasks |
| gpt-3.5-turbo | OpenAI | Efficient | $0.002 | High volume |

### 4. Core Models

**Agent**:
- Unique identifier
- Type (coordinator, specialist, executor, analyzer, validator)
- Capabilities list
- LLM configuration
- Dependencies
- Reusability score

**Architecture**:
- Problem statement
- List of agents
- Communication patterns
- Metadata
- Validation methods
- Cost estimation

## Design Decisions

### 1. Why Keyword-Based Analysis?

**Pros**:
- Fast and deterministic
- No external LLM calls needed
- Predictable results
- Easy to extend

**Cons**:
- May miss implicit requirements
- Limited to known patterns

**Alternative**: Could use LLM-based analysis for more sophisticated understanding.

### 2. Why Tiered LLM Selection?

**Rationale**:
- Balance performance and cost
- Match model capabilities to task requirements
- Avoid over-provisioning expensive models
- Allow cost optimization

### 3. Why Agent Grouping?

**Rationale**:
- Avoid too many agents (complexity)
- Avoid too few agents (lack of specialization)
- Group related capabilities
- Promote reusability

**Strategy**:
- Group by domain first
- Merge small domains
- Split high-complexity domains
- Target 3-8 agents total

### 4. Why Coordinator Pattern?

**When Used**:
- 3+ domains
- 2+ high-complexity tasks
- Complex workflows

**Benefits**:
- Central orchestration
- Clearer communication
- Better state management

**Trade-offs**:
- Additional cost (flagship model)
- Single point of failure
- Extra latency

## Data Flow

```
Problem Statement
      │
      ▼
[Domain Detection] ──→ Domains & Keywords
      │
      ▼
[Capability Extraction] ──→ Capabilities with Complexity
      │
      ▼
[Grouping Strategy] ──→ Agent Groupings
      │
      ▼
[Agent Creation] ──→ Agents with Types
      │
      ▼
[LLM Selection] ──→ Agents with LLM Configs
      │
      ▼
[Communication Design] ──→ Communication Patterns
      │
      ▼
[Validation] ──→ Validated Architecture
```

## Extension Points

### 1. Custom Domains

Add new domain patterns to ProblemAnalyzer:

```python
DOMAIN_PATTERNS["new_domain"] = {
    "keywords": [...],
    "capabilities": [...],
    "complexity": "medium"
}
```

### 2. Custom LLMs

Add new models to LLMSelector:

```python
LLM_REGISTRY["new-model"] = LLMConfig(...)
```

### 3. Custom Agent Types

Extend AgentType enum:

```python
class AgentType(str, Enum):
    CUSTOM = "custom"
```

### 4. Custom Grouping Logic

Override `suggest_agent_groupings()` in ProblemAnalyzer.

### 5. Custom Visualization

Create custom visualizers using architecture data.

## Performance Considerations

### Time Complexity

- Problem analysis: O(n × m) where n = text length, m = patterns
- Grouping: O(c²) where c = capabilities
- Agent creation: O(a) where a = agents
- **Total**: O(n × m + c² + a) ≈ O(n) for typical inputs

### Space Complexity

- Architecture object: O(a + c + d) where a = agents, c = communications, d = domains
- Typically: 3-8 agents, 10-30 capabilities, 5-15 domains
- **Total**: O(n) where n = problem statement size

### Scaling

- **Problem size**: Linear scaling with statement length
- **Complexity**: Handles complex problems well
- **Concurrency**: Stateless design allows parallel execution

## Validation

Architecture validation checks:

1. **Circular Dependencies**: Detects dependency cycles
2. **Missing Dependencies**: Ensures all referenced agents exist
3. **Orphaned Agents**: Identifies unreferenced agents
4. **Type Consistency**: Validates agent types and configurations

## Cost Model

**Formula**:
```
Cost = Σ(agents) [ requests × tokens × cost_per_1k_tokens / 1000 ]
```

**Assumptions**:
- Uniform request distribution
- Average token count per request
- No caching or batching

**Example**:
- 100K requests/month
- 1000 tokens/request
- 3 agents: Haiku ($0.004), Sonnet ($0.015), Opus ($0.075)
- Cost: 100K × 1K × (0.004 + 0.015 + 0.075) / 1000 = $9.40/month

## Future Enhancements

1. **LLM-Based Analysis**: Use LLMs to analyze problem statements
2. **Agent Templates**: Pre-built agent templates for common patterns
3. **Dynamic Scaling**: Adjust agent count based on load
4. **Cost Optimization**: ML-based model selection
5. **Visualization**: Graphical architecture diagrams
6. **Deployment**: Generate deployment configurations
7. **Testing**: Generate test suites for architectures
8. **Monitoring**: Integration with observability tools

## References

- Multi-agent systems design patterns
- LLM selection strategies
- Cost optimization techniques
- Software architecture principles
