import os
import secrets
import pickle
from flask import Flask, request, render_template
from source import recommender

application = Flask(__name__)


@application.route("/")
def index():
    # this is only for representation
    # never load data on production in this manner
    file = os.path.join('./static/', 'save.p')
    if not os.path.exists(file):
        path = os.path.join('./static/', 'movie_dataset.csv')
        recom = recommender.Recommender(path)
        recom.load()
    return render_template('index.html')


@application.route("/recommend", methods=['POST'])
def recommend():
    file = os.path.join('./static/', 'save.p')
    recom = pickle.load(open(file, 'rb'))
    movie = request.form["movie"]
    max = request.form["max"]
    output = recom.get_recommendation(movie, max)
    return render_template("recommend.html", value=output)


if __name__ == '__main__':
    application.secret_key = secrets.token_urlsafe(16)
    application.run(host='0.0.0.0', debug=True)
