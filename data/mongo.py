from pymongo import MongoClient
from os import getenv
import pandas as pd


def make_db():
    db = MongoClient(
        f"mongodb+srv://{getenv('MONGODB_USER')}:{getenv('MONGODB_PASS')}"
        f"@{getenv('MONGODB_URI')}/test?retryWrites=true&w=majority"
    ).medcabin.strain_table

    df = pd.read_csv('cannabis.csv')
    data = df.to_dict(orient='records')
    for strain in data:
        strain['Effects'] = strain['Effects'].split(',')
        strain['Flavors'] = strain['Flavors'].split(',')
        strain['Nearest'] = [
            data[int(idx)]['Name'] for idx in strain['Nearest'].split(',')]
    db.insert_many(data)


if __name__ == '__main__':
    make_db()
