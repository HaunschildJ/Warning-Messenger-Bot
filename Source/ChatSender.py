import  Bot
bot = Bot.bot


def send_message(chat_id, message_string):
    bot.send_message(chat_id, message_string)

