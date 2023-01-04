import data_service
import sender
import nina_service
import controller


def warn_users():
    chat_ids_of_warned_users = data_service.get_chat_ids_of_warned_users()

    for warning in nina_service.get_all_active_warnings():
        for chat_id in chat_ids_of_warned_users:
            if should_user_receive_this_warning(chat_id, warning):
                controller.general_warning(chat_id, nina_service.WarnType.NONE, [warning])
                if chat_id == 1770942669:
                    nina_service.get_detailed_warning(warning.id)
                    print(nina_service.get_detailed_warning(warning.id))




def should_user_receive_this_warning(chat_id: int, warning: nina_service.GeneralWarning) -> bool:
    # Call nina_service.get_detailed_warning(warning.id)
    # Get User subscriptions: data_service.get_subscriptions(chat_id)
    # For each subscription check if the given warning is relevant for that subscription
    #   use is_warning_relevant_for_subscription(warning, subscription)
    # Return True if there is any
    # Return False else
    return True


def is_warning_relevant_for_subscription(warning: nina_service.GeneralWarning, subscription: dict) -> bool:
    # location_name = subscription...
    # list( (subscription_warn_type1, subscription_warn_level1), ...)
    # Retrieve warning_location out of detailed_warning
    #   this information is saved in DetailedWarningInfoArea.area_description as for example "Stubenberg, Tann, Triftern, Unterdietfurt, Wittibreut, Wurmannsquick"
    # Return True if
    #   if warning_location contains location_name
    #       and any of (subscription_warn_type = warning_warn_type and subscription_warn_level =warning_warn_level)
    # Return false else
    return True



warn_users()
