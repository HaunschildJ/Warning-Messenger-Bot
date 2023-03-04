import datetime

from requests import HTTPError

import sender
import text_templates
import nina_service
import data_service
import place_converter
import frontend_helper
import warning_handler

from text_templates import Button, Answers
from enum_types import Commands, ReceiveInformation, WarningSeverity, ErrorCodes, WarningCategory, BotUsageHelp, \
    WarningType
from telebot.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from error import error_handler, illegal_state_handler, help_handler


def _make_location_suggestions(chat_id: int, dicts: list[dict], command_begin: str) -> tuple:
    """
    Suggests the user the given locations

    Args:
        chat_id: an Integer for the chat id of the user
        dicts: list with the dicts from place_converter
        command_begin: a string with the beginning of the callback command (has to end with ;)
    """
    markup = InlineKeyboardMarkup()

    if len(dicts) == 0:
        sender.send_message(chat_id, text_templates.get_answers(Answers.NO_LOCATION_FOUND))
        return ()

    if len(dicts) == 1:
        dic = dicts[0]
        district_id = place_converter.get_district_id_from_dict(dic)
        postal_code = place_converter.get_postal_code_from_dict(dic)
        return postal_code, district_id

    i = 0
    locations_text = []
    buttons = []
    for dic in dicts:
        place_name = place_converter.get_place_name_from_dict(dic)
        district_name = place_converter.get_district_name_from_dict(dic)
        district_id = place_converter.get_district_id_from_dict(dic)
        postal_code = place_converter.get_postal_code_from_dict(dic)
        button_name = str(i)
        if place_name is None:
            place_name = "---"

        command = command_begin + postal_code + ";" + district_id

        button = sender.create_inline_button(button_name, command)
        buttons.append(button)
        if len(buttons) == 3:
            markup.add(buttons[0], buttons[1], buttons[2])
            buttons = []
        locations_text.append(text_templates.get_select_location_for_one_location_messsage(district_name, place_name,
                                                                                           postal_code,
                                                                                           button_name))
        i = i + 1

    if len(buttons) == 2:
        markup.add(buttons[0], buttons[1])
    elif len(buttons) == 1:
        markup.add(buttons[0])

    answer = text_templates.get_select_location_message(locations_text)

    cancel_button = sender.create_inline_button(frontend_helper.CANCEL_TEXT, str(Commands.CANCEL_INLINE.value))
    markup.add(cancel_button)
    sender.send_message(chat_id, answer, markup)
    return ()


# methods called from the ChatReceiver ---------------------------------------------------------------------------------


def start(chat_id: int, username: str):
    """
    This method is called when the user adds the bot (or /start is called) \n
    It then creates buttons on the keyboard so that the user can interact with the bot more uncomplicated and sends a
    greeting message to the user (chat_id)

    Args:
        chat_id: an integer for the chatID that the message is sent to
        username: a String representing the username
    """
    answer = text_templates.get_greeting_message(username)
    data_service.set_user_state(chat_id, 0)
    sender.send_message(chat_id, answer, frontend_helper.get_main_keyboard_buttons())


def main_button_pressed(chat_id: int, button_text: str):
    """
    This method gets called if a button of the Main Keyboard is pressed (or the user types what the Button text says)
    and handles whatever the button is supposed to do (MVP 3.)

    Args:
        chat_id: an integer for the chatID that the message is sent to
        button_text: a string which is the text of the button that was pressed (constant of this class)
    """
    if button_text == frontend_helper.SETTING_BUTTON_TEXT:
        data_service.set_user_state(chat_id, 1)
        # the keyboard for the settings menu
        keyboard = frontend_helper.get_settings_keyboard_buttons()
        sender.send_message(chat_id, text_templates.get_answers(Answers.SETTINGS), keyboard)
    elif button_text == frontend_helper.WARNING_BUTTON_TEXT:
        data_service.set_user_state(chat_id, 2)
        # the keyboard for the manuel call of warnings
        keyboard = frontend_helper.get_warning_keyboard_buttons()
        sender.send_message(chat_id, text_templates.get_answers(Answers.WARNINGS), keyboard)
    elif button_text == frontend_helper.TIP_BUTTON_TEXT:
        data_service.set_user_state(chat_id, 0)
        # emergency tips
        markup = InlineKeyboardMarkup()
        yes_button = sender.create_inline_button(frontend_helper.YES_TEXT, Commands.SEND_PDF.value)
        no_button = sender.create_inline_button(frontend_helper.NO_TEXT, Commands.JUST_CANCEL_INLINE.value)
        markup.add(yes_button, no_button)
        sender.send_message(chat_id, text_templates.get_answers(Answers.EMERGENCY_TIPS))
        sender.send_message(chat_id, text_templates.get_answers(Answers.EMERGENCY_TIPS_ASK), markup)
    elif button_text == frontend_helper.HELP_BUTTON_TEXT:
        data_service.set_user_state(chat_id, 4)
        # the keyboard for the help menu
        keyboard = frontend_helper.get_help_keyboard_buttons()
        sender.send_message(chat_id, text_templates.get_answers(Answers.HELP), keyboard)
    else:
        error_handler(chat_id, ErrorCodes.NO_INPUT_EXPECTED, message=button_text)


def button_in_emergency_tips_pressed(chat_id: int, button_text: str):
    """
    This method gets called when the user presses a button (sends a message) while in the emergency tips menu state

    Args:
        chat_id: an integer for the chatID that the message is sent to
        button_text: a string which is the text of the button that was pressed
    """
    # TODO detect which tip was pressed when pdfs are received from nina_service
    sender.send_message(chat_id, "Noch nicht implementiert.")
    frontend_helper.back_to_main_keyboard(chat_id)


