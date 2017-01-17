# -*- coding: UTF-8 -*-

from hamcrest import assert_that, equal_to, none, not_none, contains_string


class Assert(object):
    """Wrapper functions on top of hamcrest assertions
    Usage:
        Assert.assert_equals(actual, expected, message)
        Assert.assert_not_equals(actual,expected, message)
        Assert.fail(message)
    """
    @staticmethod
    def assert_true(condition, message=None):
        """Assert a condition is True
        :param condition: condition to check
        :param message: message to display in case of assertion failure
        :return: None
        """
        assert_that(condition, equal_to(True), message)

    @staticmethod
    def assert_false(condition, message=None):
        """Assert a condition is False
        :param condition: condition to check
        :param message: message to display in case of assertion failure
        :return:
        """
        assert_that(condition, equal_to(False), message)

    @staticmethod
    def assert_equals(actual, expected, message=None):
        """Assert expected and actual values match
        :param actual: actual result
        :param expected: expected result
        :param message: message to display in case of assertion failure
        :return: None
        """
        assert_that(actual, equal_to(expected), message)

    @staticmethod
    def assert_contains(actual, expected, message=None):
        """Assert expected contains actual value
        :param actual: actual result
        :param expected: expected result
        :param message: message to display in case of assertion failure
        :return: None
        """
        assert_that(actual, contains_string(expected), message)

    @staticmethod
    def assert_not_equals(actual, expected, message=None):
        """Assert expected and actual values do not match
        :param actual: actual result
        :param expected: expected result
        :param message: message to display in case of assertion failure
        :return: None
        """
        assert_that(actual, not (equal_to(expected)), message)

    @staticmethod
    def assert_none(condition, message=None):
        """Assert result is None
        :param condition: condition to check
        :param message: message to display in case of assertion failure
        :return: None
        """
        assert_that(condition, none, message)

    @staticmethod
    def assert_not_none(condition, message=None):
        """Assert result is NOT None
        :param condition: condition to check
        :param message: message to display in case of assertion failure
        :return: None
        """
        assert_that(condition, not_none, message)

    @staticmethod
    def assert_fail(message=None):
        """Force fail scenario
        :param message: message to display in case of assertion failure
        :return: None
        """
        assert_that(False, equal_to(True), message)
