""" DS Build Week: MVP on Day 1
API View

by Robert Sharp
August 2020 """
from flask import Flask, jsonify, render_template, make_response, request
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


# @API.route('/index.html')
# def home_page():
#     return render_template('index.html')
#
#
# @API.route('/about.html')
# def about_page():
#     return render_template('about.html')
#
#
# @API.route('/contact.html')
# def contact_page():
#     return render_template('contact.html')
#
#
# @API.route('/search.html')
# def search_page():
#     return render_template('search.html')


@API.before_request
def before_request():
    """ CORS preflight, required for off-server access """

    def _build_cors_prelight_response():
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response

    if request.method == "OPTIONS":
        return _build_cors_prelight_response()


@API.after_request
def after_request(response):
    """ CORS headers, required for off-server access """
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == '__main__':
    # Local Testing Only
    API.run(debug=True)
