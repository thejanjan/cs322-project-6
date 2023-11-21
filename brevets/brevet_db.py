from typing import Optional

import arrow
import acp_times
import requests
import os

API_PATH = f'http://localhost:{os.environ["API_PORT"]}/api'


def store_brevet(start_time, length, distances, locations) -> int:
    start_arrow = arrow.get(start_time)
    r = requests.post(API_PATH + '/brevets', data={
        'start_time': start_time,
        'length': length,
        'distances': [d for d in distances if d],
        'locations': [l for l in locations if l],
        'open_times': [acp_times.open_time(int(distance), length, start_arrow).format('YYYY-MM-DDTHH:mm')
                       for distance in distances if distance],
        'close_times': [acp_times.close_time(int(distance), length, start_arrow).format('YYYY-MM-DDTHH:mm')
                        for distance in distances if distance],
    })
    return r.json()['brevet_id']


def get_brevet(brevet_id: Optional[int] = None):
    if brevet_id is None:
        r = requests.get(API_PATH + f'/brevets')
        brevet_json = r.json()['brevets'][-1]
    else:
        r = requests.get(API_PATH + f'/brevet/{brevet_id}')
        brevet_json = r.json()

    # Take this json and transform it to front-end expectation
    return {
        'start_time': brevet_json['start_time'],
        'length': brevet_json['length'],
        'distances': [cp['distance'] for cp in brevet_json['checkpoints']],
        'locations': [cp['location'] for cp in brevet_json['checkpoints']],
    }
