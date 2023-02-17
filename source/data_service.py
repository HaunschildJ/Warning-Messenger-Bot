import json
import os

from enum_types import Attributes
from enum_types import Language
from enum_types import ReceiveInformation
from enum_types import WarningSeverity

# See the MVP document for all possible options

_USER_DATA_PATH = "../source/data/data.json"
_WARNINGS_ALREADY_RECEIVED_PATH = "../source/data/warnings_already_received.json"
_ACTIVE_WARNINGS_PATH = "../source/data/active_warnings.json"

DEFAULT_DATA = {
    "current_state": 0,
    "receive_warnings": True,
    "receive_covid_information": 0,
    "default_level": "Manual",
    "locations": {
    },
    "favorites": [
        {
            "postal_code": "10827",
            "district_id": "11000"
        },
        {
            "postal_code": "60308",
            "district_id": "06412"
        },
        {
            "postal_code": "64291",
            "district_id": "06411"
        }
    ],
    "language": "german"
}


def open_file(path: str):
    return open(path, "rb")


def _read_file(path: str) -> dict:
    with open(path, "r") as file_object:
        json_content = file_object.read()
        return json.loads(json_content)


def _write_file(path: str, data: dict):
    """
    Writes given data into given path if file exists. If file does not exist, it creates the
    file and writes into it.

    Arguments:
        path: where to write data to
        data: what to write to path
    """
    with open(path, 'w+') as writefile:
        json.dump(data, writefile, indent=4)


if not os.path.exists(_USER_DATA_PATH):
    _write_file(path=_USER_DATA_PATH, data={})

if not os.path.exists(_ACTIVE_WARNINGS_PATH):
    _write_file(path=_ACTIVE_WARNINGS_PATH, data={})


def remove_user(chat_id: int):
    """
    Removes a User from the database. If the user is not in the database this method does nothing.

    Attributes:
        chat_id: Integer used to identify the user to be removed
    """
    all_user = _read_file(_USER_DATA_PATH)

    if str(chat_id) in all_user:
        del all_user[str(chat_id)]
        _write_file(_USER_DATA_PATH, all_user)


def set_receive_warnings(chat_id: int, new_value: bool):
    """
    Sets receive_warnings of the user (chat_id) to the new value (new_value).
    Creates user with given chat_id, if he does not exist already.

    Arguments:
        chat_id: Integer to identify the user
        new_value: Boolean of the new value
    """
    all_user = _read_file(_USER_DATA_PATH)
    cid = str(chat_id)

    if not (cid in all_user):
        all_user[cid] = DEFAULT_DATA.copy()

    all_user[cid][Attributes.RECEIVE_WARNINGS.value] = new_value

    _write_file(_USER_DATA_PATH, all_user)


def get_receive_warnings(chat_id: int) -> bool:
    """
    Returns if the user currently wants to receive warnings or not

    Arguments:
        chat_id: Integer to identify the user

    Returns:
        Boolean representing if the user currently wants to receive warnings
    """
    all_user = _read_file(_USER_DATA_PATH)

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
    all_user = _read_file(_USER_DATA_PATH)

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
    all_user = _read_file(_USER_DATA_PATH)
    cid = str(chat_id)

    if not (cid in all_user):
        all_user[cid] = DEFAULT_DATA.copy()

    all_user[cid][Attributes.CURRENT_STATE.value] = new_state

    _write_file(_USER_DATA_PATH, all_user)


def set_auto_covid_information(chat_id: int, how_often: ReceiveInformation):
    """
    Sets how often the user (chat_id) wants to receive covid information

    Arguments:
        chat_id: Integer to identify the user
        how_often: ReceiveInformation representing how often the user wants to receive covid information
    """
    all_user = _read_file(_USER_DATA_PATH)
    cid = str(chat_id)

    if not (cid in all_user):
        all_user[cid] = DEFAULT_DATA.copy()

    all_user[cid][Attributes.COVID_AUTO_INFO.value] = how_often.value

    _write_file(_USER_DATA_PATH, all_user)


def get_auto_covid_information(chat_id: int) -> ReceiveInformation:
    """
    Returns how often the user currently wants to receive covid updates

    Arguments:
        chat_id: Integer to identify the user

    Returns:
        ReceiveInformation representing how often the user currently wants to receive covid updates
    """
    all_user = _read_file(_USER_DATA_PATH)
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
    all_user = _read_file(_USER_DATA_PATH)

    if str(chat_id) in all_user:
        return all_user[str(chat_id)][Attributes.LOCATIONS.value]
    return DEFAULT_DATA[Attributes.LOCATIONS.value]


