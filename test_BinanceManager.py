import unittest
from BinanceManager import BinanceManager
from WebsocketConnection import WebsocketConnection


class TestWebsocketConnection(unittest.TestCase):
    def test_run(self):
        self.assertRaises(TypeError, BinanceManager)
        markets = ['']
        streams = ['']
        obj = BinanceManager(markets, streams)
        self.assertIsInstance(obj.websockets, tuple)

    def test_start_streams(self):
        markets = ['']
        streams = ['']
        obj = BinanceManager(markets, streams)

        self.assertIsInstance(obj.websockets, tuple)


if __name__ == '__main__':
    unittest.main()