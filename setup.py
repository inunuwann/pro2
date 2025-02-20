from setuptools import setup, find_packages

setup(
    name="koikoi_game",
    version="1.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "koikoi=main:main",
        ],
    },
)
