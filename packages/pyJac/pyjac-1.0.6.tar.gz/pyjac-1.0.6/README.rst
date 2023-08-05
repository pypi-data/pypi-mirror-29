pyJac
=====

|DOI| |Code of Conduct| |License| |PyPI| |Anaconda|

This utility creates source code to calculate the Jacobian matrix
analytically for a chemical reaction mechanism.

Documentation
-------------

The full documentation for pyJac can be found at
http://slackha.github.io/pyJac/.

User Group
----------

Further support can be found at our `user
group <https://groups.io/g/slackha-users>`__, or by `opening an
issue <https://github.com/SLACKHA/pyJac/issues>`__ on our github repo.

Installation
------------

Detailed installation instructions can be found in the `full
documentation <http://slackha.github.io/pyJac/>`__. The easiest way to
install pyJac is via ``conda``. You can install to your environment with

::

    > conda install -c slackha pyjac

pyJac can also be installed from PyPI using pip:

::

    pip install pyjac

or, using the downloaded source code, installed as a Python module:

::

    > python setup.py install

Usage
-----

pyJac can be run as a python module:

::

    > python -m pyjac [options]

The generated source code is placed within the ``out`` (by default)
directory, which is created if it doesn't exist initially. See the
documentation or use ``python pyjac -h`` for the full list of options.

Theory
------

Theory, derivations, validation and performance testing can be found in
the paper fully describing version 1.0.2 of pyJac:
https://niemeyer-research-group.github.io/pyJac-paper/, now published
via https://doi.org/10.1016/j.cpc.2017.02.004 and available openly via
```arXiv:1605.03262 [physics.comp-ph]`` <https://arxiv.org/abs/1605.03262>`__.

License
-------

pyJac is released under the MIT license; see the
`LICENSE <https://github.com/slackha/pyJac/blob/master/LICENSE>`__ for
details.

If you use this package as part of a scholarly publication, please see
`CITATION.md <https://github.com/slackha/pyJac/blob/master/CITATION.md>`__
for the appropriate citation(s).

Contributing
------------

We welcome contributions to pyJac! Please see the guide to making
contributions in the
`CONTRIBUTING.md <https://github.com/slackha/pyJac/blob/master/CONTRIBUTING.md>`__
file.

Code of Conduct
---------------

In order to have a more open and welcoming community, pyJac adheres to a
code of conduct adapted from the `Contributor
Covenant <http://contributor-covenant.org>`__ code of conduct.

