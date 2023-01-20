import unittest
import importlib.util

place_converter = importlib.util.spec_from_file_location("place_converter", "../source/place_converter.py") \
    .loader.load_module()


class MyTestCase(unittest.TestCase):

    def test_fill_districts_dict(self):
        # method does not return anything
        self.assertEqual(None, place_converter._fill_districts_dict())

        # dictionary test
        input_value = "06434"
        should_be = "Hochtaunuskreis"
        self.assertEqual(should_be, place_converter._districts_dictionary[input_value])

    def test_fill_places_dict(self):
        # method does not return anything
        self.assertEqual(None, place_converter._fill_places_dict())

        # dictionary test
        input_value = "064120000000"
        should_be = "Frankfurt am Main, Stadt"
        self.assertEqual(should_be, place_converter._places_dictionary[input_value])

    def test_fill_postal_code_dict(self):
        # method does not return anything
        self.assertEqual(None, place_converter._fill_postal_code_dict())

        # dictionary test
        input_value = "61440"
        should_be = ["Oberursel (Taunus)", "06434"]
        self.assertEqual(should_be, place_converter._postal_code_dictionary[input_value])

    def test_get_exact_address_from_coordinates(self):
        # if district is not mentioned in address
        input_lat = 49.866888380007595
        input_lon = 8.637452871622893
        should_be = ("Darmstadt", "64295")
        self.assertEqual(should_be, place_converter._get_exact_address_from_coordinates(input_lat, input_lon))

        # if district is mentioned in address
        input_lat = 49.93753533797006
        input_lon = 8.518336312227188
        should_be = ("Groß-Gerau", "64521")
        self.assertEqual(should_be, place_converter._get_exact_address_from_coordinates(input_lat, input_lon))

    def test_get_suggestions_for_place_name(self):
        input_name = "Oberursel"
        input_limit = 11
        result_list = place_converter._get_suggestions_for_place_name(input_name, input_limit)
        should_be = "Oberursel (Taunus), Stadt"
        self.assertEqual(should_be, result_list[0]['place_name'])

    def test_get_place_dict_suggestions(self):
        input_name = "Oberursel"
        input_limit = 11
        result_list = place_converter._get_place_dict_suggestions(input_name, input_limit)
        should_be = "Oberursel (Taunus), Stadt"
        self.assertEqual(should_be, result_list[0]['place_name'])
        should_be = "06434"
        self.assertEqual(should_be, result_list[0]['district_id'])

    def test_get_suggestions_for_district_name(self):
        input_name = "Hochtaunuskreis"
        input_limit = 11
        result_list = place_converter._get_suggestions_for_district_name(input_name, input_limit)
        should_be = "Hochtaunuskreis"
        self.assertEqual(should_be, result_list[0]['district_name'])

    def test_get_district_dict_suggestions(self):
        input_name = "Hochtaunuskreis"
        input_limit = 11
        result_list = place_converter._get_district_dict_suggestions(input_name, input_limit)
        should_be = "Hochtaunuskreis"
        self.assertEqual(should_be, result_list[0]['district_name'])
        self.assertEqual(None, result_list[0]['place_name'])

    def test_get_place_and_district_dict_suggestions(self):
        # district
        input_name = "Hochtaunuskreis"
        input_limit = 11
        result_list = place_converter._get_place_and_district_dict_suggestions(input_name, input_limit)
        should_be = "Hochtaunuskreis"
        self.assertEqual(should_be, result_list[11]['district_name'])
        self.assertEqual(None, result_list[11]['place_name'])

        # place
        input_name = "Oberursel"
        input_limit = 11
        result_list = place_converter._get_place_and_district_dict_suggestions(input_name, input_limit)
        should_be = "Oberursel (Taunus), Stadt"
        self.assertEqual(should_be, result_list[0]['place_name'])
        should_be = "06434"
        self.assertEqual(should_be, result_list[0]['district_id'])

        # place with double dicts
        input_name = "Frankfurt"
        input_limit = 11
        result_list = place_converter._get_place_and_district_dict_suggestions(input_name, input_limit)
        should_be = "Frankfurt am Main, Stadt"
        self.assertEqual(should_be, result_list[0]['place_name'])
        should_be = "06412"
        self.assertEqual(should_be, result_list[0]['district_id'])

    def test_get_dicts_for_postal_code(self):
        # postal code not found
        input_value = "00"
        should_be = []
        self.assertEqual(should_be, place_converter._get_dicts_for_postal_code(input_value, 11))

        # valid postal code
        input_value = "61440"
        should_be = "Oberursel (Taunus), Stadt"
        result_list = place_converter._get_dicts_for_postal_code(input_value, 11)
        self.assertEqual(should_be, result_list[0]['place_name'])

    def test_get_name_for_id(self):
        # is a valid district id with 7 zeroes
        input_value = "064120000000"
        should_be = "Frankfurt am Main, Stadt"
        self.assertEqual(should_be, place_converter.get_name_for_id(input_value))

        # is a valid district id
        input_value = "06412"
        should_be = "Frankfurt am Main"
        self.assertEqual(should_be, place_converter.get_name_for_id(input_value))

        # is a district id with 7 zeroes but without place name
        input_value = "064340000000"
        should_be = "Hochtaunuskreis"
        self.assertEqual(should_be, place_converter.get_name_for_id(input_value))

        # is a valid place id
        input_value = "064340008008"
        should_be = "Oberursel (Taunus), Stadt"
        self.assertEqual(should_be, place_converter.get_name_for_id(input_value))

        input_value = "00000"
        self.assertEqual(None, place_converter.get_name_for_id(input_value))

        input_value = "000000000000"
        self.assertEqual(None, place_converter.get_name_for_id(input_value))

        # cannot be found / not even a number
        input_value = "no"
        self.assertEqual(None, place_converter.get_name_for_id(input_value))

    def test_get_dicts_for_exact_district_name(self):  # TODO
        # is a valid district without place name
        input_value = "Hochtaunuskreis"
        should_be = [{'place_name': None, 'place_id': '064340000000', 'district_name': 'Hochtaunuskreis',
                      'district_id': '06434'}]
        self.assertEqual(should_be, place_converter.get_dicts_for_exact_district_name(input_value))

        # is a valid district with a place name
        input_value = "Frankfurt am Main"
        should_be = [
            {'place_name': 'Frankfurt am Main, Stadt', 'place_id': '064120000000', 'district_name': 'Frankfurt am Main',
             'district_id': '06412'}]
        self.assertEqual(should_be, place_converter.get_dicts_for_exact_district_name(input_value))

        # cannot be found
        input_value = "no"
        self.assertEqual([], place_converter.get_dicts_for_exact_district_name(input_value))

    def test_get_dicts_for_exact_place_name(self):
        # matches
        input_value = "Oberursel (Taunus), Stadt"
        should_be = "06434"
        result_list = place_converter.get_dicts_for_exact_place_name(input_value)
        self.assertEqual(should_be, result_list[0]['district_id'])

        # no matches
        input_value = "no"
        should_be = []
        self.assertEqual(should_be, place_converter.get_dicts_for_exact_place_name(input_value))

    def test_get_dict_suggestions(self):
        # numeric string -> postal code search
        input_value = "61440"
        should_be = "Oberursel (Taunus), Stadt"
        result_list = place_converter.get_dict_suggestions(input_value, 11)
        self.assertEqual(should_be, result_list[0]['place_name'])

        # alphabetic string -> place/district search
        input_name = "Oberursel"
        input_limit = 11
        result_list = place_converter.get_dict_suggestions(input_name, input_limit)
        should_be = "Oberursel (Taunus), Stadt"
        self.assertEqual(should_be, result_list[0]['place_name'])
        should_be = "06434"
        self.assertEqual(should_be, result_list[0]['district_id'])

    def test_get_place_name_from_dict(self):
        # place name is not None
        input_value = {'district_name': 'district', 'district_id': '12345', 'place_name': 'place',
                       'place_id': '123450000000'}
        should_be = "place"
        self.assertEqual(should_be, place_converter.get_place_name_from_dict(input_value))

        # place name is None
        input_value = {'district_name': 'district', 'district_id': '12345', 'place_name': None,
                       'place_id': '123450000000'}
        self.assertEqual(None, place_converter.get_place_name_from_dict(input_value))

    def test_get_place_id_from_dict(self):
        input_value = {'district_name': 'district', 'district_id': '12345', 'place_name': 'place',
                       'place_id': '123450000000'}
        should_be = "123450000000"
        self.assertEqual(should_be, place_converter.get_place_id_from_dict(input_value))

    def test_get_district_name_from_dict(self):
        input_value = {'district_name': 'district', 'district_id': '12345', 'place_name': 'place',
                       'place_id': '123450000000'}
        should_be = "district"
        self.assertEqual(should_be, place_converter.get_district_name_from_dict(input_value))

    def test_get_district_id_from_dict(self):
        input_value = {'district_name': 'district', 'district_id': '12345', 'place_name': 'place',
                       'place_id': '123450000000'}
        should_be = "12345"
        self.assertEqual(should_be, place_converter.get_district_id_from_dict(input_value))

    def test_get_suggestion_dicts_from_coordinates(self):
        input_lat = 49.866888380007595
        input_lon = 8.637452871622893
        input_limit = 11
        result_list = place_converter.get_suggestion_dicts_from_coordinates(input_lat, input_lon, input_limit)
        should_be = "Darmstadt, Wissenschaftsstadt"
        self.assertEqual(should_be, result_list[0]['place_name'])


if __name__ == '__main__':
    unittest.main()
