import telebot.types

import Bot
bot = Bot.bot


def start(chat_id, message_string):
    keyboard = create_keyboard(["/corona Darmstadt", "/corona Berlin", "/corona Hamburg"])
    bot.send_message(chat_id, text=message_string, reply_markup=keyboard)


def send_message(chat_id, message_string):
    bot.send_message(chat_id, message_string)


def send_chat_action(chat_id, action):
    bot.send_chat_action(chat_id, action)


# helper methods
def create_keyboard(button_names, one_time=False) -> telebot.types.ReplyKeyboardMarkup:
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=one_time)
    for name in button_names:
        button = telebot.types.KeyboardButton(name)
        keyboard.add(button)
    return keyboard

