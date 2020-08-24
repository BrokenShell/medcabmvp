""" DS Build Week: MVP on Day 1
API View

by Robert Sharp
August 2020 """
from flask import Flask, jsonify
from app.controller import PredictionBot


__all__ = ('API',)
API = Flask(__name__)
API.control = PredictionBot()


@API.route('/')
@API.route('/id/')
@API.route('/name/')
@API.route('/random/')
def index():
    """ Returns a Random Strain """
    return jsonify(API.control.random())


@API.route('/<user_input>')
@API.route('/search/<user_input>')
def search(user_input: str):
    """ Arbitrary Search Route """
    return jsonify(API.control.search(user_input))


@API.route('/name/<user_input>')
def name_lookup(user_input: str):
    """ Arbitrary Search Route """
    return jsonify(API.control.name_lookup(user_input))


@API.route('/id/<user_input>')
def id_lookup(user_input: str):
    """ Arbitrary Search Route """
    return jsonify(API.control.id_lookup(user_input))


if __name__ == '__main__':
    API.run(debug=True)
