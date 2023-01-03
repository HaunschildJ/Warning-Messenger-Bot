import json
import string
from enum import Enum

file_path = "data/textTemplates.json"


class ReplaceableAnswer(Enum):
    COVID_INFO = "covid_info"
    COVID_RULES = "covid_rules"
    GENERAL_WARNING = "general_warning"
    GREETING = "greeting"
    RECOMMENDATIONS = "recommendations"


class Button(Enum):
    SETTINGS = "settings"
    WARNINGS = "warnings"
    EMERGENCY_TIPS = "emergency_tips"
    COVID_INFORMATION = "covid_information"
    COVID_RULES = "covid_rules"
    HELP = "help"
    BACK_TO_MAIN_MENU = "back_to_main_menu"
    AUTO_WARNING = "auto_warning"
    SUGGESTION_LOCATION = "suggestion_location"
    SUBSCRIPTION = "subscription"
    AUTO_COVID_INFO = "auto_covid_info"
    LANGUAGE = "language"
    CANCEL = "cancel"
    SEND_LOCATION = "send_location"
    BIWAPP = "biwapp"
    KATWARN = "katwarn"
    MOWAS = "mowas"
    DWD = "dwd"
    LHP = "lhp"
    POLICE = "police"


class Answers(Enum):
    YES = "yes"
    NO = "no"
    SETTINGS = "settings"
    WARNINGS = "warnings"
    HELP = "help"
    AUTO_WARNINGS_TEXT = "auto_warnings_text"
    AUTO_WARNINGS_ENABLE = "auto_warnings_enable"
    AUTO_WARNINGS_DISABLE = "auto_warnings_disable"
    NO_CURRENT_WARNINGS = "no_current_warnings"
    BACK_TO_MAIN_MENU = "back_to_main_menu"
    SUGGESTION_HELPER_TEXT = "suggestion_helper_text"


def get_button_name(button: Button) -> string:
    """
    Returns a string containing the button name of the desired button.

    Arguments:
        button: a Button to determine what button name you want to be returned

    Returns:
        A String containing the desired button name.
    """

    with open(file_path, "r") as file:
        data = json.load(file)

    for topic in data:
        if topic['topic'] == "buttons":
            return topic['names'][button.value]


def get_answers(answer: Answers) -> string:
    """
    Returns a string containing the desired answer text.

    Arguments:
        answer: an Answers to determine what answer text you want to be returned

    Returns:
        A String containing the desired answer text.
    """

    with open(file_path, "r") as file:
        data = json.load(file)

    for topic in data:
        if topic['topic'] == "answers":
            return topic['text'][answer.value]


def get_replaceable_answer(r_answer: ReplaceableAnswer) -> string:
    """
    Only applicable for text with replaceable elements. Returned string will
    contain the following form: %to_be_replaced.
    Takes a value of the Enum and returns a string with formatted info from a JSON file.

    Arguments:
        r_answer: a ReplaceableAnswer to determine what information you want to be returned

    Returns:
        A String containing the desired information.
    """
    result = ""

    with open(file_path, "r") as file:
        data = json.load(file)

    for topic in data:
        if topic['topic'] == "replaceable_answers":
            for answer in topic['all_answers']:
                if answer['topic'] == r_answer.value:
                    for information in answer['information']:
                        result += information['text'] + "\n"

    return result


def get_general_warning_message(warning_id: str, version: str, start_date: str, severity: str,
                                warning_type: str, title: str) -> str:
    """
    This method will replace the placeholder (%name) with the given parameters from the message for general warnings in
    the json

    Returns:
        Message that can be sent to the user with the parameter in the message
    """
    message = get_replaceable_answer(ReplaceableAnswer.GENERAL_WARNING)
    message = message.replace("%id", warning_id)
    message = message.replace("%version", version)
    message = message.replace("%severity", severity)
    message = message.replace("%type", warning_type)
    message = message.replace("%title", title)
    message = message.replace("%start_date", start_date)
    return message


def get_covid_info_message(infektionsgefahr_stufe: str, sieben_tage_inzidenz_bundesland: str,
                           sieben_tage_inzidenz_kreis: str, allgemeine_hinweise: str) -> str:
    """
    This method will replace the placeholder (%name) with the given parameters from the message for covid infos in
    the json

    Returns:
        Message that can be sent to the user with the parameter in the message
    """
    message = get_replaceable_answer(ReplaceableAnswer.COVID_INFO)
    message = message.replace("%infektionsgefahr_stufe", infektionsgefahr_stufe)
    message = message.replace("%sieben_tage_inzidenz_bundesland", sieben_tage_inzidenz_bundesland)
    message = message.replace("%sieben_tage_inzidenz_kreis", sieben_tage_inzidenz_kreis)
    message = message.replace("%allgemeine_hinweise", allgemeine_hinweise)
    return message


def get_covid_rules_message(vaccine_info: str, contact_terms: str, school_kita_rules: str, hospital_rules: str,
                            travelling_rules: str, fines: str) -> str:
    """
    This method will replace the placeholder (%name) with the given parameters from the message for covid rules in
    the json

    Returns:
        Message that can be sent to the user with the parameter in the message
    """
    message = get_replaceable_answer(ReplaceableAnswer.COVID_RULES)
    message = message.replace("%vaccine_info", vaccine_info)
    message = message.replace("%contact_terms", contact_terms)
    message = message.replace("%school_kita_rules", school_kita_rules)
    message = message.replace("%hospital_rules", hospital_rules)
    message = message.replace("%travelling_rules", travelling_rules)
    message = message.replace("%fines", fines)
    return message
