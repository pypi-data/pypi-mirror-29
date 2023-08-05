# Copyright (C) Red Hat Inc.
#
# relvalconsumer is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author:   Adam Williamson <awilliam@redhat.com>

"""Setuptools script."""

import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

class PyTest(TestCommand):
    """Pytest integration."""
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ''
        self.test_suite = 'tests'

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args.split())
        sys.exit(errno)


# From: https://github.com/pypa/pypi-legacy/issues/148
# Produce rst-formatted long_description if pypandoc is available (to
# look nice on pypi), otherwise just use the Markdown-formatted one
try:
    import pypandoc
    longdesc = pypandoc.convert('README.md', 'rst')
except ImportError:
    longdesc = open('README.md').read()

setup(
    name="relvalconsumer",
    version="1.3.1",
    py_modules=['relvalconsumer'],
    entry_points={
        'moksha.consumer': (
            'relvalconsumer.prod = relvalconsumer:RelvalProductionConsumer',
            'relvalconsumer.test = relvalconsumer:RelvalTestConsumer',
        ),
    },
    author="Adam Williamson",
    author_email="awilliam@redhat.com",
    description=("Fedora QA wiki release validation event fedmsg consumer"),
    license="GPLv3+",
    keywords="fedora qa mediawiki validation",
    url="https://pagure.io/fedora-qa/relvalconsumer",
    install_requires=open('install.requires').read().splitlines(),
    tests_require=open('tests.requires').read().splitlines(),
    cmdclass={'test': PyTest},
    long_description=longdesc,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 or later "
        "(GPLv3+)",
    ],
)

# vim: set textwidth=120 ts=8 et sw=4:
