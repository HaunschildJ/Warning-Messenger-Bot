import telebot.types as typ

import bot
import controller
import data_service
import error
import frontend_helper
import warning_handler

from enum_types import Commands, WarningCategory, ErrorCodes

bot = bot.bot


# filter for callback handlers -----------------------------------------------------------------------------------------


def filter_callback_manual_warning_covid(call: typ.CallbackQuery) -> bool:
    split_data = call.data.split(';')
    if split_data[0] == Commands.COVID_INFO.value or split_data[0] == Commands.COVID_RULES.value:
        return True
    return False


def filter_callback_manual_warning_other(call: typ.CallbackQuery) -> bool:
    split_data = call.data.split(';')
    if split_data[0] == Commands.WEATHER.value or split_data[0] == Commands.CIVIL_PROTECTION.value \
            or split_data[0] == Commands.FLOOD.value:
        return True
    return False


def filter_callback_cancel(call: typ.CallbackQuery) -> bool:
    if call.data == Commands.CANCEL_INLINE.value:
        return True
    return False


def filter_callback_just_cancel(call: typ.CallbackQuery) -> bool:
    if call.data == Commands.JUST_CANCEL_INLINE.value:
        return True
    return False


def filter_callback_auto_warning(call: typ.CallbackQuery) -> bool:
    split_data = call.data.split(' ')
    if split_data[0] == Commands.AUTO_WARNING.value and (split_data[1] == "True" or split_data[1] == "False"):
        return True
    return False


def filter_callback_add_subscription(call: typ.CallbackQuery) -> bool:
    split_data = call.data.split(';')
    if split_data[0] == Commands.ADD_SUBSCRIPTION.value:
        return True
    return False


def filter_callback_delete_subscription(call: typ.CallbackQuery) -> bool:
    split_data = call.data.split(';')
    if split_data[0] == Commands.DELETE_SUBSCRIPTION.value:
        return True
    return False


def filter_callback_auto_covid_updates(call: typ.CallbackQuery) -> bool:
    split_data = call.data.split(' ')
    if split_data[0] == Commands.COVID_UPDATES.value:
        return True
    return False


def filter_callback_add_recommendation(call: typ.CallbackQuery) -> bool:
    split_data = call.data.split(';')
    if split_data[0] == Commands.ADD_RECOMMENDATION.value:
        return True
    return False


def filter_callback_set_default_level(call: typ.CallbackQuery) -> bool:
    split_data = call.data.split(';')
    if split_data[0] == Commands.SET_DEFAULT_LEVEL.value:
        return True
    return False


def filter_callback_delete_data(call: typ.CallbackQuery) -> bool:
    data = call.data
    if data == Commands.DELETE_DATA_SUBSCRIPTIONS.value or data == Commands.DELETE_DATA_FAVORITES.value \
            or data == Commands.DELETE_DATA_EVERYTHING.value:
        return True
    return False


def filter_callback_send_emergency_pdf(call: typ.CallbackQuery) -> bool:
    data = call.data
    if data == Commands.SEND_PDF.value:
        return True
    return False


# filter for message handler -------------------------------------------------------------------------------------------


def filter_normal_message(message: typ.Message) -> bool:
    if message.text[0] == "/":
        return False
    return True


def filter_command_message(message: typ.Message) -> bool:
    if message.text[0] != "/":
        return False
    return True


# bot message handlers -------------------------------------------------------------------------------------------------


