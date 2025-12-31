"""
Example: Exporting Architectures

Shows how to export architectures to different formats.
"""

from basil import ArchitectureDesigner
from basil.utils.exporter import ArchitectureExporter


def main():
    # Create a simple architecture
    problem = """
    Build a task management API with user authentication,
    task CRUD operations, and email notifications.
    """

    designer = ArchitectureDesigner(cost_optimize=True)
    architecture = designer.design(problem)

    exporter = ArchitectureExporter()

    # Export to JSON
    print("=" * 80)
    print("JSON Export")
    print("=" * 80)
    print(exporter.to_json(architecture))
    print()

    # Export to YAML
    print("=" * 80)
    print("YAML Export")
    print("=" * 80)
    print(exporter.to_yaml(architecture))
    print()

    # Export to Mermaid
    print("=" * 80)
    print("Mermaid Diagram")
    print("=" * 80)
    print(exporter.to_mermaid(architecture))
    print()

    # Export to Markdown
    print("=" * 80)
    print("Markdown Documentation")
    print("=" * 80)
    print(exporter.to_markdown(architecture))

    # Save to files
    with open("architecture.json", "w") as f:
        f.write(exporter.to_json(architecture))

    with open("architecture.yaml", "w") as f:
        f.write(exporter.to_yaml(architecture))

    with open("architecture.md", "w") as f:
        f.write(exporter.to_markdown(architecture))

    with open("architecture.mmd", "w") as f:
        f.write(exporter.to_mermaid(architecture))

    print("\nFiles saved:")
    print("  - architecture.json")
    print("  - architecture.yaml")
    print("  - architecture.md")
    print("  - architecture.mmd")


if __name__ == "__main__":
    main()
