""" DS Build Week: MVP on Day 1
Controller Bot

by Robert Sharp
August 2020 """
from random import randrange
from pandas import DataFrame
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from spacy.lang.en import English
from app.model import DataModel


__all__ = ('PredictionBot',)


class PredictionBot:
    """ NLP Bot for Cannabis Suggestion App """

    class Tokens:
        nlp = English()

        @classmethod
        def tokenize(cls, document):
            doc = cls.nlp(document)
            return [
                token.lemma_.strip() for token in doc
                if not token.is_stop and not token.is_punct
            ]

    data = DataModel()
    db = data.connect_db()
    df = data.read_csv()
    flavors = df['Flavors'].str.replace(',', ' ')
    effects = df['Effects'].str.replace(',', ' ')
    name = df['Name']
    training = df['Description'] + ' ' + flavors + ' ' + effects + ' ' + name
    tfidf = TfidfVectorizer(
        tokenizer=Tokens.tokenize,
        stop_words='english',
        ngram_range=(1, 2),
        max_features=5000,
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
        return self.id_lookup(randrange(2155))

    def search(self, user_input: str) -> dict:
        vectors = self.tfidf.transform([user_input]).todense()
        predict = self.knn.kneighbors(vectors, return_distance=False)[0][0]
        return self.id_lookup(predict)


if __name__ == '__main__':
    bot = PredictionBot()
    print(bot.search("insomnia sweet"))
