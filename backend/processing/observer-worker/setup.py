import os
import pathlib
import re
from io import open

from setuptools import find_packages, setup


def parse_requirements(filename):
    with open(filename) as file:
        lines = file.read().splitlines()

    return [
        line.strip()
        for line in lines
        if not (
            (not line)
            or (line.strip()[0] == "#")
            or (line.strip().startswith("--find-links"))
            or ("git+https" in line)
        )
    ]


def get_dependency_links(filename):
    with open(filename) as file:
        lines = file.read().splitlines()

    return [
        line.strip().split(" ")[1]
        for line in lines
        if line.strip().startswith("--find-links")
    ]


def version_from_file(*filepath):
    infile = os.path.join(*filepath)
    with open(infile) as fp:
        version_match = re.search(
            r"^__version__\s*=\s*['\"]([^'\"]*)['\"]", fp.read(), re.M
        )
        if version_match:
            return version_match.group(1)
        raise RuntimeError("Unable to find version string in {}.".format(infile))


here = os.path.abspath(os.path.dirname(__file__))

dependency_links = get_dependency_links("requirements.txt")
parsed_requirements = parse_requirements("requirements.txt")

# The directory containing this file
HERE = pathlib.Path(__file__).parent


setup(
    name="observer",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    dependency_links=dependency_links,
    install_requires=parsed_requirements,
    include_package_data=True,
    python_requires=">=3.7.0",
)
