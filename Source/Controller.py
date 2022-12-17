import telebot.types

import ChatSender
import TextTemplates
import NinaService
import DataService

from enum import Enum
from telebot.types import InlineKeyboardMarkup, ReplyKeyboardMarkup


class Commands(Enum):
    """
    this enum is used to have all commands in one place
    current possible commands:
    CORONA + (CORONA_INFO || CORONA_RULES) + "string"
    AUTO_WARNING + "bool as string"

    just for the bot not the user:
    CANCEL_INLINE
    """
    CORONA = "/corona"
    CORONA_INFO = "info"
    CORONA_RULES = "rule"
    AUTO_WARNING = "/autowarning"
    CANCEL_INLINE = "/cancel"


class ErrorCodes(Enum):
    """
    this enum is used to handle errors
    """
    NOT_IMPLEMENTED_YET = 0
    UNKNOWN_COMMAND = 1
    ONLY_PART_OF_COMMAND = 2


def get_main_keyboard_buttons() -> telebot.types.ReplyKeyboardMarkup:
    """
    This is a helper method which returns the keyboard for the MVP 3. menu

    Returns:
         telebot.types.ReplyKeyboardMarkup
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    button1 = ChatSender.create_button(SETTING_BUTTON_TEXT)
    button2 = ChatSender.create_button(WARNING_BUTTON_TEXT)
    button3 = ChatSender.create_button(TIP_BUTTON_TEXT)
    button4 = ChatSender.create_button(HELP_BUTTON_TEXT)
    keyboard.add(button1).add(button2).add(button3, button4)
    return keyboard


def get_settings_keyboard_buttons() -> telebot.types.ReplyKeyboardMarkup:
    """
    This is a helper method which returns the keyboard for the MVP 4. menu

    Returns:
         telebot.types.ReplyKeyboardMarkup
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = ChatSender.create_button(SETTING_AUTO_WARNING_TEXT)
    button2 = ChatSender.create_button(SETTING_SUGGESTION_LOCATION_TEXT)
    button3 = ChatSender.create_button(SETTING_SUBSCRIPTION_TEXT)
    button4 = ChatSender.create_button(SETTING_AUTO_COVID_INFO_TEXT)
    button5 = ChatSender.create_button(SETTING_LANGUAGE_TEXT)
    button6 = ChatSender.create_button(BACK_TO_MAIN_TEXT)
    keyboard.add(button1, button2).add(button3).add(button4, button5).add(button6)
    return keyboard


def get_warning_keyboard_buttons() -> telebot.types.ReplyKeyboardMarkup:
    """
    This is a helper method which returns the keyboard for the MVP 5. menu

    Returns:
         telebot.types.ReplyKeyboardMarkup
    """
    # TODO add all warnings for buttons here
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button1 = ChatSender.create_button(WARNING_COVID_INFO_TEXT)
    button2 = ChatSender.create_button(WARNING_COVID_RULES_TEXT)
    button3 = ChatSender.create_button(WARNING_BIWAPP_TEXT)
    button4 = ChatSender.create_button(BACK_TO_MAIN_TEXT)
    keyboard.add(button1).add(button2).add(button3).add(button4)
    return keyboard


# global variables -----------------------------------------------------------------------------------------------------
# main keyboard buttons (TODO get these from TextTemplates when implemented)
SETTING_BUTTON_TEXT = "Einstellungen"  # MVP 4.
WARNING_BUTTON_TEXT = "Warnungen"  # MVP 5.
TIP_BUTTON_TEXT = "Notfalltipps"  # MVP 6.
HELP_BUTTON_TEXT = "Hilfe"  # MVP 7.

# warning keyboard buttons (TODO get these from TextTemplates when implemented)
WARNING_COVID_INFO_TEXT = "Corona Informationen"  # MVP 5. i)
WARNING_COVID_RULES_TEXT = "Corona Regeln"  # MVP 5. i)
WARNING_BIWAPP_TEXT = "Aktuelle Warnungen"  # MVP 5. i)

