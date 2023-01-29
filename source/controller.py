import telebot.types

import sender
import text_templates
import nina_service
import data_service
import place_converter

from text_templates import Button, Answers
from enum_types import Commands, ReceiveInformation, WarningSeverity, ErrorCodes, WarnType, BotUsageHelp
from telebot.types import InlineKeyboardMarkup, ReplyKeyboardMarkup


def _get_main_keyboard_buttons() -> telebot.types.ReplyKeyboardMarkup:
    """
    This is a helper method which returns the keyboard for the MVP 3. menu

    Returns:
         telebot.types.ReplyKeyboardMarkup
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=False, one_time_keyboard=False, input_field_placeholder="Hauptmenü")
    settings = sender.create_button(SETTING_BUTTON_TEXT)
    warning = sender.create_button(WARNING_BUTTON_TEXT)
    tip = sender.create_button(TIP_BUTTON_TEXT)
    more = sender.create_button(HELP_BUTTON_TEXT)
    keyboard.add(warning).add(settings).add(tip, more)
    return keyboard


def _get_settings_keyboard_buttons() -> telebot.types.ReplyKeyboardMarkup:
    """
    This is a helper method which returns the keyboard for the MVP 4. menu

    Returns:
         telebot.types.ReplyKeyboardMarkup
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=False, one_time_keyboard=False)
    favorites = sender.create_button(SETTING_SUGGESTION_LOCATION_TEXT)
    subscriptions = sender.create_button(SETTING_SUBSCRIPTION_TEXT)
    delete_data = sender.create_button(SETTING_DELETE_DATA_TEXT)
    back = sender.create_button(BACK_TO_MAIN_TEXT)
    keyboard.add(subscriptions).add(favorites, delete_data).add(back)
    return keyboard


def _get_warning_keyboard_buttons() -> telebot.types.ReplyKeyboardMarkup:
    """
    This is a helper method which returns the keyboard for the MVP 5. menu

    Returns:
         telebot.types.ReplyKeyboardMarkup
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=False, one_time_keyboard=True)
    covid = sender.create_button(WARNING_COVID_TEXT)
    weather = sender.create_button(WARNING_WEATHER_TEXT)
    disaster = sender.create_button(WARNING_DISASTER_TEXT)
    flood = sender.create_button(WARNING_FLOOD_TEXT)
    general = sender.create_button(WARNING_GENERAL_TEXT)
    back = sender.create_button(BACK_TO_MAIN_TEXT)
    keyboard.add(covid).add(weather, disaster).add(flood, general).add(back)
    return keyboard


def _get_help_keyboard_buttons() -> telebot.types.ReplyKeyboardMarkup:
    """
    This is a helper method which returns the keyboard for the help menu

    Returns:
         telebot.types.ReplyKeyboardMarkup
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=False, one_time_keyboard=False)
    bot_info = sender.create_button(HELP_BOT_USAGE_TEXT)
    faq = sender.create_button(HELP_FAQ_TEXT)
    imprint = sender.create_button(HELP_IMPRINT_TEXT)
    privacy = sender.create_button(HELP_PRIVACY_TEXT)
    back = sender.create_button(BACK_TO_MAIN_TEXT)
    keyboard.add(bot_info, faq).add(imprint, privacy).add(back)
    return keyboard


def _get_covid_keyboard() -> telebot.types.ReplyKeyboardMarkup:
    """
    This is a helper method which returns the keyboard for manual warnings of covid

    Returns:
        telebot.types.ReplyKeyboardMarkup
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=False, one_time_keyboard=True)
    info = sender.create_button(WARNING_COVID_INFO_TEXT)
    rules = sender.create_button(WARNING_COVID_RULES_TEXT)
    back = sender.create_button(BACK_TO_MAIN_TEXT)
    keyboard.add(info).add(rules).add(back)
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
    show = sender.create_button(SHOW_SUBSCRIPTION_TEXT)
    add = sender.create_button(ADD_SUBSCRIPTION_TEXT)
    delete = sender.create_button(DELETE_SUBSCRIPTION_TEXT)
    default_level = sender.create_button(DEFAULT_LEVEL_TEXT)
    silence_subs = sender.create_button(SILENCE_SUBSCRIPTIONS_TEXT)
    back = sender.create_button(BACK_TO_MAIN_TEXT)
    keyboard.add(show).add(add, delete).add(default_level, silence_subs).add(back)
    return keyboard


def _get_delete_data_keyboard() -> telebot.types.ReplyKeyboardMarkup:
    """
    Helper method to get the delete data keyboard.

    Returns:
        Nothing
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=False, one_time_keyboard=True)
    subs = sender.create_button(DELETE_DATA_SUBSCRIPTIONS_TEXT)
    fav = sender.create_button(DELETE_DATA_FAVORITES_TEXT)
    everything = sender.create_button(DELETE_DATA_EVERYTHING_TEXT)
    back = sender.create_button(BACK_TO_MAIN_TEXT)
    keyboard.add(subs, fav).add(everything).add(back)
    return keyboard


