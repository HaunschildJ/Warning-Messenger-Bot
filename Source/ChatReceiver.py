import Bot
import Controller

bot = Bot.bot


# filter for message handlers


def filter_corona(message) -> bool:
    if message.text.split(' ')[0] == "/corona":
        return True
    return False

# bot message handlers


@bot.message_handler(commands=['start'])
def start(message):
    Controller.start(message.chat.id)


@bot.message_handler(func=filter_corona)
def corona(message):
    Controller.corona(message.chat.id, message.text.split('/corona ')[1])


bot.polling()

