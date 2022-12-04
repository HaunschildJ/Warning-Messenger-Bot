import telebot.types

import Bot
bot = Bot.bot


def start(chat_id, message_string):
    button1 = telebot.types.KeyboardButton("/corona Darmstadt")
    button2 = telebot.types.KeyboardButton("/corona Hessen")
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True).add(button1).add(button2)
    bot.send_message(chat_id, text=message_string, reply_markup=keyboard)


def send_message(chat_id, message_string):
    bot.send_message(chat_id, message_string)


def send_chat_action(chat_id, action):
    bot.send_chat_action(chat_id, action)