def _make_location_suggestions(chat_id: int, dicts: list[dict], command_begin: str,
                               district_id_bool: bool = True, place_id_bool: bool = True):
    """
    When place_id_bool and district_id_bool are True then both will be in command (place_id first)

    Arguments:
        chat_id: an Integer for the chat id of the user
        dicts: list with the dicts from place_converter
        command_begin: a string with the beginning of the callback command (has to end with ;)
        district_id_bool: boolean when True the district_id will be in the command
        place_id_bool: boolean when True the place_id will be in command
    """
    markup = InlineKeyboardMarkup()

    if len(dicts) == 0:
        sender.send_message(chat_id, text_templates.get_answers(Answers.NO_LOCATION_FOUND))
        return

    i = 0
    locations_text = []
    buttons = []
    for dic in dicts:
        place_name = place_converter.get_place_name_from_dict(dic)
        district_name = place_converter.get_district_name_from_dict(dic)
        place_id = place_converter.get_place_id_from_dict(dic)
        district_id = place_converter.get_district_id_from_dict(dic)
        button_name = str(i)
        if place_name is None:
            place_name = "---"

        command = command_begin

        if not place_id_bool and not district_id_bool:
            error_handler(chat_id, ErrorCodes.NOT_IMPLEMENTED_YET)
            return
        if place_id_bool:
            command = command + place_id
            if district_id_bool:
                command = command + ";" + district_id
        else:
            if district_id_bool:
                command = command + district_id

        button = sender.create_inline_button(button_name, command)
        buttons.append(button)
        if len(buttons) == 3:
            markup.add(buttons[0], buttons[1], buttons[2])
            buttons = []
        locations_text.append(text_templates.get_select_location_for_one_location_messsage(district_name, place_name,
                                                                                           button_name))
        i = i + 1

    if len(buttons) == 2:
        markup.add(buttons[0], buttons[1])
    elif len(buttons) == 1:
        markup.add(buttons[0])

    answer = text_templates.get_select_location_message(locations_text)

    cancel_button = sender.create_inline_button(CANCEL_TEXT, str(Commands.CANCEL_INLINE.value))
    markup.add(cancel_button)
    sender.send_message(chat_id, answer, markup)


# global variables -----------------------------------------------------------------------------------------------------
# main keyboard buttons
SETTING_BUTTON_TEXT = text_templates.get_button_name(Button.SETTINGS)  # MVP 4.
WARNING_BUTTON_TEXT = text_templates.get_button_name(Button.WARNINGS)  # MVP 5.
TIP_BUTTON_TEXT = text_templates.get_button_name(Button.EMERGENCY_TIPS)  # MVP 6.
HELP_BUTTON_TEXT = text_templates.get_button_name(Button.HELP)  # MVP 7.

# warning keyboard buttons
WARNING_COVID_TEXT = text_templates.get_button_name(Button.COVID)
WARNING_COVID_INFO_TEXT = text_templates.get_button_name(Button.COVID_INFORMATION)  # MVP 5. i)
WARNING_COVID_RULES_TEXT = text_templates.get_button_name(Button.COVID_RULES)  # MVP 5. i)
WARNING_WEATHER_TEXT = text_templates.get_button_name(Button.WEATHER)  # MVP 5. i)
WARNING_DISASTER_TEXT = text_templates.get_button_name(Button.DISASTER)  # MVP 5. i)
WARNING_FLOOD_TEXT = text_templates.get_button_name(Button.FLOOD)  # MVP 5. i)
WARNING_GENERAL_TEXT = text_templates.get_button_name(Button.GENERAL)  # MVP 5. i)

