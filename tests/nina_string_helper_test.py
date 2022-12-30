import importlib.util
import unittest

nina_string_helper = importlib.util.spec_from_file_location \
    ("nina_string_helper", "../source/nina_string_helper.py").loader.load_module()


class MyTestCase(unittest.TestCase):
    def test_expand_location_id_with_zeros(self):
        # test with a string length 3, so 9 zeros have to be appended
        input_value = "abc"
        should_be = "abc000000000"
        self.assertEqual(should_be, nina_string_helper.expand_location_id_with_zeros(input_value))

        # test with a string length 12, so nothing has to be appended
        input_value = "isAlreadyFul"
        should_be = input_value
        self.assertEqual(should_be, nina_string_helper.expand_location_id_with_zeros(input_value))

    def test_filter_html_tags(self):
        input_value = "<html><head>firstContent</head><body>-secondContent</body></html>"
        should_be = "firstContent-secondContent"

        self.assertEqual(should_be, nina_string_helper.filter_html_tags(input_value))

        input_value = "<html><head>firstC</head><body><a href=\"https://www.w3schools.com/\">visitW3!</a></body></html>"
        should_be = "firstContent: https:google.com"
        self.assertEqual(should_be, nina_string_helper.filter_html_tags(input_value))


if __name__ == '__main__':
    unittest.main()

