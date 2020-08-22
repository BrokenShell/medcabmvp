from flask import Flask, jsonify
from app.model import PredictionBot


API = Flask(__name__)


@API.route('/')
def index():
    return jsonify("App Online!")


@API.route('/search/<user_input>')
def search(user_input):
    bot = PredictionBot()
    return jsonify(bot.predict(user_input))


if __name__ == '__main__':
    API.run(debug=True)
