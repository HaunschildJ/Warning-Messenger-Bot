from enum import Enum


# controller -----------------------------------------------------------------------------------------------------------


class Commands(Enum):
    """
    this enum is used to have all commands in one place \n
    current possible commands:\n
    AUTO_WARNING + "bool as string"\n

    just for the bot not the user:\n
    CANCEL_INLINE\n
    JUST_CANCEL_INLINE\n
    DELETE_SUBSCRIPTION ; "postal_code" ; "district_id" ; "warn_type"\n
    ADD_SUBSCRIPTION ; "postal_code" ; "district_id" ; "warn_type" ; "warn_level"\n
    COVID_UPDATES + "ReceiveInformation from data_service as int"\n
    ADD_RECOMMENDATION ; "postal_code" ; "district_id"\n
    SET_DEFAULT_LEVEL ; "value"\n
    (DELETE_DATA_SUBSCRIPTION || DELETE_DATA_FAVORITES || DELETE_DATA_EVERYTHING)
    (COVID_INFO || COVID_RULES || WEATHER || DISASTER || FLOOD || COVID_INFO) ; "postal_code" ; "district_id"\n
    """
    AUTO_WARNING = "/aw"
    CANCEL_INLINE = "/cancel"
    JUST_CANCEL_INLINE = "just_cancel"
    ADD_RECOMMENDATION = "/addR"
    DELETE_SUBSCRIPTION = "/delS"
    ADD_SUBSCRIPTION = "/addS"
    COVID_UPDATES = "/cu"
    SET_DEFAULT_LEVEL = "/setValue"
    DELETE_DATA_SUBSCRIPTIONS = "/delAllSubs"
    DELETE_DATA_FAVORITES = "/delAllFav"
    DELETE_DATA_EVERYTHING = "/delAllAll"
    COVID_INFO = "/cI"
    COVID_RULES = "/cR"
    WEATHER = "/weather"
    CIVIL_PROTECTION = "/cP"
    FLOOD = "/flood"
    SEND_PDF = "/sendPDF"


class ErrorCodes(Enum):
    """
    this enum is used to handle errors
    """
    NOT_IMPLEMENTED_YET = 0
    UNKNOWN_COMMAND = 1
    ONLY_PART_OF_COMMAND = 2
    NINA_API = 3
    UNKNOWN_LOCATION = 4
    NO_INPUT_EXPECTED = 8
    CALLBACK_MISTAKE = 9


# data_service ---------------------------------------------------------------------------------------------------------


class ReceiveInformation(Enum):
    NEVER = 0
    DAILY = 1
    WEEKLY = 2
    MONTHLY = 3


class Language(Enum):
    GERMAN = "german"


class Attributes(Enum):
    CHAT_ID = "chat_id"
    CURRENT_STATE = "current_state"
    RECEIVE_WARNINGS = "receive_warnings"
    COVID_AUTO_INFO = "receive_covid_information"
    LOCATIONS = "locations"
    RECOMMENDATIONS = "recommendations"
    LANGUAGE = "language"
    DEFAULT_LEVEL = "default_level"


# nina_service ---------------------------------------------------------------------------------------------------------


class WarningSeverity(Enum):
    MINOR = "Minor"
    MODERATE = "Moderate"
    SEVERE = "Severe"
    EXTREME = "Extreme"
    MANUAL = "Manual"


class WarningCategory(Enum):
    """
    this enum is used to differ between the different general warnings from the nina api
    """
    WEATHER = "weather"
    CIVIL_PROTECTION = "civil_protection"
    FLOOD = "flood"
    NONE = "none"
    ALL = "all"


class WarningType(Enum):
    UPDATE = "Update"
    ALERT = "Alert"
    CANCEL = "Cancel"
    UNKNOWN = "Unknown"


# text_templates -------------------------------------------------------------------------------------------------------


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
    QUICKLY_ADD_TO_SUBSCRIPTIONS = "quickly_add_to_subscriptions"


