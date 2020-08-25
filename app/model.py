""" DS Build Week: MVP on Day 1
Data Model

by Robert Sharp
August 2020 """
from pymongo import MongoClient
from os import getenv
import pandas as pd


__all__ = ('DataModel',)


class DataModel:

    def connect_db(self):
        """ MongoDB Table Connection """
        return MongoClient(
            f"mongodb+srv://{getenv('MONGODB_USER')}:{getenv('MONGODB_PASS')}"
            f"@{getenv('MONGODB_URI')}/test?retryWrites=true&w=majority"
        ).medcabin.strain_table

    def read_csv(self):
        return pd.read_csv('app/data.csv')

    def _make_db(self):
        """ Creates and Populates the Database """
        db = self.connect_db()
        data = self.read_csv().to_dict(orient='records')
        for strain in data:
            strain['Effects'] = strain['Effects'].split(',')
            strain['Flavors'] = strain['Flavors'].split(',')
            strain['Nearest'] = [
                data[int(idx)]['Name'] for idx in strain['Nearest'].split(',')
            ]
        db.insert_many(data)


if __name__ == '__main__':
    data_model = DataModel()
    # data_model._make_db()  # DO ONLY ONCE!
    print(next(data_model.connect_db().find({'Name': 'Wedding Cake'})))
