import unittest
from unittest import TestCase

from mock import patch

import nina_service
import subscriptions
from nina_service import GeneralWarning, WarningCategory, WarningType, WarningSeverity


def get_test_subscription(warning_category: nina_service.WarningCategory, warning_severity: nina_service.WarningSeverity,
                          place_id="064110000000"):
    """

    This return a test subscription with the specified parameters as a tuple (place_id, subscription_dict)
    This tuple is also created in subscriptions when database is read (from subscriptions.items())

    Args:
        warning_category: type of the warning
        warning_severity
        place_id: default is place_id of darmstadt

    Returns: a subscription with the specified parameters

    """
    return place_id, {str(warning_category.value): warning_severity.value}


def get_test_subscriptions(warning_category: WarningCategory, warning_severity: WarningSeverity, place_id):
    """

    This returns a list of subscriptions with the specified parameters as it is in the database
    Has some default values for testing.

    Args:
        warning_category: type of the warning
        warning_severity
        place_id: place_id of the subscription

    Returns: a subscription with the specified parameters

    """
    return {place_id: {str(warning_category.value): warning_severity.value},
            "081365001088": {str(WarningCategory.DISASTER.value): WarningSeverity.Moderate.value}}


def get_test_general_warning(warning_id, severity: WarningSeverity, version=0, start_date=0,
                             warning_type=WarningType.Alert, title="Test warning"):
    warning = GeneralWarning(warning_id, version, start_date, severity, warning_type, title)
    return warning