# settings keyboard buttons
SETTING_SUGGESTION_LOCATION_TEXT = text_templates.get_button_name(Button.SUGGESTION_LOCATION)  # MVP 4. b)
SETTING_SUBSCRIPTION_TEXT = text_templates.get_button_name(Button.SUBSCRIPTION)  # MVP 4. c)
SETTING_DELETE_DATA_TEXT = text_templates.get_button_name(Button.DELETE_DATA)
SETTING_AUTO_COVID_INFO_TEXT = text_templates.get_button_name(Button.AUTO_COVID_INFO)  # currently not implemented
SETTING_LANGUAGE_TEXT = text_templates.get_button_name(Button.LANGUAGE)  # currently not implemented

# subscription keyboard buttons
SHOW_SUBSCRIPTION_TEXT = text_templates.get_button_name(Button.SHOW_SUBSCRIPTION)
DELETE_SUBSCRIPTION_TEXT = text_templates.get_button_name(Button.DELETE_SUBSCRIPTION)
ADD_SUBSCRIPTION_TEXT = text_templates.get_button_name(Button.ADD_SUBSCRIPTION)
DEFAULT_LEVEL_TEXT = text_templates.get_button_name(Button.DEFAULT_LEVEL)
SILENCE_SUBSCRIPTIONS_TEXT = text_templates.get_button_name(Button.AUTO_WARNING)

# help keyboard buttons
HELP_BOT_USAGE_TEXT = text_templates.get_button_name(Button.HELP_BOT_USAGE)
HELP_FAQ_TEXT = text_templates.get_button_name(Button.HELP_FAQ)
HELP_IMPRINT_TEXT = text_templates.get_button_name(Button.HELP_IMPRINT)
HELP_PRIVACY_TEXT = text_templates.get_button_name(Button.HELP_PRIVACY)

# delete data buttons
DELETE_DATA_SUBSCRIPTIONS_TEXT = text_templates.get_button_name(Button.DELETE_DATA_SUBSCRIPTIONS)
DELETE_DATA_FAVORITES_TEXT = text_templates.get_button_name(Button.DELETE_DATA_FAVORITES)
DELETE_DATA_EVERYTHING_TEXT = text_templates.get_button_name(Button.DELETE_DATA_EVERYTHING)

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
        data_service.set_user_state(chat_id, 0)  # remove when implemented
        sender.send_message(chat_id, "TODO tips")
    elif button_text == HELP_BUTTON_TEXT:
        data_service.set_user_state(chat_id, 4)
        keyboard = _get_help_keyboard_buttons()
        sender.send_message(chat_id, text_templates.get_answers(Answers.HELP), keyboard)
    else:
        error_handler(chat_id, ErrorCodes.MAIN_MENU)


def button_in_help_pressed(chat_id: int, button_text: str):
    """
    This method gets called when the user presses a button (sends a message) while in the help menu state

    Args:
        chat_id: an integer for the chatID that the message is sent to
        button_text: a string which is the text of the button that was pressed (constant of this class)
    """
    if button_text == HELP_BOT_USAGE_TEXT:
        message = text_templates.get_help_message(BotUsageHelp.EVERYTHING)
        sender.send_message(chat_id, message)
    elif button_text == HELP_FAQ_TEXT:
        # TODO get the FAQ from nina api
        questions = ["Wie würde eine Frage aussehen?", "Und wie die 2te?"]
        answers = ["So würde eine Antwort aussehen.", "Und so die 2te."]
        message = text_templates.get_faq_message(questions, answers)
        sender.send_message(chat_id, message)
    elif button_text == HELP_IMPRINT_TEXT:
        sender.send_message(chat_id, text_templates.get_answers(Answers.IMPRINT_TEXT))
    elif button_text == HELP_PRIVACY_TEXT:
        sender.send_message(chat_id, text_templates.get_answers(Answers.PRIVACY_TEXT))
    else:
        error_handler(chat_id, ErrorCodes.NO_INPUT_EXPECTED)


