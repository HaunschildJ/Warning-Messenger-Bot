import json
from enum import Enum

# See the MVP document for all possible options

file_path = "../source/data/data.json"
warnings_sent_path = "../source/data/warnings_already_received.json"

DEFAULT_DATA = {
    "current_state": 0,
    "receive_warnings": True,
    "receive_covid_information": 0,
    "locations": {
    },
    "recommendations": [
        {
            "name": "Berlin, Stadt",
            "place_id": "110000000000",
            "district_id": "11000"
        },
        {
            "name": "Berlin-Mitte",
            "place_id": "110010000000",
            "district_id": "11001"
        },
        {
            "name": "Darmstadt, Wissenschaftsstadt",
            "place_id": "064110000000",
            "district_id": "06411"
        }
    ],
    "language": "german"
}


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


def _read_file(path: str) -> dict:
    with open(path, "r") as file_object:
        json_content = file_object.read()
        return json.loads(json_content)


def _write_file(path: str, data: dict):
    with open(path, 'w') as writefile:
        json.dump(data, writefile, indent=4)


def remove_user(chat_id: int):
    """
    Removes a User from the database. If the user is not in the database this method does nothing.

    Attributes:
        chat_id: Integer used to identify the user to be removed
    """
    all_user = _read_file(file_path)

    if str(chat_id) in all_user:
        del all_user[str(chat_id)]
        _write_file(file_path, all_user)


def set_receive_warnings(chat_id: int, new_value: bool):
    """
    Sets receive_warnings of the user (chat_id) to the new value (new_value)

    Arguments:
        chat_id: Integer to identify the user
        new_value: Boolean of the new value
    """
    all_user = _read_file(file_path)
    cid = str(chat_id)

    if not (cid in all_user):
        all_user[cid] = DEFAULT_DATA.copy()

    all_user[cid][Attributes.RECEIVE_WARNINGS.value] = new_value

    _write_file(file_path, all_user)


def get_receive_warnings(chat_id: int) -> bool:
    """
    Returns if the user currently wants to receive warnings or not

    Arguments:
        chat_id: Integer to identify the user

    Returns:
        Boolean representing if the user currently wants to receive warnings
    """
    all_user = _read_file(file_path)

    if str(chat_id) in all_user:
        return all_user[str(chat_id)][Attributes.RECEIVE_WARNINGS.value]
    return DEFAULT_DATA[Attributes.RECEIVE_WARNINGS.value]


def get_user_state(chat_id: int) -> int:
    """
    Returns the state the user (chat_id) is currently in.

    Arguments:
        chat_id: Integer to identify the user

    Returns:
        Integer value of the state the user is currently in or 0 if the user is not in the database yet
    """
    all_user = _read_file(file_path)

    if str(chat_id) in all_user:
        return all_user[str(chat_id)][Attributes.CURRENT_STATE.value]
    return DEFAULT_DATA[Attributes.CURRENT_STATE.value]


def set_user_state(chat_id: int, new_state: int):
    """
    Sets the state of the user (chat_id) to the new state (new_state)

    Arguments:
        chat_id: Integer to identify the user
        new_state: Integer of the new state
    """
    all_user = _read_file(file_path)
    cid = str(chat_id)

    if not (cid in all_user):
        all_user[cid] = DEFAULT_DATA.copy()

    all_user[cid][Attributes.CURRENT_STATE.value] = new_state

    _write_file(file_path, all_user)


def set_auto_covid_information(chat_id: int, how_often: ReceiveInformation):
    """
    Sets how often the user (chat_id) wants to receive covid information

    Arguments:
        chat_id: Integer to identify the user
        how_often: ReceiveInformation representing how often the user wants to receive covid information
    """
    all_user = _read_file(file_path)
    cid = str(chat_id)

    if not (cid in all_user):
        all_user[cid] = DEFAULT_DATA.copy()

    all_user[cid][Attributes.COVID_AUTO_INFO.value] = how_often.value

    _write_file(file_path, all_user)


def get_auto_covid_information(chat_id: int) -> ReceiveInformation:
    """
    Returns how often the user currently wants to receive covid updates

    Arguments:
        chat_id: Integer to identify the user

    Returns:
        ReceiveInformation representing how often the user currently wants to receive covid updates
    """
    all_user = _read_file(file_path)
    cid = str(chat_id)

    if cid in all_user:
        return ReceiveInformation(all_user[cid][Attributes.COVID_AUTO_INFO.value])
    return ReceiveInformation(DEFAULT_DATA[Attributes.COVID_AUTO_INFO.value])


def get_subscriptions(chat_id: int) -> dict:
    """
    Returns a dictionary of subscriptions of the user (chat_id)

    Arguments:
        chat_id: Integer to identify the user

    Returns:
        a dictionary of subscriptions of the user
    """
    all_user = _read_file(file_path)

    if str(chat_id) in all_user:
        return all_user[str(chat_id)][Attributes.LOCATIONS.value]
    return DEFAULT_DATA[Attributes.LOCATIONS.value]


def add_subscription(chat_id: int, location: str, warning: str, warning_level: int):
    """
    Adds/Sets the subscription for the user (chat_id) for the location and the warning given

    Arguments:
        chat_id: Integer to identify the user
        location: String with the location of the subscription
        warning: String with the warning for the subscription (int of nina_service WarnType)
        warning_level: Integer representing the Level a warning is relevant to the user
    """
    all_user = _read_file(file_path)
    cid = str(chat_id)

    if not (cid in all_user):
        all_user[cid] = DEFAULT_DATA.copy()

    user = all_user[cid]

    if not (location in user[Attributes.LOCATIONS.value]):
        user[Attributes.LOCATIONS.value][location] = {warning: warning_level}
    else:
        user[Attributes.LOCATIONS.value][location][warning] = warning_level

    _write_file(file_path, all_user)


