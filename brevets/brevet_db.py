from typing import Optional

import arrow
import acp_times
import requests
import os

import json

API_PATH = f'http://{os.environ["API_ADDR"]}:{os.environ["API_PORT"]}/api'


def store_brevet(start_time, length, distances, locations, app=None) -> str:
    start_arrow = arrow.get(start_time)
    data = {
        'start_time': start_arrow.format('YYYY-MM-DD HH:mm'),
        'length': length,
        'distances': [d for d in distances],
        'locations': [l for l in locations],
        'open_times': [acp_times.open_time(int(distance), length, start_arrow).format('YYYY-MM-DD HH:mm')
                       if distance else ""
                       for distance in distances],
        'close_times': [acp_times.close_time(int(distance), length, start_arrow).format('YYYY-MM-DD HH:mm')
                        if distance else ""
                        for distance in distances],
    }
    data = json.dumps(data)
    _id = requests.post(API_PATH + '/brevets', data=data)
    if app:
        app.logger.debug(f"api_path: {API_PATH + '/brevets'}")
        app.logger.debug(f"in_json: {data}")
        app.logger.debug(f"status_code: {_id.status_code}")
        app.logger.debug(f"reason: {_id.reason}")

    if _id.status_code != 200:
        return -1

    app.logger.debug(f"text: {_id.text}")
    return _id.text


def get_brevet(brevet_id: Optional[str] = None, app=None):
    app.logger.debug(f'get_brevet - making get req')

    if brevet_id is None:
        r = requests.get(API_PATH + f'/brevets')
        import time
        time.sleep(0.5)
        brevet_json = json.loads(r.content)
        app.logger.debug(f'get_brevet - brevet_json: {brevet_json}')
        brevet_json = json.loads(brevet_json['data'][-1])
    else:
        r = requests.get(API_PATH + f'/brevet/{brevet_id}')
        brevet_json = json.loads(r.content)

    app.logger.debug(f'get_brevet - json: {brevet_json}')

    # Take this json and transform it to front-end expectation
    start_ts = int(brevet_json['start_time']['$date'])
    result = {
        'start_time': arrow.get(start_ts).format('YYYY-MM-DDTHH:mm'),
        'length': brevet_json['length'],
        'distances': [cp['distance'] for cp in brevet_json['checkpoints']],
        'locations': [cp['location'] for cp in brevet_json['checkpoints']],
    }
    app.logger.debug(f'get_brevet - result: {result}')
    return result