def button_in_manual_warnings_pressed(chat_id: int, button_text: str):
    """
    This method gets called when the user presses a button (sends a message) while in the manual warnings state

    Args:
        chat_id: an integer for the chatID that the message is sent to
        button_text: a string which is the text of the button that was pressed (constant of this class)
    """
    if button_text == WARNING_COVID_TEXT:
        data_service.set_user_state(chat_id, 20)
        sender.send_message(chat_id, text_templates.get_answers(Answers.MANUAL_WARNING_COVID_CHOICE),
                            _get_covid_keyboard())
    elif button_text == WARNING_COVID_INFO_TEXT:
        data_service.set_user_state(chat_id, 200)
        show_suggestions(chat_id, Commands.COVID_INFO.value + ";")
    elif button_text == WARNING_COVID_RULES_TEXT:
        data_service.set_user_state(chat_id, 201)
        show_suggestions(chat_id, Commands.COVID_RULES.value + ";")
    elif button_text == WARNING_WEATHER_TEXT:
        data_service.set_user_state(chat_id, 21)
        show_suggestions(chat_id, Commands.WEATHER.value + ";")
    elif button_text == WARNING_DISASTER_TEXT:
        data_service.set_user_state(chat_id, 22)
        show_suggestions(chat_id, Commands.DISASTER.value + ";")
    elif button_text == WARNING_FLOOD_TEXT:
        data_service.set_user_state(chat_id, 23)
        show_suggestions(chat_id, Commands.FLOOD.value + ";")
    elif button_text == WARNING_GENERAL_TEXT:
        data_service.set_user_state(chat_id, 24)
        show_suggestions(chat_id, Commands.GENERAL.value + ";")
    else:
        error_handler(chat_id, ErrorCodes.NO_INPUT_EXPECTED)


def button_in_settings_pressed(chat_id: int, button_text: str):
    """
    This method gets called if a button of the Setting Keyboard is pressed (or the user types what the Button text says)
    and handles whatever the button is supposed to do (MVP 4.)

    Arguments:
        chat_id: an integer for the chatID that the message is sent to
        button_text: a string which is the text of the button that was pressed (constant of this class)
    """
    if button_text == SETTING_DELETE_DATA_TEXT:
        data_service.set_user_state(chat_id, 12)
        keyboard = _get_delete_data_keyboard()
        sender.send_message(chat_id, text_templates.get_answers(Answers.DELETE_DATA), keyboard)
    elif button_text == SETTING_SUGGESTION_LOCATION_TEXT:
        data_service.set_user_state(chat_id, 11)
        keyboard = _get_send_location_keyboard()
        sender.send_message(chat_id, text_templates.get_answers(Answers.SUGGESTION_HELPER_TEXT), keyboard)
    elif button_text == SETTING_SUBSCRIPTION_TEXT:
        data_service.set_user_state(chat_id, 10)
        keyboard = _get_subscription_settings_keyboard()
        sender.send_message(chat_id, text_templates.get_answers(Answers.MANAGE_SUBSCRIPTIONS), keyboard)
    elif button_text == SETTING_AUTO_COVID_INFO_TEXT:
        # currently not implemented
        markup = InlineKeyboardMarkup()
        command = Commands.COVID_UPDATES.value + " "

        for how_often in list(ReceiveInformation):
            how_often_text = text_templates.get_button_name(Button[how_often.name])
            button = sender.create_inline_button(how_often_text, command + str(how_often.value))
            markup.add(button)

        cancel_button = sender.create_inline_button(CANCEL_TEXT, str(Commands.CANCEL_INLINE.value))
        markup.add(cancel_button)
        sender.send_message(chat_id, text_templates.get_answers(Answers.MANAGE_AUTO_COVID_UPDATES), markup)
    elif button_text == SETTING_LANGUAGE_TEXT:
        # currently not implemented
        sender.send_message(chat_id, "TODO " + button_text)
    else:
        error_handler(chat_id, ErrorCodes.SETTINGS)


