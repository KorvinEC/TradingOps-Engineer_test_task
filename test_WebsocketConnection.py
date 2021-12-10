import unittest
from WebsocketConnection import WebsocketConnection


class TestWebsocketConnection(unittest.TestCase):

    def test_run(self):
        obj = WebsocketConnection()
        self.assertRaises(ValueError, obj.run)

    def test_get_last_data(self):
        obj = WebsocketConnection()
        self.assertRaises(IndexError, obj.get_last_data)

    def test_get_rolling_average(self):
        obj = WebsocketConnection()
        self.assertRaises(ValueError, obj.get_rolling_average)

    def test_dump_log_data(self):
        obj = WebsocketConnection()
        self.assertRaises(ValueError, obj.dump_log_data)


if __name__ == '__main__':
    unittest.main()