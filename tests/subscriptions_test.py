import unittest
from unittest import TestCase
import sys

from mock import patch

sys.path.insert(0, "..\source")

import nina_service
import subscriptions
from nina_service import GeneralWarning, WarningCategory, WarningType, WarningSeverity


def get_test_subscription(warning_category: nina_service.WarningCategory,
                          warning_severity: nina_service.WarningSeverity,
                          postal_code="35394"):
    """

    This return a test subscription with the specified parameters as a tuple (place_id, subscription_dict)
    This tuple is also created in subscriptions when database is read (from subscriptions.items())

    Args:
        warning_category: type of the warning
        warning_severity
        postal_code: of the subscription

    Returns: a subscription with the specified parameters

    """
    return postal_code, {str(warning_category.value): warning_severity.value}


def get_test_subscriptions(warning_category: WarningCategory, warning_severity: WarningSeverity, postal_code: str):
    """

    This returns a list of subscriptions with the specified parameters as it is in the database
    Has some default values for testing.

    Args:
        warning_category: type of the warning
        warning_severity
        postal_code: place_id of the subscription

    Returns: a subscription with the specified parameters

    """
    return {postal_code: {str(warning_category.value): warning_severity.value},
            "081365001088": {str(WarningCategory.CIVIL_PROTECTION.value): WarningSeverity.MINOR.value}}


def get_test_general_warning(warning_id, severity: WarningSeverity, version=0, start_date=0,
                             warning_type=WarningType.ALERT, title="Test warning"):
    warning = GeneralWarning(warning_id, version, start_date, severity, warning_type, title)
    return warning