def button_in_subscriptions_pressed(chat_id: int, button_text: str):
    """
    This method will be called when the user presses a Button (or the user types what the Button text says) in the
    Subscription Menu (MVP 4. c))

    Arguments:
        chat_id: an integer for the chatID that the message is sent to
        button_text: a string which is the text of the button that was pressed (constant of this class)
    """
    if button_text == SHOW_SUBSCRIPTION_TEXT:
        show_subscriptions(chat_id)
        data_service.set_user_state(chat_id, 10)
    elif button_text == ADD_SUBSCRIPTION_TEXT:
        data_service.set_user_state(chat_id, 101)
        keyboard = _get_send_location_keyboard()
        sender.send_message(chat_id, text_templates.get_add_subscription_message(), keyboard)
    elif button_text == DELETE_SUBSCRIPTION_TEXT:
        subscriptions = data_service.get_subscriptions(chat_id)
        if len(subscriptions.keys()) == 0:
            sender.send_message(chat_id, text_templates.get_answers(Answers.NO_SUBSCRIPTIONS))
            return

        data_service.set_user_state(chat_id, 10)
        markup = InlineKeyboardMarkup()
        buttons = []
        subscriptions_text = []
        i = 0
        for location in subscriptions.keys():
            command = Commands.DELETE_SUBSCRIPTION.value + " " + location + " "
            location_name = place_converter.get_name_for_id(location)
            warnings = []
            levels = []
            corresponding_buttons = []
            for warning in subscriptions[location]:
                warning_name = _get_general_warning_name(nina_service.WarnType(warning))
                button_name = str(i)
                button = sender.create_inline_button(button_name, command + warning)
                warnings.append(warning_name)
                level = str(subscriptions[location][warning])
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

        cancel_button = sender.create_inline_button(CANCEL_TEXT, str(Commands.CANCEL_INLINE.value))
        markup.add(cancel_button)
        sender.send_message(chat_id, answer, markup)
    elif button_text == DEFAULT_LEVEL_TEXT:
        data_service.set_user_state(chat_id, 103)
        answer = text_templates.get_answers(Answers.DEFAULT_LEVEL)
        markup = InlineKeyboardMarkup()
        command = Commands.SET_DEFAULT_LEVEL.value + ";"

        buttons = []
        for level in list(WarningSeverity):
            level_name = text_templates.get_button_name(Button[level.name])
            buttons.append(sender.create_inline_button(level_name, command + str(level.value)))

        markup.add(buttons[0], buttons[1], buttons[2]).add(buttons[3])
        sender.send_message(chat_id, answer, markup)
    elif button_text == SILENCE_SUBSCRIPTIONS_TEXT:
        data_service.set_user_state(chat_id, 104)
        command = Commands.AUTO_WARNING.value + " "
        markup = InlineKeyboardMarkup()
        yes_button = sender.create_inline_button(YES_TEXT, command + "True")
        no_button = sender.create_inline_button(NO_TEXT, command + "False")
        cancel_button = sender.create_inline_button(CANCEL_TEXT, str(Commands.CANCEL_INLINE.value))
        markup.add(yes_button, no_button, cancel_button)
        sender.send_message(chat_id, text_templates.get_answers(Answers.AUTO_WARNINGS_TEXT), markup)
    else:
        error_handler(chat_id, ErrorCodes.MANAGE_SUBSCRIPTIONS)


