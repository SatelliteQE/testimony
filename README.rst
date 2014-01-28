testimony
=========
The project testimony is written to inspect and report on the python test cases.  There are several reporting features in this program.

The parameter options are:

* print - List all test cases
* summary - Summary of number of automated cases vs. manual cases
* validate_docstring - Validate docstrings
* bugs - Test cases affected by Bugs and the corresponding Bug list
* manual - List all manual test cases
* auto - List all auto test cases

Installation
------------

You could install testimony from PyPI using pip:

::

    pip install testimony

Requirements
------------
\1) Install testimony following the steps on the installation section

\2) Pre-requisites

Expected Docstring format:

::

    """
    @Feature: Login
    @Test: Log in as a valid user
    @Setup: Navigate to abc.com
    @Steps:
     1.  Launch the url
     2.  Log in with valid user credentials
    @Assert: Log in successful
    @BZ: #1234567
    @Status: Manual (REMOVE this field once automated)
    """

\3) Optional color formatting - If termcolor package is installed, output will be printed in colored text

Usage:
------

::

    $ testimony -h
    usage: testimony [-h] REPORT PATH [PATH ...]

    Inspects and report on the Python test cases.

    positional arguments:
    REPORT      report type, possible values: print, summary,
                validate_docstring, bugs, manual, auto
    PATH        a list of paths to look for tests cases

    optional arguments:
    -h, --help  show this help message and exit

::

    $ testimony print /home/apple/tests/login/

    TEST PATH: /home/apple/tests/login/
    ----------------------------------------------------------------
    Analysing test_sample.py...
    TC 1
    Feature: Login
    Test: Log in as a valid user
    Setup: Navigate to abc.com
    Steps:
     1.  Launch the url
     2.  Log in with valid user credentials
    Assert: Log in successful
    BZ: #1234567
    Status: Manual

::

    $ testimony summary /home/apple/tests/login/

    TEST PATH: /home/apple/tests/login/
    ----------------------------------------------------------------
    Total Number of test cases:      5
    Total Number of automated cases: 4
    Total Number of manual cases:    1
    Test cases with no docstrings:   0

::

    $ testimony validate_docstring /home/apple/test/login/

    TEST PATH: /home/apple/tests/login/
    ----------------------------------------------------------------
    Analyzing test_sample.py...
    -->Invalid DocString: Creates new user and delete it<--
    -->Invalid DocString: Create new user and update name<--
    -->Invalid DocString: Remove an user<--
    Total Number of invalid docstrings:  4

::

    $ testimony bugs /home/apple/tests/login/

    TEST PATH: /home/apple/tests/login/
    ----------------------------------------------------------------
    Analyzing test_sample.py...
    Total Number of test cases affected by bugs: 1
    List of bugs:                                ['#1234567']

::

    $ testimony manual /home/apple/tests/login/

    TEST PATH: /home/apple/tests/login/
    ----------------------------------------------------------------
    Analyzying test_sample.py
    Feature: Login
    Test: Log in as a valid user
    Setup: Navigate to abc.com
    Steps:
     1.  Launch the url
     2.  Log in with valid user credentials
    Assert: Log in successful
    BZ: #1234567
    Status: Manual (REMOVE this field once automated)

::

    $ testimony auto /home/apple/tests/login/

    TEST PATH: /home/apple/tests/login/
    ----------------------------------------------------------------
    Analyzying test_sample.py
    Feature: Login
    Test: Log in as an invalid user
    Setup: Navigate to abc.com
    Steps:
     1.  Launch the url
     2.  Log in with invalid user credentials
    Assert: Log in successful
    BZ: #1234567
    
::
	
	# Having termcolor installed, testimony produces colored output by default.  It can be disabled by:
    $ testimony auto /home/apple/tests/login/ --nocolor
    
    (or)
	
    $ testimony auto /home/apple/tests/login/ -n 


Known Issues
------------
None

Author
------

This software is developed by `Suresh Thirugn`_.

.. _Suresh Thirugn: https://github.com/sthirugn/
