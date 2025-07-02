"""Setup scripts for the Crypto Price Prediction package"""

import setuptools  # It is used to make the need folders as modules and we can it in PyPI website too
from pathlib import Path

# Read README.md for long description when use this repo in PyPI
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

# Project metadata for PyPI package as detailed description
__version__ = "0.1.0"
REPO_NAME = "Crypto-Price-Prediction"
AUTHOR_USER_NAME = "satyanarayana8055"
SRC_REPO = "src"  # It creates inside the src folder egg data
AUTHOR_EMAIL = "muddalasatyanarayana96@gmail.com"

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as f:
    install_requires = f.read().splitlines()

# Packages data to include non-python files
# This code tell to PyPI to include non python files
package_data = {
    "cryptoPredictor": [
        "config/*.py",
        "app/templates/*.html",
        "app/static/css/*.css",
        "app/static/js/*.js",
    ],
    ".": ["config/*.yaml", "dags/*.py", "docker/*"],
}

# Setup configuration
setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="A Python package for real-time cryptocurrency price prediction using CoinGecko data",
    long_description=long_description,
    long_description_content_type="text/markdown",  # It helps your code to write in markdown language
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
        "Documentation": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/blob/main/README.md",
    },
    license="MIT",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src", include=["*", "app.*"]),
    package_data=package_data,
    include_package_data=True,
    install_requires=install_requires,
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "crypto-predictor=cryptoPredictor.main:main",
        ]
    },
    # This is describing you package by category and language and licence
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT license",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Financial:: Investment",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    # It make easy to make the discovery in the package with keywords
    keywords=[
        "cryptocurrency",
        "price-prediction",
        "machine-learning",
        "data-science",
        "coingecko",
        "etl",
        "airflow",
    ],
)
