import telebot.types as typ

import bot
import controller
from controller import Commands
from controller import ErrorCodes
from nina_service import WarnType
import data_service

bot = bot.bot


# filter for message handlers ------------------------------------------------------------------------------------------


def filter_callback_covid(call: typ.CallbackQuery) -> bool:
    if call.data.split(';')[0] == Commands.COVID.value:
        return True
    return False


def filter_callback_cancel(call: typ.CallbackQuery) -> bool:
    if call.data == Commands.CANCEL_INLINE.value:
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
    split_data = call.data.split(' ')
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


def filter_covid(message: typ.Message) -> bool:
    if message.text.split(';')[0] == Commands.COVID.value:
        return True
    return False


def filter_main_button(message: typ.Message) -> bool:
    if message.text == controller.SETTING_BUTTON_TEXT or message.text == controller.WARNING_BUTTON_TEXT or \
            message.text == controller.TIP_BUTTON_TEXT or message.text == controller.HELP_BUTTON_TEXT:
        return True
    return False


def filter_buttons_in_settings(message: typ.Message) -> bool:
    text = message.text
    if text == controller.SETTING_AUTO_WARNING_TEXT or text == controller.SETTING_SUGGESTION_LOCATION_TEXT or \
            text == controller.SETTING_SUBSCRIPTION_TEXT or text == controller.SETTING_AUTO_COVID_INFO_TEXT or \
            text == controller.SETTING_LANGUAGE_TEXT:
        return True
    return False


def filter_covid_for_inline(message: typ.Message) -> bool:
    if message.text == controller.WARNING_COVID_RULES_TEXT or message.text == controller.WARNING_COVID_INFO_TEXT:
        return True
    return False


def filter_show_subscriptions(message: typ.Message) -> bool:
    if message.text == controller.SHOW_SUBSCRIPTION_TEXT:
        return True
    return False


def filter_add_or_delete_subscription(message: typ.Message) -> bool:
    if message.text == controller.ADD_SUBSCRIPTION_TEXT or message.text == controller.DELETE_SUBSCRIPTION_TEXT:
        return True
    return False


def filter_general_warning(message: typ.Message) -> bool:
    t = message.text
    if t == controller.WARNING_DISASTER_TEXT or t == controller.WARNING_FLOOD_TEXT or \
            t == controller.WARNING_WEATHER_TEXT or \
            t == controller.WARNING_GENERAL_TEXT:
        if data_service.get_user_state(message.chat.id) == 2:
            return True
    return False


def filer_everything_else(message: typ.Message) -> bool:
    # TODO add all filter that are not callbacks here
    if filter_covid(message) or filter_main_button(message) or \
            filter_buttons_in_settings(message) or filter_covid_for_inline(message) or \
            message.text == controller.BACK_TO_MAIN_TEXT or message.text == controller.WARNING_WEATHER_TEXT or \
            filter_show_subscriptions(message) or filter_add_or_delete_subscription(message) or \
            filter_general_warning(message):
        return False
    return True


# bot message handlers -------------------------------------------------------------------------------------------------


