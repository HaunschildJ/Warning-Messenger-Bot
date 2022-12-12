import json
import string
from enum import Enum

file_path = "../Source/Data/TextTemplates.json"

# TODO Anleitung für TextTemplates.json schreiben, also wie man darin was ändern würde

# TODO immer erweitern mit neuen Topics und dann auch in der json file ergänzen
class Topic(Enum):
    COVID_INFO = "covid_info"
    COVID_RULES = "covid_rules"
    BIWAPP_WARNING = "biwapp_warning"
    GREETING = "greeting"


class Button(Enum):
    SETTINGS = "settings"
    WARNINGS = "warnings"
    EMERGENCY_TIPS = "emergency_tips"
    COVID_INFORMATION = "covid_information"
    COVID_RULES = "covid_rules"
    HELP = "help"
    BIWAPP = "biwapp"
    BACK_TO_MAIN_MENU = "back_to_main_menu"


def get_button_name(button : Button) -> string:
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
            for j in i['names']:
                return j[button.value]





def get_topic_info(topic : Topic) -> string:
    """
    Takes a value of the Enum and returns a string with formated info from a JSON file.

    Arguments:
        topic: a Topic to determine what information you want to be returned

    Returns:
        A String containing the desired information.
    """
    result = ""

    with open(file_path, "r") as file:
        data = json.load(file)

    for i in data:
        if i['topic'] == topic.value:
            for j in i['information']:
                result += j['text'] + "\n"

    return result


s = get_button_name(Button.SETTINGS)
print(s)
