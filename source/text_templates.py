import json
import string
from enum import Enum

file_path = "data/textTemplates.json"


class ReplaceableAnswer(Enum):
    COVID_INFO = "covid_info"
    COVID_RULES = "covid_rules"
    BIWAPP_WARNING = "biwapp_warning"
    GREETING = "greeting"
    RECOMMENDATIONS = "recommendations"


class Button(Enum):
    SETTINGS = "settings"
    WARNINGS = "warnings"
    EMERGENCY_TIPS = "emergency_tips"
    COVID_INFORMATION = "covid_information"
    COVID_RULES = "covid_rules"
    HELP = "help"
    BIWAPP = "biwapp"
    BACK_TO_MAIN_MENU = "back_to_main_menu"
    AUTO_WARNING = "auto_warning"
    SUGGESTION_LOCATION = "suggestion_location"
    SUBSCRIPTION = "subscription"
    AUTO_COVID_INFO = "auto_covid_info"
    LANGUAGE = "language"
    CANCEL = "cancel"
    SEND_LOCATION = "send_location"


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

    for i in data:
        if i['topic'] == "buttons":
            return i['names'][button.value]


def get_answers(answer : Answers) -> string:
    """
    Returns a string containing the desired answer text.

    Arguments:
        answer: an Answers to determine what answer text you want to be returned

    Returns:
        A String containing the desired answer text.
    """

    with open(file_path, "r") as file:
        data = json.load(file)

    for i in data:
        if i['topic'] == "answers":
            return i['text'][answer.value]


def get_replaceable_answer(answer: ReplaceableAnswer) -> string:
    """
    Only applicable for text with replacable elements. Returned string will
    contain the following form: %to_be_replaced.
    Takes a value of the Enum and returns a string with formated info from a JSON file.

    Arguments:
        answer: a ReplaceableAnswer to determine what information you want to be returned

    Returns:
        A String containing the desired information.
    """
    result = ""

    with open(file_path, "r") as file:
        data = json.load(file)

    for i in data:
        if i['topic'] == "replacable_answers":
            for j in i['all_answers']:
                if j['topic'] == answer.value:
                    for k in j['information']:
                        result += k['text'] + "\n"

    return result