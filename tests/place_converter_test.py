import unittest
import importlib.util

place_converter = importlib.util.spec_from_file_location("place_converter", "../source/place_converter.py") \
    .loader.load_module()


class MyTestCase(unittest.TestCase):
    def test_get_district_id(self):
        # is a valid place
        input_value = "Frankfurt am Main, Stadt"
        should_be = "06412"
        self.assertEqual(should_be, place_converter.get_district_id(input_value))

        # is a valid district
        input_value = "Hochtaunuskreis"
        should_be = "06434"
        self.assertEqual(should_be, place_converter.get_district_id(input_value))

        # cannot be found
        input_value = "no"
        self.assertRaises(ValueError, place_converter.get_district_id, input_value)

    def test_get_district_id_for_district_name(self):
        # is a valid district
        input_value = "Hochtaunuskreis"
        should_be = "06434"
        self.assertEqual(should_be, place_converter.get_district_id_for_district_name(input_value))

        # cannot be found
        input_value = "no"
        self.assertEqual(None, place_converter.get_district_id_for_district_name(input_value))

    def test_get_district_id_for_place_name(self):
        # is a valid place
        input_value = "Frankfurt am Main, Stadt"
        should_be = "06412"
        self.assertEqual(should_be, place_converter.get_district_id_for_place_name(input_value))

        # cannot be found
        input_value = "no"
        self.assertEqual(None, place_converter.get_district_id_for_place_name(input_value))

    def test_get_place_for_postal_code(self):
        # is a valid postal code
        input_value = "61440"
        should_be = "Oberursel (Taunus)"
        self.assertEqual(should_be, place_converter.get_place_for_postal_code(input_value))

        # cannot be found
        input_value = "no"
        self.assertRaises(ValueError, place_converter.get_place_for_postal_code, input_value)

    def test_get_district_for_postal_code(self):
        # is a valid postal code
        input_value = "61440"
        should_be = "Hochtaunuskreis"
        self.assertEqual(should_be, place_converter.get_district_for_postal_code(input_value))

        # cannot be found
        input_value = "no"
        self.assertEqual(None, place_converter.get_district_for_postal_code(input_value))

    def test_get_similar_names(self):
        pass

    def test_get_similar_districts(self):
        pass

    def test_get_similar_places(self):
        pass

    def test_get_district_name_for_place(self):
        # is a valid place name
        input_value = "Frankfurt am Main, Stadt"
        should_be = "Frankfurt am Main"
        self.assertEqual(should_be, place_converter.get_district_name_for_place(input_value))

        # cannot be found
        input_value = "no"
        self.assertRaises(ValueError, place_converter.get_district_name_for_place, input_value)

    def test_get_place_id_for_place_name(self):
        # is a valid place name
        input_value = "Frankfurt am Main, Stadt"
        should_be = "064120000000"
        self.assertEqual(should_be, place_converter.get_place_id_for_place_name(input_value))

        # cannot be found
        input_value = "no"
        self.assertRaises(ValueError, place_converter.get_place_id_for_place_name, input_value)

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

    def test_get_place_name(self):
        # is a valid place id
        input_value = "064120000000"
        should_be = "Frankfurt am Main, Stadt"
        self.assertEqual(should_be, place_converter.get_place_name(input_value))

        # cannot be found
        input_value = "no"
        self.assertEqual(None, place_converter.get_place_name(input_value))

    def test_get_district_name(self):
        # is a valid district id
        input_value = "06412"
        should_be = "Frankfurt am Main"
        self.assertEqual(should_be, place_converter.get_district_name(input_value))

        # cannot be found
        input_value = "no"
        self.assertEqual(None, place_converter.get_district_name(input_value))


if __name__ == '__main__':
    unittest.main()
