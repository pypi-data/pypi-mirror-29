-------------
bootstrap_env
-------------

Experimental project to create a complete self contained virtualenv bootstrap file.

See: `packaging-problems issues 55 <https://github.com/pypa/packaging-problems/issues/55>`_

Fork and contribute! ;)

Compatible Python Versions (see also `.travis.yml <https://github.com/jedie/bootstrap_env/blob/master/.travis.yml>`_):

* 3.5, 3.6

* PyPy (Python v2 and v3)

+--------------------------------------+---------------------------------------------------------+
| |Status on travis-ci.org|            | `travis-ci.org/jedie/bootstrap_env`_                    |
+--------------------------------------+---------------------------------------------------------+
| |Status on appveyor.com|             | `ci.appveyor.com/project/jedie/bootstrap-env`_          |
+--------------------------------------+---------------------------------------------------------+
| |Coverage Status on coveralls.io|    | `coveralls.io/r/jedie/bootstrap_env`_                   |
+--------------------------------------+---------------------------------------------------------+
| |Status on landscape.io|             | `landscape.io/github/jedie/bootstrap_env/master`_       |
+--------------------------------------+---------------------------------------------------------+
| |Requirements Status on requires.io| | `requires.io/github/jedie/bootstrap_env/requirements/`_ |
+--------------------------------------+---------------------------------------------------------+

.. |Status on travis-ci.org| image:: https://travis-ci.org/jedie/bootstrap_env.svg?branch=master
.. _travis-ci.org/jedie/bootstrap_env: https://travis-ci.org/jedie/bootstrap_env/
.. |Status on appveyor.com| image:: http://img.shields.io/appveyor/ci/jedie/bootstrap-env.svg?style=flat
.. _ci.appveyor.com/project/jedie/bootstrap-env: https://ci.appveyor.com/project/jedie/bootstrap-env/
.. |Coverage Status on coveralls.io| image:: https://coveralls.io/repos/jedie/bootstrap_env/badge.svg
.. _coveralls.io/r/jedie/bootstrap_env: https://coveralls.io/r/jedie/bootstrap_env
.. |Status on landscape.io| image:: https://landscape.io/github/jedie/bootstrap_env/master/landscape.svg
.. _landscape.io/github/jedie/bootstrap_env/master: https://landscape.io/github/jedie/bootstrap_env/master
.. |Requirements Status on requires.io| image:: https://requires.io/github/jedie/bootstrap_env/requirements.svg
.. _requires.io/github/jedie/bootstrap_env/requirements/: https://requires.io/github/jedie/bootstrap_env/requirements/

status
======

v1.0 is a rewrite and not useable, yet!

boot bootstrap_env
==================

::

    # Download bootstrap file from github:
    /home/FooBar$ wget https://github.com/jedie/bootstrap_env/raw/master/bootstrap_env/boot_bootstrap_env.py

    # Create virtualenv with all needed packages:
    /home/FooBar$ python3 boot_bootstrap_env.py boot ~/Bootstrap-env

------------
how it works
------------

bootstrap a project
===================

Bootstrap works in this way:

* create virtualenv

* pip install <project>

* <project>_admin update_env

-----------------------------
backward incompatible changes
-----------------------------

v0.6.4 -> v1.0.0
================

tbd

-----------------
Compatible Matrix
-----------------

+---------------+----------------------------------------+
| bootstrap_env | Python                                 |
+===============+========================================+
| >=v1.0        | 3.5, 3.6, PyPy3                        |
+---------------+----------------------------------------+
| <=v0.6        | 2.7, 3.4, 3.5, PyPy (Python v2 and v3) |
+---------------+----------------------------------------+

See also combinations in:

* `.travis.yml`_

* `tox.ini <https://github.com/jedie/bootstrap_env/blob/master/tox.ini>`_ (TODO)

* `appveyor.yml <https://github.com/jedie/bootstrap_env/blob/master/appveyor.yml>`_

-------
History
-------

* `compare v0.6.4...master <https://github.com/jedie/PyLucid/compare/v0.6.4...master>`_ **dev** 

    * rewrite based on "PyLucid v3 boot" sources (by Jens Diemer)

* `v0.6.4 <https://github.com/jedie/bootstrap_env/compare/v0.6.3...v0.6.4>`_ - 30.Nov.2016:

    * Note: This pip version doesn't support pypy3. See notes above

    * Update to `get-pip v9.0.1 <https://github.com/pypa/get-pip/commit/430ba37776ae2ad89f794c7a43b90dc23bac334c>`_

