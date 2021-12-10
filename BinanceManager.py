import threading
from WebsocketConnection import WebsocketConnection
import logging
import time


logger = logging.getLogger(__file__)


class BinanceManager(threading.Thread):
    def __init__(self, markets, streams):
        self._site_path = 'wss://stream.binance.com:9443/stream?streams='
        self._threads = []
        threading.Thread.__init__(self)
        paths = []

        for market in set(markets):
            for stream in set(streams):
                paths.append(
                    f'{self._site_path}{market}@{stream}'
                )

        self._paths = tuple(paths)
        self._websockets = []
        self._init_websockets(paths)

    @property
    def websockets(self):
        return tuple(self._websockets)

    def _init_websockets(self, paths):
        for path in paths:
            self._websockets.append(
                WebsocketConnection(path)
            )

    def start_streams(self, log=False, connection_timeout=1.0, channel=None):
        if not channel:
            for websocket in self._websockets:
                thread = threading.Thread(target=websocket.run, args=(log, connection_timeout))
                self._threads.append(thread)
                thread.start()
        else:
            thread = threading.Thread(
                target=self._websockets[channel].run,
                args=(log, connection_timeout)
            )
            self._threads.append(thread)
            thread.start()

        return tuple(self._threads)

    def _websockets_closed(self):
        return [i.is_closed() for i in self._websockets]

    def stop(self):
        for websocket in self._websockets:
            websocket.stop()

        while 1:
            time.sleep(1)
            if all(self._websockets_closed()):
                return True