@bot.message_handler(func=filter_normal_message)
def normal_message_handler(message: typ.Message):
    chat_id = message.chat.id
    state = str(data_service.get_user_state(chat_id))
    state_first_number = int(state[0])
    text = message.text
    if text == frontend_helper.BACK_TO_MAIN_TEXT:
        frontend_helper.back_to_main_keyboard(chat_id)
        return
    if state_first_number == 0:  # 0
        # Main Menu: there are no substates in the Main Menu
        controller.main_button_pressed(chat_id, text)
        return
    elif state_first_number == 1:  # 1?
        # Settings
        if len(state) == 1:  # 1
            # button in Settings was pressed
            controller.button_in_settings_pressed(chat_id, text)
            return
        else:
            # sub-state of Settings
            state_second_number = int(state[1])
            if state_second_number == 0:  # 10?
                # manage subscriptions
                if len(state) == 2:  # 10
                    # button in manage subscriptions was pressed
                    controller.button_in_subscriptions_pressed(chat_id, text)
                    return
                else:
                    # sub-state of manage subscriptions
                    state_third_number = int(state[2])
                    if state_third_number == 1:  # 101?
                        # add subscription
                        controller.location_for_adding_subscription(chat_id, text)
                        return
                    elif state_third_number == 2 or state_third_number == 3 or state_third_number == 4:  # 102? - 104?
                        # deleting a subscription or default warning level or silence subscriptions
                        # --> they don't expect an input
                        error.error_handler(chat_id, ErrorCodes.NO_INPUT_EXPECTED, state=int(state), message=text)
                        return
                    else:  # 105? - 109?
                        error.illegal_state_handler(chat_id, int(state))
                        return
            elif state_second_number == 1:  # 11?
                # add location favorites
                controller.location_for_favorites(chat_id, text)
                return
            elif state_second_number == 2:  # 12?
                # delete data
                controller.button_in_delete_data_pressed(chat_id, text)
                return
            else:  # 13? - 19?
                error.illegal_state_handler(chat_id, int(state))
                return
    elif state_first_number == 2:  # 2?
        # manual warnings
        if len(state) == 1:  # 2
            # button in manual warnings was pressed
            controller.button_in_manual_warnings_pressed(chat_id, text)
            return
        else:
            # sub-state of manual warnings
            state_second_number = int(state[1])
            if state_second_number == 0:  # 20?
                # Covid
                if len(state) == 2:  # 20
                    # button in covid was pressed (either covid info or covid rules)
                    controller.button_in_manual_warnings_pressed(chat_id, text)
                    return
                else:
                    state_third_number = int(state[2])
                    if state_third_number == 0:  # 200?
                        controller.location_for_warning(chat_id, text, Commands.COVID_INFO)
                        return
                    elif state_third_number == 1:  # 201?
                        controller.location_for_warning(chat_id, text, Commands.COVID_RULES)
                        return
                    else:  # 202? - 209?
                        error.illegal_state_handler(chat_id, int(state))
                        return
            elif state_second_number == 1:  # 21?
                # Weather
                controller.location_for_warning(message.chat.id, text, Commands.WEATHER)
                return
            elif state_second_number == 2:  # 22?
                # Disaster
                controller.location_for_warning(message.chat.id, text, Commands.CIVIL_PROTECTION)
                return
            elif state_second_number == 3:  # 23?
                # Flood
                controller.location_for_warning(message.chat.id, text, Commands.FLOOD)
                return
            else:  # 24? - 29?
                error.illegal_state_handler(chat_id, int(state))
                return
    elif state_first_number == 3:  # 3?
        controller.button_in_emergency_tips_pressed(chat_id, text)
        return
    elif state_first_number == 4:  # 4?
        controller.button_in_help_pressed(chat_id, text)
        return
    else:  # 5? - 9?
        error.illegal_state_handler(chat_id, int(state))


@bot.message_handler(func=filter_command_message)
def command_message_handler(message: typ.Message):
    chat_id = message.chat.id
    state = data_service.get_user_state(chat_id)
    text = message.text.removeprefix("/").lower()
    if error.is_start(text):
        start(message)
    elif error.is_help(text):
        controller.help_handler(chat_id, str(state))
    else:
        error.error_handler(chat_id, ErrorCodes.UNKNOWN_COMMAND)


def start(message: typ.Message):
    """
    This method is called when the user sends '/start' (mainly for the start of the conversation with the bot)
    and will then initiate the chat with the user by calling start in controller

    Args:
        message: the message that the user sent in the chat
    """
    name = message.chat.username
    if name is None:
        name = message.chat.first_name
        if name is None:
            name = "Unknown Name"
        last_name = message.chat.last_name
        if last_name is not None:
            name = name + " " + last_name
    controller.start(message.chat.id, name)


