import importlib.util
import unittest
import json


DataService = importlib.util.spec_from_file_location("DataService", "../Source/DataService.py").loader.load_module()

file_path = "../Source/Data/data.json"


class MyTestCase(unittest.TestCase):
    def test_receive_warnings(self):
        # read json file and safe the current content before the test
        with open(file_path, "r") as file_object:
            json_content = file_object.read()
            user_entries = json.loads(json_content)

        # clear the json file
        with open(file_path, 'w') as writefile:
            json.dump({}, writefile, indent=4)

        # user with id == 10 wants no more auto warnings
        DataService.set_receive_warnings(10, False)

        # check if it was saved
        self.assertEqual(False, DataService.get_receive_warnings(10))

        # user with id == 10 wants auto warnings
        DataService.set_receive_warnings(10, True)

        # check if it was saved
        self.assertEqual(True, DataService.get_receive_warnings(10))

        # write data back to json from before the test
        with open(file_path, 'w') as writefile:
            json.dump(user_entries, writefile, indent=4)

    def test_user_state(self):
        # read json file and safe the current content before the test
        with open(file_path, "r") as file_object:
            json_content = file_object.read()
            user_entries = json.loads(json_content)

        # clear the json file
        with open(file_path, 'w') as writefile:
            json.dump({}, writefile, indent=4)

        for i in [0, 1, 2, 0, 3]:
            # change state of user 10
            DataService.set_user_state(10, i)

            # check if it was saved
            self.assertEqual(i, DataService.get_user_state(10))

        # write data back to json from before the test
        with open(file_path, 'w') as writefile:
            json.dump(user_entries, writefile, indent=4)

    def test_auto_covid_information(self):
        # read json file and safe the current content before the test
        with open(file_path, "r") as file_object:
            json_content = file_object.read()
            user_entries = json.loads(json_content)

        # clear the json file
        with open(file_path, 'w') as writefile:
            json.dump({}, writefile, indent=4)

        for i in DataService.ReceiveInformation:
            # check if user can change all auto covid update choices
            DataService.set_auto_covid_information(10, i)

            # check if it was saved
            self.assertEqual(i, DataService.get_auto_covid_information(10))

        # write data back to json from before the test
        with open(file_path, 'w') as writefile:
            json.dump(user_entries, writefile, indent=4)

    def test_subscriptions(self):
        # read json file and safe the current content before the test
        with open(file_path, "r") as file_object:
            json_content = file_object.read()
            user_entries = json.loads(json_content)

        # clear the json file
        with open(file_path, 'w') as writefile:
            json.dump({}, writefile, indent=4)

        # user with id == 10 wants to get weather warnings from Darmstadt with the warning level 2
        DataService.add_subscription(10, "Darmstadt", DataService.WarnType.WEATHER, 2)
        # user with id == 10 wants to get BIWAPP warnings from Darmstadt with the warning level 3
        DataService.add_subscription(10, "Darmstadt", DataService.WarnType.BIWAPP, 3)
        # user with id == 10 wants to get weather warnings from Berlin with the warning level 1
        DataService.add_subscription(10, "Berlin", DataService.WarnType.WEATHER, 1)

        should_be = {
                    "Darmstadt": {
                        "weather": 2,
                        "biwapp": 3
                        },
                    "Berlin": {
                        "weather": 1
                    }
                    }

        # check if it was saved
        self.assertEqual(should_be, DataService.get_subscriptions(10))

        # user with id == 10 wants to delete the BIWAPP warning from Darmstadt
        DataService.delete_subscription(10, "Darmstadt", DataService.WarnType.BIWAPP.value)
        # user with id == 10 wants to delete the weather warning from Berlin
        DataService.delete_subscription(10, "Berlin", DataService.WarnType.WEATHER.value)
        # user with id == 10 wants to change the warning level of the weather warning of Darmstadt to 5
        DataService.add_subscription(10, "Darmstadt", DataService.WarnType.WEATHER, 5)

        should_be = {
            "Darmstadt": {
                "weather": 5
            }
        }

        # check if it was saved
        self.assertEqual(should_be, DataService.get_subscriptions(10))

        # write data back to json from before the test
        with open(file_path, 'w') as writefile:
            json.dump(user_entries, writefile, indent=4)

    def test_suggestion(self):
        # read json file and safe the current content before the test
        with open(file_path, "r") as file_object:
            json_content = file_object.read()
            user_entries = json.loads(json_content)

        # clear the json file
        with open(file_path, 'w') as writefile:
            json.dump({}, writefile, indent=4)

        # adding a location that was not in recommendations before
        control_user = ["Darmstadt", "München", "Frankfurt"]
        DataService.add_suggestion(10, "Darmstadt")

        # check if the user entries are equal
        self.assertEqual(control_user, DataService.get_suggestions(10))

        # adding the least recently added location
        control_user = ["Frankfurt", "Darmstadt", "München"]
        DataService.add_suggestion(10, "Frankfurt")

        # check if the user entries are equal
        self.assertEqual(control_user, DataService.get_suggestions(10))

        # adding the second most recently added location
        control_user = ["Darmstadt", "Frankfurt", "München"]
        DataService.add_suggestion(10, "Darmstadt")

        # check if the user entries are equal
        self.assertEqual(control_user, DataService.get_suggestions(10))

        # adding the location that was most recently added should change nothing
        DataService.add_suggestion(10, "Darmstadt")

        self.assertEqual(control_user, DataService.get_suggestions(10))

        # write data back to json from before the test
        with open(file_path, 'w') as writefile:
            json.dump(user_entries, writefile, indent=4)

    def test_language(self):
        # read json file and safe the current content before the test
        with open(file_path, "r") as file_object:
            json_content = file_object.read()
            user_entries = json.loads(json_content)

        # clear the json file
        with open(file_path, 'w') as writefile:
            json.dump({}, writefile, indent=4)

        for i in DataService.Language:
            # check if user can change to all languages
            DataService.set_language(10, i)

            # check if it was saved
            self.assertEqual(i, DataService.get_language(10))

        # write data back to json from before the test
        with open(file_path, 'w') as writefile:
            json.dump(user_entries, writefile, indent=4)

    def test_remove_user_error(self):
        # read json file and safe the current content before the test
        with open(file_path, "r") as file_object:
            json_content = file_object.read()
            saved_user_entries = json.loads(json_content)

        # clear the json file
        with open(file_path, 'w') as writefile:
            json.dump({}, writefile, indent=4)

        # set the state of user id == 10 to 0 so the user gets a database entry
        DataService.set_user_state(10, 0)

        # remove the user with the id == 10
        DataService.remove_user(10)

        # read json file
        with open(file_path, "r") as file_object:
            json_content = file_object.read()
            user_entries = json.loads(json_content)

        # remove the user with the id == 10 (should do nothing)
        DataService.remove_user(10)

        # read json file again after remove
        with open(file_path, "r") as file_object:
            json_content = file_object.read()
            user_entries2 = json.loads(json_content)

        # check if json file after removing a non-existing user is equal to the json file before
        self.assertEqual(user_entries, user_entries2)

        # write data back to json from before the test
        with open(file_path, 'w') as writefile:
            json.dump(saved_user_entries, writefile, indent=4)


if __name__ == '__main__':
    unittest.main()





