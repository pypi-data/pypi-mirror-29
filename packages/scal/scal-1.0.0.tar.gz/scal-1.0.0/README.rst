scal 📅 School year calendar generator
======================================

|sources| |pypi| |build| |coverage| |documentation| |license|

I use this program about once a year to print a one-page school-year
calendar. But it can be used to represent any calendar.

It is heavily inspired by the simple yet powerful Robert Krause's `calendar <http://www.texample.net/tikz/examples/a-calender-for-doublesided-din-a4/>`_, itself using the complex yet powerful Till Tantau's `TikZ <http://www.ctan.org/pkg/pgf>`_ LaTeX package.

Examples:

- French school year:

  - 2017-2018:
    `zone A <http://scal.readthedocs.io/en/latest/_downloads/fr_20172018_A.pdf>`__ (`source <http://scal.readthedocs.io/en/latest/_downloads/fr_20172018_A.scl>`__),
    `zone B <http://scal.readthedocs.io/en/latest/_downloads/fr_20172018_B.pdf>`__ (`source <http://scal.readthedocs.io/en/latest/_downloads/fr_20172018_B.scl>`__),
    `zone C <http://scal.readthedocs.io/en/latest/_downloads/fr_20172018_C.pdf>`__ (`source <http://scal.readthedocs.io/en/latest/_downloads/fr_20172018_C.scl>`__)

  - 2018-2019:
    `zone A <http://scal.readthedocs.io/en/latest/_downloads/fr_20182019_A.pdf>`__ (`source <http://scal.readthedocs.io/en/latest/_downloads/fr_20182019_A.scl>`__),
    `zone B <http://scal.readthedocs.io/en/latest/_downloads/fr_20182019_B.pdf>`__ (`source <http://scal.readthedocs.io/en/latest/_downloads/fr_20182019_B.scl>`__),
    `zone C <http://scal.readthedocs.io/en/latest/_downloads/fr_20182019_C.pdf>`__ (`source <http://scal.readthedocs.io/en/latest/_downloads/fr_20182019_C.scl>`__)

What's new?
-----------

See `changelog <https://git.framasoft.org/spalax/scal/blob/master/CHANGELOG.md>`_.

Download and install
--------------------

See the end of list for a (quick and dirty) Debian package.

* Non-Python dependencies.
  This program produces LuaLaTeX code, but does not compile it. So, LaTeX is not
  needed to run this program. However, to compile the generated code, you will
  need a working LaTeX installation, with ``lualatex``, and LuaLaTeX packages
  `geometry <http://www.ctan.org/pkg/geometry>`_,
  `babel <http://www.ctan.org/pkg/babel>`_,
  `tikz <http://www.ctan.org/pkg/pgf>`_,
  `fontspec <http://www.ctan.org/pkg/fontspec>`_,
  and `translator` (provided by the `beamer <http://www.ctan.org/pkg/beamer>`_ package).
  Those are provided by `TeXLive <https://www.tug.org/texlive/>`_ on GNU/Linux, `MiKTeX <http://miktex.org/>`_ on Windows, and `MacTeX <https://tug.org/mactex/>`_ on MacOS.

* From sources:

  * Download: https://pypi.python.org/pypi/scal
  * Install (in a `virtualenv`, if you do not want to mess with your distribution installation system)::

        python3 setup.py install

* From pip::

    pip install scal

* Quick and dirty Debian (and Ubuntu?) package

  This requires `stdeb <https://github.com/astraw/stdeb>`_ to be installed::

      python3 setup.py --command-packages=stdeb.command bdist_deb
      sudo dpkg -i deb_dist/scal-<VERSION>_all.deb

Documentation
-------------

* The compiled documentation is available on `readthedocs <http://scal.readthedocs.io>`_

* To compile it from source, download and run::

      cd doc && make html


.. |documentation| image:: http://readthedocs.org/projects/scal/badge
  :target: http://scal.readthedocs.io
.. |pypi| image:: https://img.shields.io/pypi/v/scal.svg
  :target: http://pypi.python.org/pypi/scal
.. |license| image:: https://img.shields.io/pypi/l/scal.svg
  :target: http://www.gnu.org/licenses/gpl-3.0.html
.. |sources| image:: https://img.shields.io/badge/sources-scal-brightgreen.svg
  :target: http://git.framasoft.org/spalax/scal
.. |coverage| image:: https://git.framasoft.org/spalax/scal/badges/master/coverage.svg
  :target: https://git.framasoft.org/spalax/scal/builds
.. |build| image:: https://git.framasoft.org/spalax/scal/badges/master/build.svg
  :target: https://git.framasoft.org/spalax/scal/builds

