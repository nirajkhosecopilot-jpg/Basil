"""
Example: E-commerce Platform Architecture

This example demonstrates how to use Basil to design a multi-agent
architecture for a complete e-commerce platform.
"""

from basil import ArchitectureDesigner

# Define the problem statement
problem_statement = """
Build a comprehensive e-commerce platform with the following features:

1. User Management:
   - User registration and authentication
   - Profile management
   - OAuth integration for social login

2. Product Catalog:
   - Product browsing and search
   - Category management
   - Inventory tracking and stock management
   - Product recommendations using machine learning

3. Shopping Experience:
   - Shopping cart functionality
   - Wishlist management
   - Product reviews and ratings

4. Order Processing:
   - Checkout flow
   - Payment processing (Stripe, PayPal)
   - Order tracking and status updates
   - Email notifications for order updates

5. Backend Services:
   - RESTful API endpoints
   - Database for persistent storage
   - File upload for product images
   - Analytics dashboard for business metrics
   - Admin panel for inventory and order management

6. Additional Features:
   - Search functionality with filtering
   - Real-time inventory updates
   - Automated email marketing campaigns
"""


def main():
    print("=" * 80)
    print("BASIL - Multi-Agent Architecture Designer")
    print("Example: E-commerce Platform")
    print("=" * 80)
    print()

    # Create designer with Anthropic preference and cost optimization
    designer = ArchitectureDesigner(
        prefer_provider="anthropic",
        cost_optimize=True
    )

    print("Analyzing problem statement...")
    print()

    # Design the architecture
    architecture = designer.design(problem_statement)

    # Visualize the architecture
    print(designer.visualize_architecture(architecture))

    # Show detailed breakdown
    print("\n" + "=" * 80)
    print("DETAILED ANALYSIS")
    print("=" * 80)

    # Cost analysis
    print("\n💰 Cost Estimates:")
    print(f"  10K requests/month:  ${architecture.estimate_cost(10000)}")
    print(f"  100K requests/month: ${architecture.estimate_cost(100000)}")
    print(f"  1M requests/month:   ${architecture.estimate_cost(1000000)}")

    # Agent breakdown by LLM tier
    print("\n🤖 Agent Distribution by LLM Tier:")
    tiers = {}
    for agent in architecture.agents:
        tier = agent.llm_config.tier
        if tier not in tiers:
            tiers[tier] = []
        tiers[tier].append(agent.name)

    for tier, agents in sorted(tiers.items()):
        print(f"\n  {tier.upper()}:")
        for agent_name in agents:
            print(f"    - {agent_name}")

    # Reusability analysis
    print("\n♻️  Reusability Scores:")
    reusable_agents = sorted(
        architecture.agents,
        key=lambda a: a.reusability_score,
        reverse=True
    )
    for agent in reusable_agents[:5]:
        print(f"  {agent.name}: {agent.reusability_score:.1%}")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
