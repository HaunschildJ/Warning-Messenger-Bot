import telebot
from decouple import config

global bot

token = config('key')
bot = telebot.TeleBot(token)