class Button(Enum):
    SETTINGS = "settings"
    WARNINGS = "warnings"
    EMERGENCY_TIPS = "emergency_tips"
    COVID = "covid"
    COVID_INFORMATION = "covid_information"
    COVID_RULES = "covid_rules"
    HELP = "help"
    BACK_TO_MAIN_MENU = "back_to_main_menu"
    AUTO_WARNING = "auto_warning"
    SUGGESTION_LOCATION = "suggestion_location"
    SUBSCRIPTION = "subscription"
    DELETE_DATA = "delete_data"
    AUTO_COVID_INFO = "auto_covid_info"
    LANGUAGE = "language"
    CANCEL = "cancel"
    SEND_LOCATION = "send_location"
    WEATHER = "weather"  # name needs to be equal to name in nina_service.WarningCategory
    CIVIL_PROTECTION = "civil_protection"  # name needs to be equal to name in nina_service.WarningCategory
    FLOOD = "flood"  # name needs to be equal to name in nina_service.WarningCategory
    ALL = "all"  # name needs to be equal to name in nina_service.WarningCategory
    SHOW_SUBSCRIPTION = "show_subscriptions"
    DELETE_SUBSCRIPTION = "delete_subscription"
    ADD_SUBSCRIPTION = "add_subscription"
    DELETE = "delete"
    NEVER = "never"  # name needs to be equal to name in data_service.ReceiveInformation
    DAILY = "daily"  # name needs to be equal to name in data_service.ReceiveInformation
    WEEKLY = "weekly"  # name needs to be equal to name in data_service.ReceiveInformation
    MONTHLY = "monthly"  # name needs to be equal to name in data_service.ReceiveInformation
    MANUAL = "manual"  # name needs to be equal to name in data_service.WarningSeverity
    MINOR = "minor"  # name should be equal to name in nina_service.WarningSeverity
    MODERATE = "moderate"  # name should be equal to name in nina_service.WarningSeverity
    SEVERE = "severe"  # name should be equal to name in nina_service.WarningSeverity
    EXTREME = "extreme"  # name should be equal to name in nina_service.WarningSeverity
    DELETE_DATA_SUBSCRIPTIONS = "delete_data_subscriptions"
    DELETE_DATA_FAVORITES = "delete_data_favorites"
    DELETE_DATA_EVERYTHING = "delete_data_everything"
    DEFAULT_LEVEL = "default_level"
    HELP_BOT_USAGE = "help_bot_usage"
    HELP_FAQ = "help_faq"
    HELP_IMPRINT = "help_imprint"
    HELP_PRIVACY = "help_privacy"


class Answers(Enum):
    YES = "yes"
    NO = "no"
    SETTINGS = "settings"
    WARNINGS = "warnings"
    HELP = "help"
    DELETE_DATA = "delete_data"
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
    DELETE_DATA_SUBSCRIPTIONS = "delete_data_subscriptions"
    DELETE_DATA_FAVORITES = "delete_data_favorites"
    DELETE_DATA_EVERYTHING = "delete_data_everything"
    DELETE_SUBSCRIPTIONS = "deleted_subscriptions"
    DELETE_FAVORITES = "deleted_favorites"
    DELETE_EVERYTHING = "deleted_everything"
    MANUAL_WARNING_COVID_CHOICE = "manual_warning_covid_choice"
    DEFAULT_LEVEL = "default_level"
    IMPRINT_TEXT = "imprint"
    PRIVACY_TEXT = "privacy"
    UNKNOWN = "unknown"
    ERROR_NINA = "error_nina"
    ERROR_NOT_IMPLEMENTED = "error_not_implemented"
    ERROR_UNKNOWN_COMMAND = "error_unknown_command"
    ERROR_UNKNOWN_LOCATION = "error_unknown_location"
    ERROR_LOCATION_AT_WRONG_PLACE = "error_location_at_wrong_place"
    ERROR_START = "error_start"
    ERROR_NO_INPUT_EXPECTED = "error_no_input_expected"
    PDF_CAPTION = "pdf_caption"
    EMERGENCY_TIPS = "emergency_tips"
    EMERGENCY_TIPS_ASK = "emergency_tips_ask"


class BotUsageHelp(Enum):
    EVERYTHING = "everything"
    MAIN_MENU = "main_menu"
    MANUAL_WARNINGS = "manual_warnings"
    HELP_MENU = "help_menu"
    EMERGENCY_TIPS_MENU = "emergency_tips_menu"
    SETTINGS_MENU = "settings_menu"
    DELETE_DATA_MENU = "delete_data_menu"
    FAVORITES = "favorites"
    SUBSCRIPTIONS_MENU = "subscriptions_menu"


def get_integer_from_warning_severity(severity: WarningSeverity) -> int:
    severity = str(severity).lower()
    if severity == str(WarningSeverity.MINOR.value).lower():
        return 1
    elif severity == str(WarningSeverity.SEVERE.value).lower():
        return 2
    else:
        return 0