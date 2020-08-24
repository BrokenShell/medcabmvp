""" DS Build Week: MVP on Day 1
Controller Bot

by Robert Sharp
August 2020 """
from Fortuna import random_below
from pandas import DataFrame
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from app.model import connect_db, read_csv


__all__ = ('PredictionBot',)


class PredictionBot:
    """ NLP Bot for Cannabis Suggestion App """
    db = connect_db()
    df = read_csv('app/data.csv')
    flavors = df['Flavors'].str.replace(',', ' ')
    effects = df['Effects'].str.replace(',', ' ')
    name = df['Name']
    training = df['Description'] + ' ' + flavors + ' ' + effects + ' ' + name
    tfidf = TfidfVectorizer(
        stop_words='english',
        ngram_range=(1, 2),
        max_features=8000,
    )
    knn = NearestNeighbors(
        n_neighbors=1,
        n_jobs=-1,
    ).fit(DataFrame(tfidf.fit_transform(training).todense()))

    def id_lookup(self, _id) -> dict:
        return next(self.db.find({'_id': int(_id)}))

    def name_lookup(self, name: str) -> dict:
        return next(self.db.find({'Name': name.title()}))

    def random(self) -> dict:
        return self.id_lookup(random_below(2155))

    def search(self, user_input: str) -> dict:
        vectors = self.tfidf.transform([user_input]).todense()
        predict = self.knn.kneighbors(vectors, return_distance=False)[0][0]
        return self.id_lookup(predict)


if __name__ == '__main__':
    prediction = PredictionBot()
    print(prediction.name_lookup(input("Name Your Poison: ")))