def button_in_delete_data_pressed(chat_id: int, button_text: str):
    """
    This method will be called when the user presses a button in the delete data menu

    Args:
        chat_id: an integer for the chatID that the message is sent to
        button_text: a string which is the text of the button that was pressed (constant of this class)
    """
    markup = InlineKeyboardMarkup()
    if button_text == DELETE_DATA_SUBSCRIPTIONS_TEXT:
        answer = text_templates.get_answers(Answers.DELETE_DATA_SUBSCRIPTIONS)
        command = str(Commands.DELETE_DATA_SUBSCRIPTIONS.value)
        data_service.set_user_state(chat_id, 120)
    elif button_text == DELETE_DATA_FAVORITES_TEXT:
        answer = text_templates.get_answers(Answers.DELETE_DATA_FAVORITES)
        command = str(Commands.DELETE_DATA_FAVORITES.value)
        data_service.set_user_state(chat_id, 121)
    elif button_text == DELETE_DATA_EVERYTHING_TEXT:
        answer = text_templates.get_answers(Answers.DELETE_DATA_EVERYTHING)
        command = str(Commands.DELETE_DATA_EVERYTHING.value)
        data_service.set_user_state(chat_id, 122)
    else:
        error_handler(chat_id, ErrorCodes.NO_INPUT_EXPECTED)
        return
    yes_button = sender.create_inline_button(YES_TEXT, command)
    cancel_button = sender.create_inline_button(CANCEL_TEXT, str(Commands.CANCEL_INLINE.value))
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
                            _get_delete_data_keyboard())
        data_service.set_user_state(chat_id, 12)
        data_service.delete_all_subscriptions(chat_id)
    elif command == Commands.DELETE_DATA_FAVORITES.value:
        sender.send_message(chat_id, text_templates.get_answers(Answers.DELETE_FAVORITES),
                            _get_delete_data_keyboard())
        data_service.set_user_state(chat_id, 12)
        data_service.reset_favorites(chat_id)
    elif command == Commands.DELETE_DATA_EVERYTHING.value:
        sender.send_message(chat_id, text_templates.get_answers(Answers.DELETE_EVERYTHING),
                            _get_main_keyboard_buttons())
        data_service.set_user_state(chat_id, 0)
        data_service.remove_user(chat_id)
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
    split_command = callback_command.split(';')
    if len(split_command) < 2:
        return
    location = split_command[1]
    location_name = place_converter.get_name_for_id(location)
    if len(split_command) == 2:
        markup = InlineKeyboardMarkup()
        command = Commands.ADD_SUBSCRIPTION.value + ";" + location + ";"

        for warning in list(nina_service.WarnType):
            if warning == nina_service.WarnType.NONE:
                break
            warn_name = _get_general_warning_name(warning)
            button = sender.create_inline_button(warn_name, command + str(warning.value))
            markup.add(button)

        cancel_button = sender.create_inline_button(CANCEL_TEXT, str(Commands.CANCEL_INLINE.value))
        markup.add(cancel_button)
        sender.send_message(chat_id, text_templates.get_adding_subscription_warning_message(location_name), markup)
        return
    warning = split_command[2]
    if len(split_command) == 3:
        # first see if user has set a default level
        default_level = data_service.get_default_level(chat_id)
        if default_level != WarningSeverity.MANUAL:
            default_button = Button[default_level.name]
            inline_button_for_adding_subscriptions(chat_id, callback_command + ";" + str(default_button.value))
            return
        # not done with process of adding subscription yet, ask for warning level
        markup = InlineKeyboardMarkup()

        for button_level in [Button.MINOR, Button.MODERATE, Button.SEVERE]:
            button_name = text_templates.get_button_name(button_level)
            button = sender.create_inline_button(button_name, callback_command + ";" + str(button_level.value))
            markup.add(button)

        cancel_button = sender.create_inline_button(CANCEL_TEXT, str(Commands.CANCEL_INLINE.value))
        markup.add(cancel_button)
        message = text_templates.get_adding_subscription_level_message(
            location_name, _get_general_warning_name(nina_service.WarnType(warning)))
        sender.send_message(chat_id, message, markup)
    else:
        # done with process of adding subscription, and it can now be added
        warning_level = split_command[3]
        warning_type = nina_service.WarnType(warning)

        data_service.add_subscription(chat_id, location, str(warning_type.value), str(warning_level))

        show_subscriptions(chat_id)
        inline_button_for_adding_subscriptions(chat_id, split_command[0] + ";" + split_command[1])


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
    warning_name = _get_general_warning_name(nina_service.WarnType(warning))
    location_name = place_converter.get_name_for_id(location)
    sender.send_message(chat_id, text_templates.get_delete_subscription_message(location_name, warning_name))


def location_for_favorites(chat_id: int, text: str):
    """
    This method will be called when the user is in the state for adding a location to favorites and then sends a message

    Args:
        chat_id: an integer for the chatID that the message is sent to
        text: a string which contains the message the user sent
    """
    try:
        command_begin = Commands.ADD_RECOMMENDATION.value + ";"
        dicts = place_converter.get_dict_suggestions(text)
        _make_location_suggestions(chat_id, dicts, command_begin)
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
        dicts = place_converter.get_dict_suggestions(text)
        _make_location_suggestions(chat_id, dicts, command_begin, place_id_bool=True, district_id_bool=False)
    except KeyError:
        error_handler(chat_id, ErrorCodes.UNKNOWN_LOCATION)


def location_for_warning(chat_id, text: str, command: Commands):
    """
    This method will be called when the user is in the state for calling a warning
    and then sends a message

    Args:
        chat_id: an integer for the chatID that the message is sent to
        text: a string which contains the message the user sent
        command: the Command that should be used
    """
    try:
        command_begin = command.value + ";"
        dicts = place_converter.get_dict_suggestions(text)
        _make_location_suggestions(chat_id, dicts, command_begin)
    except KeyError:
        error_handler(chat_id, ErrorCodes.UNKNOWN_LOCATION)


def show_suggestions(chat_id: int, command_begin: str):
    """
    This method is called when the suggestions should be shown in chat with chat_id to finish a command.
    The button that was pressed will be determined via button_text.

    Arguments:
        chat_id: an integer for the chatID that the message is sent to
        command_begin: a string with the beginning of the command of each favorite (has to end with ;)
    """
    markup = InlineKeyboardMarkup()
    recommendations = data_service.get_suggestions(chat_id)
    for recommendation in recommendations:
        name = data_service.get_recommendation_name(recommendation)
        place_id = data_service.get_recommendation_place_id(recommendation)
        district_id = data_service.get_recommendation_district_id(recommendation)
        button = sender.create_inline_button(name, command_begin + place_id + ";" + district_id)
        markup.add(button)
    cancel_button = sender.create_inline_button(CANCEL_TEXT, str(Commands.CANCEL_INLINE.value))
    markup.add(cancel_button)
    sender.send_message(chat_id, text_templates.get_answers(Answers.CLICK_SUGGESTION), markup)


