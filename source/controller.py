import telebot.types

import sender
import text_templates
import nina_service
import data_service
from text_templates import Button, ReplaceableAnswer, Answers

from enum import Enum
from telebot.types import InlineKeyboardMarkup, ReplyKeyboardMarkup


class Commands(Enum):
    """
    this enum is used to have all commands in one place
    current possible commands:
    COVID + (COVID_INFO || COVID_RULES) + "string"
    AUTO_WARNING + "bool as string"
    ADD_RECOMMENDATION + "location as string"

    just for the bot not the user:
    CANCEL_INLINE
    DELETE_SUBSCRIPTION + "location" + "warn_type"
    ADD_SUBSCRIPTION + "location" + "warn_type" + "warn_level"
    COVID_UPDATES + "ReceiveInformation from data_service as int"
    """
    COVID = "/covid"
    COVID_INFO = "info"
    COVID_RULES = "rule"
    AUTO_WARNING = "/autowarning"
    CANCEL_INLINE = "/cancel"
    ADD_RECOMMENDATION = "/add"
    DELETE_SUBSCRIPTION = "/deleteSubscription"
    ADD_SUBSCRIPTION = "/addSubscription"
    COVID_UPDATES = "/covidupdates"


class ErrorCodes(Enum):
    """
    this enum is used to handle errors
    """
    NOT_IMPLEMENTED_YET = 0
    UNKNOWN_COMMAND = 1
    ONLY_PART_OF_COMMAND = 2


def _get_main_keyboard_buttons() -> telebot.types.ReplyKeyboardMarkup:
    """
    This is a helper method which returns the keyboard for the MVP 3. menu

    Returns:
         telebot.types.ReplyKeyboardMarkup
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=False, one_time_keyboard=False, input_field_placeholder="Hauptmenü")
    button1 = sender.create_button(SETTING_BUTTON_TEXT)
    button2 = sender.create_button(WARNING_BUTTON_TEXT)
    button3 = sender.create_button(TIP_BUTTON_TEXT)
    button4 = sender.create_button(HELP_BUTTON_TEXT)
    keyboard.add(button1).add(button2).add(button3, button4)
    return keyboard


def _get_settings_keyboard_buttons() -> telebot.types.ReplyKeyboardMarkup:
    """
    This is a helper method which returns the keyboard for the MVP 4. menu

    Returns:
         telebot.types.ReplyKeyboardMarkup
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=False, one_time_keyboard=False)
    button1 = sender.create_button(SETTING_AUTO_WARNING_TEXT)
    button2 = sender.create_button(SETTING_SUGGESTION_LOCATION_TEXT)
    button3 = sender.create_button(SETTING_SUBSCRIPTION_TEXT)
    button4 = sender.create_button(SETTING_AUTO_COVID_INFO_TEXT)
    button5 = sender.create_button(SETTING_LANGUAGE_TEXT)
    button6 = sender.create_button(BACK_TO_MAIN_TEXT)
    keyboard.add(button1, button2).add(button3).add(button4, button5).add(button6)
    return keyboard


def _get_warning_keyboard_buttons() -> telebot.types.ReplyKeyboardMarkup:
    """
    This is a helper method which returns the keyboard for the MVP 5. menu

    Returns:
         telebot.types.ReplyKeyboardMarkup
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=False, one_time_keyboard=True)
    button1 = sender.create_button(WARNING_COVID_INFO_TEXT)
    button2 = sender.create_button(WARNING_COVID_RULES_TEXT)
    button3 = sender.create_button(WARNING_BIWAPP_TEXT)
    button4 = sender.create_button(WARNING_KATWARN_TEXT)
    button5 = sender.create_button(WARNING_MOWAS_TEXT)
    button6 = sender.create_button(WARNING_DWD_TEXT)
    button7 = sender.create_button(WARNING_LHP_TEXT)
    button8 = sender.create_button(WARNING_POLICE_TEXT)
    button9 = sender.create_button(BACK_TO_MAIN_TEXT)
    keyboard.add(button1, button2).add(button3, button4, button5).add(button6, button7, button8).add(button9)
    return keyboard


def _get_send_location_keyboard() -> telebot.types.ReplyKeyboardMarkup:
    """
    This is a helper method which returns the keyboard for the MVP 4. b i)

    Returns:
         telebot.types.ReplyKeyboardMarkup
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=False, one_time_keyboard=False)
    button1 = sender.create_button(SEND_LOCATION_BUTTON_TEXT, request_location=True)
    button2 = sender.create_button(BACK_TO_MAIN_TEXT)
    keyboard.add(button1).add(button2)
    return keyboard


