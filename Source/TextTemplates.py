import string


def get_greeting_string() -> string:
    return "Guten Tag"


def get_corona_info() -> string:
    return """
%inzidenz 
%bund 
%kreis 
%tips """


def get_corona_rules() -> string:
    return """
%vaccine_info
%contact_terms
%school_kita_rules
%hospital_rules
%travelling_rules
%fines
"""


def get_inline_button_corona_info() -> string:
    return "Zu welcher Stadt möchtest du Infos haben?"


def get_inline_button_corona_rules() -> string:
    return "Zu welcher Stadt möchtest du die Regeln wissen?"

