import data_service
import sender
import nina_service
import controller
import time
import place_converter


# TODO nina_service _get_detailed_warning_infos has to be refactored to not throw KeyErrors
# For further explaination see:
# https://discord.com/channels/1031862018925404211/1031863544918065192/1060613157715976284

def start():
    # TODO Check if there are any updates to the list returned from get_all_active_warnings()
    while True:
        warn_users()
        time.sleep(120)  # 2 minutes


def warn_users():
    chat_ids_of_warned_users = data_service.get_chat_ids_of_warned_users()

    print(nina_service.get_all_active_warnings())
    for (warning, warn_type) in nina_service.get_all_active_warnings():
        for chat_id in chat_ids_of_warned_users:
            if _should_user_receive_this_warning(chat_id, warning, warn_type):
                # send warning out to user
                print("Warning will be sent out!")
                controller.general_warning(chat_id, nina_service.WarnType.NONE, [warning])
                data_service.add_warning_id_to_users_warning_list(chat_id, warning.id)


def _should_user_receive_this_warning(chat_id: int, warning: nina_service.GeneralWarning,
                                      warn_type: nina_service.WarnType) -> bool:
    """
    He should receive the warning given as parameter when...
    :return: True if for any of the useres subscriptions the warning is relevant
    """
    if data_service.has_user_already_received_warning(chat_id, warning.id):
        return False
    subscriptions = data_service.get_subscriptions(chat_id)
    for subscription in subscriptions.items():
        if _is_warning_relevant_for_subscription(warning, subscription, warn_type):
            print("The following warning is relevant for user: ")
            print(warning)
            return True
    return False


# TODO comment in the code snippets after refactoring from Lauren (marked with TODO)
def _is_warning_relevant_for_subscription(warning: nina_service.GeneralWarning, subscription: tuple,
                                          warn_type: nina_service.WarnType) -> bool:
    subscription_dict = subscription[1]

    # TODO Use this
    # subscription_location_id = subscription[0]
    subscription_location_name = subscription[0]

    # TODO Use this
    # for nina_places.get_name_for_id(subscription_location_name) in subscription_dict:
    for subscription_warning_type in subscription_dict:
        if subscription_location_name.lower() in list(map(lambda s: s.lower(), nina_service.get_warning_locations(warning))):
            print("The user has subscribed to the warning location: " + subscription_location_name)
            try:
                subscription_warning_severity = subscription_dict[
                    warn_type.name.lower()]  # TODO handle conversion from database warn_type to nina_service warn_type better
                if subscription_warning_severity == warning.severity.value:
                    return True
                print(
                    "The user has subscribed to the location and type, but the warning_severity is not relevant for him")
            except KeyError:
                print("The type of the warning is not in the users subscription")
                return False

    print("Warning is not relevant for subscription.")
    return False


warn_users()
