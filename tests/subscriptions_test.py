import unittest
from unittest import TestCase

import nina_service
from subscriptions import _is_warning_relevant_for_subscription, _should_user_receive_this_warning
from nina_service import GeneralWarning, WarnType, WarningType, WarningSeverity

# Test data
_TEST_DATA_PATH = './../tests/data/data.json'
_TEST_WARNINGS_ALREADY_RECEIVED_PATH = './../tests/data/warnings_already_received.json'

"""

TESTCASES:



"""


def clear_data():
    return 0


def clear_warnings_already_received_data():
    return 0


def get_test_subscription(place_id, warning_type, warning_severity):
    subscription = {place_id: {warning_type: warning_severity}}
    return subscription


def get_test_general_warning(warning_id, version=0, start_date=0, severity, warning_type = WarningType.Alert, title="Test warning"):
    warning = GeneralWarning(warning_id, version, start_date, severity, warning_type, title)
    return warning



def get_test_chat_id():
    return 0


class TestSubscriptions(TestCase):

    def test_is_warning_relevant_for_subscription(self):
        # Test subscription
        subscription = get_test_subscription("Darmstadt", WarnType.FLOOD, 1)

        with self.subTest('Match with exact severity'):
            warning = get_test_general_warning()
            warn_type = WarnType.FLOOD
            result = _is_warning_relevant_for_subscription(subscription, warning, warn_type)
            self.assertTrue(result)

        with self.subTest('Match with higher severity in warning'):
            self.assertTrue(True)

        with self.subTest('No match with lower severity in warning'):
            self.assertTrue(True)

        with self.subTest('No match with wrong location'):
            self.assertTrue(True)

        with self.subTest('No match with wrong warn_type'):
            self.assertTrue(True)

    def test_should_user_receive_this_warning(self):
        with self.subTest('User has no subscriptions'):
            self.assertTrue(True)

        with self.subTest('User has subscriptions'):
            self.assertTrue(True)

        with self.subTest('User does not want to receive warnings automatically'):
            self.assertTrue(True)

        with self.subTest('User has already received that warning'):
            self.assertTrue(True)

        with self.subTest('User has a subscription for a specific warning type but the warning is not of that type'):
            self.assertTrue(True)

        with self.subTest('User has a subscription for a specific warning type and the warning is of that type'):
            self.assertTrue(True)

        with self.subTest(
                'User has a subscription for a specific warning type and the warning is of that type but the warning severity is not of that level'):
            self.assertTrue(True)

        with self.subTest(
                'User has a subscription for a specific warning type and the warning is of that type and the warning severity is of that level'):
            self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()

# TODO also test the functions in data_service and nina_service
# TODO auch methoden im data_service testen, die ich erstellt habe
