PyTeCK
======

|DOI| |Build Status| |Build Status| |codecov| |Dependency Status| |Code
of Conduct| |License| |Anaconda|

This software package automatically evaluates the performance of a
chemical kinetic model using experimental data given in a specified YAML
format.

Installation
------------

The easiest way to install PyTeCK is via ``conda``. You can install to
your environment with

::

    > conda install -c kyleniemeyer pyteck

which will also handle all the dependencies. Alternatively, you can
install from PyPI with

::

    > pip install pyteck

If you prefer to install manually, or want a particular version outside
of the tagged releases distributed to those services, you can download
the source files from this repository, navigate to the directory, and
install using either ``setuptools``

::

    > python setup.py install

or ``pip``

::

    > pip install .

``pip`` is recommended due to its easy uninstall option
(``pip uninstall pyteck``).

Usage
-----

Once installed, the full list of options can be seen using ``pyteck -h``
or ``pyteck --help``.

Code of Conduct
---------------

In order to have a more open and welcoming community, PyTeCK adheres to
a code of conduct adapted from the `Contributor
Covenant <http://contributor-covenant.org>`__ code of conduct.

Please adhere to this code of conduct in any interactions you have in
the PyTeCK community. It is strictly enforced on all official PyTeCK
repositories, websites, and resources. If you encounter someone
violating these terms, please let
[@kyleniemeyer](https://github.com/kyleniemeyer) know via email at
kyle.niemeyer@gmail.com and we will address it as soon as possible.

Citation
--------

If you use this package as part of a scholarly publication, please refer
to
`CITATION.md <https://github.com/kyleniemeyer/PyTeCK/blob/master/CITATION.md>`__
for instructions on how to cite this resource directly.

License
-------

PyTeCK is released under the MIT license; see
`LICENSE <https://github.com/kyleniemeyer/PyTeCK/blob/master/LICENSE>`__
for details.

Change Log
==========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <http://keepachangelog.com/>`__
and this project adheres to `Semantic
Versioning <http://semver.org/>`__.

`Unreleased <https://github.com/kyleniemeyer/PyTeCK/compare/v0.2.3...HEAD>`__
-----------------------------------------------------------------------------

Added
~~~~~

Fixed
~~~~~

-  Fixed ability to handle ChemKED files with uncertainty for various
   properties.

Changed
~~~~~~~

`0.2.3 <https://github.com/kyleniemeyer/PyTeCK/compare/v0.2.2...0.2.3>`__ - 2018-02-07
--------------------------------------------------------------------------------------

Fixed
~~~~~

-  Standard deviation calculator now averages any duplicates to avoid an
   error.

`0.2.2 <https://github.com/kyleniemeyer/PyTeCK/compare/v0.2.1...0.2.2>`__ - 2017-09-02
--------------------------------------------------------------------------------------

Added
~~~~~

-  Adds DOI badge to README and CITATION
-  Adds AppVeyor build status badge to README
-  Adds restart option to skip existing results files.
-  Updates PyKED version requirement and adds optional validation
   skipping

Fixed
~~~~~

-  Fixes ignition delay detection for 1/2 max type (only one value
   possible, rather than list)
-  Fixes test for detecting peaks with min distance
-  Ensure time has units when 1/2 max target
-  Fixed handling of models with variants

Changed
~~~~~~~

-  Simulation input parameters now change units in place
-  Simulation input composition uses ChemKED Cantera functions

`0.2.1 <https://github.com/kyleniemeyer/PyTeCK/compare/v0.2.0...0.2.1>`__ - 2017-04-14
--------------------------------------------------------------------------------------

Added
~~~~~

-  Adds AppVeyor build for Windows conda packages
-  Adds CONTRIBUTING guide

`0.2.0 <https://github.com/kyleniemeyer/PyTeCK/compare/v0.1...0.2.0>`__ - 2017-04-13
------------------------------------------------------------------------------------

Added
~~~~~

-  Adds initial web documentation using Sphinx/Doctr
-  Deploys conda and PyPI packages with tagged releases

Changed
~~~~~~~

-  Major changes for compatibility with PyKED package and newer ChemKED
   format

`0.1.0 <https://github.com/kyleniemeyer/PyTeCK/compare/e99f757b7ea644065a0ee65ce86dbfb8f404be60...v0.1>`__ - 2016-07-12
-----------------------------------------------------------------------------------------------------------------------

Added
~~~~~

-  First published version of PyTeCK.
-  Supports validation using both shock tube and RCM experimental data
   in ChemKED format, but RCM not fully functional.

Citation of PyTeCK
==================

|DOI|

To cite PyTeCK in a scholarly article, please use

    K. E. Niemeyer. (2017) PyTeCK v0.2.1 [software]. Zenodo.
    https://doi.org/10.5281/zenodo.######

A BibTeX entry for LaTeX users is

.. code:: tex

    @misc{PyKED,
        author = {Kyle E Niemeyer},
        year = 2017,
        title = {PyTeCK v0.2.1},
        doi = {10.5281/zenodo.######},
        url = {https://github.com/kyleniemeyer/PyTeCK},
    }

In both cases, please update the entry with the version used. The DOI
for the latest version can be found in the badge at the top. If you
would like to cite a specific, older version, the DOIs for each release
are:

-  v0.2.1:
   `10.5281/zenodo.546270 <https://doi.org/10.5281/zenodo.546270>`__

.. |DOI| image:: https://zenodo.org/badge/53542212.svg
   :target: https://zenodo.org/badge/latestdoi/53542212
.. |Build Status| image:: https://travis-ci.org/kyleniemeyer/PyTeCK.svg?branch=master
   :target: https://travis-ci.org/kyleniemeyer/PyTeCK
.. |Build Status| image:: https://ci.appveyor.com/api/projects/status/a7a3prqgvfg8rr5f?svg=true
   :target: https://ci.appveyor.com/project/kyleniemeyer/pyteck
.. |codecov| image:: https://codecov.io/gh/kyleniemeyer/PyTeCK/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/kyleniemeyer/PyTeCK
.. |Dependency Status| image:: https://dependencyci.com/github/kyleniemeyer/PyTeCK/badge
   :target: https://dependencyci.com/github/kyleniemeyer/PyTeCK
.. |Code of Conduct| image:: https://img.shields.io/badge/code%20of%20conduct-contributor%20covenant-green.svg
   :target: http://contributor-covenant.org/version/1/4/
.. |License| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://opensource.org/licenses/MIT
.. |Anaconda| image:: https://anaconda.org/kyleniemeyer/pyteck/badges/version.svg
   :target: https://anaconda.org/kyleniemeyer/pyteck
