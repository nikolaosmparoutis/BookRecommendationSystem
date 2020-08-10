import pandas as pd
from sklearn.neighbors import NearestNeighbors
from model.BaseModel import BaseModel
from configurations.configs_model import CFG
# the line below will activate automatically when the metric comes from the configurations
from scipy.spatial.distance import correlation, cosine

import data.DataAnalysis


class Model(BaseModel):

    def __init__(self, config):
        super().__init__(config)
        self.dataset = pd.DataFrame
        self.algorithm = None
        self.k_num_neighbors = None
        self.metric = None

    def load_data(self, dataset_):
        self.dataset = dataset_
        print("pivoted ratings (with user who rated more than 50 books). NaN replaced by 0")
        print(self.dataset)
        return self

    def _set_training_parameters(self):
        self.algorithm = self.config.train.algorithm
        self.k_num_neighbors = self.config.train.k_num_neighbors
        self.metric = self.config.train.metric
        # print(self.metric[0], self.metric[1])

    def build(self, ratings, metric):
        pass

    def _findksimilarusers(self, user_id, metric):

        model_knn = NearestNeighbors(metric=metric, algorithm=self.algorithm)
        print("model_knn: ", model_knn)
        model_knn.fit(self.dataset)
        distances, indices = model_knn.kneighbors(self.dataset.iloc[user_id - 1, :].values.reshape(1, -1),
                                                  n_neighbors=self.k_num_neighbors + 1)
        similarities = 1 - distances.flatten()
        print('The {0} most similar users for User {1}:\n'.format(self.k_num_neighbors, user_id))
        for i in range(0, len(indices.flatten())):
            if indices.flatten()[i] + 1 == user_id:
                continue
            else:
                print('{0}: User {1}, with similarity of {2}'
                      .format(i, indices.flatten()[i] + 1, similarities.flatten()[i]))

        return similarities, indices

    def _predict_userbased(self, user_id, item_id, metric_sel):
        import numpy as np
        prediction = 0
        similarities, indices = self._findksimilarusers(user_id, metric_sel)  # similar users based on cosine similarity
        print("HERE 1")

        mean_rating = self.dataset.loc[user_id-1, ].mean()  # to adjust for zero based indexing
        print("HERE 2")
        sum_wt = np.sum(similarities) - 1
        product = 1
        wtd_sum = 0

        for i in range(0, len(indices.flatten())):
            if indices.flatten()[i] + 1 == user_id:
                continue
            else:
                ratings_diff = self.dataset.iloc[indices.flatten()[i], item_id - 1] - np.mean(
                    self.dataset.iloc[indices.flatten()[i], :])
                product = ratings_diff * (similarities[i])
                wtd_sum = wtd_sum + product

        prediction = int(round(mean_rating + (wtd_sum / sum_wt)))
        print('\n Predicted rating for user {0} -> item {1}: {2}'
              .format(user_id, item_id, prediction))
        return prediction

    def _recommendItem(self, user_id, item_id, approach):
        self._set_training_parameters()
        if user_id < 1 or user_id > 60 or type(user_id) is not int:
            print('Userid does not exist. Enter numbers from 1-6')
        else:

            if approach == 'User_based_CF(cosine)':
                prediction = self._predict_userbased(user_id, item_id, str(self.metric[0]))
            elif approach == 'User_based_CF(correlation)':
                prediction = self._predict_userbased(user_id, item_id, str(self.metric[1]))

            if self.dataset[item_id - 1][user_id - 1] != 0:
                print('Item already rated')
                # predictions with smaller rating than 6 do not have value for the user
            else:
                if prediction >= 6:
                    print('\n Item recommended')
                else:
                    print('Item not recommended')

    def train(self, user_id, item_id, approach):
        self._recommendItem(user_id, item_id, approach)

    def evaluate(self):
        pass

def main():
    ratings = data.DataAnalysis.main()
    md = Model(CFG)
    user_id = 3
    item_id = 5
    approach = "User_based_CF(cosine)"
    md.load_data(ratings)
    md.train(user_id, item_id, approach)


if __name__ == '__main__':
    main()