* `v0.6.3 <https://github.com/jedie/bootstrap_env/compare/v0.6.2...v0.6.3>`_ - 12.Sep.2016:

    * update for virtualenv v15.0.3

* `v0.6.2 <https://github.com/jedie/bootstrap_env/compare/v0.6.1...v0.6.2>`_ - 20.07.2016:

    * Update to `get-pip v8.1.2 <https://github.com/pypa/get-pip/commit/9b75908cb655a450b725e66e645765cac52ac228>`_

* `v0.6.1 <https://github.com/jedie/bootstrap_env/compare/v0.6.0...v0.6.1>`_ - 04.04.2016:

    * Update to `get-pip from 5.Mar.2016 <https://github.com/pypa/get-pip/commit/8481822bfacd435888cab6a0103fb041a2634bfb>`_

* `v0.6.0 <https://github.com/jedie/bootstrap_env/compare/v0.5.4...v0.6.0>`_ - 26.12.2015:

    * Remove old v0.4 API warnings

* `v0.5.4 <https://github.com/jedie/bootstrap_env/compare/v0.5.3...v0.5.4>`_ - 26.07.2015:

    * Bugfix for `PyPy2 under Windows <https://bitbucket.org/pypy/pypy/issues/2125/tcl-doesnt-work-inside-a-virtualenv-on#comment-21247266>`_ by a more flexible solution to find 'bin' and executeables.

* `v0.5.3 <https://github.com/jedie/bootstrap_env/compare/v0.5.2...v0.5.3>`_ - 24.07.2015 - update to pip 7.1.2

* `v0.5.2 <https://github.com/jedie/bootstrap_env/compare/v0.5.1...v0.5.2>`_ - 24.07.2015 - Made **add_extend_parser, add_adjust_options** and **add_after_install** optional in **generate_bootstrap()**

* `v0.5.1 <https://github.com/jedie/bootstrap_env/compare/v0.5.0...v0.5.1>`_ - 18.07.2015 - Update to pip 7.1.0

* `v0.5.0 <https://github.com/jedie/bootstrap_env/compare/v0.4.6...v0.5.0>`_ - 05.06.2015 - Add unittests, refactor sourcecode layout. (Please notice 'backward incompatible changes' above!)

* v0.4.6 - 03.06.2015 - Update to pip 7.0.3

* v0.4.5 - 26.05.2015 - Update to pip 7.0.1, cut filepath in generated boot file comments

* v0.4.4 - 14.04.2015 - Update to pip 6.1.1 (upload again as v0.4.4 with wheel, too.)

* v0.4.2 - 07.02.2015 - Update to pip 6.0.8

* v0.4.1 - 29.01.2015 - Update for pip 6.0.7 and pin requested url.

* v0.4.0 - 28.01.2015 - Updates for pip 6.0.6 changes

* v0.3.5 - 28.01.2015 - Update SHA256 for ``get-pip.py`` v6.0.6

* v0.3.4 - 14.11.2014 - Bugfix: if ``os.environ['SYSTEMROOT']`` not exists.

* v0.3.3 - 14.11.2014 - Add version number into generated bootstrap file.

* v0.3.2 - 14.11.2014 - Add 'boot bootstrap_env' and bugfixes for running under Windows.

* v0.3.1 - 14.11.2014 - Bugfix for "error: no such option:" while pip install, if own optional options are used.

* v0.3.0 - 13.11.2014 - typo: rename all ``bootstrip`` to ``bootstrap`` ;)

* v0.2.0 - 09.10.2014 - add ``prefix`` and ``suffix`` argument to ``generate_bootstrap()``

* v0.1.0 - 09.10.2014 - initial release

------
Links:
------

+--------+--------------------------------------------+
| PyPi   | `https://pypi.org/project/bootstrap_env/`_ |
+--------+--------------------------------------------+
| Github | `https://github.com/jedie/bootstrap_env`_  |
+--------+--------------------------------------------+

.. _https://pypi.org/project/bootstrap_env/: https://pypi.org/project/bootstrap_env/
.. _https://github.com/jedie/bootstrap_env: https://github.com/jedie/bootstrap_env

--------
donation
--------

* Send `Bitcoins <http://www.bitcoin.org/>`_ to `1823RZ5Md1Q2X5aSXRC5LRPcYdveCiVX6F <https://blockexplorer.com/address/1823RZ5Md1Q2X5aSXRC5LRPcYdveCiVX6F>`_