def button_in_help_pressed(chat_id: int, button_text: str):
    """
    This method gets called when the user presses a button (sends a message) while in the help menu state

    Args:
        chat_id: an integer for the chatID that the message is sent to
        button_text: a string which is the text of the button that was pressed
    """
    if button_text == frontend_helper.HELP_BOT_USAGE_TEXT:
        message = text_templates.get_help_message(BotUsageHelp.EVERYTHING)
        sender.send_message(chat_id, message)
    elif button_text == frontend_helper.HELP_FAQ_TEXT:
        message = text_templates.get_faq_message_from_templates()
        sender.send_message(chat_id, message)
    elif button_text == frontend_helper.HELP_IMPRINT_TEXT:
        sender.send_message(chat_id, text_templates.get_answers(Answers.IMPRINT_TEXT))
    elif button_text == frontend_helper.HELP_PRIVACY_TEXT:
        sender.send_message(chat_id, text_templates.get_answers(Answers.PRIVACY_TEXT))
    else:
        error_handler(chat_id, ErrorCodes.NO_INPUT_EXPECTED, message=button_text)


def button_in_manual_warnings_pressed(chat_id: int, button_text: str):
    """
    This method gets called when the user presses a button (sends a message) while in the manual warnings state

    Args:
        chat_id: an integer for the chatID that the message is sent to
        button_text: a string which is the text of the button that was pressed (constant of this class)
    """
    if button_text == str(frontend_helper.WARNING_COVID_TEXT):
        data_service.set_user_state(chat_id, 20)
        sender.send_message(chat_id, text_templates.get_answers(Answers.MANUAL_WARNING_COVID_CHOICE),
                            frontend_helper.get_covid_keyboard())
    elif button_text == str(frontend_helper.WARNING_COVID_INFO_TEXT):
        data_service.set_user_state(chat_id, 200)
        show_favorites_as_inline_buttons(chat_id, Commands.COVID_INFO.value + ";")
    elif button_text == str(frontend_helper.WARNING_COVID_RULES_TEXT):
        data_service.set_user_state(chat_id, 201)
        show_favorites_as_inline_buttons(chat_id, Commands.COVID_RULES.value + ";")
    elif button_text == str(frontend_helper.WARNING_WEATHER_TEXT):
        data_service.set_user_state(chat_id, 21)
        show_favorites_as_inline_buttons(chat_id, Commands.WEATHER.value + ";")
    elif button_text == str(frontend_helper.WARNING_CIVIL_PROTECTION_TEXT):
        data_service.set_user_state(chat_id, 22)
        show_favorites_as_inline_buttons(chat_id, Commands.CIVIL_PROTECTION.value + ";")
    elif button_text == str(frontend_helper.WARNING_FLOOD_TEXT):
        data_service.set_user_state(chat_id, 23)
        show_favorites_as_inline_buttons(chat_id, Commands.FLOOD.value + ";")
    elif button_text == str(frontend_helper.WARNING_ALL_TEXT):
        data_service.set_user_state(chat_id, 24)
        show_favorites_as_inline_buttons(chat_id, Commands.ALL_WARNINGS.value + ";")
    else:
        error_handler(chat_id, ErrorCodes.NO_INPUT_EXPECTED, message=button_text)


def button_in_settings_pressed(chat_id: int, button_text: str):
    """
    This method gets called if a button of the Setting Keyboard is pressed (or the user types what the Button text says)
    and handles whatever the button is supposed to do (MVP 4.)

    Args:
        chat_id: an integer for the chatID that the message is sent to
        button_text: a string which is the text of the button that was pressed (constant of this class)
    """
    if button_text == frontend_helper.SETTING_DELETE_DATA_TEXT:
        data_service.set_user_state(chat_id, 12)
        keyboard = frontend_helper.get_delete_data_keyboard()
        sender.send_message(chat_id, text_templates.get_answers(Answers.DELETE_DATA), keyboard)
    elif button_text == frontend_helper.SETTING_SUGGESTION_LOCATION_TEXT:
        data_service.set_user_state(chat_id, 11)
        keyboard = frontend_helper.get_send_location_keyboard()
        sender.send_message(chat_id, text_templates.get_answers(Answers.ADD_FAVORITE_HELPER_TEXT), keyboard)
    elif button_text == frontend_helper.SETTING_SUBSCRIPTION_TEXT:
        data_service.set_user_state(chat_id, 10)
        keyboard = frontend_helper.get_subscription_settings_keyboard()
        sender.send_message(chat_id, text_templates.get_answers(Answers.MANAGE_SUBSCRIPTIONS), keyboard)
    elif button_text == frontend_helper.SETTING_AUTO_COVID_INFO_TEXT:
        # currently not implemented
        markup = InlineKeyboardMarkup()
        command = Commands.COVID_UPDATES.value + " "

        for how_often in list(ReceiveInformation):
            how_often_text = text_templates.get_button_name(Button[how_often.name])
            button = sender.create_inline_button(how_often_text, command + str(how_often.value))
            markup.add(button)

        cancel_button = sender.create_inline_button(frontend_helper.CANCEL_TEXT, str(Commands.CANCEL_INLINE.value))
        markup.add(cancel_button)
        sender.send_message(chat_id, text_templates.get_answers(Answers.MANAGE_AUTO_COVID_UPDATES), markup)
    elif button_text == frontend_helper.SETTING_LANGUAGE_TEXT:
        # currently not implemented
        sender.send_message(chat_id, "not implemented " + button_text)
    else:
        error_handler(chat_id, ErrorCodes.NO_INPUT_EXPECTED, message=button_text)


