import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os


class Recommender:
    def __init__(self, datapath):
        self.path = datapath
        self.df = None
        self.cosine_sim = None

    def get_movie_from_index(self, index):
        return self.df[self.df.index == index]["title"].values[0]

    def get_index_from_movie(self, title):
        return self.df[self.df.title == title]["index"].values[0]

    def load(self):
        self.df = pd.read_csv(self.path)
        features = ['keywords', 'cast', 'genres', 'director']
        for feature in features:
            self.df[feature] = self.df[feature].fillna('')
            self.df["combined_features"] = self.df.apply(self.combine_features, axis=1)
        cv = CountVectorizer()
        count_matrix = cv.fit_transform(self.df["combined_features"])
        self.cosine_sim = cosine_similarity(count_matrix)
        file = os.path.join('./static/', 'save.p')
        pickle.dump(self, open(file, "wb"))

    def combine_features(self, row):
        try:
            return row['keywords'] + " " + row['cast'] + " " + row["genres"] + " " + row["director"]
        except:
            print("Error: ", row)

    def get_recommendation(self, movie_name, max_movies):
        movie_index = self.get_index_from_movie(movie_name)
        similar_movies = list(enumerate(self.cosine_sim[movie_index]))
        sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[1:]
        i = 0
        output = []
        for element in sorted_similar_movies:
            output.append(self.get_movie_from_index(element[0]))
            i = i + 1
            if i > int(max_movies):
                break
        return output
