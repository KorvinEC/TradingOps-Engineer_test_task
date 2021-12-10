import os
import sys
import logging
from BinanceManager import BinanceManager
from WebsocketConnection import WebsocketConnection

import time

from logging import StreamHandler, Formatter

log_format = '[%(asctime)s: %(levelname)s] %(message)s'

logging.basicConfig(
    filename='websocket_info.log',
    level=logging.INFO,
    format=log_format
)

handler = StreamHandler(stream=sys.stdout)
handler.setFormatter(Formatter(fmt=log_format))
logging.getLogger().addHandler(handler)


def create_data():
    markets = ['btcusdt', 'ethusdt', 'bnbbtc']
    streams = ['kline_1m']

    manager = BinanceManager(markets, streams)

    manager.start_streams(log=True, connection_timeout=60)
    time.sleep(180)

    path = 'Pickled_log_data'

    save_dir = os.path.abspath(path)

    if not os.path.exists(save_dir):
        os.mkdir(path)

    manager.stop()

    for websocket in manager.websockets:
        logging.info(f'Pickling {websocket} in {save_dir}')
        websocket.dump_log_data(path=save_dir)


if __name__ == '__main__':
    create_data()







