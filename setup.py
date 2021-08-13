"""Setup script for heron"""

import os.path

from setuptools import find_packages, setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name="heron-data",
    version="0.0.2",
    description="A client for the Heron Data API",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/heron-data/client-python",
    author="Heron Data",
    author_email="help@herondata.io",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(exclude=["tests", "examples", "tests.*"]),
    python_requires=">=3.8.*",
    include_package_data=True,
    install_requires=["requests==2.26.0"],
)
