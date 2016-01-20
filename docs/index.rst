testimony
=========
An approach to document test cases in the python source code
------------------------------------------------------------

Are you tired of managing your test cases in a test case management tool and your test code in a python automation framework?  Testimony can help to use the python automation framework as a test case repository tool.

The project testimony is written to inspect and report on the python test cases.  There are several reporting features in this program.

The parameter options are:

1. print - List all test cases
2. summary - Summary of number of automated cases vs. manual cases
3. validate_docstring - Validate docstrings. This does the following:s

- Reports test cases with invalid docstrings
- Reports test cases with missing docstrings
- Reports test cases that does not have minimal required docstrings (This will enforce that all test cases have a minimal set of docstrings). Currently testimony enforces Feature, Test, Assert as mandatory docstrings for each test case"

4. bugs - Test cases affected by Bugs and the corresponding Bug list
5. manual - List all manual test cases
6. auto - List all auto test cases
7. tags - Prints all test cases with the specified tags

Note:

1. testimony returns a non-zero error code when the test case docstrings does not follow the intended rules, returns zero otherwise.  This will help testimony to be integrated easily with tools like travis.
2. testimony also parses different folders under the given folder to verify the test files
3. testimony also displays optional colored outputs when termcolor is installed

Advantages
----------
1. Avoids a separate test case management tool to document test cases by using the python automation framework for the same
2. Enforces test cases to follow a defined standard
3. Runs in integration with tools like Travis to get a report as and when you check in code
4. Saves a lot of time from the conventional way of writing test cases using a test management tool
5. The test case information can be easily extracted from testimony and can be ported to any test management tool 

Installation
------------

You could install testimony from PyPI using pip:

::

    pip install testimony

Requirements
------------
\1) Install testimony following the steps in the installation section

\2) Pre-requisites

Expected Docstring format::

    """Log in as a valid user

    @Feature: Login

    @Setup: Navigate to abc.com

    @Steps:

    1. Launch the url
    2. Log in with valid user credentials

    @Assert: Log in successful

    @BZ: #1234567

    @Status: Manual (REMOVE this field once automated)

    @Tags: T1, T2, T3

    """

    Note: The first line of docstring will be considered as the test case name.

\3) Optional color formatting - If termcolor package is installed, output will be printed in colored text

Usage:
------

help::

    $ testimony -h
    usage: testimony [-h] [-n] [-t TAGS] REPORT PATH [PATH ...]

    Inspects and report on the Python test cases.

    positional arguments:
  	REPORT                report type, possible values: print, summary,
    	                  validate_docstring, bugs, manual, auto, tags
  	PATH                  a list of paths to look for tests cases

  	optional arguments:
  	-h, --help            show this help message and exit
  	-j, --json            JSON output
  	-n, --nocolor         Do not use color option
	-t [TAGS [TAGS ...]], --tags [TAGS [TAGS ...]]
                          space separated tags to search.  Note: Always run this
                          only in the root of the project where test cases are
                          stored
	
print - test cases::

    $ testimony print testimony/tests

    tests/test_sample.py
    ====================

    TC 1
    Test: Login with right credentials
    Assert: Login is successful
    Steps: 1. Login to the application with valid credentials
    Tags: t1, t2, t3
    Skipped lines:
      Feture: Login - Positive
      Bug: 123456
      Statues: Manual

    TC 2
    <intentionally blank to show a missing docstring>

    TC 3
    Test: Login with Latin credentials
    Feature: Login - Positive
    Assert: Login is successful
    Steps: 1. Login to the application with valid Latin credentials
    Tags: t1

    TC 4
    Test: Login with Credentials having special characters
    Feature: Login - Positive
    Assert: Activation key is created
    Steps: 1. Login to the application with valid credentials having
    special characters
    Status: Manual

    TC 5
    Test: Test missing required docstrings
    Steps: 1. Login to the application with invalid credentials
    Bugs: 123456
    Status: Manual
    Tags: t2

    TC 6
    Test: Login with invalid credentials
    Feature: Login - Negative
    Assert: Login failed
    Steps: 1. Login to the application with invalid credentials
    Bugs: 123456
    Status: Manual
    Tags: t3

    TC 7
    Test: Login with invalid credentials
    Feature: Login - Negative
    Assert: Login failed
    Steps: 1. Login to the application with valid username and no password


summary - prints summary of all tests::

    $ testimony summary /home/testimony/tests

    Total Number of test cases:      7
    Total Number of automated cases: 3 (43%)
    Total Number of manual cases:    3 (43%)
    Test cases with no docstrings:   1 (14%)


validate_docstring - to validate all tests::

    $ testimony validate_docstring /home/testimony/tests

    tests/test_sample.py
    ====================

    test_positive_login_1
    ---------------------

    * Docstring should have at least feature and assert tags
    * Unexpected tags found:
      Feture: Login - Positive
      Bug: 123456
      Statues: Manual

    test_positive_login_2
    ---------------------

    * Missing docstring.
    * Docstring should have at least feature and assert tags

    test_negative_login_5
    ---------------------

    * Docstring should have at least feature and assert tags

    Total Number of invalid docstrings:  3/7 (42.86%)
    Test cases with no docstrings:   1/7 (14.29%)
    Test cases missing minimal docstrings:  3/7 (42.86%)
    Test cases with invalid tags 1/7 (14.29%)