# ------------------------ message handler for location


@bot.message_handler(content_types=['location'])
def send_location_pressed(message: typ.Message):
    """
    This method is called whenever the user sends a location in the chat and will give the location to the controller

    Args:
        message: the message that the user sent in the chat
    """
    long = message.location.longitude
    lat = message.location.latitude
    controller.location_was_sent(message.chat.id, latitude=lat, longitude=long)


# bot callback handlers ------------------------------------------------------------------------------------------------


@bot.callback_query_handler(func=filter_callback_manual_warning_covid)
def covid_button(call: typ.CallbackQuery):
    """
    This method is a callback_handler for the covid inline buttons and will call the methods needed to give the user
    the desired output \n
    It will also delete the inline buttons

    Args:
        call: data that has been sent by the inline button
    """
    chat_id = call.message.chat.id
    covid_helper(chat_id, call.data)
    controller.delete_message(chat_id, call.message.id)


@bot.callback_query_handler(func=filter_callback_manual_warning_other)
def other_warnings_button(call: typ.CallbackQuery):
    """
    This method is a callback_handler for the warning (weather, civil protection, flood) inline buttons (suggestions)
    and will call the methods needed to give the user the desired output \n
    It will also delete the inline buttons

    Args:
        call: data that has been sent by the inline button
    """
    chat_id = call.message.chat.id
    split_message = call.data.split(';')
    if len(split_message) < 3:
        error.error_handler(chat_id, ErrorCodes.CALLBACK_MISTAKE)
        return
    postal_code = split_message[1]
    district_id = split_message[2]
    if split_message[0] == Commands.WEATHER.value:
        controller.detailed_general_warning(chat_id, WarningCategory.WEATHER, postal_code, district_id)
    elif split_message[0] == Commands.CIVIL_PROTECTION.value:
        controller.detailed_general_warning(chat_id, WarningCategory.CIVIL_PROTECTION, postal_code, district_id)
    elif split_message[0] == Commands.FLOOD.value:
        controller.detailed_general_warning(chat_id, WarningCategory.FLOOD, postal_code, district_id)
    else:
        error.error_handler(chat_id, ErrorCodes.CALLBACK_MISTAKE)
    controller.delete_message(chat_id, call.message.id)


@bot.callback_query_handler(func=filter_callback_auto_warning)
def auto_warning_button(call: typ.CallbackQuery):
    """
    This method is a callback_handler for the automatic warning inline buttons and will call the methods needed to set
    the automatic warning boolean in the database to what the user wants\n
    It will also delete the inline buttons

    Args:
        call: data that has been sent by the inline button
    """
    chat_id = call.message.chat.id
    value = False
    if call.data == Commands.AUTO_WARNING.value + " True":
        value = True
    controller.change_auto_warning_in_database(chat_id, value)
    controller.delete_message(chat_id, call.message.id)


@bot.callback_query_handler(func=filter_callback_auto_covid_updates)
def auto_covid_updates_button(call: typ.CallbackQuery):
    """
    This method is a callback_handler for the automatic covid updates inline buttons and will call the methods needed
    to set the automatic covid updates int in the database to what the user wants\n
    It will also delete the inline buttons

    Args:
        call: data that has been sent by the inline button
    """
    chat_id = call.message.chat.id
    split_data = call.data.split(' ')
    if len(split_data) != 2:
        error.error_handler(chat_id, ErrorCodes.CALLBACK_MISTAKE)

    controller.change_auto_covid_updates_in_database(chat_id, int(split_data[1]))
    controller.delete_message(chat_id, call.message.id)


@bot.callback_query_handler(func=filter_callback_add_subscription)
def add_subscription_callback(call: typ.CallbackQuery):
    """
    This method is a callback_handler for the inline buttons when adding a subscription

    Args:
        call: data that has been sent by the inline button
    """
    chat_id = call.message.chat.id
    controller.inline_button_for_adding_subscriptions(chat_id, call.data)
    controller.delete_message(chat_id, call.message.id)


