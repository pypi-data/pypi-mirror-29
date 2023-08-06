
gprofiler-official
==================

The official Python 3 interface to the g:Profiler [1] toolkit for enrichment
analysis of functional (GO and other) terms, conversion between identifier
namespaces and mapping orhologous genes in related organisms. This library
provides both a command-line tool and a Python module. It is designed to be
lightweight and not require any 3rd party packages.

Besides this README, the API documentation is available [6].

Note that this used to be a Python 2 module. Since version 0.3, it has been
migrated to Python 3. Please use v0.2.3 [7] in case you require Python 2
support.

Installation on Linux using pip
-------------------------------

The pip tool [4] is the recommended method of installing Python packages.

Optionally create a virtual environment [2]::

$ virtualenv myenv
$ source myenv/bin/activate

Install the software with pip, see [3] for instructions::

$ pip install gprofiler-official

Make sure that the installed gprofiler_cli.py script is on your $PATH. When using
a virtual environment as shown above, this should happen automatically.

Run an example query::

$ gprofiler_cli.py -o scerevisiae "swi4 swi6"

For detailed usage instructions, see::

$ gprofiler_cli.py --help

To use the module in your codebase::

	from gprofiler import GProfiler
	gp = GProfiler("MyToolName/0.1")
	result = gp.gprofile("sox2")

For details, see the API documentation [6].

Installation on Linux using the tarball
---------------------------------------

You may simply download the tarball from gprofiler-official PyPI page [5],
extract it and use the gprofiler_cli.py script without installation. For detailed
usage instructions, see::

$ gprofiler_cli.py --help

You may run the test suite with::

$ python3 setup.py test

Installation on other platforms
-------------------------------

Please see [3] for package installation instructions on various platforms.

* [1] http://biit.cs.ut.ee/gprofiler
* [2] http://docs.python-guide.org/en/latest/dev/virtualenvs/
* [3] https://python-packaging-user-guide.readthedocs.io/tutorials/installing-packages/
* [4] https://pip.pypa.io/en/stable/
* [5] https://pypi.python.org/pypi/gprofiler-official
* [6] http://biit.cs.ut.ee/gprofiler_beta/doc/python/
* [7] https://pypi.python.org/pypi/gprofiler-official/0.2.3

