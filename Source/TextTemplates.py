import string


def get_greeting_string() -> string:
    return "Guten Tag"


def get_corona_string() -> string:
    return """
Corona Inzidenz: %inzidenz 
Aktuelle Fallzahlen %case 
Aktuelle Todeszahlen %death 
Informationen vom %date """


