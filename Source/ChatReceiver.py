import telebot.types as typ

import Bot
import Controller
from Controller import Commands
from Controller import ErrorCodes

bot = Bot.bot


# filter for message handlers ------------------------------------------------------------------------------------------


def filter_corona(message: typ.Message) -> bool:
    if message.text.split(' ')[0] == Commands.CORONA.value:
        return True
    return False


def filter_add_recommendation(message: typ.Message) -> bool:
    if message.text.split(' ')[0] == Commands.ADD_RECOMMENDATION.value:
        return True
    return False


def filter_callback_corona(call: typ.CallbackQuery) -> bool:
    if call.data.split(' ')[0] == Commands.CORONA.value:
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
    if message.text == Controller.SETTING_BUTTON_TEXT or message.text == Controller.WARNING_BUTTON_TEXT or \
            message.text == Controller.TIP_BUTTON_TEXT or message.text == Controller.HELP_BUTTON_TEXT:
        return True
    return False


def filter_buttons_in_settings(message: typ.Message) -> bool:
    text = message.text
    if text == Controller.SETTING_AUTO_WARNING_TEXT or text == Controller.SETTING_SUGGESTION_LOCATION_TEXT or \
            text == Controller.SETTING_SUBSCRIPTION_TEXT or text == Controller.SETTING_AUTO_COVID_INFO_TEXT or \
            text == Controller.SETTING_LANGUAGE_TEXT:
        return True
    return False


def filter_corona_for_inline(message: typ.Message) -> bool:
    if message.text == Controller.WARNING_COVID_RULES_TEXT or message.text == Controller.WARNING_COVID_INFO_TEXT:
        return True
    return False


def filter_show_subscriptions(message: typ.Message) -> bool:
    if message.text == Controller.SHOW_SUBSCRIPTION_TEXT:
        return True
    return False


def filter_add_or_delete_subscription(message: typ.Message) -> bool:
    if message.text == Controller.ADD_SUBSCRIPTION_TEXT or message.text == Controller.DELETE_SUBSCRIPTION_TEXT:
        return True
    return False


def filer_everything_else(message: typ.Message) -> bool:
    # TODO add all filter that are not callbacks here
    if filter_corona(message) or filter_add_recommendation(message) or filter_main_button(message) or \
            filter_buttons_in_settings(message) or filter_corona_for_inline(message) or \
            message.text == Controller.BACK_TO_MAIN_TEXT or message.text == Controller.WARNING_BIWAPP_TEXT or \
            filter_show_subscriptions(message) or filter_add_or_delete_subscription(message):
        return False
    return True


# bot message handlers -------------------------------------------------------------------------------------------------


@bot.message_handler(commands=['start'])
def start(message: typ.Message):
    """
    This method is called when the user sends '/start' (mainly for the start of the conversation with the bot)
    and will then initiate the chat with the user by calling start in Controller

    Arguments:
        message: the message that the user sent in the chat
    Returns:
        Nothing
    """
    Controller.start(message.chat.id)


@bot.message_handler(func=filter_corona)
def corona(message: typ.Message):
    """
    This method is called when the user sends Commands.CORONA.value (currently '/corona') and will call the methods
    needed to give the user the desired output
    """
    corona_helper(message.chat.id, message.text)


@bot.message_handler(func=filter_add_recommendation)
def add_recommendation(message: typ.Message):
    """
    This method is called when the user sends Commands.ADD_RECOMMENDATION.value (currently '/add') and will check if
    the format of the message is '/add string' (if not error message is sent to the user)
    """
    if len(message.text.split(' ')) == 1:
        Controller.error_handler(message.chat.id, ErrorCodes.ONLY_PART_OF_COMMAND)
        return
    Controller.add_recommendation_in_database(message.chat.id, message.text.split(' ')[1])


@bot.message_handler(func=filer_everything_else)
def tmp(message: typ.Message):
    Controller.normal_input_depending_on_state(message.chat.id, message.text)


# ------------------------ message handlers for buttons


@bot.message_handler(func=filter_main_button)
def main_menu_button(message: typ.Message):
    Controller.main_button_pressed(message.chat.id, message.text)


@bot.message_handler(func=filter_buttons_in_settings)
def button_in_settings_pressed(message: typ.Message):
    Controller.button_in_settings_pressed(message.chat.id, message.text)