# settings keyboard buttons (TODO get these from TextTemplates when implemented)
SETTING_AUTO_WARNING_TEXT = "Automatische Warnungen"  # MVP 4. a)
SETTING_SUGGESTION_LOCATION_TEXT = "Standort für Schnellzugriffe auswählen"  # MVP 4. b)
SETTING_SUBSCRIPTION_TEXT = "Abonnement verwalten"  # MVP 4. c)
SETTING_AUTO_COVID_INFO_TEXT = "Automatische Corona Updates"  # MVP 4. d)
SETTING_LANGUAGE_TEXT = "Sprache auswählen"  # MVP 4. e)

# back to main keyboard button (TODO get these from TextTemplates when implemented)
BACK_TO_MAIN_TEXT = "Zurück ins Hauptmenü"  # MVP 2.

# cancel inline button
CANCEL_TEXT = "Abbrechen"

# Choose answers
YES_TEXT = "Ja"  # MVP 4. a) Ja
NO_TEXT = "Nein"  # MVP 4. a) Nein


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
    ChatSender.send_message(chat_id, TextTemplates.get_greeting_string(), get_main_keyboard_buttons())


def main_button_pressed(chat_id: int, button_text: str):
    """
    This method gets called if a button of the Main Keyboard is pressed (or the user types what the Button text says)
    and handles whatever the button is supposed to do (MVP 3.)

    Arguments:
        chat_id: an integer for the chatID that the message is sent to
        button_text: a string which is the text of the button that was pressed (constant of this class)
    Returns:
        Nothing
    """
    if button_text == SETTING_BUTTON_TEXT:
        # the keyboard for the settings menu
        keyboard = get_settings_keyboard_buttons()
        # TODO get text for message from TextTemplates
        ChatSender.send_message(chat_id, SETTING_BUTTON_TEXT + ":", keyboard)
    elif button_text == WARNING_BUTTON_TEXT:
        # the keyboard for the manuel call of warnings
        keyboard = get_warning_keyboard_buttons()
        # TODO get text for message from TextTemplates
        ChatSender.send_message(chat_id, WARNING_BUTTON_TEXT + ":", keyboard)
    elif button_text == TIP_BUTTON_TEXT:
        # TODO tips
        ChatSender.send_message(chat_id, "TODO tips")
    elif button_text == HELP_BUTTON_TEXT:
        # TODO help
        ChatSender.send_message(chat_id, "TODO help")
    else:
        error_handler(chat_id, ErrorCodes.NOT_IMPLEMENTED_YET)


def button_in_settings_pressed(chat_id: int, button_text: str):
    """
    This method gets called if a button of the Setting Keyboard is pressed (or the user types what the Button text says)
    and handles whatever the button is supposed to do (MVP 4.)

    Arguments:
        chat_id: an integer for the chatID that the message is sent to
        button_text: a string which is the text of the button that was pressed (constant of this class)
    Returns:
        Nothing
    """
    if button_text == SETTING_AUTO_WARNING_TEXT:
        command = Commands.AUTO_WARNING.value + " "
        markup = InlineKeyboardMarkup()
        button1 = ChatSender.create_inline_button(YES_TEXT, command + "True")
        button2 = ChatSender.create_inline_button(NO_TEXT, command + "False")
        button3 = ChatSender.create_inline_button(CANCEL_TEXT, Commands.CANCEL_INLINE.value)
        markup.add(button1, button2, button3)
        # TODO get Text from TextTemplates when possible
        ChatSender.send_message(chat_id, "Möchtest du automatische Warnungen erhalten? (nur eingestellte)", markup)
    elif button_text == SETTING_SUGGESTION_LOCATION_TEXT:
        ChatSender.send_message(chat_id, "TODO " + button_text)
    elif button_text == SETTING_SUBSCRIPTION_TEXT:
        ChatSender.send_message(chat_id, "TODO " + button_text)
    elif button_text == SETTING_AUTO_COVID_INFO_TEXT:
        ChatSender.send_message(chat_id, "TODO " + button_text)
    elif button_text == SETTING_LANGUAGE_TEXT:
        ChatSender.send_message(chat_id, "TODO " + button_text)
    else:
        error_handler(chat_id, ErrorCodes.NOT_IMPLEMENTED_YET)


