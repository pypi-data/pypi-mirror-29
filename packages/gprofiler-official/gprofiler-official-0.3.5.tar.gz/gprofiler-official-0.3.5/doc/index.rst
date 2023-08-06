
g:Profiler Python package documentation
=======================================

This is the documentation for the official g:Profiler_ Python package_. The package contains both a
module for inclusion into a Python codebase and the ``gprofiler_cli.py`` command-line tool for querying
g:GOSt. Invocation of the latter is not documented here, but executing ``gprofiler_cli.py --help``
yields a manual.

Synopsis::

   from gprofiler import GProfiler
   gp = GProfiler("MyTool/0.1")
   gp.gprofile("sox2")

GProfiler class
---------------

.. autoclass:: gprofiler.GProfiler
   :members:

.. _g:Profiler: http://biit.cs.ut.ee/gprofiler
.. _package: https://pypi.python.org/pypi/gprofiler-official