class TestSubscriptions(TestCase):

    @patch('controller.general_warning')
    @patch('data_service.add_warning_id_to_users_warnings_received_list')
    @patch('subscriptions._should_user_receive_this_warning')
    @patch('data_service.get_chat_ids_of_warned_users')
    @patch('nina_service.get_all_active_warnings')
    def test_warn_users(self,
                        get_all_active_warnings_mock,
                        get_chat_ids_of_warned_users_mock,
                        should_user_receive_this_warning_mock,
                        add_warning_id_to_users_warnings_received_list_mock,
                        general_warning_mock):

        # Mock data_service (database should not be affected by tests)
        add_warning_id_to_users_warnings_received_list_mock.side_effect = \
            lambda chat_id, warning_id: print(f"Added warning_id {warning_id} to database")

        # Mock controller
        general_warning_mock.side_effect = lambda chat_id, warning_category, warning: print("Sent warning")

        # Mock active warnings + warning_category
        warning_1 = (get_test_general_warning(warning_id="WARNING_ID_ABC", severity=WarningSeverity.MINOR),
                     WarningCategory.FLOOD)
        warning_2 = (get_test_general_warning(warning_id="WARNING_ID_DEF", severity=WarningSeverity.SEVERE),
                     WarningCategory.WEATHER)

        # Mock chat ids
        chat_ids = [123, 456]

        with self.subTest('There are no active warnings'):
            get_all_active_warnings_mock.return_value = []
            get_chat_ids_of_warned_users_mock.return_value = chat_ids
            result = subscriptions.warn_users()
            self.assertFalse(result)

        with self.subTest('There are active warnings but no user wants to be warned'):
            get_all_active_warnings_mock.return_value = [warning_1, warning_2]
            get_chat_ids_of_warned_users_mock.return_value = []
            result = subscriptions.warn_users()
            self.assertFalse(result)

        with self.subTest('There are active warnings and all users want to be warned'):
            should_user_receive_this_warning_mock.return_value = True
            get_chat_ids_of_warned_users_mock.return_value = chat_ids
            result = subscriptions.warn_users()
            self.assertTrue(result)

        with self.subTest('There are active warnings and some users want to be warned'):
            should_user_receive_this_warning_mock.side_effect = lambda chat_id, warning, warning_category: chat_id == 123
            get_chat_ids_of_warned_users_mock.return_value = chat_ids
            general_warning_mock.call_count = 0
            result = subscriptions.warn_users()
            self.assertEqual(general_warning_mock.call_count, 2)  # only chat_id=123 should be warned
            self.assertTrue(result)

    @patch('nina_service.get_warning_locations')
    @patch('data_service.has_user_already_received_warning')
    @patch('data_service.get_subscriptions')
    def test_should_user_receive_this_warning(self,
                                              get_subscriptions_mock,
                                              has_user_already_received_warning_mock,
                                              get_warning_locations_mock):
        # DEMO DATA
        warning = get_test_general_warning(warning_id="WARNING_ID_ABC", severity=WarningSeverity.Moderate)
        chat_id = 123
        warning_category = WarningCategory.FLOOD
        warning_locations = ['Darmstadt']
        demo_subscriptions = get_test_subscriptions(warning_category=WarningCategory.FLOOD,
                                                    warning_severity=WarningSeverity.Moderate,
                                                    place_id="064110000000")

        with self.subTest('User has already received that warning'):
            has_user_already_received_warning_mock.return_value = True
            get_subscriptions_mock.return_value = demo_subscriptions
            result = subscriptions._any_user_subscription_matches_warning(chat_id, warning, warning_category)
            self.assertFalse(result)

        with self.subTest('User has no subscriptions'):
            has_user_already_received_warning_mock.return_value = False
            get_subscriptions_mock.return_value = {}
            result = subscriptions._any_user_subscription_matches_warning(chat_id, warning, warning_category)
            self.assertFalse(result)

        with self.subTest('User has a matching subscription for the warning'):
            has_user_already_received_warning_mock.return_value = False
            get_subscriptions_mock.return_value = demo_subscriptions
            get_warning_locations_mock.return_value = warning_locations
            result = subscriptions._any_user_subscription_matches_warning(chat_id, warning, warning_category)
            self.assertTrue(result)

        with self.subTest('User has no matching subscription for the warning'):
            has_user_already_received_warning_mock.return_value = False
            get_subscriptions_mock.return_value = demo_subscriptions
            get_warning_locations_mock.return_value = ['Frankfurt']
            result = subscriptions._any_user_subscription_matches_warning(chat_id, warning, warning_category)
            self.assertFalse(result)

    @patch('nina_service.get_warning_locations')
    def test_is_warning_relevant_for_subscription(self, get_warning_locations_mock):
        # Mock subscription
        demo_subscription = get_test_subscription(place_id="064110000000",  # Darmstadt
                                                  warning_category=WarningCategory.FLOOD,
                                                  warning_severity=WarningSeverity.Moderate)

        warning_locations = ['Darmstadt']

        with self.subTest('Match with exact severity'):
            get_warning_locations_mock.return_value = warning_locations
            warning = get_test_general_warning(warning_id="test warning abc", severity=WarningSeverity.Moderate)
            result = subscriptions._is_warning_relevant_for_subscription(warning, demo_subscription, WarningCategory.FLOOD)
            self.assertTrue(result)

        with self.subTest('Match with higher severity in warning'):
            get_warning_locations_mock.return_value = warning_locations
            warning = get_test_general_warning(warning_id="test warning abc", severity=WarningSeverity.Severe)
            result = subscriptions._is_warning_relevant_for_subscription(warning, demo_subscription, WarningCategory.FLOOD)
            self.assertTrue(result)

        with self.subTest('No match with lower severity in warning'):
            get_warning_locations_mock.return_value = warning_locations
            warning = get_test_general_warning(warning_id="test warning abc", severity=WarningSeverity.Minor)
            result = subscriptions._is_warning_relevant_for_subscription(warning, demo_subscription, WarningCategory.FLOOD)
            self.assertFalse(result)

        with self.subTest('No match with wrong location'):
            get_warning_locations_mock.return_value = ['Frankfurt']
            warning = get_test_general_warning(warning_id="test warning abc", severity=WarningSeverity.Moderate)
            result = subscriptions._is_warning_relevant_for_subscription(warning, demo_subscription, WarningCategory.FLOOD)
            self.assertFalse(result)

        with self.subTest('No match with wrong warning_category'):
            get_warning_locations_mock.return_value = warning_locations
            warning = get_test_general_warning(warning_id="test warning abc", severity=WarningSeverity.Moderate)
            result = subscriptions._is_warning_relevant_for_subscription(warning, demo_subscription, WarningCategory.DISASTER)
            self.assertFalse(result)

    # TODO the implementation for this function will change so no test yet
    def test_subscription_location_matches_warning_location(self):
        with self.subTest('Subscription location matches warning location'):
            self.assertTrue(True)

        with self.subTest('Subscription location does not match warning location'):
            self.assertTrue(True)

    if __name__ == '__main__':
        unittest.main()

# TODO also test the functions in data_service and nina_service
