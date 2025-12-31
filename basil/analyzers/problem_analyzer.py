"""
Problem statement analyzer to identify required capabilities and domains
"""

from typing import List, Dict, Set
from pydantic import BaseModel
import re


class Capability(BaseModel):
    """A capability identified in the problem"""
    name: str
    description: str
    complexity: str  # "low", "medium", "high"
    domain: str
    keywords: List[str]


class ProblemAnalysis(BaseModel):
    """Analysis result of a problem statement"""
    problem_statement: str
    capabilities: List[Capability]
    domains: Set[str]
    complexity_distribution: Dict[str, int]
    estimated_agents: int
    requires_coordination: bool


class ProblemAnalyzer:
    """Analyzes problem statements to identify required capabilities"""

    # Domain patterns and their associated capabilities
    DOMAIN_PATTERNS = {
        "authentication": {
            "keywords": ["auth", "login", "signup", "register", "user management", "session", "jwt", "oauth"],
            "capabilities": ["user_authentication", "session_management", "access_control"],
            "complexity": "medium"
        },
        "data_processing": {
            "keywords": ["process", "transform", "etl", "pipeline", "batch", "stream"],
            "capabilities": ["data_transformation", "data_validation", "data_pipeline"],
            "complexity": "medium"
        },
        "api": {
            "keywords": ["api", "endpoint", "rest", "graphql", "webhook"],
            "capabilities": ["api_design", "request_handling", "response_formatting"],
            "complexity": "low"
        },
        "database": {
            "keywords": ["database", "storage", "persist", "query", "crud", "sql", "nosql"],
            "capabilities": ["data_storage", "query_optimization", "data_modeling"],
            "complexity": "medium"
        },
        "ml_ai": {
            "keywords": ["machine learning", "ai", "predict", "classify", "model", "training", "inference", "recommendation"],
            "capabilities": ["model_training", "inference", "feature_engineering"],
            "complexity": "high"
        },
        "payment": {
            "keywords": ["payment", "checkout", "billing", "transaction", "stripe", "paypal"],
            "capabilities": ["payment_processing", "transaction_management", "invoice_generation"],
            "complexity": "high"
        },
        "search": {
            "keywords": ["search", "index", "elasticsearch", "full-text", "filter"],
            "capabilities": ["indexing", "search_query", "ranking"],
            "complexity": "medium"
        },
        "notification": {
            "keywords": ["notification", "email", "sms", "push", "alert", "notify"],
            "capabilities": ["message_delivery", "template_management", "notification_routing"],
            "complexity": "low"
        },
        "analytics": {
            "keywords": ["analytics", "metrics", "tracking", "dashboard", "report", "visualization"],
            "capabilities": ["data_collection", "metric_calculation", "visualization"],
            "complexity": "medium"
        },
        "file_management": {
            "keywords": ["file", "upload", "download", "storage", "s3", "blob"],
            "capabilities": ["file_upload", "file_processing", "storage_management"],
            "complexity": "low"
        },
        "inventory": {
            "keywords": ["inventory", "stock", "warehouse", "sku", "product catalog"],
            "capabilities": ["inventory_tracking", "stock_management", "catalog_management"],
            "complexity": "medium"
        },
        "scheduling": {
            "keywords": ["schedule", "calendar", "appointment", "booking", "cron"],
            "capabilities": ["task_scheduling", "calendar_management", "resource_allocation"],
            "complexity": "medium"
        },
        "security": {
            "keywords": ["security", "encryption", "audit", "compliance", "vulnerability"],
            "capabilities": ["security_scanning", "encryption", "audit_logging"],
            "complexity": "high"
        },
        "monitoring": {
            "keywords": ["monitor", "log", "trace", "observability", "health check"],
            "capabilities": ["log_collection", "metric_monitoring", "alerting"],
            "complexity": "medium"
        },
        "workflow": {
            "keywords": ["workflow", "orchestration", "state machine", "approval", "process"],
            "capabilities": ["workflow_orchestration", "state_management", "approval_handling"],
            "complexity": "high"
        }
    }

    def analyze(self, problem_statement: str) -> ProblemAnalysis:
        """
        Analyze a problem statement to identify capabilities and domains
        """
        problem_lower = problem_statement.lower()

        # Identify domains and capabilities
        identified_capabilities = []
        identified_domains = set()

        for domain, config in self.DOMAIN_PATTERNS.items():
            # Check if any keywords match
            for keyword in config["keywords"]:
                if keyword in problem_lower:
                    identified_domains.add(domain)

                    # Add capabilities for this domain
                    for cap_name in config["capabilities"]:
                        capability = Capability(
                            name=cap_name,
                            description=f"{cap_name.replace('_', ' ').title()} capability",
                            complexity=config["complexity"],
                            domain=domain,
                            keywords=[keyword]
                        )
                        identified_capabilities.append(capability)
                    break

        # Remove duplicate capabilities
        unique_caps = {}
        for cap in identified_capabilities:
            if cap.name not in unique_caps:
                unique_caps[cap.name] = cap

        capabilities = list(unique_caps.values())

        # Calculate complexity distribution
        complexity_dist = {"low": 0, "medium": 0, "high": 0}
        for cap in capabilities:
            complexity_dist[cap.complexity] += 1

        # Estimate number of agents needed
        num_capabilities = len(capabilities)
        num_domains = len(identified_domains)

        # Heuristic: balance between capabilities and domains
        # More domains -> more specialized agents
        # More capabilities -> potential for grouping
        estimated_agents = min(
            max(3, num_domains),  # At least 3, based on domains
            max(num_capabilities // 2, 2)  # Group capabilities, minimum 2
        )

        # Add coordinator if complex
        requires_coordination = num_domains >= 3 or complexity_dist["high"] >= 2

        if requires_coordination:
            estimated_agents += 1  # Add coordinator

        return ProblemAnalysis(
            problem_statement=problem_statement,
            capabilities=capabilities,
            domains=identified_domains,
            complexity_distribution=complexity_dist,
            estimated_agents=estimated_agents,
            requires_coordination=requires_coordination
        )

    def suggest_agent_groupings(self, analysis: ProblemAnalysis) -> Dict[str, List[Capability]]:
        """
        Suggest how to group capabilities into agents
        """
        groupings = {}

        # Group by domain first
        for cap in analysis.capabilities:
            domain = cap.domain
            if domain not in groupings:
                groupings[domain] = []
            groupings[domain].append(cap)

        # Merge small domains if they're related
        merged_groupings = {}
        for domain, caps in groupings.items():
            # Keep domains with 2+ capabilities or high complexity
            if len(caps) >= 2 or any(c.complexity == "high" for c in caps):
                merged_groupings[domain] = caps
            else:
                # Merge into "general" group
                if "general" not in merged_groupings:
                    merged_groupings["general"] = []
                merged_groupings["general"].extend(caps)

        return merged_groupings
