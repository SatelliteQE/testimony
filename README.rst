testimony
=========
Are you tired of managing your test cases in a test case management tool and your test code in a python automation framework?  Testimony can help to use the python automation framework as a test case repository tool.

The project testimony is written to inspect and report on the python test cases.  There are several reporting features in this program.

The parameter options are:

1. print - List all test cases
2. summary - Summary of number of automated cases vs. manual cases
3. validate_docstring - Validate docstrings
..
 	a. Reports test cases with invalid docstrings
 	b. Reports test cases with missing docstrings
 	c. Reports test cases that does not have minimal required docstrings (This will enforce that all test cases have a minimal set of docstrings). Currently testimony enforces Feature, Test, Assert as mandatory docstrings for each test case
4. bugs - Test cases affected by Bugs and the corresponding Bug list
5. manual - List all manual test cases
6. auto - List all auto test cases

Note:
- testimony returns a non-zero error code when the test case docstrings does not follow the intended rules, returns zero otherwise
- testimony also parses different folders under the given folder to verify the test files
- testimony also displays optional colored outputs when termcolor is installed

Advantages
----------
1. Avoids a separate test case management tool to document test cases by using the python automation framework for the same
2. Enforces test cases to follow a defined standard
3. Runs in integration with tools like Travis to get a report as and when you check in code
4. Saves a lot of time from the conventional way of writing test cases using a test management tool

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
    usage: testimony [-h] [-n] REPORT PATH [PATH ...]

    Inspects and report on the Python test cases.

    positional arguments:
      REPORT       report type, possible values: print, summary,
                 validate_docstring, bugs, manual, auto
      PATH         a list of paths to look for tests cases

    optional arguments:
      -h, --help     show this help message and exit
      -n, --nocolor  Do not use color option


::

    $ testimony print /home/testimony/tests/
    
    Fetching Test Path /home/testimony/tests/
 
    Scanning test_sample.py...
 
    TC 1
    Feture: Login - Positive
    Test: Login with right credentials
    Steps:
        1. Login to the application with valid credentials
    Assert: Login is successful
    Bug: 123456
    Statues: Manual
 
    TC 2
    test_positive_login_2: Docstring missing. Please update.
 
    TC 3
    Feature: Login - Positive
    Test: Login with Latin credentials
    Steps:
        1. Login to the application with valid Latin credentials
    Assert: Login is successful
 
    TC 4
    Feature: Login - Positive
    Test: Login with Credentials having special characters
    Steps:
        1. Login to the application with valid credentials having
        special characters
    Assert: Activation key is created
    Status: Manual
 
    TC 5
    Steps:
        1. Login to the application with invalid credentials
    BZ: 123456
    Status: Manual
 
    $ echo $?
    255
    

::

    $ testimony summary /home/testimony/tests/
 
    Fetching Test Path /home/testimony/tests/
 
    Total Number of test cases:      4
    Total Number of automated cases: 2
    Total Number of manual cases:    2
    Test cases with no docstrings:   1
 
 
    $ echo $?
    255

::

    $ testimony validate_docstring /home/testimony/tests/
 
    Fetching Test Path /home/testimony/tests/
 
    Scanning test_sample.py...
    test_positive_login_1: Invalid DocString: Feture: Login - Positive
    test_positive_login_1: Invalid DocString: Bug: 123456
    test_positive_login_1: Invalid DocString: Statues: Manual
    test_positive_login_1: Need feature, test and assert at the minimum
    test_positive_login_2: Docstring missing. Please update.
    test_negative_login_5: Need feature, test and assert at the minimum
    Total Number of invalid docstrings:  3
    Test cases with no docstrings:   1
    Test cases missing minimal docstrings:  2
 
    $ echo $?
    255

::

    $ testimony bugs /home/testimony/tests/
 
    Fetching Test Path /home/estimony/tests/
 
    Scanning test_sample.py...
 
    Total Number of test cases affected by bugs: 1
 
    Bug list:
    123456
 
    $ echo $?
    255

::

     $ testimony manual /home/testimony/tests/
 
    Fetching Test Path /home/estimony/tests/
 
    Scanning test_sample.py...
    Feature: Login - Positive
    Test: Login with Credentials having special characters
    Steps:
        1. Login to the application with valid credentials having
        special characters
    Assert: Activation key is created
    Status: Manual
    Steps:
        1. Login to the application with invalid credentials
    BZ: 123456
    Status: Manual
 
    $ echo $?
    255

::

    $ testimony auto /home/testimony/tests/
 
    Fetching Test Path /home/estimony/tests/
 
    Scanning test_sample.py...
    Feture: Login - Positive
    Test: Login with right credentials
    Steps:
        1. Login to the application with valid credentials
    Assert: Login is successful
    Bug: 123456
    Statues: Manual
    Feature: Login - Positive
    Test: Login with Latin credentials
    Steps:
        1. Login to the application with valid Latin credentials
    Assert: Login is successful
 
    $ echo $?
    255


Success scenario in which testimony returns 0

::
 
    $ testimony validate_docstring /home/tests/ui/sample/
 
	Fetching Test Path home/tests/ui/sample/
 
	Scanning test_activationkey.py...
	Total Number of invalid docstrings:  0
	Test cases with no docstrings:   0
	Test cases missing minimal docstrings:  0
 
	$ echo $?
	0

 
Having termcolor installed, testimony produces colored output by default.  It can be disabled by:

::

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

Contributors
------------
- 'Og Maciel <https://github.com/omaciel/>'_
- 'Corey Welton <https://github.com/cswiii/>'_
- 'Elyézer Rezende <https://github.com/elyezer/>'_

`Python home page <http://www.python.org>`_