def button_in_subscriptions_pressed(chat_id: int, button_text: str):
    """
    This method will be called when the user presses a Button (or the user types what the Button text says) in the
    Subscription Menu (MVP 4. c))

    Args:
        chat_id: an integer for the chatID that the message is sent to
        button_text: a string which is the text of the button that was pressed (constant of this class)
    """
    if button_text == frontend_helper.SHOW_SUBSCRIPTION_TEXT:
        show_subscriptions(chat_id, True)
        data_service.set_user_state(chat_id, 10)
    elif button_text == frontend_helper.ADD_SUBSCRIPTION_TEXT:
        data_service.set_user_state(chat_id, 101)
        keyboard = frontend_helper.get_send_location_keyboard()
        sender.send_message(chat_id, text_templates.get_add_subscription_message(), keyboard)
    elif button_text == frontend_helper.DELETE_SUBSCRIPTION_TEXT:
        subscriptions = data_service.get_subscriptions(chat_id)
        if len(subscriptions.keys()) == 0:
            sender.send_message(chat_id, text_templates.get_answers(Answers.NO_SUBSCRIPTIONS))
            return

        data_service.set_user_state(chat_id, 10)
        markup = InlineKeyboardMarkup()
        buttons = []
        subscriptions_text = []
        i = 0
        for postal_code in subscriptions.keys():
            district_id = data_service.get_subscription_district_id(subscriptions[postal_code])
            command = Commands.DELETE_SUBSCRIPTION.value + ";" + postal_code + ";" + district_id + ";"
            location_name = get_location_name(district_id, postal_code)
            warnings = []
            levels = []
            corresponding_buttons = []
            for warning in subscriptions[postal_code]:
                if warning != "district_id":
                    warning_name = _get_general_warning_name(nina_service.WarningCategory(warning))
                    button_name = str(i)
                    button = sender.create_inline_button(button_name, command + warning)
                    warnings.append(warning_name)
                    level = str(subscriptions[postal_code][warning])
                    levels.append(text_templates.get_button_name(Button(level)))
                    corresponding_buttons.append(button_name)
                    buttons.append(button)
                    if len(buttons) == 3:
                        markup.add(buttons[0], buttons[1], buttons[2])
                        buttons = []
                    i = i + 1
            subscriptions_text.append(
                text_templates.get_delete_subscriptions_for_one_location_messsage(location_name, warnings, levels,
                                                                                  corresponding_buttons))

        answer = text_templates.get_delete_subscriptions_message(subscriptions_text)
        if len(buttons) == 2:
            markup.add(buttons[0], buttons[1])
        elif len(buttons) == 1:
            markup.add(buttons[0])

        cancel_button = sender.create_inline_button(frontend_helper.CANCEL_TEXT, str(Commands.JUST_CANCEL_INLINE.value))
        markup.add(cancel_button)
        sender.send_message(chat_id, answer, markup)
    elif button_text == frontend_helper.DEFAULT_LEVEL_TEXT:
        data_service.set_user_state(chat_id, 103)
        answer = text_templates.get_answers(Answers.DEFAULT_LEVEL)
        markup = InlineKeyboardMarkup()
        command = Commands.SET_DEFAULT_LEVEL.value + ";"

        buttons = []
        default_levels = list(WarningSeverity)
        default_levels.remove(WarningSeverity.EXTREME)
        default_levels.remove(WarningSeverity.MODERATE)
        for level in default_levels:
            level_name = text_templates.get_button_name(Button[level.name])
            buttons.append(sender.create_inline_button(level_name, command + str(level.value)))

        markup.add(buttons[0], buttons[1]).add(buttons[2])
        sender.send_message(chat_id, answer, markup)
    elif button_text == frontend_helper.SILENCE_SUBSCRIPTIONS_TEXT:
        data_service.set_user_state(chat_id, 10)
        command = Commands.AUTO_WARNING.value + " "
        markup = InlineKeyboardMarkup()
        yes_button = sender.create_inline_button(frontend_helper.YES_TEXT, command + "True")
        no_button = sender.create_inline_button(frontend_helper.NO_TEXT, command + "False")
        cancel_button = sender.create_inline_button(frontend_helper.CANCEL_TEXT, str(Commands.JUST_CANCEL_INLINE.value))
        markup.add(yes_button, no_button, cancel_button)
        sender.send_message(chat_id, text_templates.get_answers(Answers.AUTO_WARNINGS_TEXT), markup)
    else:
        error_handler(chat_id, ErrorCodes.NO_INPUT_EXPECTED, message=button_text)