def add_subscription(chat_id: int, postal_code: str, district_id: str, warning: str, warning_level: str):
    """
    Adds/Sets the subscription for the user (chat_id) for the location and the warning given

    Arguments:
        chat_id: Integer to identify the user
        postal_code: postal code of the subscription (key)
        district_id: district id of the subscription
        warning: String with the warning for the subscription (int of nina_service WarnType)
        warning_level: String representing the Level a warning is relevant to the user
    """
    all_user = _read_file(_USER_DATA_PATH)
    cid = str(chat_id)

    if not (cid in all_user):
        all_user[cid] = DEFAULT_DATA.copy()

    user = all_user[cid]

    if not (postal_code in user[Attributes.LOCATIONS.value]):
        user[Attributes.LOCATIONS.value][postal_code] = {
            "district_id": district_id,
            warning: warning_level
        }
    else:
        user[Attributes.LOCATIONS.value][postal_code][warning] = warning_level

    _write_file(_USER_DATA_PATH, all_user)


def delete_subscription(chat_id: int, postal_code: str, warning: str):
    """
    Removes the subscription of user (chat_id) for the location and the warning given

    Arguments:
        chat_id: Integer to identify the user
        postal_code: postal code of the subscription (key)
        warning: String with the warning of WarnType (e.g. WEATHER)
    """
    all_user = _read_file(_USER_DATA_PATH)
    cid = str(chat_id)

    if not (cid in all_user):
        return

    user = all_user[cid]
    if not (postal_code in user[Attributes.LOCATIONS.value]):
        return

    del user[Attributes.LOCATIONS.value][postal_code][warning]
    number_of_warnings_left = len(user[Attributes.LOCATIONS.value][postal_code])
    if number_of_warnings_left <= 1:
        del user[Attributes.LOCATIONS.value][postal_code]

    _write_file(_USER_DATA_PATH, all_user)


def get_favorites(chat_id: int) -> list[dict]:
    """
    Returns an array of favorites of the user (chat_id)

    Arguments:
        chat_id: Integer to identify the user

    Returns:
        list of dictionaries with the favorites (locations the user set or default locations)
    """
    all_user = _read_file(_USER_DATA_PATH)

    if str(chat_id) in all_user:
        return all_user[str(chat_id)][Attributes.FAVORITES.value]
    return DEFAULT_DATA[Attributes.FAVORITES.value]


def add_favorite(chat_id: int, postal_code: str, district_id: str) -> list[dict]:
    """
    This method adds a location to the favorite location list of a user. \n
    The list is sorted: The most recently added location is the first element and the oldest added location
    is the last element (FIFO).\n
    If user with given chat_id is not present, he will be added.

    Arguments:
        chat_id: an integer for the chatID that the message is sent to
        postal_code: string with the postal code of the favorite
        district_id: string with district id of the favorite
    Returns:
        list of dictionaries representing the favorites after the new one has been added
    """
    all_user = _read_file(_USER_DATA_PATH)
    cid = str(chat_id)

    if not (cid in all_user):
        all_user[cid] = DEFAULT_DATA.copy()

    current_favorites = all_user[cid][Attributes.FAVORITES.value]
    i = 0
    location = {
            "postal_code": postal_code,
            "district_id": district_id
    }
    prev_favorite = location
    for favorite in current_favorites:
        tmp = favorite
        current_favorites[i] = prev_favorite
        prev_favorite = tmp
        i = i + 1
        if prev_favorite == location:
            break

    _write_file(_USER_DATA_PATH, all_user)
    return current_favorites


def get_favorite_postal_code(favorite: dict) -> str:
    """
    Returns the postal_code of the dict given by add_favorite or get_favorites

    Arguments:
        favorite: dict given by add_favorite or get_favorites

    Returns:
        postal_code of the favorite
    """
    return favorite["postal_code"]


def get_favorite_district_id(favorite: dict) -> str:
    """
    Returns the district id of the dict given by add_favorite or get_favorites

    Arguments:
        favorite: dict given by add_favorite or get_favorites

    Returns:
        district id of the favorite
    """
    return favorite["district_id"]


def get_subscription_district_id(subscription: dict) -> str:
    """
    Returns the district id of the given dict

    Args:
        subscription: dict given by get subscriptions

    Returns:
        district id of the subscription
    """
    return subscription["district_id"]


def get_language(chat_id: int) -> Language:
    """
    Returns the language the user (chat_id) has currently active or the default language

    Arguments:
        chat_id: Integer to identify the user

    Returns:
        Language the user has currently active or the default language
    """
    all_user = _read_file(_USER_DATA_PATH)

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
    all_user = _read_file(_USER_DATA_PATH)
    cid = str(chat_id)

    if not (cid in all_user):
        all_user[cid] = DEFAULT_DATA.copy()

    all_user[cid][Attributes.LANGUAGE.value] = new_language.value

    _write_file(_USER_DATA_PATH, all_user)


