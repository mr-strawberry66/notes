"""Setup config for Notes CLI."""

from setuptools import setup

setup(
    py_modules=["notes"],
    install_requires=[
        "Click",
    ],
    entry_points={
        "console_scripts": [
            "notes = notes:cli",
        ],
    },
)
