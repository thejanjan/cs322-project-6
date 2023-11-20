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
    'brevet_dist': 400,
    'controls': ['5', '267', '13', '', '', '', '', '', '', '',
                 '', '', '', '', '', '', '', '', '', ''],
    'locations': ['Texas', 'Soup', 'Milk', '', '', '', '', '', '', '',
                  '', '', '', '', '', '', '', '', '', 'Surprise!'],
}


def test_db_insert():
    brevet_db.store_brevet(**brevet_test_data)


def test_db_retrieve():
    assert brevet_db.get_brevet() == brevet_test_data
