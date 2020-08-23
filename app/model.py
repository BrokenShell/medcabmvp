""" DS Build Week: MVP on Day 1
by Robert Sharp

Input -> TF-IDF -> KNN -> Output
"""
import pandas as pd
from os import getenv
from pymongo import MongoClient
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer

__all__ = ('PredictionBot',)


class PredictionBot:
    """ NLP Bot for Cannabis Suggestion App """
    db = MongoClient(
        f"mongodb+srv://{getenv('MONGODB_USER')}:{getenv('MONGODB_PASS')}"
        f"@{getenv('MONGODB_URI')}/test?retryWrites=true&w=majority"
    ).medcabin.strain_table
    df = pd.read_csv('data/cannabis.csv')
    training = df['Description'] + ' ' + df['Flavors'] + ' ' + df['Effects']
    tfidf = TfidfVectorizer(
        stop_words='english',
        ngram_range=(1, 3),
        max_features=6000,
    )
    tokens = tfidf.fit_transform(training)
    knn = NearestNeighbors(
        n_neighbors=1,
        n_jobs=-1,
    ).fit(pd.DataFrame(tokens.todense()))

    def __call__(self, user_input: str) -> dict:
        vectors = self.tfidf.transform([user_input]).todense()
        predict = self.knn.kneighbors(vectors, return_distance=False)
        return next(self.db.find({'_id': int(predict[0][0])}))