def button_in_delete_data_pressed(chat_id: int, button_text: str):
    """
    This method will be called when the user presses a button in the delete data menu

    Args:
        chat_id: an integer for the chatID that the message is sent to
        button_text: a string which is the text of the button that was pressed (constant of this class)
    """
    markup = InlineKeyboardMarkup()
    if button_text == frontend_helper.DELETE_DATA_SUBSCRIPTIONS_TEXT:
        answer = text_templates.get_answers(Answers.DELETE_DATA_SUBSCRIPTIONS)
        command = str(Commands.DELETE_DATA_SUBSCRIPTIONS.value)
        data_service.set_user_state(chat_id, 120)
    elif button_text == frontend_helper.DELETE_DATA_FAVORITES_TEXT:
        answer = text_templates.get_answers(Answers.DELETE_DATA_FAVORITES)
        command = str(Commands.DELETE_DATA_FAVORITES.value)
        data_service.set_user_state(chat_id, 121)
    elif button_text == frontend_helper.DELETE_DATA_EVERYTHING_TEXT:
        answer = text_templates.get_answers(Answers.DELETE_DATA_EVERYTHING)
        command = str(Commands.DELETE_DATA_EVERYTHING.value)
        data_service.set_user_state(chat_id, 122)
    else:
        error_handler(chat_id, ErrorCodes.NO_INPUT_EXPECTED, message=button_text)
        return
    yes_button = sender.create_inline_button(frontend_helper.YES_TEXT, command)
    cancel_button = sender.create_inline_button(frontend_helper.CANCEL_TEXT, str(Commands.CANCEL_INLINE.value))
    markup.add(yes_button, cancel_button)
    sender.send_message(chat_id, answer, markup)


