import unittest
import importlib.util

place_converter = importlib.util.spec_from_file_location("place_converter", "../source/place_converter.py")\
    .loader.load_module()


class MyTestCase(unittest.TestCase):
    def test_get_district_id(self):
        pass
    # TODO tests schreiben


if __name__ == '__main__':
    unittest.main()
