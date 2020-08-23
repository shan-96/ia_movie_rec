import os
import secrets
import pickle
from flask import Flask, request, render_template
from source import simple_recommender, colab_recommender

application = Flask(__name__)


@application.route("/")
def index():
    # this is only for representation
    # never load data on production in this manner
    file = os.path.join('./static/', 'save_simple.p')
    if not os.path.exists(file):
        path = os.path.join('./static/', 'movie_dataset.csv')
        recom1 = simple_recommender.SimpleRecommender(path)
        recom1.load()
    file = os.path.join('./static', 'save_colab.p')
    if not os.path.exists(file):
        path = os.path.join('./static','ml-100k')
        recom2 = colab_recommender.ColabRecommender(path)
        recom2.load()
    return render_template('index.html')


@application.route("/recommend", methods=['POST'])
def recommend():
    output = None
    if request.form['group1'] == 'simple':
        file = os.path.join('./static/', 'save_simple.p')
        recom = pickle.load(open(file, 'rb'))
        movie = request.form["movie"]
        max = request.form["max"]
        output = recom.get_recommendation(movie, max)
    if request.form['group1'] == 'colab':
        file = os.path.join('./static/', 'save_colab.p')
        recom = pickle.load(open(file, 'rb'))
        max = request.form["max"]
        uid = request.form["uid"]
        output = recom.get_recommendation(uid, max)
    return render_template("recommend.html", value=output)


if __name__ == '__main__':
    application.secret_key = secrets.token_urlsafe(16)
    application.run(host='0.0.0.0', debug=True)