@bot.message_handler(func=filter_corona_for_inline)
def corona_for_inline(message: typ.Message):
    """
    When 'Corona Infos' (Controller.CORONA_INFO_TEXT) or 'Corona Rules' (Controller.CORONA_RULES_TEXT) is sent in a chat
    this method gets called (mainly for the keyboard buttons) and will then call the method to show the corresponding
    inline buttons in the chat

    Arguments:
        message: the message that the user sent in the chat
    Returns:
        Nothing
    """
    Controller.show_inline_button(message.chat.id, message.text)


@bot.message_handler(regexp=Controller.WARNING_BIWAPP_TEXT)
def biwapp_button_pressed(message: typ.Message):
    Controller.biwapp(message.chat.id)


@bot.message_handler(regexp=Controller.BACK_TO_MAIN_TEXT)
def back_to_main_keyboard(message: typ.Message):
    Controller.back_to_main_keyboard(message.chat.id)


@bot.message_handler(content_types=['location'])
def send_location_pressed(message: typ.Message):
    location = [message.location.latitude, message.location.longitude]
    Controller.location_was_sent(message.chat.id, location)


@bot.message_handler(func=filter_show_subscriptions)
def show_subscription_pressed(message: typ.Message):
    Controller.show_subscriptions(message.chat.id)


@bot.message_handler(func=filter_add_or_delete_subscription)
def add_or_delete_subscription_pressed(message: typ.Message):
    Controller.button_in_subscriptions_pressed(message.chat.id, message.text)


# bot callback handlers ------------------------------------------------------------------------------------------------


@bot.callback_query_handler(func=filter_callback_corona)
def corona_button(call: typ.CallbackQuery):
    """
    This method is a callback_handler for the corona inline buttons and will call the methods needed to give the user
    the desired output \n
    It will also delete the inline buttons

    Arguments:
        call: Data that has been sent by the inline button
    """
    chat_id = call.message.chat.id
    corona_helper(chat_id, call.data)
    Controller.delete_message(chat_id, call.message.id)


@bot.callback_query_handler(func=filter_callback_auto_warning)
def auto_warning_button(call: typ.CallbackQuery):
    """
    This method is a callback_handler for the automatic warning inline buttons and will call the methods needed to set
    the automatic warning boolean in the database to what the user wants\n
    It will also delete the inline buttons

    Arguments:
        call: Data that has been sent by the inline button
    """
    chat_id = call.message.chat.id
    value = False
    if call.data == Commands.AUTO_WARNING.value + " True":
        value = True
    Controller.change_auto_warning_in_database(chat_id, value)
    Controller.delete_message(chat_id, call.message.id)


@bot.callback_query_handler(func=filter_callback_add_subscription)
def add_subscription_callback(call: typ.CallbackQuery):
    """
    This method is a callback_handler for the inline buttons when adding a subscription

    Arguments:
        call: Data that has been sent by the inline button
    """
    chat_id = call.message.chat.id
    Controller.inline_button_for_adding_subscriptions(chat_id, call.data)
    Controller.delete_message(chat_id, call.message.id)


@bot.callback_query_handler(func=filter_callback_delete_subscription)
def delete_subscription_callback(call: typ.CallbackQuery):
    """
    This method is a callback_handler for the inline buttons when deleting a subscription

    Arguments:
        call: Data that has been sent by the inline button
    """
    chat_id = call.message.chat.id
    Controller.inline_button_for_deleting_subscriptions(chat_id, call.data)


@bot.callback_query_handler(func=filter_callback_cancel)
def cancel_button(call: typ.CallbackQuery):
    """
    This method is a callback_handler for cancel inline buttons and will delete the inline buttons

    Arguments:
        call: Data that has been sent by the inline button
    """
    Controller.delete_message(call.message.chat.id, call.message.id)
    Controller.back_to_main_keyboard(call.message.chat.id)


# helper methods -------------------------------------------------------------------------------------------------------


def corona_helper(chat_id: int, message_string: str):
    """
    This is a helper method for the user input handlers above \n
    With the message/text the user/button sent (message_string) this method will then call the corresponding method in
    Controller so that the desired output will be sent to the user

    Arguments:
        chat_id: an integer for the chatID that the message is sent to
        message_string: a string of the message/text that is sent by the user/button
    Returns:
        Nothing
    """
    split_message = message_string.split(' ')
    if split_message[1] == Commands.CORONA_INFO.value:
        Controller.corona_info(chat_id, split_message[2])
    elif split_message[1] == Commands.CORONA_RULES.value:
        Controller.corona_rules(chat_id, split_message[2])
    else:
        Controller.error_handler(chat_id, ErrorCodes.ONLY_PART_OF_COMMAND)


bot.polling()
