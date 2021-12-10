import uuid
import asyncio
import websockets
import logging
import json
import datetime
import os
import matplotlib.pyplot as plt
import pandas as pd
import pickle

logger = logging.getLogger(__file__)


class WebsocketConnection:
    def __init__(self, path=None, log_data_list=None):
        self._running = False
        self._path = path
        self._uuid = uuid.uuid4()
        self._log_data_list = log_data_list if log_data_list else []
        self._event_loop = asyncio.new_event_loop()

    def run(self, log=False, timeout=10.0):
        if not self._path:
            raise ValueError('Path is required to run')
        self._running = True
        self._event_loop.run_until_complete(self._start_listen(log=log, timeout=timeout))

        return True

    async def _start_listen(self, log=False, timeout=10.0):
        if not self._path:
            raise ValueError('Path is required to run')

        logger.info(f'Starting listening {self}')

        try:
            async with websockets.connect(self._path) as websocket:
                self._websocket = websocket
                await self._log_data(log=log, timeout=timeout)
        except asyncio.exceptions.TimeoutError:
            logger.error(f'{self} timeout error. Probably wrong market or stream')
        finally:
            logger.info(f'Shutting down task {self}')

    async def _log_data(self, log=False, timeout=10.0):
        while self._running:
            recv = await asyncio.wait_for(self._websocket.recv(), timeout=timeout)
            result = json.loads(recv)
            if log:
                symbol = result["data"]["k"]["s"]
                time = datetime.timedelta(microseconds=result["data"]["E"])
                price = round(float(result["data"]["k"]["c"]), 2)
                logger.info(f'{symbol: <10} {str(time): <25} {price: >10}')
            self._log_data_list.append(
                result
            )

    def get_last_data(self):
        return self._log_data_list[-1]

    def get_rolling_average(self, window=5, plot=False) -> pd.DataFrame:
        if len(self._log_data_list) == 0:
            raise ValueError('Log data is empty')

        data = [(i['data']['E'], float(i['data']['k']['c'])) for i in self._log_data_list]

        df = pd.DataFrame(data=data, columns=['time', 'price'])

        df_rolling_average = []

        if isinstance(window, int):
            df_rolling_average.append(df.rolling(window).mean())
        elif isinstance(window, tuple or list):
            for win in window:
                df_rolling_average.append(df.rolling(win).mean())
        else:
            raise TypeError(
                f'Wrong window type: {type(window)}. Expected int, tuple or list.'
            )

        if plot:
            plt.plot(df['time'], df['price'])
            for roll_avg in df_rolling_average:
                plt.plot(df['time'], roll_avg['price'])
            plt.show()

        return df_rolling_average

    def stop(self):
        self._running = False
        logger.info(f'Waiting task {self} to stop')

    def is_closed(self):
        return not self._event_loop.is_running()

    def __repr__(self):
        return f'{self._path}, uuid: {self._uuid}'

    def dump_log_data(self, path=None, name=None):
        if len(self._log_data_list) == 0:
            raise ValueError('Log data is empty')

        save_path = os.path.join(path, name if name else f'{self._uuid}.pickle' )

        with open(save_path, 'wb') as file:
            pickle.dump(self._log_data_list, file)

    @staticmethod
    def load_log_data(path, name):
        with open(f'{os.path.join(path, name)}', 'rb') as f:
            data = pickle.load(f)
        return data
