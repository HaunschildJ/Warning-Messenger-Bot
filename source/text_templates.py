import json
import string
from enum import Enum

file_path = "data/textTemplates.json"


class ReplaceableAnswer(Enum):
    COVID_INFO = "covid_info"
    COVID_RULES = "covid_rules"
    GENERAL_WARNING = "general_warning"
    GREETING = "greeting"
    ADD_SUBSCRIPTION = "add_subscription"
    ADDING_SUBSCRIPTION_WARNING = "adding_subscription_warning"
    ADDING_SUBSCRIPTION_LEVEL = "adding_subscription_level"
    DELETE_SUBSCRIPTION = "delete_subscription"
    CHANGED_AUTO_COVID_UPDATES = "changed_auto_covid_updates"


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
    WEATHER = "weather"  # name needs to be equal to name in nina_service.WarnType
    GENERAL = "general"  # name needs to be equal to name in nina_service.WarnType
    DISASTER = "disaster"  # name needs to be equal to name in nina_service.WarnType
    FLOOD = "flood"  # name needs to be equal to name in nina_service.WarnType
    SHOW_SUBSCRIPTION = "show_subscriptions"
    DELETE_SUBSCRIPTION = "delete_subscription"
    ADD_SUBSCRIPTION = "add_subscription"
    DELETE = "delete"
    NEVER = "never"  # name needs to be equal to name in data_service.ReceiveInformation
    DAILY = "daily"  # name needs to be equal to name in data_service.ReceiveInformation
    WEEKLY = "weekly"  # name needs to be equal to name in data_service.ReceiveInformation
    MONTHLY = "monthly"  # name needs to be equal to name in data_service.ReceiveInformation
    MINOR = "minor"
    MODERATE = "moderate"
    SEVERE = "severe"


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
    MANAGE_SUBSCRIPTIONS = "manage_subscriptions"
    MANAGE_AUTO_COVID_UPDATES = "manage_auto_covid_updates"
    NO_SUBSCRIPTIONS = "no_subscriptions"
    CLICK_SUGGESTION = "click_suggestion"
    NO_LOCATION_FOUND = "no_location_found"


def _read_file(path: str):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_button_name(button: Button) -> string:
    """
    Returns a string containing the button name of the desired button.

    Arguments:
        button: a Button to determine what button name you want to be returned

    Returns:
        A String containing the desired button name.
    """

    data = _read_file(file_path)

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

    data = _read_file(file_path)

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

    data = _read_file(file_path)

    for topic in data:
        if topic['topic'] == "replaceable_answers":
            for answer in topic['all_answers']:
                if answer['topic'] == r_answer.value:
                    for information in answer['information']:
                        result += information['text'] + "\n"

    return result


def _get_show_subscriptions() -> dict:
    """
    Returns a dictionary with the format for showing subscriptions

    Returns:
        a dictionary with the format for showing subscriptions
    """

    data = _read_file(file_path)

    for topic in data:
        if topic['topic'] == "show_subscriptions":
            return topic


def _get_delete_subscriptions() -> dict:
    """
    Returns a dictionary with the format for deleting subscriptions

    Returns:
        a dictionary with the format for deleting subscriptions
    """

    data = _read_file(file_path)

    for topic in data:
        if topic['topic'] == "delete_subscription":
            return topic


def _get_select_location() -> dict:
    """
    Returns a dictionary with the format for selecting a location

    Returns:
        a dictionary with the format for selecting a location
    """

    data = _read_file(file_path)

    for topic in data:
        if topic['topic'] == "select_location":
            return topic


def _get_show_recommendations() -> dict:
    """
    Returns a dictionary with the format for showing recommendations

    Returns:
        a dictionary with the format for showing recommendations
    """

    data = _read_file(file_path)

    for topic in data:
        if topic['topic'] == "recommendations":
            return topic


# fill in the replaceable answer ---------------------------------------------------------------------------------------


def get_greeting_message(username: str) -> str:
    """
    This method will replace the placeholder (%name) with the given parameters from the greeting in the json

    Returns:
        Message that can be sent to the user with the parameter in the message
    """
    message = get_replaceable_answer(ReplaceableAnswer.GREETING)
    message = message.replace("%username", username)
    return message


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


def get_covid_info_message(location: str, infektionsgefahr_stufe: str, sieben_tage_inzidenz_bundesland: str,
                           sieben_tage_inzidenz_kreis: str, allgemeine_hinweise: str) -> str:
    """
    This method will replace the placeholder (%name) with the given parameters from the message for covid infos in
    the json

    Returns:
        Message that can be sent to the user with the parameter in the message
    """
    message = get_replaceable_answer(ReplaceableAnswer.COVID_INFO)
    message = message.replace("%location", location)
    message = message.replace("%infektionsgefahr_stufe", infektionsgefahr_stufe)
    message = message.replace("%sieben_tage_inzidenz_bundesland", sieben_tage_inzidenz_bundesland)
    message = message.replace("%sieben_tage_inzidenz_kreis", sieben_tage_inzidenz_kreis)
    message = message.replace("%allgemeine_hinweise", allgemeine_hinweise)
    return message


