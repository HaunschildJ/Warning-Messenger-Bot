import sender
import text_templates
import data_service

from enum_types import ErrorCodes, BotUsageHelp
from frontend_helper import back_to_main_keyboard


# helper methods -------------------------------------------------------------------------------------------------------


def is_location(text: str) -> bool:
    if text == "Darmstadt":
        return True
    return False


def is_help(text: str) -> bool:
    lower_text = text.lower()
    if ("help" in lower_text) or ("hilf" in lower_text):
        return True
    return False


def is_start(text: str) -> bool:
    lower_text = text.lower()
    if ("start" in lower_text) or lower_text == "beginn":
        return True
    return False


def is_insult(text: str) -> bool:
    lower_text = text.lower()
    if ("doof" in lower_text) or ("idiot" in lower_text) or ("dumm" in lower_text):
        return True
    return False


# error handlers -------------------------------------------------------------------------------------------------------


def error_handler(chat_id: int, error_code: ErrorCodes, state: int = None, message: str = None):
    """
    this method will/should be called whenever an error occurs that the user needs to know of

    Args:
        chat_id: integer with the users chat id
        error_code: ErrorCodes enum with the Error Code
        state: integer with the users state if is None this method will get state from data_service
        message: string with the users text (optional only used when error_code is NO_INPUT_EXPECTED)
    """
    if state is None:
        state = data_service.get_user_state(chat_id)
    if error_code == ErrorCodes.NINA_API:
        # TODO text_templates
        sender.send_message(chat_id, "Es ist ein Fehler mit der Nina-API aufgetreten.")
        print("WARNING: a Nina-API error was thrown (user was in state: " + str(state) + ")")
        back_to_main_keyboard(chat_id)
    elif error_code == ErrorCodes.NOT_IMPLEMENTED_YET or error_code == ErrorCodes.CALLBACK_MISTAKE \
            or error_code == ErrorCodes.ONLY_PART_OF_COMMAND:
        # TODO text_templates
        sender.send_message(chat_id, "Diese Funktionalität wurde noch nicht implementiert.")
        print("WARNING: " + error_code.value + " (user was in state: " + str(state) + ")")
        back_to_main_keyboard(chat_id)
    elif error_code == ErrorCodes.UNKNOWN_COMMAND:
        # TODO text_templates
        sender.send_message(chat_id, "Unbekannter Befehlt. Bitte benutze das Menü oder gib /help für Hilfe ein.")
    elif error_code == ErrorCodes.UNKNOWN_LOCATION:
        # TODO text_templates
        sender.send_message(chat_id, "Unbekannter Ort. Bitte versuche es erneut mit einer präziseren Eingabe.")
    elif error_code == ErrorCodes.NO_INPUT_EXPECTED:
        if message is None:
            help_handler(chat_id, str(state))
            return
        if is_location(message):
            # TODO text_templates
            sender.send_message(chat_id, "Es wurde ein Ort erkannt, jedoch kannst du hier nichts eingeben. "
                                         "Nutze /help um zu erfahren was du jetzt machen kannst oder gehe "
                                         "zurück ins Hauptmenü um von dort aus über 'mehr' und 'Botbedienung' eine "
                                         "komplette Anleitung für den Bot zu finden.")
        elif is_help(message):
            help_handler(chat_id, str(state))
        elif is_start(message):
            # TODO text_templates
            sender.send_message(chat_id, "Bitte gib /start ein, um deine Konversation mit dem Bot zu starten.")
        elif is_insult(message):
            # TODO text_templates
            sender.send_message(chat_id, "🤨")
        else:
            # TODO text_templates
            sender.send_message(chat_id, "Es wurde keine Eingabe erwartet. "
                                         "Nutze /help um zu erfahren was du jetzt machen kannst oder gehe "
                                         "zurück ins Hauptmenü um von dort aus über 'mehr' und 'Botbedienung' eine "
                                         "komplette Anleitung für den Bot zu finden.")
    else:
        error_handler(chat_id, ErrorCodes.NOT_IMPLEMENTED_YET, state, message)


def illegal_state_handler(chat_id: int, state: int):
    """
    This method will be called when a user is in a normally unreachable state

    Args:
        chat_id: the user
        state: the users state
    """
    print("User: " + str(chat_id) + " was in the normally unreachable state: " + str(state))
    back_to_main_keyboard(chat_id)


def help_handler(chat_id: int, state: str):
    """
    This method will be called when a user wants specific help in a state

    Args:
        chat_id: the user
        state: the users state
    """
    state_first_number = int(state[0])
    if state_first_number == 0:
        # user is in main menu
        message = text_templates.get_help_message(BotUsageHelp.MAIN_MENU)
    elif state_first_number == 1:
        # settings
        if len(state) == 1:
            # in the settings menu
            message = text_templates.get_help_message(BotUsageHelp.SETTINGS_MENU)
        else:
            # in a sub-state
            state_second_number = int(state[1])
            if state_second_number == 0:
                # subscriptions
                message = text_templates.get_help_message(BotUsageHelp.SUBSCRIPTIONS_MENU)
            elif state_second_number == 1:
                # favorites
                message = text_templates.get_help_message(BotUsageHelp.FAVORITES)
            elif state_second_number == 2:
                # delete data
                message = text_templates.get_help_message(BotUsageHelp.DELETE_DATA_MENU)
            else:
                illegal_state_handler(chat_id, int(state))
                return
    elif state_first_number == 2:
        # manual warnings
        message = text_templates.get_help_message(BotUsageHelp.MANUAL_WARNINGS)
    elif state_first_number == 3:
        # emergency pdfs
        message = text_templates.get_help_message(BotUsageHelp.EMERGENCY_TIPS_MENU)
    elif state_first_number == 4:
        # more/ help menu
        message = text_templates.get_help_message(BotUsageHelp.HELP_MENU)
    else:
        illegal_state_handler(chat_id, int(state))
        return
    sender.send_message(chat_id, message)
