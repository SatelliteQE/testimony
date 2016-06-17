Testimony
=========

An approach to document test cases in the Python source code
------------------------------------------------------------

Are you tired of managing your test cases in a test case management tool and
your test code in a Python automation framework?  Testimony can help to use the
Python automation framework as a test case repository tool.

The project Testimony is written to inspect and report on the Python test
cases.  There are several reporting features in this program.

Testimony allows you configure a set of expected tokens in order to customize
the information you need to be present on every test, also it allows you to
configure the minimum set of tokens to be considered as a valid docstring.

Testimony comes with a default set of tokens: ``assert``, ``bz``, ``feature``,
``setup``, ``status``, ``steps``, ``tags``, ``test`` and ``type``. Also, it
comes with a default set of minimum tokens: ``assert``, ``feature`` and
``test``.

On a docstring, every token should be prefixed with ``@`` and suffixed with
``:``. This will ensure that Testimony parses the information and provide the
following reports:

1. print - will print out all captured test and will present all tokens parsed
   for each test. Also it will present of a non recognized tokens to help
   identifying some spell issues for example.
2. summary - as the name states, a summary of all tests will presented, you
   will be able to see how many tests is missing docstrings, how many tests
   each token was defined and the total number of test cases.
3. validate - validate report helps you ensure the minimal set of tokens are
   present on each test, a non-zero return code will be returned whenever the
   minimal docstring is not match, whenever a test is missing the docstring and
   whenever a unexpected token was found. In addition it will print all the
   issues found for each test and also a summary with how many tests have
   failed each of the checks.

Testimony can also print colored output, make sure ``termcolor`` package is
installed and the ``--no-color`` option was not specified.

Advantages
----------
1. Avoids a separate test case management tool to document test cases by using
   the Python automation framework for the same
2. Enforces test cases to follow a defined standard
3. Runs in integration with tools like Travis to get a report as and when you
   check in code
4. Saves a lot of time from the conventional way of writing test cases using a
   test management tool
5. The test case information can be easily extracted from Testimony and can be
   ported to any test management tool

Installation
------------

You can install Testimony from PyPI using pip::

    pip install testimony

Test lookup and definition
--------------------------

Testimony will capture every ``.py`` file found on the ``PATH`` argument which
can be specified multiple times. If the ``PATH`` is a directory, the directory
and its subdirectories will be searched for ``.py`` files. Worth mention that
only files that its filename starts with ``test_`` will be considered test
modules and will be captured.

Inside a test module, Testimony will look for functions or methods which names
start with ``test_`` in order to parse the docstring and extract the tokens
information. Also it will create some namespaces, the module as well as every
test case class docstrings will be parsed as well and it allows you define
tokens that will reused on children tests. For example, if a module have
defined the token ``feature`` then all tests will inherit it by default, but
tests can override that token by defining it on its docstring. The token lookup
will happen from the function or method, then the class and finally the module
and the lookup will end on the first match.

A sample docstring would be like the following::

    """My test description.

    More description for the test.

    @test: check if login works

    @feature: Login

    @setup: Navigate to abc.com

    @steps:

    1. Launch the url
    2. Log in with valid user credentials

    @assert: Log in successful

    @bz: 1234567

    @automated: false
    """

Considering that the above docstring was defined inside a module which path is
``tests/test_login.py`` a print report will output something like the
following::

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

Usage
-----

Make sure you have Testimony installed and run::

    testimony --help

Some basic usage::

    testimony print tests/

    testimony summary tests/

    testimony validate tests/

For further information about the options check Testimony's help.

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