def delete_subscription(chat_id: int, location: str, warning: str):
    """
    Removes the subscription of user (chat_id) for the location and the warning given

    Arguments:
        chat_id: Integer to identify the user
        location: String with the location of the subscription
        warning: String with the warning of WarnType (e.g. WEATHER)
    """
    all_user = _read_file(file_path)
    cid = str(chat_id)

    if not (cid in all_user):
        return

    user = all_user[cid]
    if not (location in user[Attributes.LOCATIONS.value]):
        return

    del user[Attributes.LOCATIONS.value][location][warning]

    if len(user[Attributes.LOCATIONS.value][location]) == 0:
        del user[Attributes.LOCATIONS.value][location]

    _write_file(file_path, all_user)


def get_suggestions(chat_id: int) -> list[dict]:
    """
    Returns an array of suggestions of the user (chat_id)

    Arguments:
        chat_id: Integer to identify the user

    Returns:
        list of dictionaries with the recommendations (locations the user set or default locations)
    """
    all_user = _read_file(file_path)

    if str(chat_id) in all_user:
        return all_user[str(chat_id)][Attributes.RECOMMENDATIONS.value]
    return DEFAULT_DATA[Attributes.RECOMMENDATIONS.value]


def add_suggestion(chat_id: int, location_name: str, place_id: str, district_id: str) -> list[dict]:
    """
    This method adds a location to the recommended location list of a user. \n
    The list is sorted: The most recently added location is the first element and the oldest added location
    is the last element (FIFO)

    Arguments:
        chat_id: Integer to identify the user
        location_name: string with the location name of the recommendation
        place_id: string with the place id
        district_id: string with district id
    Returns:
        list of dictionaries representing the recommendations after the new one has been added
    """
    all_user = _read_file(file_path)
    cid = str(chat_id)

    if not (cid in all_user):
        all_user[cid] = DEFAULT_DATA.copy()

    current_recommendations = all_user[cid][Attributes.RECOMMENDATIONS.value]
    i = 0
    location = {
        "name": location_name,
        "place_id": place_id,
        "district_id": district_id
        }
    prev_recommendation = location
    for recommendation in current_recommendations:
        tmp = recommendation
        current_recommendations[i] = prev_recommendation
        prev_recommendation = tmp
        i = i + 1
        if prev_recommendation == location:
            break

    _write_file(file_path, all_user)
    return current_recommendations


def get_recommendation_name(recommendation: dict) -> str:
    return recommendation["name"]


def get_recommendation_place_id(recommendation: dict) -> str:
    return recommendation["place_id"]


def get_recommendation_district_id(recommendation: dict) -> str:
    return recommendation["district_id"]


def get_language(chat_id: int) -> Language:
    """
    Returns the language the user (chat_id) has currently active or the default language

    Arguments:
        chat_id: Integer to identify the user

    Returns:
        Language the user has currently active or the default language
    """
    all_user = _read_file(file_path)

    if str(chat_id) in all_user:
        return Language(all_user[str(chat_id)][Attributes.LANGUAGE.value])
    return Language(DEFAULT_DATA[Attributes.LANGUAGE.value])


def set_language(chat_id: int, new_language: Language):
    """
    Sets the language of the user (chat_id) to the new language (new_language)

    Arguments:
        chat_id: Integer to identify the user
        new_language: Language represents the new language the user wants
    """
    all_user = _read_file(file_path)
    cid = str(chat_id)

    if not (cid in all_user):
        all_user[cid] = DEFAULT_DATA.copy()

    all_user[cid][Attributes.LANGUAGE.value] = new_language.value

    _write_file(file_path, all_user)


def get_all_chat_ids() -> list[int]:
    """
    Returns: List of all chat_ids that are saved in the database
    """
    chat_ids = []
    all_users = _read_file(file_path)
    for key, value in all_users.items():
        chat_ids.append(int(key))
    return chat_ids


def get_chat_ids_of_warned_users() -> list[int]:
    """
    Returns: List of all chat_ids that have receiveWarnings set to true
    """
    filtered_ids = filter(lambda chat_id: get_receive_warnings(chat_id), get_all_chat_ids())
    return list(filtered_ids)


# TODO: lhp warning_id look like this "lhp.HOCHWASSERZENTRALEN.DE.BY", which is most probably not a unique id
# There has to be a more specific id
def add_warning_id_to_users_warnings_received_list(chat_id: int, general_warning_id: str):
    user_data = _read_file(warnings_sent_path)
    chat_id_string = str(chat_id)

    if chat_id_string not in user_data:
        user_data[chat_id_string] = []

    list_of_received_warnings = user_data[chat_id_string]
    list_of_received_warnings.append(general_warning_id)

    _write_file(warnings_sent_path, user_data)


def get_users_already_received_warning_ids(chat_id: int) -> list[str]:
    user_data = _read_file(warnings_sent_path)
    chat_id_string = str(chat_id)

    if chat_id_string not in user_data:
        return []

    return user_data[chat_id_string]


def has_user_already_received_warning(chat_id: int, general_warning_id: str) -> bool:
    list_of_received_warnings = get_users_already_received_warning_ids(chat_id)
    if general_warning_id in list_of_received_warnings:
        print("User " + str(chat_id) + " was already warned about warning with id: " + general_warning_id)
        return True
    else:
        return False

