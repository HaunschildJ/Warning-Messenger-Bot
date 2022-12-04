import ChatSender
import TextTemplates
def start(chat_id):
    ChatSender.send_message(chat_id, TextTemplates.get_greeting_string())