import data_service
import sender
import nina_service
import controller
import time


def start():
    # TODO Check if there are any updates to the list returned from get_all_active_warnings()
    while True:
        warn_users()
        time.sleep(120)  # 2 minutes


def warn_users():
    chat_ids_of_warned_users = data_service.get_chat_ids_of_warned_users()

    # TODO bei get_active_warnings noch den Typ mit speichern
    print(nina_service.get_all_active_warnings())
    for (warning, warn_type) in nina_service.get_all_active_warnings():
        for chat_id in chat_ids_of_warned_users:
            if _should_user_receive_this_warning(chat_id, warning, warn_type):
                # send warning out to user
                controller.general_warning(chat_id, nina_service.WarnType.NONE, [warning])


def _should_user_receive_this_warning(chat_id: int, warning: nina_service.GeneralWarning,
                                      warn_type: nina_service.WarnType) -> bool:
    """
    He should receive the warning given as parameter when...
    :return: True if for any of the useres subscriptions the warning is relevant
    """
    if has_user_received_this_warning_before(chat_id, warning):
        return False
    subscriptions = data_service.get_subscriptions(chat_id)
    for subscription in subscriptions.items():
        if _is_warning_relevant_for_subscription(warning, subscription, warn_type):
            print("The following warning is relevant for user: ")
            print(warning)
            return True
    return False


def _is_warning_relevant_for_subscription(warning: nina_service.GeneralWarning, subscription: tuple,
                                          warn_type: nina_service.WarnType) -> bool:
    subscription_dict = subscription[1]
    subscription_location_name = subscription[0]
    for subscription_warning_type in subscription_dict:
        if subscription_location_name.lower() in list(map(lambda s: s.lower(), get_warning_locations(warning))):
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


# TODO move this to nina_service.py
def get_warning_locations(warning: nina_service.GeneralWarning):
    # Retrieve warning_location out of detailed_warning
    #   this information is saved in DetailedWarningInfoArea.area_description as for example "Stubenberg, Tann, Triftern, Unterdietfurt, Wittibreut, Wurmannsquick"
    detailed_warning = nina_service.get_detailed_warning(warning.id)
    locations = []
    for info in detailed_warning.infos:
        for area in info.area:
            for location in area.area_description.split(", "):
                locations.append(location)


    locations.append("Darmstadt") # TODO remove (just for debugging)
    return locations


def has_user_received_this_warning_before(chat_id: int, warning: nina_service.GeneralWarning):
    # TODO implement
    return False


warn_users()
