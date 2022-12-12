import ChatSender
import TextTemplates
import NinaService

from enum import Enum
from telebot.types import InlineKeyboardMarkup, ReplyKeyboardMarkup


class ButtonType(Enum):
    """
    this enum is used to list all buttons that result in inline buttons when clicked
    """
    CORONA_INFO = 1
    CORONA_RULES = 2


class Commands(Enum):
    """
    this enum is used to have all commands in one place
    current possible commands:
    CORONA + (CORONA_INFO || CORONA_RULES) + "string"
    """
    CORONA = "/corona"
    CORONA_INFO = "info"
    CORONA_RULES = "rule"


class ErrorCodes(Enum):
    """
    this enum is used to handle errors
    """
    NOT_IMPLEMENTED_YET = 0
    UNKNOWN_COMMAND = 1
    ONLY_PART_OF_COMMAND = 2


# global variables -----------------------------------------------------------------------------------------------------
# get these from TextTemplates when implemented
SETTING_BUTTON_TEXT = "Einstellung"
WARNING_BUTTON_TEXT = "Warnungen"
TIP_BUTTON_TEXT = "Notfalltipps"
HELP_BUTTON_TEXT = "Hilfe"

# methods called from the ChatReceiver ---------------------------------------------------------------------------------


def start(chat_id):
    """
    This method is called when the user adds the bot (or /start is called) \n
    It then creates buttons on the keyboard so that the user can interact with the bot more uncomplicated and sends a
    greeting message to the user (chat_id)

    Arguments:
        chat_id: an integer for the chatID that the message is sent to
    Returns:
        Nothing
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    button1 = ChatSender.create_button(SETTING_BUTTON_TEXT)
    button2 = ChatSender.create_button(WARNING_BUTTON_TEXT)
    button3 = ChatSender.create_button(TIP_BUTTON_TEXT)
    button4 = ChatSender.create_button(HELP_BUTTON_TEXT)
    keyboard.add(button1).add(button2).add(button3, button4)
    ChatSender.send_message(chat_id, TextTemplates.get_greeting_string(), keyboard)


# methods for main buttons


def main_button_pressed(chat_id, button_text):
    if button_text == SETTING_BUTTON_TEXT:
        ChatSender.send_message(chat_id, "settings")
    elif button_text == WARNING_BUTTON_TEXT:
        ChatSender.send_message(chat_id, "warnings")
    elif button_text == TIP_BUTTON_TEXT:
        ChatSender.send_message(chat_id, "tips")
    elif button_text == HELP_BUTTON_TEXT:
        ChatSender.send_message(chat_id, "help")
    else:
        error_handler(chat_id, ErrorCodes.NOT_IMPLEMENTED_YET)


def corona_info(chat_id, city_name):
    """
    Sets the chat action of the bot to typing \n
    Calls for corona information of a city (city_name) from the Nina API via the NinaService \n
    Sends this information back to the chat (chat_id)

    Arguments:
        chat_id: an integer for the chatID that the message is sent to
        city_name: a string with the city name for the information of this city
    Returns:
        Nothing
    """
    ChatSender.send_chat_action(chat_id, "typing")
    info = NinaService.get_covid_infos(city_name)
    message = TextTemplates.get_corona_info()
    message = message.replace("%inzidenz", info.infektion_danger_level)
    message = message.replace("%bund", info.sieben_tage_inzidenz_bundesland)
    message = message.replace("%kreis", info.sieben_tage_inzidenz_kreis)
    message = message.replace("%tips", info.general_tips)
    ChatSender.send_message(chat_id, city_name+":\n"+message)


def corona_rules(chat_id, city_name):
    """
    Sets the chat action of the bot to typing \n
    Calls for corona rules of a city (city_name) from the Nina API via the NinaService \n
    Sends this information back to the chat (chat_id)

    Arguments:
        chat_id: an integer for the chatID that the message is sent to
        city_name: a string with the city name for the rules of this city
    Returns:
        Nothing
    """
    ChatSender.send_chat_action(chat_id, "typing")
    rules = NinaService.get_covid_rules(city_name)
    message = TextTemplates.get_corona_rules()
    message = message.replace("%vaccine_info", rules.vaccine_info)
    message = message.replace("%contact_terms", rules.contact_terms)
    message = message.replace("%school_kita_rules", rules.school_kita_rules)
    message = message.replace("%hospital_rules", rules.hospital_rules)
    message = message.replace("%travelling_rules", rules.travelling_rules)
    message = message.replace("%fines", rules.fines)
    ChatSender.send_message(chat_id, city_name+":\n"+message)


def show_inline_button(chat_id, button_type):
    """
    This method is called by a specific button (button_type) to show inline buttons so that the user can finish the
    command in the chat (chat_id)

    Arguments:
        chat_id: an integer for the chatID that the message is sent to
        button_type: an enum of ButtonType from Controller which shows what button has been pressed
    Returns:
        Nothing
    """
    command_first_part = Commands.CORONA.value + " "
    markup = InlineKeyboardMarkup()
    if button_type == ButtonType.CORONA_INFO:
        command_first_part = command_first_part + Commands.CORONA_INFO.value + " "
        button1 = ChatSender.create_inline_button("Darmstadt", command_first_part + "Darmstadt")
        button2 = ChatSender.create_inline_button("Hamburg", command_first_part + "Hamburg")
        button3 = ChatSender.create_inline_button("Berlin", command_first_part + "Berlin")
        markup.add(button1, button2, button3)
    elif button_type == ButtonType.CORONA_RULES:
        command_first_part = command_first_part + Commands.CORONA_RULES.value + " "
        button1 = ChatSender.create_inline_button("Darmstadt", command_first_part + "Darmstadt")
        button2 = ChatSender.create_inline_button("Hamburg", command_first_part + "Hamburg")
        button3 = ChatSender.create_inline_button("Berlin", command_first_part + "Berlin")
        markup.add(button1, button2, button3)
    else:
        ChatSender.send_message(chat_id, "Not implemented yet: "+button_type.name)
        return
    ChatSender.send_message(chat_id, TextTemplates.get_inline_button_corona_rules(), markup)


def delete_message(chat_id, message_id):
    ChatSender.delete_message(chat_id, message_id)


def error_handler(chat_id, error_code):
    ChatSender.send_message(chat_id, "currently no real error message for error " + error_code.name)
