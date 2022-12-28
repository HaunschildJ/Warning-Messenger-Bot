import telebot.types as typ

import bot
import controller
from controller import Commands
from controller import ErrorCodes

bot = bot.bot


# filter for message handlers ------------------------------------------------------------------------------------------


def filter_covid(message: typ.Message) -> bool:
    if message.text.split(' ')[0] == Commands.COVID.value:
        return True
    return False


def filter_add_recommendation(message: typ.Message) -> bool:
    if message.text.split(' ')[0] == Commands.ADD_RECOMMENDATION.value:
        return True
    return False


def filter_callback_covid(call: typ.CallbackQuery) -> bool:
    if call.data.split(' ')[0] == Commands.COVID.value:
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
    split_data = call.data.split(' ')
    if split_data[0] == Commands.ADD_SUBSCRIPTION.value:
        return True
    return False


def filter_callback_delete_subscription(call: typ.CallbackQuery) -> bool:
    split_data = call.data.split(' ')
    if split_data[0] == Commands.DELETE_SUBSCRIPTION.value:
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


def filer_everything_else(message: typ.Message) -> bool:
    # TODO add all filter that are not callbacks here
    if filter_covid(message) or filter_add_recommendation(message) or filter_main_button(message) or \
            filter_buttons_in_settings(message) or filter_covid_for_inline(message) or \
            message.text == controller.BACK_TO_MAIN_TEXT or message.text == controller.WARNING_BIWAPP_TEXT or \
            filter_show_subscriptions(message) or filter_add_or_delete_subscription(message):
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
    controller.start(message.chat.id)


@bot.message_handler(func=filter_covid)
def covid(message: typ.Message):
    """
    This method is called when the user sends Commands.COVID.value (currently '/covid') and will call the methods
    needed to give the user the desired output
    """
    covid_helper(message.chat.id, message.text)


@bot.message_handler(func=filter_add_recommendation)
def add_recommendation(message: typ.Message):
    """
    This method is called when the user sends Commands.ADD_RECOMMENDATION.value (currently '/add') and will check if
    the format of the message is '/add string' (if not error message is sent to the user)
    """
    if len(message.text.split(' ')) == 1:
        controller.error_handler(message.chat.id, ErrorCodes.ONLY_PART_OF_COMMAND)
        return
    controller.add_recommendation_in_database(message.chat.id, message.text.split(' ')[1])


@bot.message_handler(func=filer_everything_else)
def tmp(message: typ.Message):
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
    Returns:
        Nothing
    """
    controller.show_inline_button(message.chat.id, message.text)


@bot.message_handler(regexp=controller.WARNING_BIWAPP_TEXT)
def biwapp_button_pressed(message: typ.Message):
    controller.biwapp(message.chat.id)


@bot.message_handler(regexp=controller.BACK_TO_MAIN_TEXT)
def back_to_main_keyboard(message: typ.Message):
    controller.back_to_main_keyboard(message.chat.id)


@bot.message_handler(content_types=['location'])
def send_location_pressed(message: typ.Message):
    location = [message.location.latitude, message.location.longitude]
    controller.location_was_sent(message.chat.id, location)


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


# helper methods -------------------------------------------------------------------------------------------------------


def covid_helper(chat_id: int, message_string: str) -> None:
    """
    This is a helper method for the user input handlers above \n
    With the message/text the user/button sent (message_string) this method will then call the corresponding method in
    controller so that the desired output will be sent to the user

    Arguments:
        chat_id: an integer for the chatID that the message is sent to
        message_string: a string of the message/text that is sent by the user/button
    Returns:
        Nothing
    """
    split_message = message_string.split(' ')
    if len(split_message) <= 1:
        controller.error_handler(chat_id, ErrorCodes.ONLY_PART_OF_COMMAND)
        return

    if split_message[1] == Commands.COVID_INFO.value:
        controller.covid_info(chat_id, split_message[2])
    elif split_message[1] == Commands.COVID_RULES.value:
        controller.covid_rules(chat_id, split_message[2])
    else:
        controller.error_handler(chat_id, ErrorCodes.ONLY_PART_OF_COMMAND)


bot.polling()
