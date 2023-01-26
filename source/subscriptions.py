import data_service
import nina_service
import controller
import time
import place_converter


def start_subscriptions(minutes_to_wait: int = 2):
    """

    This endless loop should only be started once when the main script is started.

    Args:
        minutes_to_wait: amount of minutes to wait after checking for new warnings (2 minutes by default)


    """
    print("Subscriptions running...")
    while True:
        warn_users()
        time.sleep(minutes_to_wait*60)


def warn_users():
    """

    Warns every user following his warning subscriptions.

    """
    chat_ids_of_warned_users = data_service.get_chat_ids_of_warned_users()
    active_warnings = nina_service.get_all_active_warnings()
    warnings_sent_counter = 0
    for (warning, warn_type) in active_warnings:
        for chat_id in chat_ids_of_warned_users:
            if _should_user_receive_this_warning(chat_id, warning, warn_type):
                controller.general_warning(chat_id, nina_service.WarnType.NONE, [warning])
                data_service.add_warning_id_to_users_warnings_received_list(chat_id, warning.id)
                warnings_sent_counter += 1

    print(f'There are {str(len(active_warnings))} active warnings.')
    print(f'{warnings_sent_counter} users were warned.\n')


def _should_user_receive_this_warning(chat_id: int, warning: nina_service.GeneralWarning,
                                      warn_type: nina_service.WarnType) -> bool:
    """

    Args:
        chat_id: of the user
        warning: warning that should be checked
        warn_type: of the warning (do not confuse with WarningType which contains different information)

    Returns: True if user should receive the specified warning

    """

    if data_service.has_user_already_received_warning(chat_id, warning.id):
        return False
    subscriptions = data_service.get_subscriptions(chat_id)
    for subscription in subscriptions.items():
        if _is_warning_relevant_for_subscription(warning, subscription, warn_type):
            return True
    return False


def _is_warning_relevant_for_subscription(warning: nina_service.GeneralWarning, subscription: tuple,
                                          warn_type: nina_service.WarnType) -> bool:
    """

    Args:
        warning: warning that should be checked
        subscription: subscription the warning should be checked against
        warn_type: of the warning (do not confuse with WarningType which contains different information)

    Returns: True if the warning matches the subscription

    """
    subscription_location_name = place_converter.get_name_for_id(subscription[0])
    lower_case_locations_list = list(map(lambda s: s.lower(), nina_service.get_warning_locations(warning)))
    subscription_dict = subscription[1]

    for _ in subscription_dict:
        if subscription_location_name.lower() in lower_case_locations_list:
            try:
                subscription_warning_severity = subscription_dict[str(warn_type.value)]
                if subscription_warning_severity <= warning.severity.value:
                    return True
            except KeyError:
                return False

    return False
