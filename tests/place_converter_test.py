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

    def test_get_place_for_postal_code(self):
        # is a valid postal code
        input_value = "61440"
        should_be = "Oberursel (Taunus)", "06434"
        self.assertEqual(should_be, place_converter.get_place_for_postal_code(input_value))

        # cannot be found
        input_value = "no"
        self.assertRaises(ValueError, place_converter.get_place_for_postal_code, input_value)

    def test_get_district_name_for_postal_code(self):
        # is a valid postal code
        input_value = "61440"
        should_be = "Hochtaunuskreis"
        self.assertEqual(should_be, place_converter.get_district_name_for_postal_code(input_value))

        # cannot be found
        input_value = "no"
        self.assertEqual(None, place_converter.get_district_name_for_postal_code(input_value))

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
        pass

    def test_get_name_for_id(self):
        # is a valid place id
        input_value = "064120000000"
        should_be = "Frankfurt am Main, Stadt"
        self.assertEqual(should_be, place_converter.get_name_for_id(input_value))

        # is a valid district id
        input_value = "06412"
        should_be = "Frankfurt am Main"
        self.assertEqual(should_be, place_converter.get_name_for_id(input_value))

        # cannot be found
        input_value = "no"
        self.assertRaises(ValueError, place_converter.get_name_for_id, input_value)

    def test_get_suggestions_for_place_name(self):
        pass

    def test_get_place_dict_suggestions(self):
        pass

    def test_get_suggestions_for_district_name(self):
        pass

    def test_get_district_dict_suggestions(self):
        pass

    def test_get_dict_suggestions(self):
        pass

    def test_get_dicts_for_postal_code(self):
        pass


if __name__ == '__main__':
    unittest.main()
