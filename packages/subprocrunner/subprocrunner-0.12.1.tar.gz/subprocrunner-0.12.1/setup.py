# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import unicode_literals

import os.path
import sys

import setuptools

MODULE_NAME = "subprocrunner"
REQUIREMENT_DIR = "requirements"

pkg_info = {}

with open(os.path.join(MODULE_NAME, "__version__.py")) as f:
    exec(f.read(), pkg_info)


class ReleaseCommand(setuptools.Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        tag = "v{}".format(pkg_info["__version__"])

        print("Pushing git tags: {}".format(tag))

        os.system("git tag {}".format(tag))
        os.system("git push --tags")


with open("README.rst") as fp:
    long_description = fp.read()

with open(os.path.join(REQUIREMENT_DIR, "requirements.txt")) as f:
    install_requires = [line.strip() for line in f if line.strip()]

with open(os.path.join(REQUIREMENT_DIR, "test_requirements.txt")) as f:
    tests_requires = [line.strip() for line in f if line.strip()]

with open(os.path.join(REQUIREMENT_DIR, "docs_requirements.txt")) as f:
    docs_requires = [line.strip() for line in f if line.strip()]

needs_pytest = set(["pytest", "test", "ptr"]).intersection(sys.argv)
pytest_runner = ["pytest-runner"] if needs_pytest else []

setuptools.setup(
    name=MODULE_NAME,
    version=pkg_info["__version__"],
    url="https://github.com/thombashi/{:s}".format(MODULE_NAME),

    author=pkg_info["__author__"],
    author_email=pkg_info["__email__"],
    description="A Python wrapper library for subprocess module.",
    include_package_data=True,
    keywords=["library", "subprocess"],
    license=pkg_info["__license__"],
    long_description=long_description,
    packages=setuptools.find_packages(exclude=["test*"]),

    install_requires=install_requires,
    setup_requires=pytest_runner,
    tests_require=tests_requires,
    extras_require={
        "test": tests_requires,
        "docs": docs_requires,
    },

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    cmdclass={
        "release": ReleaseCommand,
    })
