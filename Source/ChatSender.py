import telebot.types

import Bot
bot = Bot.bot


def send_message(chat_id, message_string, reply_markup=None) -> telebot.types.Message:
    """
    Arguments:
        chat_id: an integer for the chatID that the message is sent to
        message_string: a string for the message that is sent
        reply_markup: optional reply_markup
    Returns:
        The message that was sent
    """
    return bot.send_message(chat_id, message_string, reply_markup=reply_markup)


def send_chat_action(chat_id, action):
    """
    Arguments:
        chat_id: an integer for the chatID in which the chat action is shown
        action: a string for action that the bot is doing (typing, upload_photo, record_video, upload_video,
                record_voice, upload_voice, upload_document, choose_sticker, find_location, record_video_node,
                upload_video_node)
    Returns:
        Nothing
    """
    bot.send_chat_action(chat_id, action)


def delete_message(chat_id, message_id):
    bot.delete_message(chat_id, message_id)


# helper methods -------------------------------------------------------------------------------------------------------
def create_keyboard(button_names, one_time=False) -> telebot.types.ReplyKeyboardMarkup:
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=one_time)
    for name in button_names:
        button = telebot.types.KeyboardButton(name)
        keyboard.add(button)
    return keyboard


def create_button(text, request_contact=False, request_location=False):
    return telebot.types.KeyboardButton(text, request_contact=request_contact, request_location=request_location)


def create_inline_button(text, callback_data):
    """
    Arguments:
        text: a string with the button text
        callback_data: a string (only string?) Data to be sent in a callback query to the bot when button is pressed
    Returns:
        Nothing
    """
    return telebot.types.InlineKeyboardButton(text, callback_data=callback_data)