def general_warning(chat_id: int, warning: WarnType, warnings: list[nina_service.GeneralWarning] = None):
    """
    Sets the chat action of the bot to typing
    Calls for the warnings (warning) from the Nina API via the nina_service
    Or if warning is NONE then the given list warnings will be sent to the user
    Sends this information back to the chat (chat_id)
    """
    keyboard = None
    if warning != nina_service.WarnType.NONE:
        sender.send_chat_action(chat_id, "typing")
        keyboard = _get_warning_keyboard_buttons()
        data_service.set_user_state(chat_id, 2)
        try:
            warnings = nina_service.call_general_warning(warning)
        except:
            error_handler(chat_id, ErrorCodes.NINA_API)
            return
        if len(warnings) == 0:
            sender.send_message(chat_id, text_templates.get_answers(Answers.NO_CURRENT_WARNINGS),
                                keyboard)
            return

    counter = 0
    for warning in warnings:
        message = text_templates.get_general_warning_message(str(warning.id), str(warning.version), warning.start_date,
                                                             str(warning.severity.value), str(warning.type.name),
                                                             warning.title)
        try:
            detail = nina_service.get_detailed_warning(warning.id)
            sender.send_message(chat_id, message, keyboard)
        except:
            counter += 1
    if counter == (len(warnings)+1)/2 and counter != 0:
        print("Something with pulling general warnings from the nina-API went wrong (" + str(counter) + " of " +
              str(len(warnings)) + " tries failed)")
        error_handler(chat_id, ErrorCodes.NINA_API)


