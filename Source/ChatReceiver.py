import Bot
import Controller

bot = Bot.bot

@bot.message_handler(commands=['start'])
def start(message):
    Controller.start(message.chat.id)

bot.polling()

