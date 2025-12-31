from setuptools import setup, find_packages

setup(
    name="basil",
    version="0.1.0",
    description="Multi-Agent Architecture Framework",
    author="Basil Team",
    packages=find_packages(),
    install_requires=[
        "pydantic>=2.0.0",
        "pyyaml>=6.0",
        "networkx>=3.0",
        "matplotlib>=3.7.0",
        "anthropic>=0.18.0",
        "openai>=1.0.0",
        "tiktoken>=0.5.0",
        "python-dotenv>=1.0.0",
        "jinja2>=3.1.0",
        "rich>=13.0.0",
    ],
    python_requires=">=3.9",
)