@bot.message_handler(commands=['start'])
def start(message: typ.Message):
    """
    This method is called when the user sends '/start' (mainly for the start of the conversation with the bot)
    and will then initiate the chat with the user by calling start in controller

    Arguments:
        message: the message that the user sent in the chat
    Returns:
        Nothing
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


@bot.message_handler(func=filter_covid)
def covid(message: typ.Message):
    """
    This method is called when the user sends Commands.COVID.value (currently '/covid') and will call the methods
    needed to give the user the desired output
    """
    covid_helper(message.chat.id, message.text)


@bot.message_handler(func=filer_everything_else)
def everything_else(message: typ.Message):
    controller.normal_input_depending_on_state(message.chat.id, message.text)


# ------------------------ message handlers for buttons


@bot.message_handler(func=filter_main_button)
def main_menu_button(message: typ.Message):
    controller.main_button_pressed(message.chat.id, message.text)


@bot.message_handler(func=filter_buttons_in_settings)
def button_in_settings_pressed(message: typ.Message):
    controller.button_in_settings_pressed(message.chat.id, message.text)


@bot.message_handler(func=filter_covid_for_inline)
def covid_for_inline(message: typ.Message):
    """
    When 'Corona Infos' (controller.COVID_INFO_TEXT) or 'Corona Rules' (controller.COVID_RULES_TEXT) is sent in a chat
    this method gets called (mainly for the keyboard buttons) and will then call the method to show the corresponding
    inline buttons in the chat

    Arguments:
        message: the message that the user sent in the chat
    """
    controller.show_suggestions(message.chat.id, message.text)


@bot.message_handler(func=filter_general_warning)
def general_warning_button_pressed(message: typ.Message):
    t = message.text
    if t == controller.WARNING_DISASTER_TEXT:
        controller.general_warning(message.chat.id, WarnType.DISASTER)
    elif t == controller.WARNING_FLOOD_TEXT:
        controller.general_warning(message.chat.id, WarnType.FLOOD)
    elif t == controller.WARNING_WEATHER_TEXT:
        controller.general_warning(message.chat.id, WarnType.WEATHER)
    elif t == controller.WARNING_GENERAL_TEXT:
        controller.general_warning(message.chat.id, WarnType.GENERAL)


@bot.message_handler(regexp=controller.BACK_TO_MAIN_TEXT)
def back_to_main_keyboard(message: typ.Message):
    controller.back_to_main_keyboard(message.chat.id)


@bot.message_handler(content_types=['location'])
def send_location_pressed(message: typ.Message):
    long = message.location.longitude
    lat = message.location.latitude
    controller.location_was_sent(message.chat.id, latitude=lat, longitude=long)


@bot.message_handler(func=filter_show_subscriptions)
def show_subscription_pressed(message: typ.Message):
    controller.show_subscriptions(message.chat.id)


@bot.message_handler(func=filter_add_or_delete_subscription)
def add_or_delete_subscription_pressed(message: typ.Message):
    controller.button_in_subscriptions_pressed(message.chat.id, message.text)


# bot callback handlers ------------------------------------------------------------------------------------------------


@bot.callback_query_handler(func=filter_callback_covid)
def covid_button(call: typ.CallbackQuery):
    """
    This method is a callback_handler for the covid inline buttons and will call the methods needed to give the user
    the desired output \n
    It will also delete the inline buttons

    Arguments:
        call: data that has been sent by the inline button
    """
    chat_id = call.message.chat.id
    covid_helper(chat_id, call.data)
    controller.delete_message(chat_id, call.message.id)


@bot.callback_query_handler(func=filter_callback_auto_warning)
def auto_warning_button(call: typ.CallbackQuery):
    """
    This method is a callback_handler for the automatic warning inline buttons and will call the methods needed to set
    the automatic warning boolean in the database to what the user wants\n
    It will also delete the inline buttons

    Arguments:
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

    Arguments:
        call: data that has been sent by the inline button
    """
    chat_id = call.message.chat.id
    split_data = call.data.split(' ')
    if len(split_data) != 2:
        controller.error_handler(chat_id, ErrorCodes.ONLY_PART_OF_COMMAND)

    controller.change_auto_covid_updates_in_database(chat_id, int(split_data[1]))
    controller.delete_message(chat_id, call.message.id)


@bot.callback_query_handler(func=filter_callback_add_subscription)
def add_subscription_callback(call: typ.CallbackQuery):
    """
    This method is a callback_handler for the inline buttons when adding a subscription

    Arguments:
        call: data that has been sent by the inline button
    """
    chat_id = call.message.chat.id
    controller.inline_button_for_adding_subscriptions(chat_id, call.data)
    controller.delete_message(chat_id, call.message.id)


@bot.callback_query_handler(func=filter_callback_delete_subscription)
def delete_subscription_callback(call: typ.CallbackQuery):
    """
    This method is a callback_handler for the inline buttons when deleting a subscription

    Arguments:
        call: data that has been sent by the inline button
    """
    chat_id = call.message.chat.id
    controller.inline_button_for_deleting_subscriptions(chat_id, call.data)


@bot.callback_query_handler(func=filter_callback_cancel)
def cancel_button(call: typ.CallbackQuery):
    """
    This method is a callback_handler for cancel inline buttons and will delete the inline buttons

    Arguments:
        call: data that has been sent by the inline button
    """
    controller.delete_message(call.message.chat.id, call.message.id)
    controller.back_to_main_keyboard(call.message.chat.id)


@bot.callback_query_handler(func=filter_callback_add_recommendation)
def add_recommendation(call: typ.CallbackQuery):
    split_message = call.data.split(';')
    if len(split_message) < 3:
        controller.error_handler(call.message.chat.id, ErrorCodes.ONLY_PART_OF_COMMAND)
        return
    place_id = split_message[1]
    district_id = split_message[2]
    controller.add_recommendation_in_database(call.message.chat.id, place_id, district_id)
    controller.delete_message(call.message.chat.id, call.message.id)


# helper methods -------------------------------------------------------------------------------------------------------


def covid_helper(chat_id: int, message_string: str):
    """
    This is a helper method for the user input handlers above \n
    With the message/text the user/button sent (message_string) this method will then call the corresponding method in
    controller so that the desired output will be sent to the user

    Arguments:
        chat_id: an integer for the chatID that the message is sent to
        message_string: a string of the message/text that is sent by the user/button
    """
    split_message = message_string.split(';')
    if len(split_message) < 4:
        controller.error_handler(chat_id, ErrorCodes.ONLY_PART_OF_COMMAND)
        return
    place_id = split_message[2]
    district_id = split_message[3]
    if split_message[1] == Commands.COVID_INFO.value:
        controller.covid_info(chat_id, None, district_id)
    elif split_message[1] == Commands.COVID_RULES.value:
        controller.covid_rules(chat_id, None, district_id)
    else:
        controller.error_handler(chat_id, ErrorCodes.ONLY_PART_OF_COMMAND)


bot.polling()
