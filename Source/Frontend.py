import telebot
import requests
from decouple import config

token = config('key')
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'help'])
def greet(message):
    bot.send_message(message.chat.id, "Hey "+message.from_user.full_name+"!")


@bot.message_handler(commands=['dice'])
def dice(message):
    bot.send_dice(message.chat.id)


@bot.message_handler(commands=['ort'])
def ort(message):
    bot.send_poll(message.chat.id, "Wo lebst du?", ["Hessen", "Darmstadt", "Berlin", "Nicht dort"])


@bot.message_handler(commands=['type'])
def typing(message):
    bot.send_chat_action(message.chat.id, "typing")


@bot.message_handler(commands=['button'])
def button(message):
    typing(message)
    bot.send_message(message.chat.id, "button missing")


@bot.message_handler(regexp="yes")
def handle_message(message):
    bot.send_message(message.chat.id, "No")


@bot.message_handler(commands=['faq'])
def faq(message):
    typing(message)
    res = requests.request('GET', 'https://nina.api.proxy.bund.dev/api31/appdata/gsb/faqs/DE/faq.json')
    bot.send_message(message.chat.id, res.text.split(",")[0])


@bot.message_handler(commands=['tip'])
def tip(message):
    typing(message)
    res = requests.request('GET', 'https://nina.api.proxy.bund.dev/api31/appdata/gsb/notfalltipps/DE/notfalltipps.json')
    alltips = res.text.split("\",\"")
    bot.send_message(message.chat.id, "Work in progress")


bot.polling()

