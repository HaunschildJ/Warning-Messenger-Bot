import time

import controller
import data_service
import nina_service
import place_converter
from nina_service import WarnType, GeneralWarning


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
    active_warnings = nina_service.get_all_active_warnings()
    warnings_sent_counter = 0

    for chat_id in chat_ids_of_warned_users:
        postal_codes = data_service.get_user_subscription_postal_codes(chat_id)
        filtered_warnings = filter_out_warnings_user_has_already_received(chat_id, active_warnings)

        for (warning, warn_type) in filtered_warnings:
            if _any_user_subscription_matches_warning(chat_id, warning, warn_type):
                controller.send_detailed_general_warnings(chat_id, warn_type, [warning], postal_codes)
                data_service.add_warning_id_to_users_warnings_received_list(chat_id, warning.id)
                warnings_sent_counter += 1

    print(f'There are {str(len(active_warnings))} active warnings.')
    print(f'{warnings_sent_counter} users were warned.\n')

    return warnings_sent_counter > 0


def filter_out_warnings_user_has_already_received(chat_id: int, warnings: list) -> list:
    """

    Args:
        warnings: list of warnings that should be filtered
        chat_id: of the user

    Returns: list of warnings the user has not received yet

    """
    filtered_warnings = []
    for warning in warnings:
        if not data_service.has_user_already_received_warning(chat_id, warning.id):
            filtered_warnings.append(warning)

    return filtered_warnings


def _any_user_subscription_matches_warning(chat_id: int, warning: GeneralWarning, warn_type: WarnType) -> bool:
    """

    Args:
        chat_id: of the user
        warning: warning that should be checked
        warn_type: of the warning (do not confuse with WarningType which contains different information)

    Returns: True if user should receive the specified warning

    """
    subscriptions = data_service.get_subscriptions(chat_id)
    for subscription in subscriptions.items():
        if _do_subscription_and_warning_match_severity(warning, subscription, warn_type):
            return True
    return False


def _do_subscription_and_warning_match_severity(warning: GeneralWarning, subscription: tuple,
                                                warn_type: WarnType) -> bool:
    """

    Args:
        warning: warning that should be checked
        subscription: subscription the warning should be checked against
        warn_type: of the warning (do not confuse with WarningType which contains different information)

    Returns: True if the warning matches the subscription

    """
    subscription_dict = subscription[1]

    for _ in subscription_dict:
        try:
            subscription_warning_severity = subscription_dict[str(warn_type.value)]
            if subscription_warning_severity <= warning.severity.value:
                return True
        except KeyError:
            return False

    return False
