import time

import controller
import data_service
import nina_service
from nina_service import WarningCategory, GeneralWarning


def start_subscriptions(minutes_to_wait: int = 2):
    """

    This endless loop should only be started once when the main script is started.

    Args:
        minutes_to_wait: amount of minutes to wait after checking for new warnings (2 minutes by default)


    """
    print("Subscriptions running...")
    while True:
        warn_users()
        time.sleep(minutes_to_wait * 60)


def warn_users() -> bool:
    """

    Warns every user following his warning subscriptions.

    Returns: True if at least one user was warned

    """
    chat_ids_of_warned_users = data_service.get_chat_ids_of_warned_users()
    active_warnings_with_category = nina_service.get_all_active_warnings()
    warnings_sent_counter = 0

    for chat_id in chat_ids_of_warned_users:
        postal_codes = data_service.get_user_subscription_postal_codes(chat_id)
        filtered_warnings = list(filter(lambda x: not data_service.has_user_already_received_warning(chat_id, x[0].id), active_warnings_with_category))

        for (warning, warning_category) in filtered_warnings:
            if _any_user_subscription_matches_warning(chat_id, warning, warning_category):
                controller.send_detailed_general_warnings(chat_id, [warning], postal_codes)
                data_service.add_warning_id_to_users_warnings_received_list(chat_id, warning.id)
                warnings_sent_counter += 1

    print(f'There are {str(len(active_warnings_with_category))} active warnings.')
    print(f'{warnings_sent_counter} warnings were sent out.\n')

    return warnings_sent_counter > 0


def _any_user_subscription_matches_warning(chat_id: int, warning: GeneralWarning, warning_category: WarningCategory) -> bool:
    """

    Args:
        chat_id: of the user
        warning: warning that should be checked
        warning_category: of the warning

    Returns: True if user should receive the specified warning

    """
    subscriptions = data_service.get_subscriptions(chat_id)
    for subscription in subscriptions.items():
        if _do_subscription_and_warning_match_severity_and_category(warning, subscription, warning_category):
            return True
    return False


def _do_subscription_and_warning_match_severity_and_category(warning: GeneralWarning, subscription: tuple,
                                                warning_category: WarningCategory) -> bool:
    """

    Args:
        warning: warning that should be checked
        subscription: subscription the warning should be checked against
        warning_category: of the warning

    Returns: True if the warning matches the subscription

    """
    subscription_dict = subscription[1]
    for _ in subscription_dict:
        try:
            subscription_warning_severity = subscription_dict[str(warning_category.value)]
            if subscription_warning_severity <= warning.severity.value:
                return True
        except KeyError:
            return False

    return False
