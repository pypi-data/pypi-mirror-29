from __future__ import print_function

import re
import sys

import pkg_resources
from puck.backend import pypi_backend


"""Logic related to parsing requirements text files and setup.py files for
pinned versions of the form `abc===1.2.3`"""


def parse_requirement(line, source, backend=pypi_backend):
    """
    Parses a given line as a valid requirements line in the form `abc==1.2.3`
    and returns a dict with information.

    @param line: str containing a valid requirements line
    @param source: str representing from which file this line was taken
    @param backend: backend function to use to fetch information
    """
    try:
        r = pkg_resources.Requirement.parse(line)
        if '==' in line:
            current_version = line.split('==', 1)[-1]
            latest = backend(r.name)
            return {
                'name': r.name,
                'pinned_version': current_version.strip(),
                'latest_version': latest,
                'source': source,
            }
    except Exception:
        print("Error while parsing or retrieving the latest version for:", line, file=sys.stderr)  # noqa
        return None


def parse_requirements_file(requirements_file, backend=pypi_backend):
    """Parses a requirements.txt type file"""
    results = []
    with open(requirements_file, 'r') as rfile:
        for line in rfile.readlines():
            res = parse_requirement(
                line.strip(),
                requirements_file,
                backend=backend,
            )
            if res:
                results.append(res)
    return results


def parse_setup_py(setup_py, backend=pypi_backend):
    """Parses a setup.py file"""
    results = []
    with open(setup_py, 'r') as sfile:
        for line in sfile.readlines():
            req = re.search('[\w\-\_]+==[\w\.]+', line.strip())
            if req:
                requirement = req.group()
                res = parse_requirement(
                    requirement,
                    setup_py,
                    backend=backend,
                )
                if res:
                    results.append(res)
    return results
