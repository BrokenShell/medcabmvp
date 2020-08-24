""" DS Build Week: MVP on Day 1
Data Model

by Robert Sharp
August 2020 """
from pymongo import MongoClient
from os import getenv
import pandas as pd


__all__ = ('connect_db', 'read_csv')


def connect_db():
    """ MongoDB Table Connection """
    return MongoClient(
        f"mongodb+srv://{getenv('MONGODB_USER')}:{getenv('MONGODB_PASS')}"
        f"@{getenv('MONGODB_URI')}/test?retryWrites=true&w=majority"
    ).medcabin.strain_table


def read_csv(file_name):
    return pd.read_csv(file_name)


def make_db(file_name: str):
    """ Creates and Populates the Database """
    db = connect_db()
    data = read_csv(file_name).to_dict(orient='records')
    for strain in data:
        strain['Effects'] = strain['Effects'].split(',')
        strain['Flavors'] = strain['Flavors'].split(',')
        strain['Nearest'] = [
            data[int(idx)]['Name'] for idx in strain['Nearest'].split(',')
        ]
    db.insert_many(data)


if __name__ == '__main__':
    # make_db('app/data.csv')  # DO ONLY ONCE!
    print(next(connect_db().find({'Name': 'Wedding Cake'})))
