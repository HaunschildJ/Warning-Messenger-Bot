import ChatSender
import TextTemplates


def start(chat_id):
    ChatSender.start(chat_id, TextTemplates.get_greeting_string())


def corona(chat_id, city_name):
    ChatSender.send_chat_action(chat_id, "typing")
    message = TextTemplates.get_corona_string()
    message = message.replace("%inzidenz", "10")
    message = message.replace("%case", "10")
    message = message.replace("%death", "10")
    message = message.replace("%date", "10.10.2010")
    ChatSender.send_message(chat_id, city_name+":\n"+message)
