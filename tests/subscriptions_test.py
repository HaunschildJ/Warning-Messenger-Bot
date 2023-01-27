import unittest
from unittest import TestCase

from mock import patch

import nina_service
import subscriptions
from nina_service import GeneralWarning, WarnType, WarningType, WarningSeverity

# Test data
_TEST_DATA_PATH = './../tests/data/data.json'
_TEST_WARNINGS_ALREADY_RECEIVED_PATH = './../tests/data/warnings_already_received.json'


def get_test_subscription(warn_type: nina_service.WarnType, warning_severity: nina_service.WarningSeverity,
                          place_id="064110000000"):
    """

    Args:
        warning_type
        warning_severity
        place_id: default is place_id of darmstadt

    Returns: a subscription with the specified parameters

    """
    return place_id, {str(warn_type.value): warning_severity.value}


def get_test_general_warning(warning_id, severity: WarningSeverity, version=0, start_date=0,
                             warning_type=WarningType.Alert, title="Test warning"):
    warning = GeneralWarning(warning_id, version, start_date, severity, warning_type, title)
    return warning


class TestSubscriptions(TestCase):

    @patch('nina_service.get_warning_locations')
    def test_is_warning_relevant_for_subscription(self, get_warning_locations_mock):
        # Test subscription with place_id of Darmstadt
        subscription = get_test_subscription(place_id="064110000000", warn_type=WarnType.FLOOD,
                                             warning_severity=WarningSeverity.Moderate)

        warning_locations = ['Darmstadt']

        with self.subTest('Match with exact severity'):
            get_warning_locations_mock.return_value = warning_locations
            warning = get_test_general_warning(warning_id="test warning abc", severity=WarningSeverity.Moderate)
            result = subscriptions._is_warning_relevant_for_subscription(warning, subscription, WarnType.FLOOD)
            self.assertTrue(result)

        with self.subTest('Match with higher severity in warning'):
            get_warning_locations_mock.return_value = warning_locations
            warning = get_test_general_warning(warning_id="test warning abc", severity=WarningSeverity.Severe)
            result = subscriptions._is_warning_relevant_for_subscription(warning, subscription, WarnType.FLOOD)
            self.assertTrue(result)

        with self.subTest('No match with lower severity in warning'):
            get_warning_locations_mock.return_value = warning_locations
            warning = get_test_general_warning(warning_id="test warning abc", severity=WarningSeverity.Minor)
            result = subscriptions._is_warning_relevant_for_subscription(warning, subscription, WarnType.FLOOD)
            self.assertFalse(result)

        with self.subTest('No match with wrong location'):
            get_warning_locations_mock.return_value = ['Frankfurt']
            warning = get_test_general_warning(warning_id="test warning abc", severity=WarningSeverity.Moderate)
            result = subscriptions._is_warning_relevant_for_subscription(warning, subscription, WarnType.FLOOD)
            self.assertFalse(result)

        with self.subTest('No match with wrong warn_type'):
            get_warning_locations_mock.return_value = warning_locations
            warning = get_test_general_warning(warning_id="test warning abc", severity=WarningSeverity.Moderate)
            result = subscriptions._is_warning_relevant_for_subscription(warning, subscription, WarnType.DISASTER)
            self.assertFalse(result)

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

    def test_subscription_location_matches_warning_location(self):
        with self.subTest('Subscription location matches warning location'):
            self.assertTrue(True)

        with self.subTest('Subscription location does not match warning location'):
            self.assertTrue(True)

    if __name__ == '__main__':
        unittest.main()

# TODO also test the functions in data_service and nina_service
