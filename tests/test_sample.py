# -*- encoding: utf-8 -*-
"""Test class for Sample Test"""


class Testsample():
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

        """
        # Login to the application