def delete_data_confirmed(chat_id: int, command: str):
    """
    This method will be called when the user pressed yes when deleting data

    Args:
        chat_id: an integer for the chatID that the message is sent to
        command: string with the callback data from the yes button
            (Commands.DELETE_DATA_SUBSCRIPTIONS.value || Commands.DELETE_DATA_FAVORITES.value ||
            Commands.DELETE_DATA_EVERYTHING.value)
    """
    if command == Commands.DELETE_DATA_SUBSCRIPTIONS.value:
        sender.send_message(chat_id, text_templates.get_answers(Answers.DELETE_SUBSCRIPTIONS),
                            frontend_helper.get_delete_data_keyboard())
        data_service.set_user_state(chat_id, 12)
        data_service.delete_all_subscriptions(chat_id)
    elif command == Commands.DELETE_DATA_FAVORITES.value:
        sender.send_message(chat_id, text_templates.get_answers(Answers.DELETE_FAVORITES),
                            frontend_helper.get_delete_data_keyboard())
        data_service.set_user_state(chat_id, 12)
        data_service.reset_favorites(chat_id)
    elif command == Commands.DELETE_DATA_EVERYTHING.value:
        sender.send_message(chat_id, text_templates.get_answers(Answers.DELETE_EVERYTHING),
                            frontend_helper.get_main_keyboard_buttons())
        data_service.set_user_state(chat_id, 0)
        data_service.delete_user(chat_id)
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

    Args:
        chat_id: an integer for the chatID that the message is sent to
        callback_command: a string which contains the command that the inline buttons will send
    """
    split_command = callback_command.split(';')
    if len(split_command) < 3:
        return
    district_id = split_command[2]
    postal_code = split_command[1]
    location_name = get_location_name(district_id, postal_code)
    if len(split_command) == 3:
        markup = InlineKeyboardMarkup()

        for warning in list(WarningCategory):
            if warning == WarningCategory.NONE:
                continue
            warn_name = _get_general_warning_name(warning)
            button = sender.create_inline_button(warn_name, callback_command + ";" + str(warning.value))
            markup.add(button)

        cancel_button = sender.create_inline_button(frontend_helper.CANCEL_TEXT, str(Commands.CANCEL_INLINE.value))
        markup.add(cancel_button)
        sender.send_message(chat_id, text_templates.get_adding_subscription_warning_message(location_name), markup)
        return
    warning = split_command[3]
    if len(split_command) == 4:
        # first see if user has set a default level
        default_level = data_service.get_default_level(chat_id)
        if default_level != WarningSeverity.MANUAL:
            default_button = Button[default_level.name]
            inline_button_for_adding_subscriptions(chat_id, callback_command + ";" + str(default_button.value))
            return
        # not done with process of adding subscription yet, ask for warning level
        markup = InlineKeyboardMarkup()

        buttons = []
        for button_level in [Button.MINOR, Button.SEVERE]:
            button_name = text_templates.get_button_name(button_level)
            button = sender.create_inline_button(button_name, callback_command + ";" + str(button_level.value))
            buttons.append(button)

        markup.add(buttons[0], buttons[1])

        cancel_button = sender.create_inline_button(frontend_helper.CANCEL_TEXT, str(Commands.CANCEL_INLINE.value))
        markup.add(cancel_button)
        message = text_templates.get_adding_subscription_level_message(
            location_name, _get_general_warning_name(WarningCategory(warning)))
        sender.send_message(chat_id, message, markup)
    else:
        # done with process of adding subscription, and it can now be added
        warning_level = split_command[4]
        warning_type = WarningCategory(warning)

        # add to database
        if warning_type == WarningCategory.ALL_WARNINGS:
            for one_warning in list(WarningCategory):
                if one_warning == WarningCategory.NONE or one_warning == WarningCategory.ALL_WARNINGS:
                    continue
                data_service.add_subscription(chat_id, postal_code, district_id,
                                              str(one_warning.value), str(warning_level))
        else:
            data_service.add_subscription(chat_id, postal_code, district_id,
                                          str(warning_type.value), str(warning_level))
        # set state right (subscriptions settings)
        markup = frontend_helper.get_subscription_settings_keyboard()
        data_service.set_user_state(chat_id, 10)
        # show subscriptions
        show_subscriptions(chat_id, only_show=False, markup=markup)


def inline_button_for_deleting_subscriptions(chat_id: int, callback_command: str):
    """
    This method will be called when the user pressed an inline button to delete a subscription.
    The subscription to delete will be determined through the command (callback_command) the inline button will send.

    Args:
        chat_id: an integer for the chatID that the message is sent to
        callback_command: a string which contains the command that the inline buttons will send
    """
    split_command = callback_command.split(';')
    if len(split_command) < 4:
        return
    postal_code = split_command[1]
    district_id = split_command[2]
    warning = split_command[3]
    data_service.delete_subscription(chat_id, postal_code, warning)

    warning_name = _get_general_warning_name(nina_service.WarningCategory(warning))
    location_name = get_location_name(district_id, postal_code)
    sender.send_message(chat_id, text_templates.get_delete_subscription_message(location_name, warning_name))


def location_for_favorites(chat_id: int, text: str):
    """
    This method will be called when the user is in the state for adding a location to favorites and then sends a message

    Args:
        chat_id: an integer for the chatID that the message is sent to
        text: a string which contains the message the user sent
    """
    try:
        command_begin = Commands.ADD_FAVORITE.value + ";"
        suggestion_dicts = place_converter.get_non_covid_dict_suggestions(text)
        result = _make_location_suggestions(chat_id, suggestion_dicts, command_begin)
        if result != ():
            add_favorites_in_database(chat_id, result[0], result[1])
    except KeyError:
        error_handler(chat_id, ErrorCodes.UNKNOWN_LOCATION)


def location_for_adding_subscription(chat_id: int, text: str):
    """
    This method will be called when the user is in the state for adding a subscription and then sends a message

    Args:
        chat_id: an integer for the chatID that the message is sent to
        text: a string which contains the message the user sent
    """
    try:
        command_begin = Commands.ADD_SUBSCRIPTION.value + ";"
        suggestion_dicts = place_converter.get_non_covid_dict_suggestions(text)
        result = _make_location_suggestions(chat_id, suggestion_dicts, command_begin)
        if result != ():
            inline_button_for_adding_subscriptions(chat_id, command_begin + result[0] + ";" + result[1])
    except KeyError:
        error_handler(chat_id, ErrorCodes.UNKNOWN_LOCATION)


def location_for_warning(chat_id: int, text: str, command: Commands):
    """
    This method will be called when the user is in the state for calling a warning
    and then sends a message

    Args:
        chat_id: an integer for the chatID that the message is sent to
        text: a string which contains the message the user sent
        command: the Command that should be used
    """
    # just for the test warning
    warning_category = WarningCategory.NONE
    if command.value == Commands.WEATHER.value:
        warning_category = WarningCategory.WEATHER
    elif command.value == Commands.CIVIL_PROTECTION.value:
        warning_category = WarningCategory.CIVIL_PROTECTION
    elif command.value == Commands.FLOOD.value:
        warning_category = WarningCategory.FLOOD
    elif command.value == Commands.ALL_WARNINGS.value:
        warning_category = WarningCategory.ALL_WARNINGS
    if text.lower() == "teststadt":
        if warning_category is not WarningCategory.NONE:
            default_general_warning_for_test_location(chat_id, warning_category)
            return
    if text.lower() == "testhausen":
        if warning_category is not WarningCategory.NONE:
            try:
                general_warnings = nina_service.call_general_warning(warning_category)
                text = warning_handler.get_random_postal_code_for_active_warning(general_warnings[0])
            except IndexError:
                text = "64285"
    # end of "just for the test warning"
    try:
        command_begin = command.value + ";"
        suggestion_dicts = place_converter.get_non_covid_dict_suggestions(text)
        result = _make_location_suggestions(chat_id, suggestion_dicts, command_begin)
        if result != ():
            postal_code = result[0]
            district_id = result[1]
            if command.value == Commands.WEATHER.value:
                detailed_general_warning(chat_id, WarningCategory.WEATHER, postal_code, district_id)
            elif command.value == Commands.CIVIL_PROTECTION.value:
                detailed_general_warning(chat_id, WarningCategory.CIVIL_PROTECTION, postal_code, district_id)
            elif command.value == Commands.FLOOD.value:
                detailed_general_warning(chat_id, WarningCategory.FLOOD, postal_code, district_id)
            elif command.value == Commands.ALL_WARNINGS.value:
                categories = list(WarningCategory)
                categories.remove(WarningCategory.ALL_WARNINGS)
                categories.remove(WarningCategory.NONE)
                for category in categories:
                    detailed_general_warning(chat_id, category, postal_code, district_id, True)
            elif command.value == Commands.COVID_INFO.value:
                covid_info(chat_id, postal_code, district_id)
            elif command.value == Commands.COVID_RULES.value:
                covid_rules(chat_id, postal_code, district_id)
    except KeyError:
        error_handler(chat_id, ErrorCodes.UNKNOWN_LOCATION)


def show_favorites_as_inline_buttons(chat_id: int, command_begin: str):
    """
    This method is called when the favorites should be shown in chat with chat_id to finish a command.

    Args:
        chat_id: an integer for the chatID that the message is sent to
        command_begin: a string with the beginning of the command of each favorite (has to end with ';')
    """
    markup = InlineKeyboardMarkup()
    favorites = data_service.get_favorites(chat_id)
    for favorite in favorites:
        postal_code = data_service.get_favorite_postal_code(favorite)
        district_id = data_service.get_favorite_district_id(favorite)
        location_name = get_location_name(district_id, postal_code)
        button = sender.create_inline_button(location_name, command_begin + postal_code + ";" + district_id)
        markup.add(button)
    cancel_button = sender.create_inline_button(frontend_helper.CANCEL_TEXT, str(Commands.CANCEL_INLINE.value))
    markup.add(cancel_button)
    sender.send_message(chat_id, text_templates.get_answers(Answers.CLICK_ADD_FAVORITE), markup)


def default_general_warning_for_test_location(chat_id: int, warning: WarningCategory):
    """
    This method will send a dummy general warning in the chat

    Args:
        chat_id: integer with the chat id
        warning: WarningCategory Enum with the Warning Category (currently does nothing)
    """
    if warning == WarningCategory.WEATHER:
        title = "Amtliche WARNUNG vor SCHWEREN STURMBÖEN"
        desc = "Es treten oberhalb 1000 m schwere Sturmböen mit Geschwindigkeiten zwischen 80 km/h " \
               "(22 m/s, 44 kn, Bft 9) und 100 km/h (28 m/s, 55 kn, Bft 10) aus nordöstlicher Richtung auf. " \
               "In exponierten Lagen muss mit orkanartigen Böen um 110 km/h (31 m/s, 60 kn, Bft 11) gerechnet werden."
    elif warning == WarningCategory.FLOOD:
        title = "Titel"
        desc = "Beschreibung"
    else:
        title = "+++ Betretungsverbot Bergschadensgebiet Stadt Mechernich +++"
        desc = "Die Stadt Mechernich informiert: Die Flutschäden im Juli haben zu einigen Absenkungen im " \
               "Bergschadensgebiet Mechernich geführt, die noch nicht alle verfüllt werden konnten. Der Bereich " \
               "bleibt bis auf weiteres abgesperrt. Aus diesem Grund besteht weiterhin eine Gefahr, sodass das " \
               "Betretungsverbot noch bestehen bleibt."
    general_warning = nina_service.GeneralWarning("Test_ID", 0, "2023-02-25 06:51", WarningSeverity.MINOR,
                                                  WarningType.UPDATE, "Test Warnung")
    detailed_warning_info = nina_service.DetailedWarningInfo("event", WarningSeverity.MINOR, "2042-01-27 02:00",
                                                             "Dies ist eine Test Warnung!\n" + title, desc,
                                                             "deutsch", [])
    detailed_warning = nina_service.DetailedWarning("Test_ID", "Warning_Messenger_Bot", "date_sent", "status",
                                                    detailed_warning_info, "https://warnung.bund.de/meldung")
    send_detailed_general_warnings(chat_id, [general_warning], [], detailed_warning)


def detailed_general_warning(chat_id: int, warning: WarningCategory, postal_code: str, district_id: str,
                             is_for_all: bool = False):
    """
    Sets the chat action of the bot to typing
    Calls for the warnings (warning) from the Nina API via the nina_service
    Sends this information back to the chat (chat_id)
    And if the user has no subscription for the given postal_code this method will ask the user if they want to add this
    warning as a subscription

    Args:
        chat_id: an integer for the chatID that the message is sent to
        warning: WarnType enum for the general warning that should be sent to the user
        postal_code: string with the postal code
        district_id: string with the district id
        is_for_all: boolean when true this method was called when asking for all warning categories at once
    """
    if warning == nina_service.WarningCategory.NONE:
        return
    sender.send_chat_action(chat_id, "typing")
    keyboard = frontend_helper.get_warning_keyboard_buttons()
    data_service.set_user_state(chat_id, 2)
    try:
        warnings = nina_service.call_general_warning(warning)
    except HTTPError:
        error_handler(chat_id, ErrorCodes.NINA_API)
        return
    if len(warnings) == 0:
        sender.send_message(chat_id, text_templates.get_no_current_warnings_message(_get_general_warning_name(warning)),
                            keyboard)
        if is_for_all:
            warning = WarningCategory.ALL_WARNINGS
        ask_if_add_to_subscriptions(chat_id, warning, postal_code, district_id)
        return

    num_sent = send_detailed_general_warnings(chat_id, warnings, [postal_code])
    if num_sent == 0:
        sender.send_message(chat_id, text_templates.get_no_current_warnings_message(_get_general_warning_name(warning)),
                            keyboard)
    if is_for_all:
        warning = WarningCategory.ALL_WARNINGS
    ask_if_add_to_subscriptions(chat_id, warning, postal_code, district_id)


def ask_if_add_to_subscriptions(chat_id: int, warning: WarningCategory, postal_code: str, district_id: str):
    """
    This method will check if the user already has a subscription for this postal code, if not the user will be asked if
    they want to add this subscription

    Args:
        chat_id: integer with the chat id
        warning: WarningCategory Enum with the warning Category for the subscription
        postal_code: string with the postal code for the subscription
        district_id: string with the district id for the subscription
    """
    subscriptions = data_service.get_subscriptions(chat_id)
    # if the called warning is not in the users subscriptions yet, ask if they want to add it
    if postal_code not in subscriptions:
        markup = InlineKeyboardMarkup()
        command = Commands.ADD_SUBSCRIPTION.value + ";" + postal_code + ";" + district_id + ";"

        yes_button = sender.create_inline_button(text_templates.get_answers(Answers.YES), command + str(warning.value))

        cancel_button = sender.create_inline_button(frontend_helper.NO_TEXT, str(Commands.JUST_CANCEL_INLINE.value))
        markup.add(yes_button, cancel_button)

        location_name = get_location_name(district_id, postal_code)
        warning_name = _get_general_warning_name(warning)
        answer = text_templates.get_quickly_add_to_subscriptions_message(location_name, warning_name)
        sender.send_message(chat_id, answer, markup)


def send_detailed_general_warnings(chat_id: int, general_warnings: list[nina_service.GeneralWarning],
                                   relevant_postal_codes: list[str],
                                   detail_for_testing: nina_service.DetailedWarning = None) -> int:
    """
    This method will send a detailed warning for each warning in general_warnings when the warning is relevant for
    at least one of the given postal codes (relevant_postal_codes)

    Args:
        chat_id: integer for the users chat id
        general_warnings: list of GeneralWarning enum for all general_warnings which could be relevant for sending
        relevant_postal_codes: list of postal code strings.
                            If the general warning has a postal code that is in this list
                            the detailed warning will be sent to the user with the chat_id
        detail_for_testing: DetailedWarning which is only used when the user asks for the test location


    Returns:
        integer with the number of relevant warnings that were sent
    """
    # just for the test location
    if detail_for_testing is not None:
        relevant_warning_ids = [general_warnings[0].id]
    else:
        relevant_warning_ids = warning_handler.get_all_relevant_warning_ids(general_warnings, relevant_postal_codes)

    for warning_id in relevant_warning_ids:
        try:
            # just for the test location
            if detail_for_testing is not None:
                detail = detail_for_testing
            else:
                detail = nina_service.get_detailed_warning(warning_id)
            event = detail.info.event
            headline = detail.info.headline
            description = detail.info.description
            severity_value = detail.info.severity
            severity = text_templates.get_button_name(Button[severity_value.name])
            warning_type = ""
            start_date = ""
            for warning in general_warnings:
                if warning.id == warning_id:
                    warning_type = warning.type.value
                    start_date = warning.start_date
                    break
            date_expires = detail.info.date_expires
            status = detail.status
            link = detail.government_warning_url
            answer = text_templates.get_general_warning_message(event, headline, description, severity, warning_type,
                                                                start_date, date_expires, status, link)
            sender.send_message(chat_id, answer, frontend_helper.get_warning_keyboard_buttons())
            data_service.set_user_state(chat_id, 2)
        except HTTPError:
            pass
    return len(relevant_warning_ids)


def covid_info(chat_id: int, postal_code: str, district_id: str, info: nina_service.CovidInfo = None):
    """
    Sets the chat action of the bot to typing
    Calls for covid information of a city from the Nina API via the nina_service
    Or if the parameter info is set it will take this information instead
    Sends this information back to the chat (chat_id)

    Args:
        chat_id: an integer for the chatID that the message is sent to
        postal_code: a string with the postal code of the city
        district_id: a string with the district id for the rules of this city
        info: an Enum CovidInfo from nina_service if this parameter is set the info will not be pulled from nina_service
    """
    if info is None:
        sender.send_chat_action(chat_id, "typing")
        try:
            info = nina_service.get_covid_infos(district_id)
        except:
            error_handler(chat_id, ErrorCodes.NINA_API)
            return
    location_name = get_location_name(district_id, postal_code)
    message = text_templates.get_covid_info_message(location_name, info.infektionsgefahr_stufe,
                                                    info.sieben_tage_inzidenz_bundesland,
                                                    info.sieben_tage_inzidenz_kreis, info.allgemeine_hinweise)
    data_service.set_user_state(chat_id, 20)
    sender.send_message(chat_id, message, frontend_helper.get_covid_keyboard())


def covid_rules(chat_id: int, postal_code: str, district_id: str, rules: nina_service.CovidRules = None):
    """
    Sets the chat action of the bot to typing\n
    Calls for covid rules of a city from the Nina API via the nina_service\n
    Or if the parameter info is set it will take this information instead\n
    Sends this information back to the chat (chat_id)

    Args:
        chat_id: an integer for the chatID that the message is sent to
        postal_code: a string with the postal code of the city
        district_id: a string with the district id for the rules of this city
        rules: an Enum of CovidRules from nina_service if this parameter is set the info will not be pulled from
            nina_service
    """
    if rules is None:
        sender.send_chat_action(chat_id, "typing")
        try:
            rules = nina_service.get_covid_rules(district_id)
        except HTTPError:
            error_handler(chat_id, ErrorCodes.NINA_API)
            return
    location_name = get_location_name(district_id, postal_code)
    message = text_templates.get_covid_rules_message(location_name, rules.vaccine_info, rules.contact_terms,
                                                     rules.school_kita_rules,
                                                     rules.hospital_rules, rules.travelling_rules, rules.fines)
    data_service.set_user_state(chat_id, 20)
    sender.send_message(chat_id, message, frontend_helper.get_covid_keyboard())


def show_subscriptions(chat_id: int, only_show: bool = False, markup: ReplyKeyboardMarkup = None):
    """
    This method will send the current subscriptions to the user (chat_id)

    Args:
        chat_id: an integer for the chatID that the message is sent to
        only_show: a boolean when True then the user only want to see subscriptions and has not recently added one
        markup: the markup for the user keyboard buttons
    """
    subscriptions = data_service.get_subscriptions(chat_id)
    if len(subscriptions.keys()) == 0:
        sender.send_message(chat_id, text_templates.get_answers(Answers.NO_SUBSCRIPTIONS))
        return
    subscriptions_text = []
    for postal_code in subscriptions.keys():
        district_id = data_service.get_subscription_district_id(subscriptions[postal_code])
        warnings = []
        levels = []
        for warning in subscriptions[postal_code].keys():
            if warning != "district_id":
                warnings.append(_get_general_warning_name(nina_service.WarningCategory(warning)))
                level = str(subscriptions[postal_code][warning])
                levels.append(text_templates.get_button_name(Button(level)))
        district_name = place_converter.get_district_name_for_district_id(district_id)
        place_name = place_converter.get_place_name_for_postal_code(postal_code)
        location_name = text_templates.get_display_name_for_location(district_name, place_name, postal_code)
        subscriptions_text.append(text_templates.get_show_subscriptions_for_one_location_messsage(location_name,
                                                                                                  warnings,
                                                                                                  levels))
    message = text_templates.get_show_subscriptions_message(subscriptions_text, only_show)
    sender.send_message(chat_id, message, markup)


def location_was_sent(chat_id: int, latitude: float, longitude: float):
    """
    This method turns the location into a city name or PLZ and\n
    - adds it to the recommendations in the database

    Args:
        chat_id: an integer for the chatID that the message is sent to
        latitude: float with latitude
        longitude: float with longitude
    """
    try:
        suggestion_dict = place_converter.get_non_covid_dict_from_coordinates(latitude=latitude, longitude=longitude)
    except:
        error_handler(chat_id, ErrorCodes.UNKNOWN_LOCATION)
        return
    state = data_service.get_user_state(chat_id)
    district_id = place_converter.get_district_id_from_dict(suggestion_dict)
    postal_code = place_converter.get_postal_code_from_dict(suggestion_dict)
    if state == 11:
        # add recommendation
        add_favorites_in_database(chat_id, postal_code, district_id)
    elif state == 101:
        # add subscription
        callback_data = Commands.ADD_SUBSCRIPTION.value + ";" + postal_code + ";" + district_id
        inline_button_for_adding_subscriptions(chat_id, callback_data)
    else:
        error_handler(chat_id, ErrorCodes.NO_INPUT_EXPECTED)
        return


def send_emergency_pdf(chat_id: int):
    """
    When this method is called the bot will send the emergency pdf to the user
    Args:
        chat_id: integer with the chat id
    """
    caption = text_templates.get_answers(Answers.PDF_CAPTION)
    sender.send_document(chat_id, data_service.open_file(frontend_helper.EMERGENCY_TIPS), caption)


def change_auto_warning_in_database(chat_id: int, value: bool):
    """
    This method will change the boolean in the database which determines if the user will get automatic warnings or not

    Args:
        chat_id: an integer for the chatID that the message is sent to
        value: a boolean which determines if the user will get automatic warnings or not
    """
    data_service.set_receive_warnings(chat_id, value)
    if value:
        text = text_templates.get_answers(Answers.AUTO_WARNINGS_ENABLE)
    else:
        text = text_templates.get_answers(Answers.AUTO_WARNINGS_DISABLE)
    data_service.set_user_state(chat_id, 10)
    sender.send_message(chat_id, text, frontend_helper.get_subscription_settings_keyboard())


def change_auto_covid_updates_in_database(chat_id: int, updates: int):
    """
    This method will change the integer in the database which determines how often the user wants automatic corona
    updates

    Args:
        chat_id: an integer for the chatID that the message is sent to
        updates: an integer with the value of the Enum ReceiveInformation in data_service
    """
    sender.send_chat_action(chat_id, "typing")
    how_often = data_service.ReceiveInformation(updates)
    how_often_text = text_templates.get_button_name(Button[how_often.name])
    data_service.set_auto_covid_information(chat_id, how_often)
    sender.send_message(chat_id, text_templates.get_changed_auto_covid_updates_message(how_often_text))


def add_favorites_in_database(chat_id: int, postal_code: str, district_id: str):
    """
    This method changes the recommended locations in the database and informs the user about the recommended locations
    that are stored now

    Args:
        chat_id: an integer for the chatID that the message is sent to
        postal_code: string with the postal code of the favorite
        district_id: string with district id of the favorite
    """
    # update the database
    favorites = data_service.add_favorite(chat_id, postal_code, district_id)

    # inform the user
    names = []
    for favorite in favorites:
        local_district_id = data_service.get_favorite_district_id(favorite)
        local_postal_code = data_service.get_favorite_postal_code(favorite)
        location_name = get_location_name(local_district_id, local_postal_code)
        names.append(location_name)
    message = text_templates.get_show_favorites_message(names)
    data_service.set_user_state(chat_id, 1)
    sender.send_message(chat_id, message, frontend_helper.get_settings_keyboard_buttons())


def set_default_level(chat_id: int, level: str):
    """
    This method will set the users default level in the database and send a reply to the user

    Args:
        chat_id: integer with the users chat id
        level: string with the new default level for the user
    """
    severity = WarningSeverity.MANUAL
    try:
        data_service.set_default_level(chat_id, WarningSeverity(level))
        severity = WarningSeverity(level)
    except ValueError:
        data_service.set_default_level(chat_id, WarningSeverity.MANUAL)
    message = text_templates.get_set_default_level_message(severity)
    data_service.set_user_state(chat_id, 10)
    sender.send_message(chat_id, message, frontend_helper.get_subscription_settings_keyboard())


# helper/short methods -------------------------------------------------------------------------------------------------


def delete_message(chat_id: int, message_id: int):
    """
    This method will delete the message (message_id) in the chat (chat_id).

    Args:
        chat_id: an integer for the chatID that the message is sent to
        message_id: an integer for the ID of the message
    """
    sender.delete_message(chat_id, message_id)


def _get_general_warning_name(warn_type: nina_service.WarningCategory) -> str:
    """
    Helper Method to convert a nina_service.WarnType to a string from text_templates
    """
    return text_templates.get_button_name(Button[warn_type.name])


def get_location_name(district_id: str, postal_code: str) -> str:
    district_name = place_converter.get_district_name_for_district_id(district_id)
    place_name = place_converter.get_place_name_for_postal_code(postal_code)
    return text_templates.get_display_name_for_location(district_name, place_name, postal_code)
