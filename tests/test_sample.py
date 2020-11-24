# coding=utf-8
"""Test class for Sample Test

:Setup: Global setup
"""


def test_outside_class():
    """Test testimony works with test functions.

    :Feature: Test functions

    :Assert: Testimony works with test functions
    """


class Testsample1():
    """This is a dummy test file used for testing testimony

    :Setup: Setup Testsample1
    """

    # Test with incorrect doctrings:
    # Feture vs. Feature, Statues vs. Status,
    # Statues vs. Status
    # bug vs bz
    def test_positive_login_1(self):
        """Login with right credentials

        :Feture: Login - Positive

        :Steps: 1. Login to the application with valid credentials
                2. Add a colon to the steps token: it should appear.

        :Assert: Login is successful

        :Bug: 123456

        :Statues: Manual

        :Tags: t1, t2, t3

        :Types: Functional
        """
        # Code to perform the test
        pass

    # Test with no docstring
    def test_positive_login_2(self):
        # Code to perform the test
        pass

    # Test with all required docstrings and is automated
    def test_positive_login_3(self):
        """Login with Latin credentials

        :Setup: Setup test_positive_login_3

        :Feature: Login - Positive

        :Steps: 1. Login to the application with valid Latin credentials

        :Assert: Login is successful

        :Tags: t1
        """
        # Code to perform the test
        pass

    # Test with all required docstrings and is manual
    def test_positive_login_4(self):
        """Login with Credentials having special characters

        :Feature: Login - Positive

        :Steps: 1. Login to the application with valid credentials having
                   special characters

        :Assert: Activation key is created

        :Status: Manual
        """
        # Code to perform the test
        pass

# Test missing required docstrings
    def test_negative_login_5(self):
        """Test missing required docstrings

        :Steps: 1. Login to the application with invalid credentials

        :BZ: 123456

        :Status: Manual

        :Tags: t2

        """
        # Login to the application


class Testsample2():
    """This is the second class in this test module.  This is added to make
    sure testimony covers test functions in multiple classes in a test
    module"""

    def test_negative_login_6(self):
        """Login with invalid credentials

        :Feature: Login - Negative

        :Steps: 1. Login to the application with invalid credentials

        :Assert: Login failed

        :BZ: 123456

        :Status: Manual

        :Tags: t3

        :Type: Functional
        """
        # Code to perform the test
        pass


class Testsample3():
    """This is the third class in this test module.  This is added to make
    sure testimony covers test functions in multiple classes in a test
    module"""

    def test_negative_login_7(self):
        """Login with invalid credentials

        :Feature: Login - Negative

        :Steps: 1. Login to the application with valid username
                   and no password

        :Assert: Login failed
        """
        # Code to perform the test
        pass


class RSTFormattingTestCase():
    """Class to test Testimony RST parsing issues features."""

    def test_invalid_list_style(self):
        """Check invalid list style parsing issue.

        :Feature: RST Parsing Issues

        :Steps:
            1. Have a RST list on any of the tokens, like steps.
            2. Make sure one of the items on the list goes across multiple
            lines and the lines are not properly indented.

        :Assert:
            1. Testimony reports RST parsing issue for the list with the
               indentation issue
            2. Testimony does not report RST parsing issue on list properly
               formatted.
    """


class ConfigurationFileTestCase():
    """Class to test Testimony config file support.

    Behavior was observed in GitHub issue #148 where case sensitivity was not applied correctly
    The failure was missed by the original unit test test_case_mismatch_case_sensitive_values
    Because it was the only test using the case sensitive token.
    CaseImportance and CaseAutomation tokens are now included in cases not directly testing them
    """

    def test_lowercase_key(self):
        """Check that key can be provided in all lowercase.

        :Feature: Config file support

        :Assert: Metadata key can be all-lowercase

        :status: Manual
        """
        pass

    def test_mixedcase_key(self):
        """Check that key can be provided in mixed case.

        :Feature: Config file support

        :AsSeRt: Metadata key can be mixed case
        """
        pass

    def test_overwrite_key_with_variable_case(self):
        """Check overwriting keys that use different casing on various levels.

        :Feature: Config file support

        :Assert: Test-level key overwrites module-level key

        :setup: test-level setup
        """
        pass

    def test_multiple_invalid_keys(self):
        """Check that multiple invalid keys are properly displayed.

        :Feature: Config file support

        :Status: Invalid

        :CaseImportance: Lowest

        :Assert: Multiple metadata keys with invalid values
        """
        pass

    def test_case_mismatch_case_insensitive_values(self):
        """Check 'Status' value is case insensitive.

        :Feature: Config file support

        :Assert: Value doesn't have to match case

        :Status: MANUAL

        :CaseImportance: Critical

        :CaseAutomation: Automated
        """
        pass

    def test_case_mismatch_case_sensitive_values(self):
        """Check 'CaseAutomation' and 'CaseImportance' validation is case sensitive.

        :Feature: Config file support

        :Assert: Value has to match case

        :Status: manual

        :CaseImportance: critical

        :CaseAutomation: AUTOMATED
        """
        pass


class DecoratorsTestCase():
    """Class to test Testimony support for decorators

    :Feature: Decorators

    :Assert: Decorators are properly read
    """

    def test_no_decorator(self):
        """Test without decorator."""
        pass

    @tier1
    def test_one_decorator(self):
        """Test with one decorator."""
        pass

    @tier1
    @tier2
    def test_multiple_decorators(self):
        """Test with multiple decorators."""
        pass


@tier1
class MergeDecoratorsTestCase():
    """Class to test Testimony support for decorated classes

    :Feature: Decorators

    :Assert: Decorators are properly read
    """

    def test_no_decorator(self):
        """Test without decorator."""
        pass

    @tier2
    def test_decorator(self):
        """Test with one decorator."""
        pass
