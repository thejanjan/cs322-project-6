from pymongo import MongoClient
import os


# Get mongo connection.
mongo_client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)
db = mongo_client.saves


def store_brevet(start_time, brevet_dist, controls, locations):
    db.brevets.insert_one({
        'start_time': start_time,
        'brevet_dist': brevet_dist,
        'controls': controls,
        'locations': locations
    })


def get_brevet():
    query = db.brevets.find().sort({'_id': -1}).limit(1).next()
    query.pop('_id')
    return query
