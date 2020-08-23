""" DS Build Week: MVP on Day 1
by Robert Sharp

Input -> TF-IDF -> KNN -> Output
"""
import spacy
import pandas as pd
from os import getenv
from pymongo import MongoClient
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer

__all__ = ('PredictionBot',)
nlp = spacy.load('en_core_web_sm')


def tokenize(document: str):
    return [
        token.lemma_ for token in nlp(document)
        if not token.is_stop and not token.is_punct
    ]


class PredictionBot:
    """ NLP Bot for Cannabis Suggestion App """
    db = MongoClient(
        f"mongodb+srv://{getenv('MONGODB_USER')}:{getenv('MONGODB_PASS')}"
        f"@{getenv('MONGODB_URI')}/test?retryWrites=true&w=majority"
    ).medcabin.strain_table
    df = pd.read_csv('data/cannabis.csv')
    training = df['Description'] + ' ' + df['Flavors'] + ' ' + df['Effects']
    tfidf = TfidfVectorizer(
        tokenizer=tokenize,
        stop_words='english',
        ngram_range=(1, 2),
        max_features=8000,
    )
    knn = NearestNeighbors(
        n_neighbors=1,
        n_jobs=-1,
    ).fit(pd.DataFrame(tfidf.fit_transform(training).todense()))

    def __call__(self, user_input: str) -> dict:
        vectors = self.tfidf.transform([user_input]).todense()
        predict = self.knn.kneighbors(vectors, return_distance=False)[0][0]
        return next(self.db.find({'_id': int(predict)}))
