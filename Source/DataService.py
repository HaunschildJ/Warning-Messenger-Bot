import json
from enum import Enum
from types import SimpleNamespace

# See the MVP document for all possible options

file_path = "../Source/Data/data.json"


class WarnType(Enum):
    NONE = "none"
    WEATHER = "weather"
    BIWAPP = "biwapp"


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


class UserData:
    """
    User Data in concise form. Is read from a JSON file.
    """
    def __init__(self, current_state=0,
                 receive_warnings=False,
                 receive_covid_information=ReceiveInformation.NEVER.value,
                 locations=None,
                 recommendation=None,
                 language=Language.GERMAN.value):
        """
        Initializes a Set of User Data Attributes.

        Arguments:
            current_state: Integer used to identify the state the user is currently in
            receive_warnings: boolean whether User wants to receive warnings or not.
            receive_covid_information: Enum (ReceiveInformation) whether and if yes,
                   how often User wants to receive covid information or not.
            locations: Array of Dictionaries. Mainly set through methods.
            recommendation: Array of string to save the recommendation of citys
            language: Enum with various languages. Default case German.
        """
        if recommendation is None:
            recommendation = ["München", "Frankfurt", "Berlin"]
        self.user_entry = {
            Attributes.CURRENT_STATE.value: current_state,
            Attributes.RECEIVE_WARNINGS.value: receive_warnings,
            Attributes.COVID_AUTO_INFO.value: receive_covid_information,
            Attributes.LOCATIONS.value: locations,
            Attributes.RECOMMENDATIONS.value: recommendation,
            Attributes.LANGUAGE.value: language
        }

    def change_entry(self, attribute: Attributes, value):
        """
        Changes attribute to value.

        Arguments:
            attribute: Enum (Attributes) which represents Element of attribute one wants to change.
            value: Any Type depends on Type of attribute. Value of desired value.
        """
        self.user_entry[attribute.value] = value

    def set_location(self, location_name: str, warning: WarnType, warning_level: int):
        """
        Either sets or replaces location with given parameter.

        Arguments:
            location_name: String, which location is to be changed.
            warning: Enum of WarnType, what kind of warning is to be changed.
            warning_level: Integer, what warning level is wished for given location.
        """
        all_locations = self.user_entry[Attributes.LOCATIONS.value]
        if all_locations is None:
            self.user_entry[Attributes.LOCATIONS.value] = [{
                "name": location_name, "warning_level": [warning_level], "warnings": [warning.name]
            }]
            return
        for location in all_locations:
            if location["name"] == location_name:
                i = 0
                for warning_old in location["warnings"]:
                    if warning_old == warning.name:
                        location["warning_level"][i] = warning_level
                        return
                    i = i+1
                location["warnings"].append(warning.name)
                location["warning_level"].append(warning_level)
                return
        all_locations.append({
                "name": location_name, "warning_level": [warning_level], "warnings": [warning.name]
            })

    def remove_location(self, location_name: str):
        """
        Removes given location.

        Arguments:
            location_name: String of location one wants to remove.
        """
        current_locations = self.user_entry[Attributes.LOCATIONS.value].copy()
        for location in current_locations:
            if location["name"] == location_name:
                self.user_entry[Attributes.LOCATIONS.value].remove(location)
                return

    def remove_all_locations(self):
        """
        Removes all locations.
        """
        self.user_entry[Attributes.LOCATIONS.value].clear()

    def add_recommended_location(self, location_name: str):
        """
        This method adds a location to the recommended location list of a user. \n
        The list is sorted: The most recently added location is the first element and the least recently added location
        ist the last element

        Attributes:
            location_name: String of location one wants to add to recommendations.
        """
        current_recommendations = self.user_entry[Attributes.RECOMMENDATIONS.value]
        i = 0
        prev_recommendation = location_name
        for recommendation in current_recommendations:
            tmp = recommendation
            current_recommendations[i] = prev_recommendation
            prev_recommendation = tmp
            i = i + 1
            if prev_recommendation == location_name:
                return


