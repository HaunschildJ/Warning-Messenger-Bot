import telebot
import data_service
import text_templates
import sender

from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from enum_types import Button, Answers


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
WARNING_CIVIL_PROTECTION_TEXT = text_templates.get_button_name(Button.CIVIL_PROTECTION)  # MVP 5. i)
WARNING_FLOOD_TEXT = text_templates.get_button_name(Button.FLOOD)  # MVP 5. i)

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


# helper methods from controller ---------------------------------------------------------------------------------------

def get_main_keyboard_buttons() -> telebot.types.ReplyKeyboardMarkup:
    """
    This is a helper method which returns the keyboard for the MVP 3. menu

    Returns:
         telebot.types.ReplyKeyboardMarkup
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=False, one_time_keyboard=False, input_field_placeholder="Hauptmenü")
    settings_button = sender.create_button(SETTING_BUTTON_TEXT)
    warning_button = sender.create_button(WARNING_BUTTON_TEXT)
    tip_button = sender.create_button(TIP_BUTTON_TEXT)
    more_button = sender.create_button(HELP_BUTTON_TEXT)
    keyboard.add(warning_button).add(settings_button).add(tip_button, more_button)
    return keyboard


def get_settings_keyboard_buttons() -> telebot.types.ReplyKeyboardMarkup:
    """
    This is a helper method which returns the keyboard for the MVP 4. menu

    Returns:
         telebot.types.ReplyKeyboardMarkup
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=False, one_time_keyboard=False)
    favorites_button = sender.create_button(SETTING_SUGGESTION_LOCATION_TEXT)
    subscriptions_button = sender.create_button(SETTING_SUBSCRIPTION_TEXT)
    delete_data_button = sender.create_button(SETTING_DELETE_DATA_TEXT)
    back_button = sender.create_button(BACK_TO_MAIN_TEXT)
    keyboard.add(subscriptions_button).add(favorites_button, delete_data_button).add(back_button)
    return keyboard


def get_warning_keyboard_buttons() -> telebot.types.ReplyKeyboardMarkup:
    """
    This is a helper method which returns the keyboard for the MVP 5. menu

    Returns:
         telebot.types.ReplyKeyboardMarkup
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=False, one_time_keyboard=True)
    covid_button = sender.create_button(WARNING_COVID_TEXT)
    weather_button = sender.create_button(WARNING_WEATHER_TEXT)
    civil_protection_button = sender.create_button(WARNING_CIVIL_PROTECTION_TEXT)
    flood_button = sender.create_button(WARNING_FLOOD_TEXT)
    back_button = sender.create_button(BACK_TO_MAIN_TEXT)
    keyboard.add(covid_button).add(weather_button, flood_button).add(civil_protection_button).add(back_button)
    return keyboard


def get_help_keyboard_buttons() -> telebot.types.ReplyKeyboardMarkup:
    """
    This is a helper method which returns the keyboard for the help menu

    Returns:
         telebot.types.ReplyKeyboardMarkup
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=False, one_time_keyboard=False)
    bot_info_button = sender.create_button(HELP_BOT_USAGE_TEXT)
    faq_button = sender.create_button(HELP_FAQ_TEXT)
    imprint_button = sender.create_button(HELP_IMPRINT_TEXT)
    privacy_button = sender.create_button(HELP_PRIVACY_TEXT)
    back_button = sender.create_button(BACK_TO_MAIN_TEXT)
    keyboard.add(bot_info_button, faq_button).add(imprint_button, privacy_button).add(back_button)
    return keyboard


def get_emergency_pdfs_keyboard() -> telebot.types.ReplyKeyboardMarkup:
    """
    This is a helper method which returns the keyboard for the emergency PDFs menu

    Returns:
         telebot.types.ReplyKeyboardMarkup
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=False, one_time_keyboard=False)
    # TODO get pdf names from nina
    list_names = ["Richtig handeln im Notfall", "Besondere Gefahren", "Hochwasser", "Unwetter", "Stromausfall", "Feuer",
                  "Gefahrenstoffe", "Persönliche Notfallvorsorge", "Stromspartipps für Smartphones", "Hitze"]
    for name in list_names:
        button = sender.create_button(name)
        keyboard.add(button)

    back_button = sender.create_button(BACK_TO_MAIN_TEXT)
    keyboard.add(back_button)
    return keyboard


def get_covid_keyboard() -> telebot.types.ReplyKeyboardMarkup:
    """
    This is a helper method which returns the keyboard for manual warnings of covid

    Returns:
        telebot.types.ReplyKeyboardMarkup
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=False, one_time_keyboard=True)
    info_button = sender.create_button(WARNING_COVID_INFO_TEXT)
    rules_button = sender.create_button(WARNING_COVID_RULES_TEXT)
    back_button = sender.create_button(BACK_TO_MAIN_TEXT)
    keyboard.add(info_button).add(rules_button).add(back_button)
    return keyboard


def get_send_location_keyboard() -> telebot.types.ReplyKeyboardMarkup:
    """
    This is a helper method which returns the keyboard for the MVP 4. b i)

    Returns:
         telebot.types.ReplyKeyboardMarkup
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=False, one_time_keyboard=False)
    send_location_button = sender.create_button(SEND_LOCATION_BUTTON_TEXT, request_location=True)
    back_button = sender.create_button(BACK_TO_MAIN_TEXT)
    keyboard.add(send_location_button).add(back_button)
    return keyboard


def get_subscription_settings_keyboard() -> telebot.types.ReplyKeyboardMarkup:
    """
    Helper method to get subscription settings keyboard.

    Returns:
        Nothing
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=False, one_time_keyboard=False)
    show_button = sender.create_button(SHOW_SUBSCRIPTION_TEXT)
    add_button = sender.create_button(ADD_SUBSCRIPTION_TEXT)
    delete_button = sender.create_button(DELETE_SUBSCRIPTION_TEXT)
    default_level_button = sender.create_button(DEFAULT_LEVEL_TEXT)
    silence_subs_button = sender.create_button(SILENCE_SUBSCRIPTIONS_TEXT)
    back_button = sender.create_button(BACK_TO_MAIN_TEXT)
    keyboard.add(show_button).add(add_button, delete_button).add(default_level_button, silence_subs_button)
    keyboard.add(back_button)
    return keyboard


def get_delete_data_keyboard() -> telebot.types.ReplyKeyboardMarkup:
    """
    Helper method to get the delete data keyboard.

    Returns:
        Nothing
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=False, one_time_keyboard=True)
    subscriptions_button = sender.create_button(DELETE_DATA_SUBSCRIPTIONS_TEXT)
    favorites_button = sender.create_button(DELETE_DATA_FAVORITES_TEXT)
    all_data_button = sender.create_button(DELETE_DATA_EVERYTHING_TEXT)
    back_button = sender.create_button(BACK_TO_MAIN_TEXT)
    keyboard.add(subscriptions_button, favorites_button).add(all_data_button).add(back_button)
    return keyboard


def back_to_main_keyboard(chat_id: int):
    """
    If the user is not already in the main menu:
    Sets the Keyboard (of the user = chat_id) to the Main Keyboard (Main Menu) \n
    Also sends a message which indicates that the user now is in the Main Menu

    Args:
        chat_id: an integer for the chatID that the message is sent to
    """
    if data_service.get_user_state(chat_id) == 0:
        return
    data_service.set_user_state(chat_id, 0)
    keyboard = get_main_keyboard_buttons()
    sender.send_message(chat_id, text_templates.get_answers(Answers.BACK_TO_MAIN_MENU), keyboard)
