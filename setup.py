"""Setup script for heron"""

import os.path

from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name="heron",
    version="0.0.1",
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
    packages=["heron"],
    python_requires=">=3.8.*",
    include_package_data=True,
    install_requires=["requests"],
)
