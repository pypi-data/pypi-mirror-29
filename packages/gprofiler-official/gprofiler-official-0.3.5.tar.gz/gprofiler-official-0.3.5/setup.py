from distutils.core import setup
from distutils.cmd import Command

import subprocess
import sys
import re

from gprofiler_cli import VERSION

def readme():
    with open('README.txt') as f:
        return map_references(f.read())


def map_references(text):
    ids = []
    urls = []
    # find the reference definitions in the form
    # * [<id>] <url>
    for i in re.finditer('\*\s\[(?P<id>\d+)\]\s+(?P<url>.*)', text):
        ids.append(i.group('id'))
        urls.append(i.group('url'))

    assert len(set(ids)) == len(ids), "Id's for references must be unique. Got {ids}".format(ids=', '.join(ids))

    mapping = dict(zip(ids, urls))

    # replace the occurrences of [\d+] if they are not in the definition block
    result = (re.sub('(?<!\s\*\s)\[(\d+)\]', lambda match: '`[{result}] <{url}>`_'.format(
        result=match.groups()[0],
        url=mapping[match.groups()[0]]
    ), text))
    return result

def get_version():
    return VERSION

class TestCommand(Command):
    description = "Run the test suite."
    user_options = [
        ("tests=", None, "Specify the test IDs to run, comma-separated")
    ]

    def initialize_options(self):
        self.tests = None

    def finalize_options(self):
        pass

    def run(self):
        test_args = [sys.executable, '-m', 'gprofiler.test']
        
        if (self.tests):
            test_args.append("--tests=" + self.tests)
        raise SystemExit(subprocess.call(test_args))

setup(
    name = 'gprofiler-official',
    py_modules = ['gprofiler.gprofiler', 'gprofiler.paramtransform', 'gprofiler.test'],
    scripts = ['gprofiler_cli.py'],
    version = get_version(),
    description = 'Functional enrichment analysis and more via the g:Profiler toolkit',
    author = 'Tambet Arak',
    author_email = 'biit.support@lists.ut.ee',
    url = 'http://biit.cs.ut.ee/gprofiler',
    keywords = ['biology', 'bioinformatics', 'enrichment', 'gprofiler'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Bio-Informatics'
    ],
    cmdclass = {
        'test' : TestCommand
    },
    long_description = readme()
)