@bot.callback_query_handler(func=filter_callback_delete_subscription)
def delete_subscription_callback(call: typ.CallbackQuery):
    """
    This method is a callback_handler for the inline buttons when deleting a subscription

    Args:
        call: data that has been sent by the inline button
    """
    chat_id = call.message.chat.id
    controller.inline_button_for_deleting_subscriptions(chat_id, call.data)


@bot.callback_query_handler(func=filter_callback_cancel)
def cancel_button(call: typ.CallbackQuery):
    """
    This method is a callback_handler for cancel inline buttons and will delete the inline buttons

    Args:
        call: data that has been sent by the inline button
    """
    controller.delete_message(call.message.chat.id, call.message.id)
    frontend_helper.back_to_main_keyboard(call.message.chat.id)


@bot.callback_query_handler(func=filter_callback_just_cancel)
def just_cancel_button(call: typ.CallbackQuery):
    """
    This method is a callback_handler for cancel inline buttons and will delete the inline buttons

    Args:
        call: data that has been sent by the inline button
    """
    controller.delete_message(call.message.chat.id, call.message.id)


@bot.callback_query_handler(func=filter_callback_add_recommendation)
def add_recommendation(call: typ.CallbackQuery):
    """
    This method is called whenever the user presses a button for adding a recommendation

    Args:
        call: data that has been sent by the inline button
    """
    split_message = call.data.split(';')
    if len(split_message) < 3:
        error.error_handler(call.message.chat.id, ErrorCodes.CALLBACK_MISTAKE)
        return
    postal_code = split_message[1]
    district_id = split_message[2]
    controller.add_recommendation_in_database(call.message.chat.id, postal_code, district_id)
    controller.delete_message(call.message.chat.id, call.message.id)


@bot.callback_query_handler(func=filter_callback_set_default_level)
def set_default_level(call: typ.CallbackQuery):
    """
    This method gets called when the user selects a default level for all Warnings

    Args:
        call: data that has been sent by the inline button
    """
    split_message = call.data.split(';')
    if len(split_message) != 2:
        error.error_handler(call.message.chat.id, ErrorCodes.CALLBACK_MISTAKE)
        return
    controller.set_default_level(call.message.chat.id, split_message[1])
    controller.delete_message(call.message.chat.id, call.message.id)


@bot.callback_query_handler(func=filter_callback_delete_data)
def delete_data(call: typ.CallbackQuery):
    """
    This method gets called when the user presses yes when deleting data

    Args:
        call: data that has been sent by the inline button
    """
    controller.delete_data_confirmed(call.message.chat.id, call.data)
    controller.delete_message(call.message.chat.id, call.message.id)


@bot.callback_query_handler(func=filter_callback_send_emergency_pdf)
def send_pdf(call: typ.CallbackQuery):
    """
    This method gets called when the user presses yes when asking if the pdf should be sent

    Args:
        call: data that has been sent by the inline button
    """
    controller.send_emergency_pdf(call.message.chat.id)
    controller.delete_message(call.message.chat.id, call.message.id)


# helper methods -------------------------------------------------------------------------------------------------------


def covid_helper(chat_id: int, message_string: str):
    """
    This is a helper method for the user input handlers above \n
    With the message/text the user/button sent (message_string) this method will then call the corresponding method in
    controller so that the desired output will be sent to the user

    Args:
        chat_id: an integer for the chatID that the message is sent to
        message_string: a string of the message/text that is sent by the user/button
    """
    split_message = message_string.split(';')
    if len(split_message) < 3:
        error.error_handler(chat_id, ErrorCodes.CALLBACK_MISTAKE)
        return
    postal_code = split_message[1]
    district_id = split_message[2]
    if split_message[0] == Commands.COVID_INFO.value:
        controller.covid_info(chat_id, postal_code, district_id)
    elif split_message[0] == Commands.COVID_RULES.value:
        controller.covid_rules(chat_id, postal_code, district_id)
    else:
        error.error_handler(chat_id, ErrorCodes.CALLBACK_MISTAKE)


def start_receiver():
    print("Receiver running...")
    warning_handler.init_warning_handler()
    bot.polling()
