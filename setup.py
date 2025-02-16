from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name='Pyatus',
    version='1.0.1',
    install_requires=[
        "pyspellchecker",
        "openpyxl",
        "XlsxWriter",
        "pandas",
        "PyYAML"
    ],
    entry_points={
        "console_scripts": [
            "sample=sample:main",
        ],
    },
    author="Ayumu Hanba",
    description="Pyatus is another localization QA tool.",
    long_description=long_description,
    long_description_content_type="text/markdown", 
    url="https://github.com/ahanba/pyatus",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)