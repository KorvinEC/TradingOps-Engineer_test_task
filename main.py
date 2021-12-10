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
    try:
        manager.start_streams(log=True)
        time.sleep(180)
        raise KeyboardInterrupt
    except KeyboardInterrupt:
        logging.info(f'KeyboardInterrupt raised. Exiting program and saving data.')
        path = 'Pickled_log_data'

        save_dir = os.path.abspath(path)

        if not os.path.exists(save_dir):
            os.mkdir(path)

        manager.stop()

        for websocket in manager.websockets:
            logging.info(f'Pickling {websocket} in {save_dir}')
            websocket.dump_log_data(path=save_dir)


def load_data():
    folder = 'Pickled_log_data'
    folder_path = os.path.abspath(folder)
    folder_files = os.listdir(folder_path)

    websockets_log_data = []

    for name in folder_files:
        websockets_log_data.append(
            WebsocketConnection.load_log_data(folder_path, name)
        )

    websockets_list = []

    for websocket_log_data in websockets_log_data:
        websockets_list.append(
            WebsocketConnection(log_data_list=websocket_log_data)
        )

    for websocket in websockets_list:
        websocket.get_rolling_average(plot=True)


if __name__ == '__main__':
    create_data()
    # load_data()