def get_covid_rules_message(location: str, vaccine_info: str, contact_terms: str, school_kita_rules: str, hospital_rules: str,
                            travelling_rules: str, fines: str) -> str:
    """
    This method will replace the placeholder (%name) with the given parameters from the message for covid rules in
    the json

    Returns:
        Message that can be sent to the user with the parameter in the message
    """
    message = get_replaceable_answer(ReplaceableAnswer.COVID_RULES)
    message = message.replace("%location", location)
    message = message.replace("%vaccine_info", vaccine_info)
    message = message.replace("%contact_terms", contact_terms)
    message = message.replace("%school_kita_rules", school_kita_rules)
    message = message.replace("%hospital_rules", hospital_rules)
    message = message.replace("%travelling_rules", travelling_rules)
    message = message.replace("%fines", fines)
    return message


def get_add_subscription_message() -> str:
    """
    This method will return the message the bot will send when the user wants to add a subscription
    (pressed add subscription button)

    Returns:
        message from the json
    """
    message = get_replaceable_answer(ReplaceableAnswer.ADD_SUBSCRIPTION)
    message = message.replace("%location_button", get_button_name(Button.SEND_LOCATION))
    return message


def get_adding_subscription_level_message(location: str, warning: str) -> str:
    """
    This method will return the message the bot will send when the user is in the process of adding a subscription
    (needs to add the warning level)

    Arguments:
        location: a String with the location name
        warning: a String with the warning name

    Returns:
        message from the json with the parameters inserted
    """
    message = get_replaceable_answer(ReplaceableAnswer.ADDING_SUBSCRIPTION_LEVEL)
    message = message.replace("%location", location)
    message = message.replace("%warning", warning)
    return message


def get_adding_subscription_warning_message(location: str) -> str:
    """
    This method will return the message the bot will send when the user is in the process of adding a subscription
    (needs to add the warning)

    Arguments:
        location: a String with the location name

    Returns:
        message from the json with the parameters inserted
    """
    message = get_replaceable_answer(ReplaceableAnswer.ADDING_SUBSCRIPTION_WARNING)
    message = message.replace("%location", location)
    return message


def get_delete_subscription_message(location: str, warning: str) -> str:
    """
    This method will return the message the bot will send when the user deleted a Subscription

    Arguments:
        location: a String with the location name
        warning: a String with the warning name

    Returns:
        message from the json with the parameters inserted
    """
    message = get_replaceable_answer(ReplaceableAnswer.DELETE_SUBSCRIPTION)
    message = message.replace("%location", location)
    message = message.replace("%warning", warning)
    return message


def get_show_subscriptions_for_one_location_messsage(location: str, warnings: list[str], levels: list[str]) -> str:
    dic = _get_show_subscriptions()
    message = dic["location"]
    message = message.replace("%location", location)
    for (warning, level) in zip(warnings, levels):
        single_warning = dic["warning"]
        single_warning = single_warning.replace("%warning", warning)
        single_warning = single_warning.replace("%level", level)
        message = message + "\n" + single_warning
    return message


def get_show_subscriptions_message(subscriptions: list[str]) -> str:
    dic = _get_show_subscriptions()
    message = dic["headline"]
    for subscription in subscriptions:
        message = message + "\n" + subscription
    return message


def get_delete_subscriptions_for_one_location_messsage(location: str, warnings: list[str], levels: list[str],
                                                       corresponding_button_names: list[str]) -> str:
    dic = _get_delete_subscriptions()
    message = dic["location"]
    message = message.replace("%location", location)
    for (warning, level, button) in zip(warnings, levels, corresponding_button_names):
        single_warning = dic["warning"]
        single_warning = single_warning.replace("%warning", warning)
        single_warning = single_warning.replace("%level", level)
        single_warning = single_warning.replace("%button_name", button)
        message = message + "\n" + single_warning
    return message


def get_delete_subscriptions_message(subscriptions: list[str]) -> str:
    dic = _get_delete_subscriptions()
    message = dic["headline"]
    for subscription in subscriptions:
        message = message + "\n" + subscription
    end_text = dic["end"]
    if end_text != "":
        message = message + "\n" + end_text
    return message


def get_select_location_for_one_location_messsage(district_name: str, place_name: str,
                                                  corresponding_button_name: str) -> str:
    dic = _get_select_location()
    message = dic["text"]
    message = message.replace("%place_name", place_name)
    message = message.replace("%district_name", district_name)
    message = message.replace("%button_name", corresponding_button_name)
    return message


def get_select_location_message(locations: list[str]) -> str:
    dic = _get_select_location()
    message = dic["headline"]
    for location in locations:
        message = message + "\n" + location
    end_text = dic["end"]
    if end_text != "":
        message = message + "\n" + end_text
    return message


def get_changed_auto_covid_updates_message(interval: str) -> str:
    message = get_replaceable_answer(ReplaceableAnswer.CHANGED_AUTO_COVID_UPDATES)
    message = message.replace("%interval", interval)
    return message


def get_show_recommendations_message(suggestions: list[str]) -> str:
    dic = _get_show_recommendations()
    message = dic["headline"]
    for suggestion in suggestions:
        message = message + "\n" + dic["recommendation"].replace("%r", suggestion)
    message = message + "\n" + dic["end"]
    return message