class TestSubscriptions(TestCase):

    @patch('data_service.has_user_already_received_warning')
    @patch('data_service.get_user_subscription_postal_codes')
    @patch('controller.send_detailed_general_warnings')
    @patch('data_service.add_warning_id_to_users_warnings_received_list')
    @patch('subscriptions._any_user_subscription_matches_warning')
    @patch('data_service.get_chat_ids_of_warned_users')
    @patch('nina_service.get_all_active_warnings')
    def test_warn_users(self,
                        get_all_active_warnings_mock,
                        get_chat_ids_of_warned_users_mock,
                        any_user_subscription_matches_warning_mock,
                        add_warning_id_to_users_warnings_received_list_mock,
                        send_detailed_general_warnings_mock,
                        get_user_subscription_postal_codes_mock,
                        has_user_already_received_warning_mock
                        ):
        # Mock data_service (database should not be affected by tests)
        add_warning_id_to_users_warnings_received_list_mock.side_effect = \
            (lambda chat_id, warning_id: print(f"Added warning_id {warning_id} to database"))

        # Mock active warnings + warning_category
        warning_1 = (get_test_general_warning(warning_id="WARNING_ID_ABC", severity=WarningSeverity.MINOR),
                     WarningCategory.FLOOD)
        warning_2 = (get_test_general_warning(warning_id="WARNING_ID_DEF", severity=WarningSeverity.SEVERE),
                     WarningCategory.WEATHER)

        # Mock chat ids
        chat_ids = [123, 456]

        # Mock subscription postal codes
        get_user_subscription_postal_codes_mock.return_value = ["64283", "64297"]

        with self.subTest('There are no active warnings'):
            has_user_already_received_warning_mock.return_value = False
            get_all_active_warnings_mock.return_value = []
            get_chat_ids_of_warned_users_mock.return_value = chat_ids
            result = subscriptions.warn_users()
            self.assertFalse(result)

        with self.subTest('There are active warnings but no user wants to be warned'):
            has_user_already_received_warning_mock.return_value = False
            get_all_active_warnings_mock.return_value = [warning_1, warning_2]
            get_chat_ids_of_warned_users_mock.return_value = []
            result = subscriptions.warn_users()
            self.assertFalse(result)

        with self.subTest('There are active warnings and all users want to be warned'):
            has_user_already_received_warning_mock.return_value = False
            any_user_subscription_matches_warning_mock.return_value = True
            send_detailed_general_warnings_mock.return_value = 4
            get_chat_ids_of_warned_users_mock.return_value = chat_ids
            result = subscriptions.warn_users()
            self.assertTrue(result)

        with self.subTest('There are active warnings and some users want to be warned'):
            any_user_subscription_matches_warning_mock.side_effect = (lambda chat_id, warning,
                                                                             warning_category: chat_id == 123)
            get_chat_ids_of_warned_users_mock.return_value = chat_ids
            send_detailed_general_warnings_mock.call_count = 0
            send_detailed_general_warnings_mock.return_value = 2
            result = subscriptions.warn_users()
            self.assertEqual(send_detailed_general_warnings_mock.call_count, 2)  # only chat_id=123 should be warned
            self.assertTrue(result)

    @patch('data_service.get_subscriptions')
    def test_any_user_subscription_matches_warning(self, get_subscriptions_mock):
        # Mock subscription
        demo_subscriptions = get_test_subscriptions(postal_code="35394",
                                                    warning_category=WarningCategory.FLOOD,
                                                    warning_severity=WarningSeverity.MINOR)

        # Mock chat id
        chat_id = 123

        with self.subTest('User has a subscription'):
            get_subscriptions_mock.return_value = demo_subscriptions
            warning_category = WarningCategory.FLOOD
            warning = get_test_general_warning(warning_id="test warning abc", severity=WarningSeverity.MINOR)
            result = subscriptions._any_user_subscription_matches_warning(chat_id, warning, warning_category)
            self.assertTrue(result)

        with self.subTest('User has no subscriptions'):
            get_subscriptions_mock.return_value = {}
            warning_category = WarningCategory.FLOOD
            warning = get_test_general_warning(warning_id="test warning abc", severity=WarningSeverity.MINOR)
            result = subscriptions._any_user_subscription_matches_warning(chat_id, warning, warning_category)
            self.assertFalse(result)

    def test_do_subscription_and_warning_match_severity_and_category(self):
        # Mock subscription
        demo_subscription = get_test_subscription(postal_code="35394",
                                                  warning_category=WarningCategory.FLOOD,
                                                  warning_severity=WarningSeverity.MINOR)

        with self.subTest('Match with exact severity'):
            warning = get_test_general_warning(warning_id="test warning abc", severity=WarningSeverity.MINOR)
            result = subscriptions._do_subscription_and_warning_match_severity_and_category(warning, demo_subscription,
                                                                                            WarningCategory.FLOOD)
            self.assertTrue(result)

        with self.subTest('Match with higher severity in warning'):
            warning = get_test_general_warning(warning_id="test warning abc", severity=WarningSeverity.SEVERE)
            result = subscriptions._do_subscription_and_warning_match_severity_and_category(warning, demo_subscription,
                                                                                            WarningCategory.FLOOD)
            self.assertTrue(result)

        with self.subTest('No match with lower severity in warning'):
            demo_subscription = get_test_subscription(postal_code="35394",
                                                      warning_category=WarningCategory.FLOOD,
                                                      warning_severity=WarningSeverity.SEVERE)
            warning = get_test_general_warning(warning_id="test warning abc", severity=WarningSeverity.MODERATE)
            result = subscriptions._do_subscription_and_warning_match_severity_and_category(warning, demo_subscription,
                                                                                            WarningCategory.FLOOD)
            self.assertFalse(result)

        with self.subTest('No match with wrong warning_category'):
            warning = get_test_general_warning(warning_id="test warning abc", severity=WarningSeverity.MINOR)
            result = subscriptions._do_subscription_and_warning_match_severity_and_category(warning, demo_subscription,
                                                                                            WarningCategory.CIVIL_PROTECTION)
            self.assertFalse(result)

    if __name__ == '__main__':
        unittest.main()
