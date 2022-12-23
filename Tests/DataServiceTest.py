import importlib.util
import unittest
import json


DataService = importlib.util.spec_from_file_location("DataService", "../Source/DataService.py").loader.load_module()

file_path = "../Source/Data/data.json"


class MyTestCase(unittest.TestCase):
    def test_write_read(self):
        # read json file and safe the current content before the test
        with open(file_path, "r") as file_object:
            json_content = file_object.read()
            user_entries = json.loads(json_content)

        # clear the json file
        with open(file_path, 'w') as writefile:
            json.dump({}, writefile, indent=4)

        # create a UserData instance for the user (id == 10) that will be written into the json file
        a = DataService.UserData()
        a.change_entry(DataService.Attributes.RECEIVE_WARNINGS, True)
        a.set_location("Darmstadt", DataService.WarnType.WEATHER, 7)
        a.set_location("Hamburg", DataService.WarnType.WEATHER, 3)

        # write the user into the json file
        DataService.write_file(10, a)

        # check if the read user is equal to the written user
        self.assertEqual(a.user_entry, DataService.read_user(10).user_entry)

        # write data back to json from before the test
        with open(file_path, 'w') as writefile:
            json.dump(user_entries, writefile, indent=4)

    def test_remove(self):
        # create a UserData instance for the user (id == 10) that will be written into the json file
        a = DataService.UserData()
        a.change_entry(DataService.Attributes.RECEIVE_WARNINGS, True)
        a.set_location("Darmstadt", DataService.WarnType.WEATHER, 7)
        a.set_location("Hamburg", DataService.WarnType.WEATHER, 3)

        # write the user into the json file
        DataService.write_file(10, a)

        # remove the user with the id == 10
        DataService.remove_user(10)

        # create a new UserData instance for user with id == 10 with everything else on default
        should_be = DataService.UserData()

        # check if the user was not found in the json file (so everything but the user id on default)
        self.assertEqual(should_be.user_entry, DataService.read_user(10).user_entry)

    def test_remove_user_error(self):
        # create a UserData instance for the user (id == 10) that will be written into the json file
        a = DataService.UserData()
        a.change_entry(DataService.Attributes.RECEIVE_WARNINGS, True)
        a.set_location("Darmstadt", DataService.WarnType.WEATHER, 7)
        a.set_location("Hamburg", DataService.WarnType.WEATHER, 3)

        # write the user into the json file
        DataService.write_file(10, a)

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

    def test_add_recommendation(self):
        # create a UserData instance for the user (id == 10)
        test_user = DataService.UserData(10)
        control_user = DataService.UserData(10)

        # adding a location that was not in recommendations before
        control_user.user_entry["recommendations"] = ["Darmstadt", "München", "Frankfurt"]
        test_user.add_recommended_location("Darmstadt")

        # check if the user entries are equal
        self.assertEqual(control_user.user_entry, test_user.user_entry)

        # adding the least recently added location
        control_user.user_entry["recommendations"] = ["Frankfurt", "Darmstadt", "München"]
        test_user.add_recommended_location("Frankfurt")

        # check if the user entries are equal
        self.assertEqual(control_user.user_entry, test_user.user_entry)

        # adding the second most recently added location
        control_user.user_entry["recommendations"] = ["Darmstadt", "Frankfurt", "München"]
        test_user.add_recommended_location("Darmstadt")

        # check if the user entries are equal
        self.assertEqual(control_user.user_entry, test_user.user_entry)

        # adding the location that was most recently added should change nothing
        test_user.add_recommended_location("Darmstadt")

        # check if the user entries are equal
        self.assertEqual(control_user.user_entry, test_user.user_entry)


if __name__ == '__main__':
    unittest.main()





