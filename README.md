testimony
=========
The project testimony is written to inspect and report on the python test cases.  There are several reporting features in this program.

The parameter options are
    print - List all test cases
    summary - Summary of number of automated cases vs. manual cases
    validate_docstring - Validate docstrings
    bugs - Test cases affected by Bugs and the corresponding Bug list
    manual - List all manual test cases
    auto - List all auto test cases

Requirements
------------
1)If you haven't cloned the source code yet, then make sure to do it now:

```
git clone https://github.com/sthirugn/testimony.git
```

2)Pre-requisites
  Expected Docstring format:

```	
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
```

3) Update constants.py -> TEST_PATH to add any number of test folder paths as array items.

Usage:
-----

```
#python testimony.py print

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
```

```
#python testimony.py summary

TEST PATH: /home/apple/tests/login/
----------------------------------------------------------------
Total Number of test cases:      5
Total Number of automated cases: 4
Total Number of manual cases:    1
Test cases with no docstrings:   0
```

```
#python testimony.py validate_docstring

TEST PATH: /home/apple/tests/login/
----------------------------------------------------------------
Analyzing test_sample.py...
-->Invalid DocString: Creates new user and delete it<--
-->Invalid DocString: Create new user and update name<--
-->Invalid DocString: Remove an user<--
Total Number of invalid docstrings:  4
```

```
#python testimony.py bugs

TEST PATH: /home/apple/tests/login/
----------------------------------------------------------------
Analyzing test_sample.py...
Total Number of test cases affected by bugs: 1
List of bugs:                                ['#1234567']
```

```
#python testimony.py manual

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
```

```
# python testimony.py auto

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
```

```
# python testimony.py
Please enter a valid option to proceed:
print
summary
validate_docstring
bugs
manual
auto
```

```
# python testimony.py invalid
Please enter a valid option to proceed:
print
summary
validate_docstring
bugs
manual
auto
```

Known Issues
============
None

Author
------

This software is developed by [Suresh Thirugn] [1].

[1]: https://github.com/sthirugn/   "Suresh Thirugn"
