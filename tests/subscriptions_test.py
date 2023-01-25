import unittest

import nina_service

# Test data
_TEST_DATA_PATH = './../tests/data/data.json'
_TEST_WARNINGS_ALREADY_RECEIVED_PATH = './../tests/data/warnings_already_received.json'

# TODO: Implement tests for subscriptions.py
# TODO: use randomized test data

"""

TESTCASES:

01 - User has no subscriptions and there are active warnings
02 - User has no subscriptions and there are no active warnings
03 - User has subscriptions and there are active warnings
04 - User has subscriptions but there are no active warnings
05 - User does not want to receive warnings automatically
06 - User has already received that warning
07 - User has a subscription for a specific warning type but the warning is not of that type
08 - User has a subscription for a specific warning type and the warning is of that type
09 - User has a subscription for a specific warning type and the warning is of that type but the warning severity is not of that level
10 - User has a subscription for a specific warning type and the warning is of that type and the warning severity is of that level


"""


# Integration test:
# Make data_service use data.json in test directory
# Mock the return values of nina_service and data_service
# To be specific: nina_service.get_all_active_warnings()

# @patch('subscriptions.some_fn')
# def test_a(mock_get_all_active_warnings):
#     mock_get_all_active_warnings.return_value = 'test-val-1'
#     tmp = subscriptions.Subscriptions()
#     assert tmp.method_2() == 'test-val-1'


# Test each method individually

# def create_test_warning(warning_id: str, warn_type: nina_service.WarnType,
#                         severity: nina_service.Severity) -> nina_service.GeneralWarning:
#     warning = nina_service.GeneralWarning()
#     warning.id = warning_id
#     warning.severity = severity
#     return warning


def clear_data():
    return 0


def clear_warnings_already_received_data():
    return 0


class TestSubscriptions(unittest.TestCase):

    def test_is_warning_relevant_for_subscription(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
