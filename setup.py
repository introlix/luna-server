from setuptools import setup
import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="luna-server",
    version="0.0.1",
    author="Introlix Team",
    author_email="introlixai@gmail.com",
    description="Luna-Server is a python package to run LLM on Fastapi Server locally.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires=">=3.10",
)