def show_inline_button(chat_id: int, button_text: str):
    """
    This method is called by a specific button with button_text as text to show inline buttons so that the user can
    finish the command in the chat (chat_id)

    Arguments:
        chat_id: an integer for the chatID that the message is sent to
        button_text: a string which is the text of the button that was pressed (constant of this class)
    Returns:
        Nothing
    """
    command_first_part = Commands.CORONA.value + " "
    markup = InlineKeyboardMarkup()
    if button_text == WARNING_COVID_INFO_TEXT:
        command_first_part = command_first_part + Commands.CORONA_INFO.value + " "
        # TODO make suggestions
        button1 = ChatSender.create_inline_button("Darmstadt", command_first_part + "Darmstadt")
        button2 = ChatSender.create_inline_button("Hamburg", command_first_part + "Hamburg")
        button3 = ChatSender.create_inline_button("Berlin", command_first_part + "Berlin")
        button4 = ChatSender.create_inline_button(CANCEL_TEXT, Commands.CANCEL_INLINE.value)
        markup.add(button1, button2, button3).add(button4)
    elif button_text == WARNING_COVID_RULES_TEXT:
        command_first_part = command_first_part + Commands.CORONA_RULES.value + " "
        # TODO make suggestions
        button1 = ChatSender.create_inline_button("Darmstadt", command_first_part + "Darmstadt")
        button2 = ChatSender.create_inline_button("Hamburg", command_first_part + "Hamburg")
        button3 = ChatSender.create_inline_button("Berlin", command_first_part + "Berlin")
        button4 = ChatSender.create_inline_button(CANCEL_TEXT, Commands.CANCEL_INLINE.value)
        markup.add(button1, button2, button3).add(button4)
    else:
        ChatSender.send_message(chat_id, "Not implemented yet: "+button_text)
        return
    ChatSender.send_message(chat_id, TextTemplates.get_inline_button_corona_rules(), markup)


def biwapp(chat_id: int):
    """
    Sets the chat action of the bot to typing \n
    Calls for BIWAPP warnings from the Nina API via the NinaService \n
    Sends this information back to the chat (chat_id)

    Arguments:
        chat_id: an integer for the chatID that the message is sent to
    Returns:
        Nothing
    """
    ChatSender.send_chat_action(chat_id, "typing")
    warnings = NinaService.poll_biwapp_warning()
    if len(warnings) == 0:
        # TODO get string from TextTemplates when able to
        ChatSender.send_message(chat_id, "Aktuell gibt es keine Warnungen!")
        return
    for warning in warnings:
        # TODO get string from TextTemplates when able to
        message = "Warnung: %title \nSchwere: %severity \n Warnung vom Typ: %warning_type"
        message = message.replace("%id", warning.id)
        message = message.replace("%version", str(warning.version))
        message = message.replace("%severity", str(warning.severity.value))
        message = message.replace("%warning_type", str(warning.type.value))
        message = message.replace("%title", warning.title)
        ChatSender.send_message(chat_id, message)


def corona_info(chat_id: int, city_name: str):
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


def corona_rules(chat_id: int, city_name: str):
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


def change_auto_warning_in_database(chat_id: int, value: bool):
    user = DataService.read_user(chat_id)
    user.change_entry(DataService.Attributes.RECEIVE_WARNINGS, value)
    DataService.write_file(user)
    # TODO get Text from TextTemplates
    text = "Automatische Warnungen sind jetzt ausgeschaltet"
    if value:
        text = "Automatische Warnungen sind jetzt eingeschaltet"
    ChatSender.send_message(chat_id, text)


def back_to_main_keyboard(chat_id: int):
    """
    Sets the Keyboard (of the user = chat_id) to the Main Keyboard (Main Menu) \n
    Also sends a message which indicates that the user now is in the Main Menu

    Arguments:
        chat_id: an integer for the chatID that the message is sent to
    Returns:
        Nothing
    """
    keyboard = get_main_keyboard_buttons()
    # TODO get text from TextTemplates when possible
    ChatSender.send_message(chat_id, "Hauptmenü", keyboard)


def delete_message(chat_id: int, message_id: int):
    ChatSender.delete_message(chat_id, message_id)


def error_handler(chat_id: int, error_code: ErrorCodes):
    ChatSender.send_message(chat_id, "currently no real error message for error " + error_code.name)
