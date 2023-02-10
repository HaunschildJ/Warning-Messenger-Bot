import importlib.util
import unittest
import sys

sys.path.insert(0, "..\source")

import data_service
import enum_types

file_path = "../source/data/data.json"
warnings_already_received_path = "../source/data/warnings_already_received.json"
active_warnings_path = "../source/data/active_warnings.json"


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
        data_service.delete_subscription(1, "64287", "weather")
        test_entries = data_service._read_file(file_path)
        self.assertEqual({}, test_entries)

        # user 1 wants to delete a subscription but has no subscriptions yet
        should_be = {"1": data_service.DEFAULT_DATA.copy()}
        data_service._write_file(file_path, should_be)
        data_service.delete_subscription(1, "64287", "flood")
        self.assertEqual(should_be, data_service._read_file(file_path))

        # clear the json file
        data_service._write_file(file_path, {})

        # user with id == 10 wants to get different warnings
        data_service.add_subscription(chat_id=10,
                                      postal_code="64287",
                                      district_id="06411",
                                      warning="weather",
                                      warning_level="severe")
        data_service.add_subscription(chat_id=10,
                                      postal_code="64287",
                                      district_id="06411",
                                      warning="flood",
                                      warning_level="moderate")
        data_service.add_subscription(chat_id=10,
                                      postal_code="99099",
                                      district_id="16051",
                                      warning="civil_protection",
                                      warning_level="minor")
        # 3 entries expected. 2 for Darmstadt, 1 for Erfurt
        should_be = {
            "64287": {
                "district_id": "06411",
                "weather": "severe",
                "flood": "moderate"
            },
            "99099": {
                "district_id": "16051",
                "civil_protection": "minor"
            }
        }

        # check if it was saved
        self.assertEqual(should_be, data_service.get_subscriptions(10))

        # delete severe weather warnings for Darmstadt
        data_service.delete_subscription(chat_id=10,
                                         postal_code="64287",
                                         warning="weather")

        # add all weather warnings to Erfurt
        data_service.add_subscription(chat_id=10,
                                      postal_code="99099",
                                      district_id="16051",
                                      warning="weather",
                                      warning_level="minor")

        # 3 entries expected. 1 for Darmstadt, 2 for Erfurt
        should_be = {
            "64287": {
                "district_id": "06411",
                "flood": "moderate"
            },
            "99099": {
                "district_id": "16051",
                "civil_protection": "minor",
                "weather": "minor"
            }
        }

        # check if it was saved
        self.assertEqual(should_be, data_service.get_subscriptions(10))

        # delete all subscriptions
        data_service.delete_subscription(10, "64287", "flood")
        data_service.delete_subscription(10, "99099", "civil_protection")
        data_service.delete_subscription(10, "99099", "weather")

        # check whether postal code got deleted when last warning gets deleted
        entries_after_deleting_all_subscriptions = data_service._read_file(file_path)
        locations = entries_after_deleting_all_subscriptions["10"]["locations"]
        self.assertEqual(locations, {})

        # get subscriptions of user 1 who is currently not in json
        expected = data_service.DEFAULT_DATA["locations"]
        self.assertEqual(expected, data_service.get_subscriptions(1))

        # write data back to json from before the test
        data_service._write_file(file_path, user_entries)

    def test_suggestion(self):
        """Tests various methods related to favorites in data_service.py.\n
         First checks if reading suggestions of non-existing entry correctly returns default parameters.\n
         Then adds 3 favorites and reshuffles them in all possible ways:
             (i) Readding the least recently added favorit
             (ii) Readding the second least recently added favorit
             (iii) Readding the most recenlty added favorit
         and checks whether the readded favorite correctly becomes first favorit and whether the other
         favorites are correctly moved back one place without deleting them.
         """
        # read json file and safe the current content before the test
        user_entries = data_service._read_file(file_path)

        # clear the json file
        data_service._write_file(file_path, {})

        # user 1 wants to see their suggestions but is not in the json yet
        expected = data_service.DEFAULT_DATA["recommendations"]
        self.assertEqual(expected, data_service.get_suggestions(1))

        # adding a location that was not in recommendations before
        expected_favorites_after_adding = [
            {
                'postal_code': '70599',
                'district_id': '08111'
            },
            {
                'postal_code': '99099',
                'district_id': '16051'
            },
            {
                'postal_code': '22559',
                'district_id': '02000'
            }
        ]
        data_service.add_suggestion(10, '22559', '02000')
        data_service.add_suggestion(10, '99099', '16051')
        favorites = data_service.add_suggestion(10, '70599', '08111')

        actual_suggestions = data_service.get_suggestions(10)

        # check if add_suggestions
        #   (i) added correct favorites to newly generated user with chat_id 10 and
        #   (ii) returned the right list of dicts
        self.assertEqual(favorites, actual_suggestions, expected_favorites_after_adding)

        for (control_recommendation, result_recommendation) in zip(expected_favorites_after_adding, favorites):
            self.assertEqual(control_recommendation["postal_code"],
                             data_service.get_recommendation_postal_code(result_recommendation))
            self.assertEqual(control_recommendation["district_id"],
                             data_service.get_recommendation_district_id(result_recommendation))

        # adding the least recently added location, 1-2-3 should become 3-1-2
        expected_favorites_after_readding_least_recently = [
            {
                'postal_code': '22559',
                'district_id': '02000'
            },
            {
                'postal_code': '70599',
                'district_id': '08111'
            },
            {
                'postal_code': '99099',
                'district_id': '16051'
            }
        ]
        actual_favorites_after_readding_least_recently = data_service.add_suggestion(10, "22559", '02000')
        self.assertEqual(expected_favorites_after_readding_least_recently,
                         data_service.get_suggestions(10),
                         actual_favorites_after_readding_least_recently)

        # adding the 2nd recently added location, 1-2-3 should become 2-1-3
        expected_favorites_after_readding_second_least_recently = [
            {
                'postal_code': '70599',
                'district_id': '08111'
            },
            {
                'postal_code': '22559',
                'district_id': '02000'
            },
            {
                'postal_code': '99099',
                'district_id': '16051'
            }
        ]
        actual_favorites_after_readding_second_least_recently = data_service.add_suggestion(10, '70599', '08111')

        # check if the user entries are equal
        self.assertEqual(expected_favorites_after_readding_second_least_recently,
                         data_service.get_suggestions(10),
                         actual_favorites_after_readding_second_least_recently)

        # adding the location that was most recently added should change nothing
        actual_favorites_after_readding_most_recenlty = data_service.add_suggestion(10, '70599', '08111')

        self.assertEqual(expected_favorites_after_readding_second_least_recently,
                         data_service.get_suggestions(10),
                         actual_favorites_after_readding_most_recenlty)

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
        entries_before_deleting_non_existing_user = data_service._read_file(file_path)

        # remove the user with the id == 10 (should do nothing)
        data_service.remove_user(10)

        # read json file again after remove
        entries_after_deleting_non_existing_user = data_service._read_file(file_path)

        # check if json file after removing a non-existing user is equal to the json file before
        self.assertEqual(entries_before_deleting_non_existing_user, entries_after_deleting_non_existing_user)

        # write data back to json from before the test
        data_service._write_file(file_path, saved_user_entries)

    def test_delete_all_subscriptions(self):
        """
        Tests delete_all_subscriptions in data_service.py.\n
        Creates two users (user_10 and user_20) and adds some subscriptions for both of them.\n
        First checks whether subscriptions got written correctly to data base.\n
        Then calls tested method for user_20 and checks if all subscriptions were deleted.\n
        Lastly checks if subscriptions of user_10 stayed the same.
        """

        # read json file and safe the current content before the test
        entries_before_test = data_service._read_file(file_path)

        # clear the json file
        data_service._write_file(file_path, {})
        # delete all subs for non existing user -> nothing should happen
        data_service.delete_all_subscriptions(99)
        test_entries = data_service._read_file(file_path)
        self.assertEqual({}, test_entries)

        # writing 2 users (chat_ids 10 and 20) to data base, both with default values
        entries = {"10": data_service.DEFAULT_DATA.copy(),
                   "20": data_service.DEFAULT_DATA.copy()}
        data_service._write_file(file_path, entries)

        # add various warnings for user with chat_id 20
        data_service.add_subscription(chat_id=20,
                                      postal_code="22559",
                                      district_id="02000",
                                      warning="weather",
                                      warning_level="moderate")
        data_service.add_subscription(chat_id=20,
                                      postal_code="99099",
                                      district_id="16051",
                                      warning="flood",
                                      warning_level="severe")
        data_service.add_subscription(chat_id=20,
                                      postal_code="70599",
                                      district_id="08111",
                                      warning="weather",
                                      warning_level="minor")

        # add one warning for user with chat_id 10
        data_service.add_subscription(chat_id=10,
                                      postal_code="22559",
                                      district_id="02000",
                                      warning="flood",
                                      warning_level="moderate")

        # check if data base has correct subscriptions for user with chat_id 20
        expected_subscriptions_after_adding = {
            '22559':
                {
                    'district_id': '02000',
                    'weather': 'moderate'
                },
            '99099':
                {
                    'district_id': '16051',
                    'flood': 'severe'
                },
            '70599':
                {
                    'district_id': '08111',
                    'weather': 'minor'
                }
        }
        actual_subscriptions_after_adding = data_service.get_subscriptions(20)
        self.assertEqual(actual_subscriptions_after_adding, expected_subscriptions_after_adding)

        # check whether subscriptions of user with chat_id 10 stayed the same
        expected_subscriptions_user_chat_id_10 = {
            '22559':
                {
                    'district_id': '02000',
                    'flood': 'moderate'
                }
        }
        actual_subscriptions_user_chat_id_10 = data_service.get_subscriptions(10)
        self.assertEqual(expected_subscriptions_user_chat_id_10, actual_subscriptions_user_chat_id_10)

        # check if deleting all subscriptions of user with chat_id 20 works
        data_service.delete_all_subscriptions(20)
        expected_subscriptions_after_deleting_all_subscriptions = {}
        actual_subscriptions_after_deleting_all_subscriptions = data_service.get_subscriptions(20)
        self.assertEqual(actual_subscriptions_after_deleting_all_subscriptions,
                         expected_subscriptions_after_deleting_all_subscriptions)

        # write data back to json from before the test
        data_service._write_file(file_path, entries_before_test)

    def test_reset_favorites(self):
        """
        Tests reset_favorites in data_service.py.
        Creates two users (user_10 and user_20) and adds 3 favorites for user_20.\n
        First checks whether favorites of user_20 got written correctly to data base.
        Then calls tested method for one user_20 and checks if favorites of both users match default favorites.
            (i) user_10 because he never got other favorites
            (ii) user_20 because his were resetted.\n
        """
        # read json file and safe the current content before the test
        entries_before_test = data_service._read_file(file_path)

        # clear the json file
        data_service._write_file(file_path, {})
        # delete all favorites for non existing user -> nothing should happen
        data_service.reset_favorites(99)
        test_entries = data_service._read_file(file_path)
        self.assertEqual({}, test_entries)

        # writing 2 users (chat_ids 10 and 20) to data base, both with default values
        entries = {"10": data_service.DEFAULT_DATA.copy(), "20": data_service.DEFAULT_DATA.copy()}
        data_service._write_file(file_path, entries)

        # add 3 favorites to user with chat_id 20
        data_service.add_suggestion(chat_id=20,
                                    postal_code="22559",
                                    district_id="02000")
        data_service.add_suggestion(chat_id=20,
                                    postal_code="99099",
                                    district_id="16051")
        data_service.add_suggestion(chat_id=20,
                                    postal_code="70599",
                                    district_id="08111")

        # check if data base has correct favorites for user with chat_id 20
        expected_favorites_after_adding = [
            {
                'postal_code': '70599',
                'district_id': '08111'
            },
            {
                'postal_code': '99099',
                'district_id': '16051'
            },
            {
                'postal_code': '22559',
                'district_id': '02000'
            }
        ]
        actual_favorites_after_adding = data_service.get_suggestions(20)
        self.assertEqual(actual_favorites_after_adding, expected_favorites_after_adding)

        # check if both users have default suggestions, chat_id 20 because all its favorites got resetted
        #   and chat_id 10 because his favorites were never changed after initialization
        data_service.reset_favorites(20)
        default_favorites = data_service.DEFAULT_DATA['recommendations']

        actual_favorites_chat_id_20_after_deleting = data_service.get_suggestions(20)
        actual_favorites_chat_id_10 = data_service.get_suggestions(10)

        self.assertEqual(actual_favorites_chat_id_20_after_deleting, default_favorites)
        self.assertEqual(actual_favorites_chat_id_10, default_favorites)

        # write data back to json from before the test
        data_service._write_file(file_path, entries_before_test)

    def test_delete_user(self):
        """Tests reset_favorites in data_service.py.
        reates two users (user_10 and user_20) and adds 3 favorites for user_20.\n
        First checks whether favorites of user_20 got written correctly to data base.
        Then calls tested method for one user_20 and checks if favorites of both users match default favorites.
            (i) user_10 because he never got other favorites
            (ii) user_20 because his were resetted.\n
        """
        # read json file and safe the current content before the test
        entries_before_test = data_service._read_file(file_path)

        # clear the json file
        data_service._write_file(file_path, {})
        # delete non existing user -> nothing should happen
        data_service.delete_user(99)
        test_entries = data_service._read_file(file_path)
        self.assertEqual({}, test_entries)


        # writing 2 users (chat_ids 10 and 20) to data base, both with default values
        entries = {"10": data_service.DEFAULT_DATA.copy(), "20": data_service.DEFAULT_DATA.copy()}
        data_service._write_file(file_path, entries)

        # add dummy values for favorites and subscriptions for user with chat_id 10
        data_service.add_suggestion(chat_id=10,
                                    postal_code="22559",
                                    district_id="02000")
        data_service.add_subscription(chat_id=10,
                                      postal_code="22559",
                                      district_id="02000",
                                      warning="flood",
                                      warning_level="moderate")
        # add dummy values for favorites and subscriptions for user with chat_id 20
        data_service.add_suggestion(chat_id=20,
                                    postal_code="99099",
                                    district_id="16051")
        data_service.add_subscription(chat_id=20,
                                      postal_code="70599",
                                      district_id="08111",
                                      warning="weather",
                                      warning_level="minor")

        # check if data base has correct favorites for user with chat_id 10
        expected_favorites_user_10_after_deleting_user_20 = [
            {
                "postal_code": "22559",
                "district_id": "02000"
            },
            {
                "postal_code": "10827",
                "district_id": "11000"
            },
            {
                "postal_code": "60308",
                "district_id": "06412"
            }
        ]
        actual_favorites_user_10_after_deleting_user_20 = data_service.get_suggestions(10)
        self.assertEqual(actual_favorites_user_10_after_deleting_user_20,
                         expected_favorites_user_10_after_deleting_user_20)

        # check if data base has correct subscriptions for user with chat_id 10
        expected_subscriptions_user_10_after_deleting_user_20 = {
            '22559':
                {
                    'district_id': '02000',
                    'flood': 'moderate'
                }
        }
        actual_subscriptions_user_10_after_deleting_user_20 = data_service.get_subscriptions(10)
        self.assertEqual(actual_subscriptions_user_10_after_deleting_user_20,
                         expected_subscriptions_user_10_after_deleting_user_20)

        # check if data base has correct favorites for user with chat_id 20
        expected_favorites_user_20 = [
            {
                "postal_code": "99099",
                "district_id": "16051"
            },
            {
                "postal_code": "10827",
                "district_id": "11000"
            },
            {
                "postal_code": "60308",
                "district_id": "06412"
            }
        ]
        actual_favorites_user_20 = data_service.get_suggestions(20)
        self.assertEqual(actual_favorites_user_20, expected_favorites_user_20)

        # check if data base has correct subscriptions for user with chat_id 20
        expected_subscriptions_user_20 = {
            '70599':
                {
                    'district_id': '08111',
                    'weather': 'minor'
                }
        }
        actual_subscriptions_user_20 = data_service.get_subscriptions(20)
        self.assertEqual(actual_subscriptions_user_20, expected_subscriptions_user_20)

        # BEFORE deleting user 20 there should be 2 entries
        d = data_service._read_file(file_path)
        dict_keys_before_deleting_user_20 = d.keys()
        self.assertEqual(len(dict_keys_before_deleting_user_20), 2)

        # remove user with chat_id 20
        data_service.delete_user(20)

        # AFTER deleting user 20 there should be 1 entry
        d = data_service._read_file(file_path)
        dict_keys_after_deleting_user_20 = d.keys()
        self.assertEqual(len(dict_keys_after_deleting_user_20), 1)

        # check that user with chat_id 10 is unchanged in data base
        expected_favorites_user_10_after_deleting_user_20 = [
            {
                "postal_code": "22559",
                "district_id": "02000"
            },
            {
                "postal_code": "10827",
                "district_id": "11000"
            },
            {
                "postal_code": "60308",
                "district_id": "06412"
            }
        ]
        actual_favorites_user_10_after_deleting_user_20 = data_service.get_suggestions(10)
        self.assertEqual(actual_favorites_user_10_after_deleting_user_20,
                         expected_favorites_user_10_after_deleting_user_20)

        # check if data base still has correct subscriptions for user with chat_id 10
        expected_subscriptions_user_10_after_deleting_user_20 = {
            '22559':
                {
                    'district_id': '02000',
                    'flood': 'moderate'
                }
        }
        actual_subscriptions_user_10_after_deleting_user_20 = data_service.get_subscriptions(10)
        self.assertEqual(actual_subscriptions_user_10_after_deleting_user_20,
                         expected_subscriptions_user_10_after_deleting_user_20)

        # write data back to json from before the test
        data_service._write_file(file_path, entries_before_test)

    def test_get_subscription_district_id(self):
        saved_user_entries = data_service._read_file(file_path)

        # clear the json file
        data_service._write_file(file_path, {})
        # write 2 dummy entries into the json file
        entries = {"10": data_service.DEFAULT_DATA.copy(), "20": data_service.DEFAULT_DATA.copy()}
        data_service._write_file(file_path, entries)
        # add a subscription
        data_service.add_subscription(chat_id=10,
                                      postal_code="99099",
                                      district_id="16051",
                                      warning="weather",
                                      warning_level="minor")

        entries_after_adding_subscription = data_service._read_file(file_path)
        warnings_dict_postal_code_99099 = entries_after_adding_subscription["10"]["locations"]["99099"]

        expected_district_id_for_postal_code_99099 = "16051"
        actual_distr_id_postal_code_99099 = data_service.get_subscription_district_id(warnings_dict_postal_code_99099)

        self.assertEqual(actual_distr_id_postal_code_99099, expected_district_id_for_postal_code_99099)

        # write data back to json from before the test
        data_service._write_file(file_path, saved_user_entries)

    def test_set_default_level(self):

        saved_user_entries = data_service._read_file(file_path)

        # clear the json file
        data_service._write_file(file_path, {})
        # write 2 dummy entries into the json file
        entries = {"10": data_service.DEFAULT_DATA.copy(), "20": data_service.DEFAULT_DATA.copy()}
        data_service._write_file(file_path, entries)
        # add a subscription
        data_service.add_subscription(chat_id=10,
                                      postal_code="99099",
                                      district_id="16051",
                                      warning="flood",
                                      warning_level="minor")

        expected = enum_types.WarningSeverity.SEVERE

        data_service.set_default_level(10, expected)
        actual = data_service.get_default_level(10)
        self.assertEqual(actual, expected)

        expected = enum_types.WarningSeverity.MINOR
        data_service.set_default_level(11, expected)
        actual = data_service.get_default_level(11)
        self.assertEqual(actual, expected)

        # write data back to json from before the test
        data_service._write_file(file_path, saved_user_entries)

    def test_get_default_level(self):
        """
        Tests get_default_level in data_service.py\n
        Writes dummy values for a user with chat id 10 to data.json. Then changes his
        default_level from "Manual" which is the default severity for new users to "Severe".
        Checks whether that worked e.g. whether "Severe" gets returned. \n
        Then calls tested method again with a non existing user and check whether
        "Manual" gets returned as it ought to be when the user does not exist.
        """

        saved_user_entries = data_service._read_file(file_path)

        # clear the json file
        data_service._write_file(file_path, {})
        # write 2 dummy entries into the json file
        entries = {"10": data_service.DEFAULT_DATA.copy()}
        data_service._write_file(file_path, entries)
        # add a subscription

        expected_default_level = "Severe"

        entries = data_service._read_file(file_path)
        entries["10"]["default_level"] = expected_default_level
        data_service._write_file(file_path, entries)
        tested_default_level = data_service.get_default_level(10)

        self.assertEqual(tested_default_level.value, expected_default_level)

        # check for non existing user if default level is default ("manual")
        expected_default_level = "Manual"
        tested_default_level = data_service.get_default_level(20)

        self.assertEqual(tested_default_level.value, expected_default_level)

        # write data back to json from before the test
        data_service._write_file(file_path, saved_user_entries)

    def test_get_all_chat_ids(self):
        """ Tests get_all_chat_ids() in data_service.py\n
        Clears the data.json file and writes {} into it
        Loops 0-49 and fills a list acting as keys.
        Adds default values as values and then writes all those entries with the interface
         { i : default value }   where i is the index
        to the file.
        Finally checks whether tested method correctly returns a list with integers from 0-49.
        """

        saved_user_entries = data_service._read_file(file_path)

        # clear the json file
        data_service._write_file(file_path, {})
        # write 2 dummy entries into the json file

        some_chat_ids = []
        entries = {}

        for i in range(50):
            some_chat_ids.append(i)
            key = str(i)
            entries[key] = data_service.DEFAULT_DATA.copy()

        data_service._write_file(file_path, entries)

        tested_list_of_chat_ids = data_service.get_all_chat_ids()

        self.assertEqual(tested_list_of_chat_ids, some_chat_ids)

        # write data back to json from before the test
        data_service._write_file(file_path, saved_user_entries)

    def test_get_chat_ids_of_warned_users(self):
        """ Tests get_chat_ids_of_warned_users() in data_service.py. \n
        First creates 3 dummy entries. Expects all their chat ids in return from tested method, since
        default value of receive_warning is True.\n
        Then sets the receive_warnings value for 2 users to False, thus expecting that only the
        left out users chat id gets returned from tested method.
        """

        saved_user_entries = data_service._read_file(file_path)

        # clear the json file
        data_service._write_file(file_path, {})

        # write 3 dummy entries into the json file
        entries = {"10": data_service.DEFAULT_DATA.copy(),
                   "20": data_service.DEFAULT_DATA.copy(),
                   "30": data_service.DEFAULT_DATA.copy()}
        data_service._write_file(file_path, entries)
        # default value for "receive_warnings" key is True -> all three chat ids should be in returned list
        expected_list_with_three_default_users = [10, 20, 30]
        actual_list_with_three_default_users = data_service.get_chat_ids_of_warned_users()
        self.assertEqual(actual_list_with_three_default_users, expected_list_with_three_default_users)

        # change some receive_warnings for 2 users and check whether it worked
        entries['10']["receive_warnings"] = False
        entries["30"]["receive_warnings"] = False
        data_service._write_file(file_path, entries)
        expected_list_where_two_users_do_not_want_to_receive_warnings = [20]
        actual_list_where_two_users_do_not_want_to_receive_warnings = data_service.get_chat_ids_of_warned_users()

        self.assertEqual(actual_list_where_two_users_do_not_want_to_receive_warnings,
                         expected_list_where_two_users_do_not_want_to_receive_warnings)

        # write data back to json from before the test
        data_service._write_file(file_path, saved_user_entries)

    def test_add_warning_id_to_users_warnings_received_list(self):
        saved_received_warnings = data_service._read_file(warnings_already_received_path)

        # clear the json file
        data_service._write_file(warnings_already_received_path, {})

        entry = {
            "10": [
                "lhp.HOCHWASSERZENTRALEN.DE.BY",
                "lhp.HOCHWASSERZENTRALEN.DE.HE"
            ]
        }
        data_service._write_file(warnings_already_received_path, entry)

        # adding general warning for non existing user
        data_service.add_warning_id_to_users_warnings_received_list(20, "test_warning")
        file_after_adding_to_non_existing_user = data_service._read_file(warnings_already_received_path)
        expected = ['test_warning']
        actual = file_after_adding_to_non_existing_user["20"]
        self.assertEqual(expected, actual)

        # check for both users
        expected_complete_file = {
            "10": [
                "lhp.HOCHWASSERZENTRALEN.DE.BY",
                "lhp.HOCHWASSERZENTRALEN.DE.HE"
            ],
            "20": [
                "test_warning"
            ]
        }
        actual_file = data_service._read_file(warnings_already_received_path)
        self.assertEqual(expected_complete_file, actual_file)

        # write data back to json from before the test
        data_service._write_file(warnings_already_received_path, saved_received_warnings)

    def test_get_users_already_received_warning_ids_and_has_user_already_received_warning(self):
        saved_received_warnings = data_service._read_file(warnings_already_received_path)

        # clear the json file
        data_service._write_file(warnings_already_received_path, {})

        entry = {
            "10": [
                "lhp.HOCHWASSERZENTRALEN.DE.BY",
                "lhp.HOCHWASSERZENTRALEN.DE.HE"
            ]
        }
        data_service._write_file(warnings_already_received_path, entry)

        # adding general warning for non existing user
        actual = data_service.get_users_already_received_warning_ids(20)
        expected = []
        self.assertEqual(expected, actual)

        file_after_adding_user_10 = data_service._read_file(warnings_already_received_path)

        # check for both users
        expected_warning_ids = [
            "lhp.HOCHWASSERZENTRALEN.DE.BY",
            "lhp.HOCHWASSERZENTRALEN.DE.HE"
        ]
        actual_file = data_service.get_users_already_received_warning_ids(10)
        self.assertEqual(expected_warning_ids, actual_file)

        # tests for has_user_already_received_warning()
        should_be_in_user_10s_list = "lhp.HOCHWASSERZENTRALEN.DE.BY"
        actual_boolean = data_service.has_user_already_received_warning(10, should_be_in_user_10s_list)
        self.assertEqual(True, actual_boolean)

        should_not_be_in_user_10s_list = "nothing_to_see_here"
        actual_boolean = data_service.has_user_already_received_warning(10, should_not_be_in_user_10s_list)
        self.assertEqual(False, actual_boolean)

        # write data back to json from before the test
        data_service._write_file(warnings_already_received_path, saved_received_warnings)

    def test_active_warnings_getter_and_setter(self):
        saved_active_warnings = data_service._read_file(active_warnings_path)

        # clear the json file
        data_service._write_file(active_warnings_path, {})

        test_dict = {
            "test_key_1": "very important value",
            "key_to_rule_them_all": "epstein didn't kill himself"
        }
        data_service.set_active_warnings_dict(test_dict)
        actual_entries_after_setting_and_getting_test_dict = data_service.get_active_warnings_dict()

        self.assertEqual(test_dict, actual_entries_after_setting_and_getting_test_dict)

        # write data back to json from before the test
        data_service._write_file(active_warnings_path, saved_active_warnings)


if __name__ == '__main__':
    unittest.main()