Please adhere to this code of conduct in any interactions you have in
the pyJac community. It is strictly enforced on all official pyJac
repositories, websites, and resources. If you encounter someone
violating these terms, please let a maintainer
([@kyleniemeyer](https://github.com/kyleniemeyer) or
[@arghdos](https://github.com/arghdos), via email at
slackha@googlegroups.com) know and we will address it as soon as
possible.

Authors
-------

Created by `Kyle Niemeyer <http://kyleniemeyer.com>`__
(kyle.niemeyer@gmail.com) and Nicholas Curtis (arghdos@gmail.com)

Change Log
==========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <http://keepachangelog.com/>`__
and this project adheres to `Semantic
Versioning <http://semver.org/>`__.

[1.0.6] - 2018-02-21
--------------------

Added
~~~~~

-  DOI for 1.0.4

Fixed
~~~~~

-  Syntax errors in readme.md
-  Conda install instructions in install.md
-  Corrected TRange columns in parser
-  Minor documentation fixes

Added
~~~~~

-  Add check to reactions to test that all species exist
-  Duplicate warning from falloff->chemically-activated TROE reactions
   for zero-parameters
-  Add handling of non-unity default third body efficiency

Changed
~~~~~~~

-  Bump internal version to 1.0.5.c

[1.0.5.b0] - 2017-06-02
-----------------------

Added
~~~~~

-  Added usergroup info to README and documentation

Fixed
~~~~~

Changed
~~~~~~~

-  Now strip whitespace from mechanism file lines prior to parsing
   keywords

Removed
~~~~~~~

-  Removed plotting scripts specific to first paper on pyJac

`1.0.4 <https://github.com/slackha/pyJac/compare/v1.0.3...v1.0.4>`__ - 2017-04-18
---------------------------------------------------------------------------------

Added
~~~~~

-  Adds Travis config for automatic PyPI and conda builds
-  Adds minimal unittest test suite for module imports
-  Adds code of conduct

Changed
~~~~~~~

-  Changed README back to Markdown for simplicity
-  Updated citation instructions

`1.0.3 <https://github.com/slackha/pyJac/compare/v1.0.2...v1.0.3>`__ - 2017-04-01
---------------------------------------------------------------------------------

Fixed
~~~~~

-  Fix for SRI Falloff functions with non-default third bodies (`issue
   #12 <https://github.com/SLACKHA/pyJac/issues/12>`__)
-  Fixed removal of jac/rate lists before libgen of functional\_tester
-  Fixed pywrap module import

Changed
~~~~~~~

-  Issue warning in Cantera parsing if the installed version doesn't
   have access to species thermo properties.

Added
~~~~~

-  Added significantly more documentation and examples for data
   ordering, the state vector / Jacobian, and using the python interface

`1.0.2 <https://github.com/slackha/pyJac/compare/v1.0.1...v1.0.2>`__ - 2017-01-18
---------------------------------------------------------------------------------

Added
~~~~~

-  Added CHANGELOG
-  Added documentation for libgen / pywrap features

Changed
~~~~~~~

-  Minor compilation fixes for including OpenMP
-  Updated github links to point to SLACKHA / Niemeyer Research Group

Deprecated
~~~~~~~~~~

-  Shared library creation for CUDA disabled, as CUDA does not allow
   linkage of SO's into another CUDA kernel

Fixed
~~~~~

-  Explicitly conserve mass in PaSR
-  Minor path fixes
-  Division by zero in some TROE parameter cases

`1.0.1 <https://github.com/slackha/pyJac/compare/v1.0...v1.0.1>`__ - 2016-05-25
-------------------------------------------------------------------------------

Added
~~~~~

-  Added GPU macros, e.g., THREAD\_ID, GRID\_SIZE

Changed
~~~~~~~

-  Much better handling of removal of files created during testing

Fixed
~~~~~

-  Bugfix that generates data.bin files correctly from .npy files for
   performance testing (**important**)
-  Explicit setting of OpenMP # threads for performance testing

`1.0 <https://github.com/slackha/pyJac/compare/v0.9.1-beta...v1.0>`__ - 2016-05-07
----------------------------------------------------------------------------------

Added
~~~~~

-  pyJac is now a Python package
-  pyJac can now create a static/shared library for a mechanism (for
   external linkage)
-  Added documentation
-  Added examples

Changed
~~~~~~~

-  Handles CUDA compilation better via Cython
-  pointers are now restricted where appropriate
-  better Python3 compatibility

Fixed
~~~~~

-  other minor bugfixes

`0.9.1-beta <https://github.com/slackha/pyJac/compare/v0.9-beta...v0.9.1-beta>`__ - 2015-10-29
----------------------------------------------------------------------------------------------

Changed
~~~~~~~

-  Implemented the strict mass conservation formulation
-  Updated CUDA implementation such that it is testable vs. pyJac
   c-version (and Cantera where applicable)
-  More robust build folder management
-  More robust mapping for strict mass conservation

0.9-beta - 2015-10-02
---------------------

Added
~~~~~

-  First working / tested version of pyJac

Citation of pyJac
=================

|DOI|

If you use pyJac in a scholarly article, please cite it directly as

    Kyle E. Niemeyer and Nicholas J. Curtis (2017). pyJac v1.0.4
    [Software]. Zenodo.
    `https://doi.org/10.5281/zenodo.###### <https://doi.org/10.5281/zenodo.######>`__

A BibTeX entry for LaTeX users is

BibTeX entry:
-------------

.. code:: tex

    @misc{pyJac,
        author = {Kyle E Niemeyer and Nicholas J Curtis},
        year = 2017,
        title = {{pyJac} v1.0.4},
        doi = {10.5281/zenodo.######},
        url = {https://github.com/slackha/pyJac},
    }

In both cases, please update the entry with the version used. The DOI
for the latest version can be found in the badge at the top. If you
would like to cite a specific, older version, the DOIs for each release
are:

-  v1.0.4:
   `10.5281/zenodo.555950 <https://doi.org/10.5281/zenodo.555950>`__
-  v1.0.3:
   `10.5281/zenodo.439682 <https://doi.org/10.5281/zenodo.439682>`__
-  v1.0.2:
   `10.5281/zenodo.251144 <https://doi.org/10.5281/zenodo.251144>`__

.. |DOI| image:: https://zenodo.org/badge/19829533.svg
   :target: https://zenodo.org/badge/latestdoi/19829533
.. |Code of Conduct| image:: https://img.shields.io/badge/code%20of%20conduct-contributor%20covenant-green.svg
   :target: http://contributor-covenant.org/version/1/4/
.. |License| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://opensource.org/licenses/MIT
.. |PyPI| image:: https://badge.fury.io/py/pyJac.svg
   :target: https://badge.fury.io/py/pyJac
.. |Anaconda| image:: https://anaconda.org/slackha/pyjac/badges/version.svg
   :target: https://anaconda.org/slackha/pyjac
