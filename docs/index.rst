Testimony
=========

An approach to document test cases in the Python source code
------------------------------------------------------------

Are you tired of managing your test cases in a test case management tool and
your test code in a Python automation framework?  Testimony can help you to use
your Python automation framework as a test case repository tool.

The project Testimony is written to inspect and report on the Python test
cases.  There are several reporting features in this program.

Testimony allows you to configure:

1. tokens - Allowed values to be used as docstring items in your tests.  Default
   tokens are ``assert``, ``bz``, ``feature``, ``setup``, ``status``, ``steps``,
   ``tags``, ``test`` and ``type``.
2. minimum-tokens - minimum set of tokens that are needed for each of your
   tests.  Default minimum tokens are ``assert``, ``feature`` and ``test``.

In a test case docstring, every token should be prefixed with ``@`` and
suffixed with ``:``. This will ensure that Testimony provides right reports.
The reports supported by testimony are:

1. print - prints all captured tests with the parsed tokens for each test. Also
   it prints non-recognized tokens.
2. summary - presents a summary of all tests with useful information like:
   number of tests missing docstring, number of tests corresponding to each
   defined token, and total number of test cases.
3. validate - helps ensure that all your tests atleast have the minimal set
   of tokens defined.  The information presented by this command will help you
   identify the issues pertaining to each test.  A non-zero return code will be
   returned when:

     - minimal set of tokens is not present for atleast 1 test case
     - one or more tests is missing the docstring
     - An unexpected token identified

Advantages
----------
1. Avoids using a test case management tool to document test cases by reusing
   the Python automation framework.
2. Enforces test cases to follow a defined standard.
3. Runs in integration with tools like Travis to get a report as and when you
   check in the code.
4. Saves a lot of time from the conventional way of writing test cases using a
   test management tool.
5. The test case information can be easily extracted from Testimony and can be
   ported to any test management tool.

Test lookup and definition
--------------------------

The ``PATH`` argument of testimony accepts more than one value.  Testimony
captures all python test modules (``.py`` files whose names start with
``test_``) in the given paths. If ``PATH`` is a directory, then the directory
and its subdirectories will be considered as well.

Inside a test module, Testimony looks for functions whose names start with
``test_``.  It then parses the function docstrings and extracts the tokens.
Also it creates namespaces for module and class level docstrings which will
then be reused in the children tests. For example, if a module has a token
called ``feature``, then all tests in that module will inherit it by default.
But the individual tests can choose to override this value by defining their
own.  The token lookup will happen in the following order and it will stop on
the very first match::

 1. function level
 2. class level
 3. module level

A sample docstring will look like the following::

    """Test to check log in as a valid user

    More description for the test.

    @feature: Login

    @setup: Navigate to abc.com

    @steps:

    1. Launch the url
    2. Log in with valid user credentials

    @assert: Log in successful

    @bz: 1234567

    @automated: false
    """

Considering that the above docstring was defined on a test in a module
``tests/test_login.py``, a print report will output something like::

    tests/test_login.py
    ===================

    TC 1
    Assert: Log in successful
    Automated: false
    Bz: 1234567
    Feature: Login
    Setup: Navigate to abc.com
    Steps: 1. Launch the url
    2. Log in with valid user credentials
    Test: check if login works

Installation
------------

You can install Testimony from PyPI using pip::

    pip install testimony

Usage
-----

The help command can be used to learn about different available options::

    testimony --help

Some basic usage::

    testimony print tests/

    testimony summary tests/

    testimony validate tests/

Misc:

1. a json output is provided when ``--json`` option is specified.
2. a colored output is provided when ``termcolor`` package is installed. This
   can be disabled by specifying ``--no-color`` option.

Contribute
----------

1. Fork the repository on GitHub and make your changes
2. Test your changes
3. Send a pull request
4. Watch for the Travis update on the PR as it runs flake8
5. The PR will be merged after 2 ACKs

Author
------

This software is developed by `Suresh Thirugn`_.

.. _Suresh Thirugn: https://github.com/sthirugn/

Contributors
------------
| `Og Maciel <https://github.com/omaciel/>`_
| `Corey Welton <https://github.com/cswiii/>`_
| `Elyézer Rezende <https://github.com/elyezer/>`_
