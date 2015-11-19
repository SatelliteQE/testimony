# -*- encoding: utf-8 -*-
"""Test class for Sample Test"""


class Testsample1():
    """This is a dummy test file used for testing testimony"""

    # Test with incorrect doctrings:
    # Feture vs. Feature, Statues vs. Status,
    # Statues vs. Status
    # bug vs bz
    def test_positive_login_1(self):
        """@Test: Login with right credentials

        @Feture: Login - Positive

        @Steps:

        1. Login to the application with valid credentials

        @Assert: Login is successful

        @Bug: 123456

        @Statues: Manual

        @Tags: t1, t2, t3

        """
        # Code to perform the test
        pass

    # Test with no docstring
    def test_positive_login_2(self):
        # Code to perform the test
        pass

    # Test with all required docstrings and is automated
    def test_positive_login_3(self):
        """@Test: Login with Latin credentials

        @Feature: Login - Positive

        @Steps:

        1. Login to the application with valid Latin credentials

        @Assert: Login is successful

        @Tags: t1

        """
        # Code to perform the test
        pass

    # Test with all required docstrings and is manual
    def test_positive_login_4(self):
        """@Test: Login with Credentials having special characters

        @Feature: Login - Positive

        @Steps:

        1. Login to the application with valid credentials having
        special characters

        @Assert: Activation key is created

        @Status: Manual

        """
        # Code to perform the test
        pass

# Test missing required docstrings
    def test_negative_login_5(self):
        """@Steps:

        1. Login to the application with invalid credentials

        @BZ: 123456

        @Status: Manual

        @Tags: t2

        """
        # Login to the application


class Testsample2():
    """This is the second class in this test module.  This is added to make
    sure testimony covers test functions in multiple classes in a test
    module"""

    def test_negative_login_6(self):
        """@Test: Login with invalid credentials

        @Feature: Login - Negative

        @Steps:

        1. Login to the application with invalid credentials

        @Assert: Login failed

        @BZ: 123456

        @Status: Manual

        @Tags: t3

        """
        # Code to perform the test
        pass


class Testsample3():
    """This is the third class in this test module.  This is added to make
    sure testimony covers test functions in multiple classes in a test
    module"""

    def test_negative_login_7(self):
        """@Test: Login with invalid credentials

        @Feature: Login - Negative

        @Steps:

        1. Login to the application with valid username and no password

        @Assert: Login failed

        """
        # Code to perform the test
        pass
