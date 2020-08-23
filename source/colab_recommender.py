import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances
import os
import pickle


class ColabRecommender:
    def __init__(self, datapath):
        self.path = os.path.join(datapath, 'u.data')
        self.user_similarity = None
        self.item_similarity = None
        self.data_matrix = None

    def load(self):
        r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']
        ratings = pd.read_csv(self.path, sep='\t', names=r_cols, encoding='latin-1')
        n_users = ratings.user_id.unique().shape[0]
        n_items = ratings.movie_id.unique().shape[0]

        self.data_matrix = np.zeros((n_users, n_items))
        for t in ratings.itertuples():
            # movie_id and user_id start from 1 so subtract 1. add later
            self.data_matrix[t[1] - 1, t[2] - 1] = t[3]

        self.user_similarity = pairwise_distances(self.data_matrix, metric='cosine')
        self.item_similarity = pairwise_distances(self.data_matrix.T, metric='cosine')
        file = os.path.join('./static/', 'save_colab.p')
        pickle.dump(self, open(file, "wb"))

    def create_similar(self, ratings, similarity, type='user'):
        pred = None
        if type == 'user':
            mean_user_rating = ratings.mean(axis=1)
            ratings_diff = (ratings - mean_user_rating[:, np.newaxis])
            pred = mean_user_rating[:, np.newaxis] + similarity.dot(ratings_diff) / np.array(
                [np.abs(similarity).sum(axis=1)]).T
        elif type == 'item':
            pred = ratings.dot(similarity) / np.array([np.abs(similarity).sum(axis=1)])
        return pred

    def get_recommendation(self, user_id, max_limit):
        user_prediction = self.create_similar(self.data_matrix, self.user_similarity, type='user')[int(user_id)]
        item_prediction = self.create_similar(self.data_matrix, self.item_similarity, type='item')[int(user_id)]

        # linearly combine ranks for each prediction
        recommendation_array = user_prediction + item_prediction
        recommendation_movies = []

        i = 1  # counter from index + 1 as movie ID starts from 1
        for x in recommendation_array:
            recommendation_movies.append((i, x))
            i = i + 1
        # sort based on rank not movie_id
        recommendation_movies.sort(key=lambda x: x[1], reverse=True)
        return recommendation_movies[:int(max_limit)]
