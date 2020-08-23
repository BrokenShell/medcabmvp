""" DS Build Week: MVP on Day 1
by Robert Sharp """
from flask import Flask, jsonify
from app.model import PredictionBot

__all__ = ('API',)
API = Flask(__name__)
API.predict = PredictionBot()


@API.route('/')
def index():
    """ Default Route """
    return jsonify("App Online!")


@API.route('/search/')
@API.route('/search/<user_input>')
def search(user_input: str = 'cannabis'):
    """ Arbitrary Search Route """
    return jsonify(API.predict(user_input))


if __name__ == '__main__':
    API.run(debug=True)
