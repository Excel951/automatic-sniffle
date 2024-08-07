import logging

import requests
import json

URL = 'http://192.168.18.17:3021/datalogger/create/'
FILE = '../read_and_delete/saved_data/20240806173943_XN1000_9.json'


def read_data(file: str):
    with open(file, 'r') as f:
        data = json.load(f)
    return data

def send_data(url: str, data: json):
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        logging.info(f"Data sent to {url} with response {response.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error sending data to {url}")
        logging.error(e)
    except Exception as e:
        logging.error(f"Unknown error")
        logging.error(e)

if __name__ == '__main__':
    data = read_data(FILE)

    file_handler = logging.FileHandler(filename='app.log')
    stdout_handler = logging.StreamHandler()
    logging.basicConfig(
        handlers=[
            file_handler,
            stdout_handler
        ],
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    send_data(URL, data)
