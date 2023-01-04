import data_service
import sender
import nina_service
import controller


def warn_users():
    chat_ids_of_warned_users = data_service.get_chat_ids_of_warned_users()

    for warning in nina_service.get_all_active_warnings():
        for chat_id in chat_ids_of_warned_users:
            if should_user_receive_this_warning(warning):
                controller.general_warning(chat_id, nina_service.WarnType.NONE, [warning])
                if chat_id == 1770942669:
                    print(warning)




def should_user_receive_this_warning(warning: nina_service.WarnType) -> bool:
    return True


warn_users()
