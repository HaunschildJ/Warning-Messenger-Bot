import json
from enum import Enum
from types import SimpleNamespace

# See the MVP document for all possible options

file_path = "./Data/data.json"


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
    LANGUAGE = "language"


class UserData:
    def __init__(self, chat_id,
                 receive_warnings=False,
                 receive_covid_information=ReceiveInformation.NEVER.value,
                 locations=None,
                 language=Language.GERMAN.value):
        self.user_entry = {
            Attributes.CHAT_ID.value: chat_id,
            Attributes.RECEIVE_WARNINGS.value: receive_warnings,
            Attributes.COVID_AUTO_INFO.value: receive_covid_information,
            Attributes.LOCATIONS.value: locations,
            Attributes.LANGUAGE.value: language
        }

    def change_entry(self, attribute, value):
        self.user_entry[attribute.value] = value

    def set_location(self, location_name, warning, warning_level):
        all_users = self.user_entry[Attributes.LOCATIONS.value]
        if all_users is None:
            self.user_entry[Attributes.LOCATIONS.value] = [{
                "name": location_name, "warning_level": [warning_level], "warnings": [warning.name]
            }]
            return
        for user in all_users:
            if user["name"] == location_name:
                i = 0
                for warning_old in user["warnings"]:
                    if warning_old == warning.name:
                        user["warning_level"][i] = warning_level
                        return
                    i = i+1
                user["warnings"].append(warning.name)
                user["warning_level"].append(warning_level)
                return
        all_users.append({
                "name": location_name, "warning_level": [warning_level], "warnings": [warning.name]
            })

    def remove_location(self, location_name):
        current_locations = self.user_entry[Attributes.LOCATIONS.value].copy()
        for location in current_locations:
            if location["name"] == location_name:
                self.user_entry[Attributes.LOCATIONS.value].remove(location)
                return

    def remove_all_locations(self):
        self.user_entry[Attributes.LOCATIONS.value].clear()


def write_file(user_data):
    file_object = open(file_path, "r")
    json_content = file_object.read()
    user_entries = json.loads(json_content)

    chat_id = user_data.user_entry[Attributes.CHAT_ID.value]

    for entry in user_entries:
        if entry[Attributes.CHAT_ID.value] == chat_id:
            user_entries.remove(entry)

    user_entries.append(user_data.user_entry)
    with open(file_path, 'w') as writefile:
        json.dump(user_entries, writefile, indent=4)


def remove_user(chat_id):
    file_object = open(file_path, "r")
    json_content = file_object.read()
    user_entries = json.loads(json_content)

    for entry in user_entries:
        if entry[Attributes.CHAT_ID.value] == chat_id:
            user_entries.remove(entry)

    with open(file_path, 'w') as writefile:
        json.dump(user_entries, writefile, indent=4)


def get_data_model(data) -> dict:
    return json.loads(data, object_hook=lambda d: SimpleNamespace(**d))


def read_user(chat_id) -> UserData:
    file_object = open(file_path, "r")
    json_content = file_object.read()
    user_entries = json.loads(json_content)

    for entry in user_entries:
        if entry[Attributes.CHAT_ID.value] == chat_id:
            model = get_data_model(json.dumps(entry, indent=4))
            result = UserData(chat_id, receive_warnings=model.receive_warnings,
                              receive_covid_information=model.receive_covid_information, language=model.language)
            for location in model.locations:
                i = 0
                for warning in location.warnings:
                    result.set_location(location.name, WarnType.__getitem__(warning), location.warning_level[i])
                    i = i+1
                if i == 0:
                    result.set_location(location.name, [], [])
            return result
    return UserData(chat_id)


a = UserData(10)
print(a.user_entry)
a.change_entry(Attributes.RECEIVE_WARNINGS, True)
print(a.user_entry)
a.set_location("Darmstadt", WarnType.WEATHER, 5)
print(a.user_entry)
a.set_location("Darmstadt", WarnType.WEATHER, 7)
print(a.user_entry)
a.set_location("Hamburg", WarnType.WEATHER, 3)
print(a.user_entry)

write_file(a)

print(read_user(10).user_entry)
