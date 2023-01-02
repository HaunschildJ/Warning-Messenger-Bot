import data_service
import sender
import nina_service

dispatcher = {
    "biwapp": nina_service.poll_biwapp_warning,
    "weather": nina_service.poll_dwd_warning
}


# TODO durch aktiven warnungen iterieren und dann durch alle nutzer und schauen ob er diese warnung gerade will

def warn_users():
    for chat_id in data_service.get_warned_users():
        warn_user(chat_id)


def warn_user(chat_id: int):
    subscriptions = data_service.get_subscriptions(chat_id)
    for subscription in subscriptions.items():
        # subscription: ('Darmstadt', {'weather': 4, 'biwapp': 5})
        for warn_type in data_service.get_warn_types_for_subscription(subscription):
            warning_level = subscription[1][warn_type]
            warning = dispatcher[warn_type]()
            sender.send_message(chat_id)


# TODO check if warning was already sent


warn_users()