def write_file(chat_id: int, user_data: UserData):
    """
    Writes parameter user_data into a JSON file. Replacing it if already existing.

    Arguments:
        chat_id: Integer used to identify Telegram Chat. Needed to identify User.
        user_data: UserData instance containing information, that one wants to add to the JSON file.
    """
    with open(file_path, "r") as file_object:
        json_content = file_object.read()
        all_user = json.loads(json_content)

    all_user[str(chat_id)] = user_data.user_entry

    with open(file_path, 'w') as writefile:
        json.dump(all_user, writefile, indent=4)


def remove_user(chat_id: int):
    """
    Removes a User from the database. If the user is not in the database this method does nothing.

    Attributes:
        chat_id: Integer used to identify the user to be removed
    """
    with open(file_path, "r") as file_object:
        json_content = file_object.read()
        all_user = json.loads(json_content)

    if str(chat_id) in all_user:
        del all_user[str(chat_id)]
        with open(file_path, 'w') as writefile:
            json.dump(all_user, writefile, indent=4)


def _get_data_model(data) -> dict:
    return json.loads(data, object_hook=lambda d: SimpleNamespace(**d))


def read_user(chat_id: int) -> UserData:
    """
    Returns an instance of UserData depending on given chat_id. If JSON file does not contain the user yet,
    a new UserData Set is created with default values.

    Does not write into the JSON file.

    Arguments:
        chat_id: Integer, which represents the user.

    Returns:
        Instance of UserData. Either from JSON DATA or newly constructed.
    """
    with open(file_path, "r") as file_object:
        json_content = file_object.read()
        all_user = json.loads(json_content)

    if str(chat_id) in all_user:
        entry = all_user[str(chat_id)]
        model = _get_data_model(json.dumps(entry, indent=4))
        result = UserData(current_state=model.current_state, receive_warnings=model.receive_warnings,
                          receive_covid_information=model.receive_covid_information, language=model.language,
                          recommendation=model.recommendations)
        if model.locations is None:
            return result
        for location in model.locations:
            i = 0
            for warning in location.warnings:
                result.set_location(location.name, WarnType.__getitem__(warning), location.warning_level[i])
                i = i+1
            if i == 0:
                result.set_location(location.name, [], [])
        return result
    # not found in JSON file -> return new one
    return UserData()


def get_user_state(chat_id: int) -> int:
    """
    Returns the state the user (chat_id) is currently in.

    Attributes:
        chat_id: Integer to identify the user

    Returns:
        Integer value of the state the user is currently in or 0 if the user is not in the database yet
    """
    with open(file_path, "r") as file_object:
        json_content = file_object.read()
        all_user = json.loads(json_content)

    if str(chat_id) in all_user:
        return all_user[str(chat_id)][Attributes.CURRENT_STATE.value]
    return 0


def set_user_state(chat_id: int, new_state: int):
    """
    Sets the state of the user (chat_id) to the new state (new_state)

    Attributes:
        chat_id: Integer to identify the user
        new_state: Integer of the new state
    """
    with open(file_path, "r") as file_object:
        json_content = file_object.read()
        all_user = json.loads(json_content)

    if not (str(chat_id) in all_user):
        all_user[str(chat_id)] = UserData(current_state=new_state).user_entry
    else:
        all_user[str(chat_id)][Attributes.CURRENT_STATE.value] = new_state

    with open(file_path, 'w') as writefile:
        json.dump(all_user, writefile, indent=4)


def get_subscriptions(chat_id: int):
    """
    Returns an array of subscriptions of the user (chat_id)

    Attributes:
        chat_id: Integer to identify the user
    """
    with open(file_path, "r") as file_object:
        json_content = file_object.read()
        all_user = json.loads(json_content)

    if str(chat_id) in all_user:
        return all_user[str(chat_id)][Attributes.LOCATIONS.value]
    return None


def get_suggestions(chat_id: int):
    """
    Returns an array of suggestions of the user (chat_id)

    Attributes:
        chat_id: Integer to identify the user
    """
    with open(file_path, "r") as file_object:
        json_content = file_object.read()
        all_user = json.loads(json_content)

    if str(chat_id) in all_user:
        return all_user[str(chat_id)][Attributes.RECOMMENDATIONS.value]
    return UserData().user_entry[Attributes.RECOMMENDATIONS.value]

