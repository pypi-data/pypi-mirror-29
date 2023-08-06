import os

from pipenv.project import Project
from pipenv.utils import convert_deps_to_pip
from setuptools import setup


def requirements():
    pipfile = Project(chdir=False).parsed_pipfile
    return convert_deps_to_pip(pipfile['packages'], r=False)


def readme():
    with open("README.md") as f:
        return f.read()


def version():
    tag_version = os.getenv("CIRCLE_TAG")
    return tag_version if tag_version else "LOCAL"


setup(
    name="awsfunctions",
    version=version(),
    description=
    "A collection of high level AWS functions built on top of boto3",
    long_description=readme(),
    author="productml.com",
    author_email="info@productml.com",
    url="https://github.com/productml/awsfunctions",
    packages=['awsfunctions'],
    install_requires=requirements(),
    python_requires='>=3.6',
    classifiers=[
        "Development Status :: 4 - Beta",  # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