def set_default_level(chat_id: int, new_level: WarningSeverity):
    all_users = _read_file(_USER_DATA_PATH)
    cid = str(chat_id)

    if not (cid in all_users):
        all_users[cid] = DEFAULT_DATA.copy()

    all_users[cid][Attributes.DEFAULT_LEVEL.value] = new_level.value

    _write_file(_USER_DATA_PATH, all_users)


def get_default_level(chat_id: int) -> WarningSeverity:
    """
    Returns the language the user (chat_id) has currently active or the default language
    If user for given chat_id is not found in database, returns the default_level "Manual".

    Arguments:
        chat_id: Integer to identify the user

    Returns:
        WarningSeverity the user has currently as the default level. "Manual" if
        user does not exist in database.
    """
    all_user = _read_file(_USER_DATA_PATH)

    if str(chat_id) in all_user:
        return WarningSeverity(all_user[str(chat_id)][Attributes.DEFAULT_LEVEL.value])
    return WarningSeverity(DEFAULT_DATA[Attributes.DEFAULT_LEVEL.value])


def get_all_chat_ids() -> list[int]:
    """

    Returns: list of all chat_ids that are saved in the database

    """
    chat_ids = []
    all_users = _read_file(_USER_DATA_PATH)
    for key, value in all_users.items():
        chat_ids.append(int(key))
    return chat_ids


def get_chat_ids_of_warned_users() -> list[int]:
    """

    Returns: list of all chat_ids that have receiveWarnings set to True

    """
    return list(filter(lambda chat_id: get_receive_warnings(chat_id), get_all_chat_ids()))


def add_warning_id_to_users_warnings_received_list(chat_id: int, general_warning_id: str):
    """

    Args:
        chat_id: of the user
        general_warning_id: of the warning that should be added to users warnings_already_received list


    """
    user_data = _read_file(_WARNINGS_ALREADY_RECEIVED_PATH)
    chat_id_string = str(chat_id)

    if chat_id_string not in user_data:
        user_data[chat_id_string] = []

    list_of_received_warnings = user_data[chat_id_string]
    list_of_received_warnings.append(general_warning_id)

    _write_file(_WARNINGS_ALREADY_RECEIVED_PATH, user_data)


def get_users_already_received_warning_ids(chat_id: int) -> list[str]:
    """

    Args:
        chat_id: of the user

    Returns: a list of the warning_ids of warnings the user has already received

    """
    user_data = _read_file(_WARNINGS_ALREADY_RECEIVED_PATH)
    chat_id_string = str(chat_id)

    if chat_id_string not in user_data:
        return []

    return user_data[chat_id_string]


def has_user_already_received_warning(chat_id: int, general_warning_id: str) -> bool:
    """

    Args:
        chat_id: of the user
        general_warning_id: of the warning that should be checked

    Returns: True if the user has already received the warning

    """
    list_of_received_warnings = get_users_already_received_warning_ids(chat_id)
    if general_warning_id in list_of_received_warnings:
        return True
    else:
        return False


def delete_all_subscriptions(chat_id: int):
    """
    This method deletes all subscriptions for the given user

    Args:
        chat_id: to identify the user
    """
    all_user = _read_file(_USER_DATA_PATH)
    cid = str(chat_id)

    if not (cid in all_user):
        return

    all_user[cid][Attributes.LOCATIONS.value] = DEFAULT_DATA[Attributes.LOCATIONS.value]

    _write_file(_USER_DATA_PATH, all_user)


def reset_favorites(chat_id: int):
    """
    This method resets the favorites for the given user

    Args:
        chat_id: to identify the user
    """
    all_user = _read_file(_USER_DATA_PATH)
    cid = str(chat_id)

    if not (cid in all_user):
        return

    all_user[cid][Attributes.FAVORITES.value] = DEFAULT_DATA[Attributes.FAVORITES.value]

    _write_file(_USER_DATA_PATH, all_user)


def delete_user(chat_id: int):
    """
    This method removes a user from the database

    Args:
        chat_id: to identify the user
    """
    all_user = _read_file(_USER_DATA_PATH)
    cid = str(chat_id)

    if not (cid in all_user):
        return

    del all_user[cid]

    _write_file(_USER_DATA_PATH, all_user)


def get_active_warnings_dict() -> dict:
    return _read_file(_ACTIVE_WARNINGS_PATH)


def set_active_warnings_dict(new_data: dict):
    _write_file(_ACTIVE_WARNINGS_PATH, new_data)


def get_user_subscription_postal_codes(chat_id: int) -> list[str]:
    """
    Returns a list of all postal codes the user is subscribed to

    Args:
        chat_id: to identify the user

    Returns: list of all postal codes the user is subscribed to

    """
    all_user = _read_file(_USER_DATA_PATH)
    cid = str(chat_id)

    if not (cid in all_user):
        return []

    return list(all_user[cid][Attributes.LOCATIONS.value].keys())
