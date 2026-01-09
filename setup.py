"""Setup script for ServiceNow MCP Server."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="servicenow-mcp",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="MCP Server for ServiceNow with MFA support and session caching",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/servicenow-mcp",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "PyYAML>=6.0.1",
        "mcp>=0.9.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "mypy>=1.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "sn-connect=servicenow_mcp.cli.sn_connect:main",
            "servicenow-mcp=servicenow_mcp.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "servicenow_mcp": ["py.typed"],
    },
)
