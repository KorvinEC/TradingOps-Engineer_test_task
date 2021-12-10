import os
from WebsocketConnection import WebsocketConnection


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
    load_data()






