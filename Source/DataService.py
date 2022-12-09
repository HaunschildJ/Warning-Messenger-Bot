import json
from types import SimpleNamespace

# See the MVP document for all possible options

file_path = "./Data/data.json"

userEntry = {
    "chat_id": "",
    "receive_warnings": "false",
    "warn_level": "none",
    "warn_type": "none",
    "receive_covid_information": "never",
    "locations": [
        "Darmstadt"
    ],
    "language": "german"
}

json_object = json.dumps(userEntry, indent=4)


def write_file(user_entry):
    with open(file_path, "w") as outfile:
        outfile.write(json_object)


def get_data_model(data) -> dict:
    return json.loads(data, object_hook=lambda d: SimpleNamespace(**d))


def read_user(chat_id) -> dict:
    file_object = open(file_path, "r")
    json_content = file_object.read()
    user_entries = json.loads(json_content)

    for entry in user_entries:
        if entry['chat_id'] == str(chat_id):
            return get_data_model(json.dumps(entry, indent=4))