def covid_info(chat_id: int, city_name: str, district_id: str, info: nina_service.CovidInfo = None):
    """
    Sets the chat action of the bot to typing
    Calls for covid information of a city (city_name) from the Nina API via the nina_service
    Or if the parameter info is set it will take this information instead
    Sends this information back to the chat (chat_id)

    Arguments:
        chat_id: an integer for the chatID that the message is sent to
        city_name: a string with the name of the city
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
    if city_name is None:
        city_name = place_converter.get_name_for_id(district_id)
    message = text_templates.get_covid_info_message(city_name, info.infektionsgefahr_stufe,
                                                    info.sieben_tage_inzidenz_bundesland,
                                                    info.sieben_tage_inzidenz_kreis, info.allgemeine_hinweise)
    data_service.set_user_state(chat_id, 20)
    sender.send_message(chat_id, message, _get_covid_keyboard())


def covid_rules(chat_id: int, city_name: str, district_id: str, rules: nina_service.CovidRules = None):
    """
    Sets the chat action of the bot to typing\n
    Calls for covid rules of a city (city_name) from the Nina API via the nina_service\n
    Or if the parameter info is set it will take this information instead\n
    Sends this information back to the chat (chat_id)

    Arguments:
        chat_id: an integer for the chatID that the message is sent to
        city_name: a string with the name of the city
        district_id: a string with the district id for the rules of this city
        rules: an Enum of CovidRules from nina_service if this parameter is set the info will not be pulled from
            nina_service
    """
    if rules is None:
        sender.send_chat_action(chat_id, "typing")
        try:
            rules = nina_service.get_covid_rules(district_id)
        except:
            error_handler(chat_id, ErrorCodes.NINA_API)
            return
    if city_name is None:
        city_name = place_converter.get_name_for_id(district_id)
    message = text_templates.get_covid_rules_message(city_name, rules.vaccine_info, rules.contact_terms,
                                                     rules.school_kita_rules,
                                                     rules.hospital_rules, rules.travelling_rules, rules.fines)
    data_service.set_user_state(chat_id, 20)
    sender.send_message(chat_id, message, _get_covid_keyboard())


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
            warnings.append(_get_general_warning_name(nina_service.WarnType(warning)))
            level = str(subscriptions[location][warning])
            levels.append(text_templates.get_button_name(Button(level)))
        location_name = place_converter.get_name_for_id(location)
        subscriptions_text.append(text_templates.get_show_subscriptions_for_one_location_messsage(location_name,
                                                                                                  warnings,
                                                                                                  levels))
    message = text_templates.get_show_subscriptions_message(subscriptions_text)
    sender.send_message(chat_id, message)


def location_was_sent(chat_id: int, latitude: float, longitude: float):
    """
    This method turns the location into a city name or PLZ and\n
    - adds it to the recommendations in the database

    Arguments:
        chat_id: an integer for the chatID that the message is sent to
        latitude: float with latitude
        longitude: float with longitude
    """
    dicts = place_converter.get_suggestion_dicts_from_coordinates(latitude=latitude, longitude=longitude)
    state = data_service.get_user_state(chat_id)
    if state == 11:
        command_begin = Commands.ADD_RECOMMENDATION.value + ";"
        _make_location_suggestions(chat_id, dicts, command_begin)
    elif state == 101:
        command_begin = Commands.ADD_SUBSCRIPTION.value + ";"
        _make_location_suggestions(chat_id, dicts, command_begin, district_id_bool=False, place_id_bool=True)
    else:
        error_handler(chat_id, ErrorCodes.NO_INPUT_EXPECTED)
        return


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
    data_service.set_user_state(chat_id, 10)
    sender.send_message(chat_id, text, _get_subscription_settings_keyboard())


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
    how_often_text = text_templates.get_button_name(Button[how_often.name])
    data_service.set_auto_covid_information(chat_id, how_often)
    sender.send_message(chat_id, text_templates.get_changed_auto_covid_updates_message(how_often_text))


def add_recommendation_in_database(chat_id: int, place_id: str, district_id: str, location_name: str = None):
    """
    This method changes the recommended locations in the database and informs the user about the recommended locations
    that are stored now

    Arguments:
        chat_id: an integer for the chatID that the message is sent to
        location_name: string with the location name of the recommendation
        place_id: string with the place id
        district_id: string with district id
    """
    if location_name is None:
        location_name = place_converter.get_name_for_id(place_id)
    # update the database
    recommendations = data_service.add_suggestion(chat_id, location_name, place_id, district_id)

    # inform the user
    names = []
    for recommendation in recommendations:
        names.append(data_service.get_recommendation_name(recommendation))
    message = text_templates.get_show_recommendations_message(names)
    sender.send_message(chat_id, message, _get_send_location_keyboard())


def set_default_level(chat_id: int, level: str):
    severity = WarningSeverity.MANUAL
    try:
        data_service.set_default_level(chat_id, WarningSeverity(level))
        severity = WarningSeverity(level)
    except ValueError:
        data_service.set_default_level(chat_id, WarningSeverity.MANUAL)
    message = text_templates.get_set_default_level_message(severity)
    data_service.set_user_state(chat_id, 10)
    sender.send_message(chat_id, message, _get_subscription_settings_keyboard())


# helper/short methods -------------------------------------------------------------------------------------------------


def back_to_main_keyboard(chat_id: int):
    """
    Sets the Keyboard (of the user = chat_id) to the Main Keyboard (Main Menu) \n
    Also sends a message which indicates that the user now is in the Main Menu

    Arguments:
        chat_id: an integer for the chatID that the message is sent to
    """
    if data_service.get_user_state(chat_id) == 0:
        return
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
    """
    TODO in a future US
    this method will/should be called whenever a error occurs that the user needs to know of
    """
    sender.send_message(chat_id, "currently no real error message for error " + error_code.name)
    if error_code == ErrorCodes.NINA_API or error_code == ErrorCodes.NOT_IMPLEMENTED_YET:
        back_to_main_keyboard(chat_id)


def state_error_handler(chat_id: int, state: int):
    """
    TODO in a future US
    this method will be called when a user is in a normally unreachable state

    Args:
        chat_id: the user
        state: the users state
    """
    print("User: " + str(chat_id) + " was in the normally unreachable state: " + str(state))
    back_to_main_keyboard(chat_id)


def help_handler(chat_id: int, state: int):
    """
    TODO in a future US
    this method will be called when a users wants help

    Args:
        chat_id: the user
        state: the users state
    """
    sender.send_message(chat_id, "Hilfe für state: " + str(state) + " muss noch eingefügt werden.")


def _get_general_warning_name(warn_type: nina_service.WarnType) -> str:
    """
    Helper Method to convert a nina_service.WarnType to a string from text_templates
    """
    return text_templates.get_button_name(Button[warn_type.name])