def _get_subscription_settings_keyboard() -> telebot.types.ReplyKeyboardMarkup:
    """
    Helper method to get subscription settings keyboard.

    Returns:
        Nothing
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=False, one_time_keyboard=False)
    button1 = sender.create_button(SHOW_SUBSCRIPTION_TEXT)
    button2 = sender.create_button(ADD_SUBSCRIPTION_TEXT)
    button3 = sender.create_button(DELETE_SUBSCRIPTION_TEXT)
    button4 = sender.create_button(BACK_TO_MAIN_TEXT)
    keyboard.add(button1).add(button2, button3).add(button4)
    return keyboard


# global variables -----------------------------------------------------------------------------------------------------
# main keyboard buttons
SETTING_BUTTON_TEXT = text_templates.get_button_name(Button.SETTINGS)  # MVP 4.
WARNING_BUTTON_TEXT = text_templates.get_button_name(Button.WARNINGS)  # MVP 5.
TIP_BUTTON_TEXT = text_templates.get_button_name(Button.EMERGENCY_TIPS)  # MVP 6.
HELP_BUTTON_TEXT = text_templates.get_button_name(Button.HELP)  # MVP 7.

# warning keyboard buttons
WARNING_COVID_INFO_TEXT = text_templates.get_button_name(Button.COVID_INFORMATION)  # MVP 5. i)
WARNING_COVID_RULES_TEXT = text_templates.get_button_name(Button.COVID_RULES)  # MVP 5. i)
WARNING_BIWAPP_TEXT = text_templates.get_button_name(Button.BIWAPP)  # MVP 5. i)
WARNING_KATWARN_TEXT = text_templates.get_button_name(Button.KATWARN)  # MVP 5. i)
WARNING_MOWAS_TEXT = text_templates.get_button_name(Button.MOWAS)  # MVP 5. i)
WARNING_DWD_TEXT = text_templates.get_button_name(Button.DWD)  # MVP 5. i)
WARNING_LHP_TEXT = text_templates.get_button_name(Button.LHP)  # MVP 5. i)
WARNING_POLICE_TEXT = text_templates.get_button_name(Button.POLICE)  # MVP 5. i)

# settings keyboard buttons
SETTING_AUTO_WARNING_TEXT = text_templates.get_button_name(Button.AUTO_WARNING)  # MVP 4. a)
SETTING_SUGGESTION_LOCATION_TEXT = text_templates.get_button_name(Button.SUGGESTION_LOCATION)  # MVP 4. b)
SETTING_SUBSCRIPTION_TEXT = text_templates.get_button_name(Button.SUBSCRIPTION)  # MVP 4. c)
SETTING_AUTO_COVID_INFO_TEXT = text_templates.get_button_name(Button.AUTO_COVID_INFO)  # MVP 4. d)
SETTING_LANGUAGE_TEXT = text_templates.get_button_name(Button.LANGUAGE)  # MVP 4. e)

# subscription keyboard buttons
SHOW_SUBSCRIPTION_TEXT = text_templates.get_button_name(Button.SHOW_SUBSCRIPTION)
DELETE_SUBSCRIPTION_TEXT = text_templates.get_button_name(Button.DELETE_SUBSCRIPTION)
ADD_SUBSCRIPTION_TEXT = text_templates.get_button_name(Button.ADD_SUBSCRIPTION)

# back to main keyboard button
BACK_TO_MAIN_TEXT = text_templates.get_button_name(Button.BACK_TO_MAIN_MENU)  # MVP 2.

# cancel inline button
CANCEL_TEXT = text_templates.get_button_name(Button.CANCEL)

# Choose answers
YES_TEXT = text_templates.get_answers(Answers.YES)  # MVP 4. a) Ja
NO_TEXT = text_templates.get_answers(Answers.NO)  # MVP 4. a) Nein

# delete subscription
DELETE_TEXT = text_templates.get_button_name(Button.DELETE)

# Send location
SEND_LOCATION_BUTTON_TEXT = text_templates.get_button_name(Button.SEND_LOCATION)  # MVP 4. b i)


# methods called from the ChatReceiver ---------------------------------------------------------------------------------


def start(chat_id: int, username: str):
    """
    This method is called when the user adds the bot (or /start is called) \n
    It then creates buttons on the keyboard so that the user can interact with the bot more uncomplicated and sends a
    greeting message to the user (chat_id)

    Arguments:
        chat_id: an integer for the chatID that the message is sent to
        username: a String representing the username
    """
    answer = text_templates.get_greeting_message(username)
    sender.send_message(chat_id, answer, _get_main_keyboard_buttons())


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
        data_service.set_user_state(chat_id, 1)
        # the keyboard for the settings menu
        keyboard = _get_settings_keyboard_buttons()
        sender.send_message(chat_id, text_templates.get_answers(Answers.SETTINGS), keyboard)
    elif button_text == WARNING_BUTTON_TEXT:
        data_service.set_user_state(chat_id, 2)
        # the keyboard for the manuel call of warnings
        keyboard = _get_warning_keyboard_buttons()
        sender.send_message(chat_id, text_templates.get_answers(Answers.WARNINGS), keyboard)
    elif button_text == TIP_BUTTON_TEXT:
        data_service.set_user_state(chat_id, 3)
        # TODO tips
        sender.send_message(chat_id, "TODO tips")
    elif button_text == HELP_BUTTON_TEXT:
        data_service.set_user_state(chat_id, 4)
        # TODO help
        sender.send_message(chat_id, "TODO help")
    else:
        error_handler(chat_id, ErrorCodes.NOT_IMPLEMENTED_YET)


def button_in_settings_pressed(chat_id: int, button_text: str):
    """
    This method gets called if a button of the Setting Keyboard is pressed (or the user types what the Button text says)
    and handles whatever the button is supposed to do (MVP 4.)

    Arguments:
        chat_id: an integer for the chatID that the message is sent to
        button_text: a string which is the text of the button that was pressed (constant of this class)
    """
    if button_text == SETTING_AUTO_WARNING_TEXT:
        command = Commands.AUTO_WARNING.value + " "
        markup = InlineKeyboardMarkup()
        button1 = sender.create_inline_button(YES_TEXT, command + "True")
        button2 = sender.create_inline_button(NO_TEXT, command + "False")
        button3 = sender.create_inline_button(CANCEL_TEXT, Commands.CANCEL_INLINE.value)
        markup.add(button1, button2, button3)
        sender.send_message(chat_id, text_templates.get_answers(Answers.AUTO_WARNINGS_TEXT), markup)
    elif button_text == SETTING_SUGGESTION_LOCATION_TEXT:
        data_service.set_user_state(chat_id, 10)
        keyboard = _get_send_location_keyboard()
        sender.send_message(chat_id, text_templates.get_answers(Answers.SUGGESTION_HELPER_TEXT), keyboard)
    elif button_text == SETTING_SUBSCRIPTION_TEXT:
        data_service.set_user_state(chat_id, 11)
        keyboard = _get_subscription_settings_keyboard()
        sender.send_message(chat_id, text_templates.get_answers(Answers.MANAGE_SUBSCRIPTIONS), keyboard)
    elif button_text == SETTING_AUTO_COVID_INFO_TEXT:
        markup = InlineKeyboardMarkup()
        command = Commands.COVID_UPDATES.value + " "

        for how_often in list(data_service.ReceiveInformation):
            how_often_text = text_templates.get_button_name(Button.__getitem__(how_often.name))
            button = sender.create_inline_button(how_often_text, command + str(how_often.value))
            markup.add(button)

        cancel_button = sender.create_inline_button(CANCEL_TEXT, Commands.CANCEL_INLINE.value)
        markup.add(cancel_button)
        sender.send_message(chat_id, text_templates.get_answers(Answers.MANAGE_AUTO_COVID_UPDATES), markup)
    elif button_text == SETTING_LANGUAGE_TEXT:
        sender.send_message(chat_id, "TODO " + button_text)
    else:
        error_handler(chat_id, ErrorCodes.NOT_IMPLEMENTED_YET)


def button_in_subscriptions_pressed(chat_id: int, button_text: str):
    """
    This method will be called when the user presses a Button (or the user types what the Button text says) in the
    Subscription Menu (MVP 4. c))

    Arguments:
        chat_id: an integer for the chatID that the message is sent to
        button_text: a string which is the text of the button that was pressed (constant of this class)
    """
    if button_text == ADD_SUBSCRIPTION_TEXT:
        data_service.set_user_state(chat_id, 110)
        keyboard = _get_send_location_keyboard()
        sender.send_message(chat_id, text_templates.get_add_subscription_message(), keyboard)
    elif button_text == DELETE_SUBSCRIPTION_TEXT:
        subscriptions = data_service.get_subscriptions(chat_id)
        if len(subscriptions.keys()) == 0:
            sender.send_message(chat_id, text_templates.get_answers(Answers.NO_SUBSCRIPTIONS))
            return

        markup = InlineKeyboardMarkup()
        for location in subscriptions.keys():
            command = Commands.DELETE_SUBSCRIPTION.value + " " + location + " "
            for warning in subscriptions[location]:
                button = sender.create_inline_button(location + ": " + warning + " " +
                                                     str(subscriptions[location][warning]), command + warning)
                markup.add(button)

        cancel_button = sender.create_inline_button(CANCEL_TEXT, Commands.CANCEL_INLINE.value)
        markup.add(cancel_button)
        sender.send_message(chat_id, text_templates.get_answers(Answers.DELETE_SUBSCRIPTION), markup)
    else:
        error_handler(chat_id, ErrorCodes.NOT_IMPLEMENTED_YET)


def inline_button_for_adding_subscriptions(chat_id: int, callback_command: str):
    """
    This method is called when the user presses an inline button during the process of adding a subscription
    The inline buttons the user could have pressed are:
    1. Selection of a warning type for the subscription
    2. Selection of a warning level for the subscription\n
    A case is selected based on the parameter callback_command. In case 1. the user is not done with adding a
    subscription so this method will go on with the process. In case 2. the user is done and the subscription will be
    added in the database.

    Arguments:
        chat_id: an integer for the chatID that the message is sent to
        callback_command: a string which contains the command that the inline buttons will send
    """
    split_command = callback_command.split(' ')
    if len(split_command) < 3:
        return
    location = split_command[1]
    warning = int(split_command[2])
    if len(split_command) == 3:
        # not done with process of adding subscription yet, ask for warning level
        markup = InlineKeyboardMarkup()

        # TODO add all Warning Level

        for i in [1, 2, 3, 4, 5]:
            button = sender.create_inline_button(str(i), callback_command + " " + str(i))
            markup.add(button)

        cancel_button = sender.create_inline_button(CANCEL_TEXT, Commands.CANCEL_INLINE.value)
        markup.add(cancel_button)
        message = text_templates.get_adding_subscription_level_message(
            location, _get_general_warning_name(nina_service.WarnType(warning)))
        sender.send_message(chat_id, message, markup)
    else:
        # done with process of adding subscription, and it can now be added
        warning_level = split_command[3]
        warning_type = nina_service.WarnType(warning)

        data_service.add_subscription(chat_id, location, str(warning_type.value), int(warning_level))

        show_subscriptions(chat_id)
        sender.send_message(chat_id, text_templates.get_add_subscription_message(), _get_send_location_keyboard())


def inline_button_for_deleting_subscriptions(chat_id: int, callback_command: str):
    """
    This method will be called when the user pressed an inline button to delete a subscription.
    The subscription to delete will be determined through the command (callback_command) the inline button will send.

    Arguments:
        chat_id: an integer for the chatID that the message is sent to
        callback_command: a string which contains the command that the inline buttons will send
    """
    split_command = callback_command.split(' ')
    if len(split_command) < 3:
        return
    location = split_command[1]
    warning = split_command[2]
    data_service.delete_subscription(chat_id, location, warning)
    warning_name = _get_general_warning_name(nina_service.WarnType(int(warning)))
    sender.send_message(chat_id, text_templates.get_delete_subscription_message(location, warning_name))


def normal_input_depending_on_state(chat_id: int, text: str):
    """
    This method will be called whenever the user sends a message to the bot that does not come from the menu.
    This message can either be not relevant so the user needs to know what was wrong,
    or it can be relevant, so it needs to be precessed properly.
    If it is relevant or not will be determined by the current state of the user.

    Arguments:
        chat_id: an integer for the chatID that the message is sent to
        text: a string which contains the message the user sent
    """
    state = data_service.get_user_state(chat_id)
    if state == 10:
        # TODO check if text is a valid location
        add_recommendation_in_database(chat_id, text)
    elif state == 110:
        # TODO check if text is a valid location
        markup = InlineKeyboardMarkup()
        command = Commands.ADD_SUBSCRIPTION.value + " " + text + " "

        for warning in list(nina_service.WarnType):
            if warning == nina_service.WarnType.NONE:
                break
            warn_name = _get_general_warning_name(warning)
            button = sender.create_inline_button(warn_name, command + str(warning.value))
            markup.add(button)

        cancel_button = sender.create_inline_button(CANCEL_TEXT, Commands.CANCEL_INLINE.value)
        markup.add(cancel_button)
        sender.send_message(chat_id, text_templates.get_adding_subscription_warning_message(text), markup)
    elif state == 20:
        covid_info(chat_id, text)
    elif state == 21:
        covid_rules(chat_id, text)
    else:
        error_handler(chat_id, ErrorCodes.UNKNOWN_COMMAND)


def show_suggestions(chat_id: int, button_text: str):
    """
    This method is called when the suggestions should be shown in chat with chat_id to finish a command.
    The button that was pressed will be determined via button_text.

    Arguments:
        chat_id: an integer for the chatID that the message is sent to
        button_text: a string which is the text of the button that was pressed (constant of this class)
    """
    command_first_part = Commands.COVID.value + " "
    if button_text == WARNING_COVID_INFO_TEXT:
        data_service.set_user_state(chat_id, 20)
        command_first_part = command_first_part + Commands.COVID_INFO.value + " "
    elif button_text == WARNING_COVID_RULES_TEXT:
        data_service.set_user_state(chat_id, 21)
        command_first_part = command_first_part + Commands.COVID_RULES.value + " "
    else:
        sender.send_message(chat_id, "Not implemented yet: " + button_text)
        return
    markup = InlineKeyboardMarkup()
    suggestions = data_service.get_suggestions(chat_id)
    button1 = sender.create_inline_button(suggestions[0], command_first_part + suggestions[0])
    button2 = sender.create_inline_button(suggestions[1], command_first_part + suggestions[1])
    button3 = sender.create_inline_button(suggestions[2], command_first_part + suggestions[2])
    button4 = sender.create_inline_button(CANCEL_TEXT, Commands.CANCEL_INLINE.value)
    markup.add(button1, button2, button3).add(button4)
    sender.send_message(chat_id, text_templates.get_answers(Answers.CLICK_SUGGESTION), markup)


def general_warning(chat_id: int, warning: nina_service.WarnType, warnings: list[nina_service.GeneralWarning] = None):
    """
    Sets the chat action of the bot to typing
    Calls for the warnings (warning) from the Nina API via the nina_service
    Or if warning is NONE then the given list warnings will be sent to the user
    Sends this information back to the chat (chat_id)
    """
    if warning != nina_service.WarnType.NONE:
        sender.send_chat_action(chat_id, "typing")
        warnings = nina_service.call_general_warning(warning)
        if len(warnings) == 0:
            sender.send_message(chat_id, text_templates.get_answers(Answers.NO_CURRENT_WARNINGS),
                                _get_warning_keyboard_buttons())
            return

    for warning in warnings:
        message = text_templates.get_general_warning_message(str(warning.id), str(warning.version), warning.start_date,
                                                             str(warning.severity.value), str(warning.type.name),
                                                             warning.title)
        sender.send_message(chat_id, message, _get_warning_keyboard_buttons())


def covid_info(chat_id: int, city_name: str, info: nina_service.CovidInfo = None):
    """
    Sets the chat action of the bot to typing
    Calls for covid information of a city (city_name) from the Nina API via the nina_service
    Or if the parameter info is set it will take this information instead
    Sends this information back to the chat (chat_id)

    Arguments:
        chat_id: an integer for the chatID that the message is sent to
        city_name: a string with the city name for the information of this city
        info: an Enum CovidInfo from nina_service if this parameter is set the info will not be pulled from nina_service
    """
    if info is None:
        sender.send_chat_action(chat_id, "typing")
        info = nina_service.get_covid_infos(city_name)
    message = text_templates.get_covid_info_message(city_name, info.infektionsgefahr_stufe,
                                                    info.sieben_tage_inzidenz_bundesland,
                                                    info.sieben_tage_inzidenz_kreis, info.allgemeine_hinweise)
    sender.send_message(chat_id, message, _get_warning_keyboard_buttons())


def covid_rules(chat_id: int, city_name: str, rules: nina_service.CovidRules = None):
    """
    Sets the chat action of the bot to typing\n
    Calls for covid rules of a city (city_name) from the Nina API via the nina_service\n
    Or if the parameter info is set it will take this information instead\n
    Sends this information back to the chat (chat_id)

    Arguments:
        chat_id: an integer for the chatID that the message is sent to
        city_name: a string with the city name for the rules of this city
        rules: an Enum of CovidRules from nina_service if this parameter is set the info will not be pulled from
            nina_service
    """
    if rules is None:
        sender.send_chat_action(chat_id, "typing")
        rules = nina_service.get_covid_rules(city_name)
    message = text_templates.get_covid_rules_message(city_name, rules.vaccine_info, rules.contact_terms,
                                                     rules.school_kita_rules,
                                                     rules.hospital_rules, rules.travelling_rules, rules.fines)
    sender.send_message(chat_id, message, _get_warning_keyboard_buttons())


def show_subscriptions(chat_id: int):
    """
    This method will send the current subscriptions to the user (chat_id)

    Arguments:
        chat_id: an integer for the chatID that the message is sent to
    """
    subscriptions = data_service.get_subscriptions(chat_id)
    if len(subscriptions.keys()) == 0:
        sender.send_message(chat_id, text_templates.get_answers(Answers.NO_SUBSCRIPTIONS))
        return
    subscriptions_text = []
    for location in subscriptions.keys():
        warnings = []
        levels = []
        for warning in subscriptions[location].keys():
            warnings.append(_get_general_warning_name(nina_service.WarnType(int(warning))))
            levels.append(str(subscriptions[location][warning]))
        subscriptions_text.append(text_templates.get_show_subscriptions_for_one_location_messsage(location, warnings,
                                                                                                  levels))
    message = text_templates.get_show_subscriptions_message(subscriptions_text)
    sender.send_message(chat_id, message)


def location_was_sent(chat_id: int, location: list):
    """
    This method turns the location into a city name or PLZ and\n
    - adds it to the recommendations in the database

    Arguments:
        chat_id: an integer for the chatID that the message is sent to
        location: Array with 2 entries for latitude and longitude
    """
    # TODO location verarbeiten mit state
    location_name = "Your_Location"
    add_recommendation_in_database(chat_id, location_name)


def change_auto_warning_in_database(chat_id: int, value: bool):
    """
    This method will change the boolean in the database which determines if the user will get automatic warnings or not

    Arguments:
        chat_id: an integer for the chatID that the message is sent to
        value: a boolean which determines if the user will get automatic warnings or not
    """
    data_service.set_receive_warnings(chat_id, value)
    if value:
        text = text_templates.get_answers(Answers.AUTO_WARNINGS_ENABLE)
    else:
        text = text_templates.get_answers(Answers.AUTO_WARNINGS_DISABLE)
    sender.send_message(chat_id, text)


def change_auto_covid_updates_in_database(chat_id: int, updates: int):
    """
    This method will change the integer in the database which determines how often the user wants automatic corona
    updates

    Arguments:
        chat_id: an integer for the chatID that the message is sent to
        updates: an integer with the value of the Enum ReceiveInformation in data_service
    """
    sender.send_chat_action(chat_id, "typing")
    how_often = data_service.ReceiveInformation(updates)
    how_often_text = text_templates.get_button_name(Button.__getitem__(how_often.name))
    data_service.set_auto_covid_information(chat_id, how_often)
    sender.send_message(chat_id, text_templates.get_changed_auto_covid_updates_message(how_often_text))


def add_recommendation_in_database(chat_id: int, location: str):
    """
    This method changes the recommended locations in the database and informs the user about the recommended locations
    that are stored now

    Arguments:
        chat_id: an integer for the chatID that the message is sent to
        location: a string with the location that should be added to the recommended locations in the database
    """
    # TODO check if location is valid
    # update the database
    suggestions = data_service.add_suggestion(chat_id, location)

    # inform the user
    message = text_templates.get_show_recommendations_message(suggestions)
    sender.send_message(chat_id, message, _get_send_location_keyboard())

# helper/short methods -------------------------------------------------------------------------------------------------


def back_to_main_keyboard(chat_id: int):
    """
    Sets the Keyboard (of the user = chat_id) to the Main Keyboard (Main Menu) \n
    Also sends a message which indicates that the user now is in the Main Menu

    Arguments:
        chat_id: an integer for the chatID that the message is sent to
    """
    data_service.set_user_state(chat_id, 0)
    keyboard = _get_main_keyboard_buttons()
    sender.send_message(chat_id, text_templates.get_answers(Answers.BACK_TO_MAIN_MENU), keyboard)


def delete_message(chat_id: int, message_id: int):
    """
    This method will delete the message (message_id) in the chat (chat_id).

    Arguments:
        chat_id: an integer for the chatID that the message is sent to
        message_id: an integer for the ID of the message
    """
    sender.delete_message(chat_id, message_id)


def error_handler(chat_id: int, error_code: ErrorCodes):
    sender.send_message(chat_id, "currently no real error message for error " + error_code.name)


def _get_general_warning_name(warn_type: nina_service.WarnType) -> str:
    button = Button.__getitem__(warn_type.name)
    return text_templates.get_button_name(button)

