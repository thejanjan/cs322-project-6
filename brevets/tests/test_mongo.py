"""
Nose tests for mongodb
"""

from pymongo import MongoClient

import nose    # Testing framework
import logging
import os

import brevet_db

logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)


mongo_client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)
db = mongo_client.mydb


brevet_test_data = {
    'start_time': "2023-08-09T18:16",
    'length': 400,
    'distances': ['5', '267', '13', '', '', '', '', '', '', '',
                 '', '', '', '', '', '', '', '', '', ''],
    'locations': ['Texas', 'Soup', 'Milk', '', '', '', '', '', '', '',
                  '', '', '', '', '', '', '', '', '', 'Surprise!'],
}


brevet_id = None


def test_db_insert():
    global brevet_id
    assert brevet_db.store_brevet(**brevet_test_data)


def test_db_retrieve():
    assert brevet_id is not None
    assert brevet_db.get_brevet(brevet_id) == brevet_test_data
