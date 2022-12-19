import json
from enum import Enum
from types import SimpleNamespace

# See the MVP document for all possible options

file_path = "../Source/Data/data.json"


class WarnType(Enum):
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
    RECEIVE_WARNINGS = "receive_warnings"
    COVID_AUTO_INFO = "receive_covid_information"
    LOCATIONS = "locations"
    RECOMMENDATIONS = "recommendations"
    LANGUAGE = "language"


class UserData:
    """
    User Data in concise form. Is read from a JSON file.
    """
    def __init__(self, chat_id: int,
                 receive_warnings=False,
                 receive_covid_information=ReceiveInformation.NEVER.value,
                 locations=None,
                 recommendation=None,
                 language=Language.GERMAN.value):
        """
        Initializes the User Data Attributes. Chat ID is only mandatory parameter. Other ones can be set later.

        Arguments:
            chat_id: Integer used to identify Telegram Chat. Needed to identify User.
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
            Attributes.CHAT_ID.value: chat_id,
            Attributes.RECEIVE_WARNINGS.value: receive_warnings,
            Attributes.COVID_AUTO_INFO.value: receive_covid_information,
            Attributes.LOCATIONS.value: locations,
            Attributes.RECOMMENDATIONS.value: recommendation,
            Attributes.LANGUAGE.value: language
        }

    def change_entry(self, attribute, value):
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


def write_file(user_data: UserData):
    """
    Writes parameter user_data into a JSON file. Replacing it if already existing.

    Arguments:
        user_data: UserData instance containing information, that one wants to add to the JSON file.
    """
    with open(file_path, "r") as file_object:
        json_content = file_object.read()
        user_entries = json.loads(json_content)

    chat_id = user_data.user_entry[Attributes.CHAT_ID.value]

    for entry in user_entries:
        if entry[Attributes.CHAT_ID.value] == chat_id:
            user_entries.remove(entry)

    user_entries.append(user_data.user_entry)
    with open(file_path, 'w') as writefile:
        json.dump(user_entries, writefile, indent=4)


def remove_user(chat_id: int):
    with open(file_path, "r") as file_object:
        json_content = file_object.read()
        user_entries = json.loads(json_content)

    for entry in user_entries:
        if entry[Attributes.CHAT_ID.value] == chat_id:
            user_entries.remove(entry)

    with open(file_path, 'w') as writefile:
        json.dump(user_entries, writefile, indent=4)


def _get_data_model(data) -> dict:
    return json.loads(data, object_hook=lambda d: SimpleNamespace(**d))


def read_user(chat_id: int) -> UserData:
    """
    Returns an instance of UserData depending on given chat_id. If JSON file does not contain the user yet,
    the user gets constructed, solely with given chat_id.

    Does not write into the JSON file.

    Arguments:
        chat_id: Integer, which represents the user.

    Returns:
        Instance of UserData. Either from JSON DATA or newly constructed with chat_id.
    """
    with open(file_path, "r") as file_object:
        json_content = file_object.read()
        user_entries = json.loads(json_content)

    for entry in user_entries:
        if entry[Attributes.CHAT_ID.value] == chat_id:
            model = _get_data_model(json.dumps(entry, indent=4))
            result = UserData(chat_id, receive_warnings=model.receive_warnings,
                              receive_covid_information=model.receive_covid_information, language=model.language)
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
    return UserData(chat_id)

