"""
Example: Data Processing Pipeline Architecture

This example shows how to design an architecture for a
complex data processing and analytics pipeline.
"""

from basil import ArchitectureDesigner

problem_statement = """
Design a data processing pipeline for a financial analytics platform:

1. Data Ingestion:
   - Ingest data from multiple sources (APIs, databases, file uploads)
   - Support batch and streaming data
   - Handle various file formats (CSV, JSON, Parquet)

2. Data Processing:
   - Data validation and cleansing
   - ETL transformations
   - Data aggregation and summarization
   - Machine learning model inference for predictions

3. Storage and Indexing:
   - Store processed data in database
   - Index data for fast search
   - Implement data versioning

4. Analytics and Reporting:
   - Generate business metrics and KPIs
   - Create visualization dashboards
   - Schedule automated reports
   - Send email notifications for alerts

5. Security and Compliance:
   - Audit logging for all operations
   - Data encryption at rest and in transit
   - Compliance with financial regulations

6. Monitoring:
   - Monitor pipeline health
   - Track processing metrics
   - Alert on failures or anomalies
"""


def main():
    print("Designing Data Pipeline Architecture...")
    print()

    # Use OpenAI with balanced cost optimization
    designer = ArchitectureDesigner(
        prefer_provider="openai",
        cost_optimize=False
    )

    architecture = designer.design(problem_statement)

    # Visualize
    print(designer.visualize_architecture(architecture))

    # Export to YAML (simplified)
    print("\n" + "=" * 80)
    print("ARCHITECTURE EXPORT (YAML Format)")
    print("=" * 80)
    print()
    print("agents:")
    for agent in architecture.agents:
        print(f"  - id: {agent.id}")
        print(f"    name: {agent.name}")
        print(f"    type: {agent.type}")
        print(f"    llm: {agent.llm_config.model}")
        print(f"    capabilities:")
        for cap in agent.capabilities:
            print(f"      - {cap}")
        print()


if __name__ == "__main__":
    main()
