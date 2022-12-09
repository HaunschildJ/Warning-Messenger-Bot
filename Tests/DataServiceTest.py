import unittest
from Source import DataService
import Source


class MyTestCase(unittest.TestCase):
    def test_write_read(self):
        a = DataService.UserData(10)
        a.change_entry(DataService.Attributes.RECEIVE_WARNINGS, True)
        a.set_location("Darmstadt", DataService.WarnType.WEATHER, 5)
        a.set_location("Darmstadt", DataService.WarnType.WEATHER, 7)
        a.set_location("Hamburg", DataService.WarnType.WEATHER, 3)
        DataService.write_file(a)

        self.assertEqual(a.user_entry, DataService.read_user(10).user_entry)






if __name__ == '__main__':
    unittest.main()





