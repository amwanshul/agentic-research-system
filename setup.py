from setuptools import setup, find_packages

setup(
    name="agentic-research-system",
    version="0.1.0",
    description="Autonomous state-graph research agent with reflection loops and trajectory tracing",
    author="Anshul Wankhede",
    packages=find_packages(),
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "agentic-research=agentic_research.cli:main",
        ],
    },
)
