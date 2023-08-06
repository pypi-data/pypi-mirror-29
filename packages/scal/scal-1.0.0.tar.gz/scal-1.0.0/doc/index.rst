Welcome to `scal`'s documentation!
==================================

I use this program about once a year to print a one-page school-year
calendar. But it can be used to represent any calendar.

It is heavily inspired by the simple yet powerful Robert Krause's `calendar
<http://www.texample.net/tikz/examples/a-calender-for-doublesided-din-a4/>`_,
itself using the complex yet powerful Till Tantau's `TikZ
<http://www.ctan.org/pkg/pgf>`_ LaTeX package.

Examples:

- French school year:

  - 2017-2018:
    :download:`zone A <examples/fr_20172018_A.pdf>` (:download:`source <examples/fr_20172018_A.scl>`),
    :download:`zone B <examples/fr_20172018_B.pdf>` (:download:`source <examples/fr_20172018_B.scl>`),
    :download:`zone C <examples/fr_20172018_C.pdf>` (:download:`source <examples/fr_20172018_C.scl>`)

  - 2018-2019:
    :download:`zone A <examples/fr_20182019_A.pdf>` (:download:`source <examples/fr_20182019_A.scl>`),
    :download:`zone B <examples/fr_20182019_B.pdf>` (:download:`source <examples/fr_20182019_B.scl>`),
    :download:`zone C <examples/fr_20182019_C.pdf>` (:download:`source <examples/fr_20182019_C.scl>`)

Download and install
--------------------

See the `main project page <http://git.framasoft.org/spalax/scal>`_ for
instructions, and `changelog
<https://git.framasoft.org/spalax/scal/blob/master/CHANGELOG.md>`_.

Usage
-----

Here are the command line options for `scal`.

.. argparse::
    :module: scal.options
    :func: commandline_parser
    :prog: scal

Note that `scal` only produce the LuaLaTeX code corresponding to the calendar. To get the `pdf` calendar, save the code as a :file:`.tex` file, or pipe the output through `lualatex`:

.. code-block:: bash

    scal FILE | lualatex

Configuration file
------------------

The file given in argument contains the information about the calendar. Here
is, for example, the file corresponding to a school year calendar.

.. literalinclude:: examples/fr_20172018_B.scl

The file is parsed line per line, the following way.

- The ``#`` character starts a comment: it, and everything following it, are ignored.
- Blank lines are ignored.
- The date format is ``YYYY-MM-DD`` (or ``MM-DD`` in some cases).
- Start and end date of the calendar are set by a line ``From STARTDATE to ENDDATE``.
- The base command to define a holiday is ``STARTDATE ENDDATE NAME``, where ``STARTDATE`` and ``ENDDATE`` are the first and last days of the holiday, and ``NAME`` is the holiday name (as a LuaLaTeX code), to be displayed on the calendar.

  - ``NAME`` can be omitted;
  - ``STARTDATE`` can be omitted for a one-day vacation (e.g. ``2015-04-05 Easter``);
  - The year can be omitted if the vacation happens every year (e.g. ``05-01 Labour day``).

- Moreover, the following configuration variables can be set, as ``VARIABLE = VALUE``:

  - ``papersize``: Paper size (this string must be recognized by the `geometry <http://www.ctan.org/pkg/geometry>`_ LaTeX package).
  - ``lang``: Language of the calendar (this string must be recognized by the `babel <http://www.ctan.org/pkg/babel>`_ LaTeX package).

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