bugs - print test cases affected with bugs::

    $ testimony bugs /home/testimony/tests

    Test cases affected by 123456
    =============================

    tests/test_sample.py
    --------------------

    * test_negative_login_5
    * test_negative_login_6


    Total Number of test cases affected by bugs: 2/7 (28.57%)


manual - print manual tests::

    $ testimony manual /home/testimony/tests/

    tests/test_sample.py
    ====================

    TC 1
    Test: Login with Credentials having special characters
    Feature: Login - Positive
    Assert: Activation key is created
    Steps: 1. Login to the application with valid credentials having
    special characters
    Status: Manual

    TC 2
    Test: Test missing required docstrings
    Steps: 1. Login to the application with invalid credentials
    Bugs: 123456
    Status: Manual
    Tags: t2

    TC 3
    Test: Login with invalid credentials
    Feature: Login - Negative
    Assert: Login failed
    Steps: 1. Login to the application with invalid credentials
    Bugs: 123456
    Status: Manual
    Tags: t3

auto - print auto tests::

    $ testimony auto /home/testimony/tests/

    tests/test_sample.py
    ====================

    TC 1
    Test: Login with right credentials
    Assert: Login is successful
    Steps: 1. Login to the application with valid credentials
    Tags: t1, t2, t3
    Skipped lines:
      Feture: Login - Positive
      Bug: 123456
      Statues: Manual

    TC 2
    Test: Login with Latin credentials
    Feature: Login - Positive
    Assert: Login is successful
    Steps: 1. Login to the application with valid Latin credentials
    Tags: t1

    TC 3
    Test: Login with invalid credentials
    Feature: Login - Negative
    Assert: Login failed
    Steps: 1. Login to the application with valid username and no password

    tags - print tests with given tags::

        $ testimony tags tests/ --tag t1
	    ['tests.test_sample.Testsample1.test_positive_login_1',
	     'tests.test_sample.Testsample1.test_positive_login_3']

        $ testimony tags tests/ --tag t1 t2
	    ['tests.test_sample.Testsample1.test_positive_login_1',
	     'tests.test_sample.Testsample1.test_positive_login_3',
	     'tests.test_sample.Testsample1.test_negative_login_5']
    

Success scenario in which testimony returns 0:

Testimony returns zero when there are no validation errors encountered::

    $ testimony validate_docstring tests/

    Total Number of invalid docstrings:  0/10 (0.00%)
    Test cases with no docstrings:   0/10 (0.00%)
    Test cases missing minimal docstrings:  0/10 (0.00%)
    Test Cases with invalid tags: 0/10 (0.00%)

    $ echo $?
    0

Colored output support:
-----------------------
Having termcolor installed, testimony produces colored output by default.  It can be disabled by::

    $ testimony auto /home/apple/tests/login/ --nocolor

    (or)

    $ testimony auto /home/apple/tests/login/ -n

json support:
-------------
Testimony supports json output format to integrate with other applications easily.  This can be done by adding --json or -j to any of the testimony commands as shown below::

    $ testimony summary --json tests/
	[{"auto_count": 2, "manual_count": 2, "auto_percent": 50.0, "no_docstring": 1, "path": "tests/", "tc_count": 4, "manual_percent": 50.0}]

	$ testimony summary -j tests/
	[{"auto_count": 2, "manual_count": 2, "auto_percent": 50.0, "no_docstring": 1, "path": "tests/", "tc_count": 4, "manual_percent": 50.0}]


Known Issues
------------
None

Contribute
----------

1. Fork the repository on GitHub and make your changes
2. Test your changes
3. Send a pull request
4. Watch for the travis update on the PR as it runs flake8
5. The PR will be merged after 2 ACKs

Version History:
----------------

v1.0.3
  - Support added to accept test modules as input (Only directory was supported earlier)

v1.0.2
  - Code refresh

v1.0.1
  - Major code refactor for modularizing the code
  - Added Tags support
  - If `@Test` is not present, the first line of docstring will be used instead

v1.0.0
  - json support now incorporated

v0.3.0
  - Bug fix: Manual vs. automated test count is wrong when the test cases are written with "status" tag vs. "Status"

v0.2.0
  - fix to check the tests starting with `test_` rather than just `test`
  - Testimony will return error code when docstrings are missing, incorrect docstrings found, minimal docstrings not present
  - Make validate_docstring return a 0 success return code if no errors are found
  - Organized Constants
  - Now testimony accepts --nocolor or --n argument to avoid color output
  - testimony will now not error out if termcolor is not installed.
  - Make termcolor an optional dependency
  - Add Travis configuration to automatically run pep8 when testimony is updated
  - Get tests from subfolders of the given path

v0.1.0
  - Initial Release

Author
------

This software is developed by `Suresh Thirugn`_.

.. _Suresh Thirugn: https://github.com/sthirugn/

Contributors
------------
| `Og Maciel <https://github.com/omaciel/>`_
| `Corey Welton <https://github.com/cswiii/>`_
| `Elyézer Rezende <https://github.com/elyezer/>`_
