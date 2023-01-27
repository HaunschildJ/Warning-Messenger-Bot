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

    This return a test subscription with the specified parameters as a tuple (place_id, subscription_dict)
    This tuple is also created in subscriptions when database is read (from subscriptions.items())

    Args:
        warn_type: type of the warning
        warning_severity
        place_id: default is place_id of darmstadt

    Returns: a subscription with the specified parameters

    """
    return place_id, {str(warn_type.value): warning_severity.value}


def get_test_subscriptions(warn_type: WarnType, warning_severity: WarningSeverity, place_id):
    """

    This returns a list of subscriptions with the specified parameters as it is in the database
    Has some default values for testing.

    Args:
        warn_type: type of the warning
        warning_severity
        place_id: place_id of the subscription

    Returns: a subscription with the specified parameters

    """
    return {place_id: {str(warn_type.value): warning_severity.value},
            "081365001088": {str(WarnType.DISASTER.value): WarningSeverity.Moderate.value}}


def get_test_general_warning(warning_id, severity: WarningSeverity, version=0, start_date=0,
                             warning_type=WarningType.Alert, title="Test warning"):
    warning = GeneralWarning(warning_id, version, start_date, severity, warning_type, title)
    return warning


class TestSubscriptions(TestCase):

    @patch('data_service.has_user_already_received_warning')
    @patch('data_service.get_subscriptions')
    @patch('nina_service.get_warning_locations')
    def test_should_user_receive_this_warning(self,
                                              get_subscriptions_mock,
                                              has_user_already_received_warning_mock,
                                              get_warning_locations_mock):
        # DEMO DATA
        warning = get_test_general_warning(warning_id="WARNING_ID_ABC", severity=WarningSeverity.Moderate)
        chat_id = 123
        warn_type = WarnType.FLOOD
        warning_locations = ['Darmstadt']
        demo_subscriptions = get_test_subscriptions(warn_type=WarnType.FLOOD,
                                                    warning_severity=WarningSeverity.Moderate,
                                                    place_id="064110000000")

        with self.subTest('User has already received that warning'):
            has_user_already_received_warning_mock.return_value = True
            get_subscriptions_mock.return_value = demo_subscriptions
            result = subscriptions._should_user_receive_this_warning(chat_id, warning, warn_type)
            self.assertFalse(result)

        with self.subTest('User has no subscriptions'):
            has_user_already_received_warning_mock.return_value = False
            get_subscriptions_mock.return_value = {}
            result = subscriptions._should_user_receive_this_warning(chat_id, warning, warn_type)
            self.assertFalse(result)

        with self.subTest('User has a matching subscription for the warning'):
            has_user_already_received_warning_mock.return_value = False
            get_subscriptions_mock.return_value = demo_subscriptions
            # get_warning_locations_mock.return_value = warning_locations
            result = subscriptions._should_user_receive_this_warning(chat_id, warning, warn_type)
            self.assertTrue(result)

        with self.subTest('User has no matching subscription for the warning'):
            has_user_already_received_warning_mock.return_value = False
            get_subscriptions_mock.return_value = demo_subscriptions
            get_warning_locations_mock.return_value = ['Frankfurt']
            result = subscriptions._should_user_receive_this_warning(chat_id, warning, warn_type)
            self.assertFalse(result)

    @patch('nina_service.get_warning_locations')
    def test_is_warning_relevant_for_subscription(self, get_warning_locations_mock):
        # Mock subscription
        demo_subscription = get_test_subscription(place_id="064110000000",  # Darmstadt
                                                  warn_type=WarnType.FLOOD,
                                                  warning_severity=WarningSeverity.Moderate)

        warning_locations = ['Darmstadt']

        with self.subTest('Match with exact severity'):
            get_warning_locations_mock.return_value = warning_locations
            warning = get_test_general_warning(warning_id="test warning abc", severity=WarningSeverity.Moderate)
            result = subscriptions._is_warning_relevant_for_subscription(warning, demo_subscription, WarnType.FLOOD)
            self.assertTrue(result)

        with self.subTest('Match with higher severity in warning'):
            get_warning_locations_mock.return_value = warning_locations
            warning = get_test_general_warning(warning_id="test warning abc", severity=WarningSeverity.Severe)
            result = subscriptions._is_warning_relevant_for_subscription(warning, demo_subscription, WarnType.FLOOD)
            self.assertTrue(result)

        with self.subTest('No match with lower severity in warning'):
            get_warning_locations_mock.return_value = warning_locations
            warning = get_test_general_warning(warning_id="test warning abc", severity=WarningSeverity.Minor)
            result = subscriptions._is_warning_relevant_for_subscription(warning, demo_subscription, WarnType.FLOOD)
            self.assertFalse(result)

        with self.subTest('No match with wrong location'):
            get_warning_locations_mock.return_value = ['Frankfurt']
            warning = get_test_general_warning(warning_id="test warning abc", severity=WarningSeverity.Moderate)
            result = subscriptions._is_warning_relevant_for_subscription(warning, demo_subscription, WarnType.FLOOD)
            self.assertFalse(result)

        with self.subTest('No match with wrong warn_type'):
            get_warning_locations_mock.return_value = warning_locations
            warning = get_test_general_warning(warning_id="test warning abc", severity=WarningSeverity.Moderate)
            result = subscriptions._is_warning_relevant_for_subscription(warning, demo_subscription, WarnType.DISASTER)
            self.assertFalse(result)



    def test_subscription_location_matches_warning_location(self):
        with self.subTest('Subscription location matches warning location'):
            self.assertTrue(True)

        with self.subTest('Subscription location does not match warning location'):
            self.assertTrue(True)

    if __name__ == '__main__':
        unittest.main()

# TODO also test the functions in data_service and nina_service
