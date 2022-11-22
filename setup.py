from pathlib import Path

from setuptools import find_namespace_packages, setup

# Load packages from requirements.txt
BASE_DIR = Path(__file__).parent
with open(Path(BASE_DIR, "requirements.txt"), "r") as file:
    required_packages = [ln.strip() for ln in file.readlines()]

analysis_packes = ["jupyterlab==3.4.6"]
docs_packages = ["mkdocs==1.3.0", "mkdocstrings==0.18.1"]
# Define our package
setup(
    name="Car Price Prediction",
    version=1.0,
    description="",
    author="Mawada Sweis",
    author_email="mawada.sweis19@gmail.com",
    python_requires=">=3.7",
    packages=find_namespace_packages(),
    install_requires=[required_packages],
    extras_require={
        "dev": analysis_packes,
        "docs": docs_packages,
    },
)
