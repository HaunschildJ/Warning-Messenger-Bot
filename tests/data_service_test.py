import importlib.util
import unittest
import sys

sys.path.insert(0, "..\source")

import data_service

file_path = "../source/data/data.json"


class MyTestCase(unittest.TestCase):
    def test_receive_warnings(self):
        # read json file and safe the current content before the test
        user_entries = data_service._read_file(file_path)

        # clear the json file
        data_service._write_file(file_path, {})

        # user with id == 10 wants no more auto warnings
        data_service.set_receive_warnings(10, False)

        # check if it was saved
        self.assertEqual(False, data_service.get_receive_warnings(10))

        # user with id == 10 wants auto warnings
        data_service.set_receive_warnings(10, True)

        # check if it was saved
        self.assertEqual(True, data_service.get_receive_warnings(10))

        # user with id == 1 wants auto warnings but user 1 is not in the json yet
        expected = data_service.DEFAULT_DATA["receive_warnings"]
        actual = data_service.get_receive_warnings(1)
        self.assertEqual(expected, actual)

        # write data back to json from before the test
        data_service._write_file(file_path, user_entries)

    def test_user_state(self):
        # read json file and safe the current content before the test
        user_entries = data_service._read_file(file_path)

        # clear the json file
        data_service._write_file(file_path, {})

        for i in [0, 1, 2, 0, 3]:
            # change state of user 10
            data_service.set_user_state(10, i)

            # check if it was saved
            self.assertEqual(i, data_service.get_user_state(10))

        # get state of user 1 who is currently not in json
        expected = data_service.DEFAULT_DATA["current_state"]
        self.assertEqual(expected, data_service.get_user_state(1))

        # write data back to json from before the test
        data_service._write_file(file_path, user_entries)

    def test_auto_covid_information(self):
        # read json file and safe the current content before the test
        user_entries = data_service._read_file(file_path)

        # clear the json file
        data_service._write_file(file_path, {})

        for i in data_service.ReceiveInformation:
            # check if user can change all auto covid update choices
            data_service.set_auto_covid_information(10, i)

            # check if it was saved
            self.assertEqual(i, data_service.get_auto_covid_information(10))

        # get how often user 1 wants to get covid updates. user 1 is currently not in json
        expected = data_service.ReceiveInformation(data_service.DEFAULT_DATA["receive_covid_information"])
        self.assertEqual(expected, data_service.get_auto_covid_information(1))

        # write data back to json from before the test
        data_service._write_file(file_path, user_entries)

    def test_subscriptions(self):
        # read json file and safe the current content before the test
        user_entries = data_service._read_file(file_path)

        # clear the json file
        data_service._write_file(file_path, {})

        # user 1 wants to delete a subscription but is not in json yet -> nothing should happen
        data_service.delete_subscription(1, "Darmstadt", "3")
        test_entries = data_service._read_file(file_path)
        self.assertEqual({}, test_entries)

        # user 1 wants to delete a subscription but has no subscriptions yet
        should_be = {"1": data_service.DEFAULT_DATA}
        data_service._write_file(file_path, should_be)
        data_service.delete_subscription(1, "Darmstadt", "3")
        self.assertEqual(should_be, data_service._read_file(file_path))

        # clear the json file
        data_service._write_file(file_path, {})

        # user with id == 10 wants to get different warnings
        data_service.add_subscription(10, "Darmstadt", "3", 2)
        data_service.add_subscription(10, "Darmstadt", "0", 3)
        data_service.add_subscription(10, "Berlin", "3", 1)

        should_be = {
                    "Darmstadt": {
                        "3": 2,
                        "0": 3
                        },
                    "Berlin": {
                        "3": 1
                    }
                    }

        # check if it was saved
        self.assertEqual(should_be, data_service.get_subscriptions(10))

        # user with id == 10 wants to delete warnings
        data_service.delete_subscription(10, "Darmstadt", "0")
        data_service.delete_subscription(10, "Berlin", "3")
        data_service.add_subscription(10, "Darmstadt", "3", 5)

        should_be = {
            "Darmstadt": {
                "3": 5
            }
        }

        # check if it was saved
        self.assertEqual(should_be, data_service.get_subscriptions(10))

        # get subscriptions of user 1 who is currently not in json
        expected = data_service.DEFAULT_DATA["locations"]
        self.assertEqual(expected, data_service.get_subscriptions(1))

        # write data back to json from before the test
        data_service._write_file(file_path, user_entries)

    def test_suggestion(self):
        # read json file and safe the current content before the test
        user_entries = data_service._read_file(file_path)

        # clear the json file
        data_service._write_file(file_path, {})

        # user 1 wants to see their suggestions but is not in the json yet
        expected = data_service.DEFAULT_DATA["recommendations"]
        self.assertEqual(expected, data_service.get_suggestions(1))

        # adding a location that was not in recommendations before
        control_user = [{
                "name": "Test",
                "place_id": "12345",
                "district_id": "12345"
            },
            {
                "name": "Berlin, Stadt",
                "place_id": "110000000000",
                "district_id": "11000"
            },
            {
                "name": "Berlin-Mitte",
                "place_id": "110010000000",
                "district_id": "11001"
            }
        ]
        return_value = data_service.add_suggestion(10, "Test", "12345", "12345")

        # check if the user entries are equal
        self.assertEqual(control_user, data_service.get_suggestions(10))

        for (control_recommendation, result_recommendation) in zip(control_user, return_value):
            self.assertEqual(control_recommendation["name"],
                             data_service.get_recommendation_name(result_recommendation))
            self.assertEqual(control_recommendation["place_id"],
                             data_service.get_recommendation_place_id(result_recommendation))
            self.assertEqual(control_recommendation["district_id"],
                             data_service.get_recommendation_district_id(result_recommendation))

        # adding the least recently added location
        control_user = [{
                "name": "Berlin-Mitte",
                "place_id": "110010000000",
                "district_id": "11001"
            },
            {
            "name": "Test",
            "place_id": "12345",
            "district_id": "12345"
            },
            {
                "name": "Berlin, Stadt",
                "place_id": "110000000000",
                "district_id": "11000"
            }
        ]
        data_service.add_suggestion(10, "Berlin-Mitte", "110010000000", "11001")

        # check if the user entries are equal
        self.assertEqual(control_user, data_service.get_suggestions(10))

        # adding the second most recently added location
        control_user = [{
                "name": "Test",
                "place_id": "12345",
                "district_id": "12345"
            },
            {
            "name": "Berlin-Mitte",
            "place_id": "110010000000",
            "district_id": "11001"
            },
            {
                "name": "Berlin, Stadt",
                "place_id": "110000000000",
                "district_id": "11000"
            }
        ]
        data_service.add_suggestion(10, "Test", "12345", "12345")

        # check if the user entries are equal
        self.assertEqual(control_user, data_service.get_suggestions(10))

        # adding the location that was most recently added should change nothing
        data_service.add_suggestion(10, "Test", "12345", "12345")

        self.assertEqual(control_user, data_service.get_suggestions(10))

        # write data back to json from before the test
        data_service._write_file(file_path, user_entries)

    def test_language(self):
        # read json file and safe the current content before the test
        user_entries = data_service._read_file(file_path)

        # clear the json file
        data_service._write_file(file_path, {})

        # user 1 wants to see their language but is not in the json yet
        expected = data_service.Language(data_service.DEFAULT_DATA["language"])
        self.assertEqual(expected, data_service.get_language(1))

        for i in data_service.Language:
            # check if user can change to all languages
            data_service.set_language(10, i)

            # check if it was saved
            self.assertEqual(i, data_service.get_language(10))

        # write data back to json from before the test
        data_service._write_file(file_path, user_entries)

    def test_remove_user_error(self):
        # read json file and safe the current content before the test
        saved_user_entries = data_service._read_file(file_path)

        # clear the json file
        data_service._write_file(file_path, {})

        # set the state of user id == 10 to 0 so the user gets a database entry
        data_service.set_user_state(10, 0)

        # remove the user with the id == 10
        data_service.remove_user(10)

        # read json file
        user_entries = data_service._read_file(file_path)

        # remove the user with the id == 10 (should do nothing)
        data_service.remove_user(10)

        # read json file again after remove
        user_entries2 = data_service._read_file(file_path)

        # check if json file after removing a non-existing user is equal to the json file before
        self.assertEqual(user_entries, user_entries2)

        # write data back to json from before the test
        data_service._write_file(file_path, saved_user_entries)


if __name__ == '__main__':
    unittest.main()





