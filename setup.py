from setuptools import setup, find_packages

setup(
    name='Pyatus',
    version='1.0.0',
    install_requires=[
        "pyspellchecker",
        "openpyxl",
        "XlsxWriter",
        "pandas"
    ],
    entry_points={
        "console_scripts": [
            "sample=sample:main",
        ],
    },
    author="ahanba",
    description="A translation QA tool",
    url="https://github.com/ahanba/pyatus",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)