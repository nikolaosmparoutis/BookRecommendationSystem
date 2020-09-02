import pandas as pd
from sklearn.neighbors import NearestNeighbors
from model.BaseModel import BaseModel
from configurations.configs_model import CFG
import data.DataAnalysis
from logging_utils.LoggerCls import LoggerCls
import os


class Model(BaseModel):
    dir_path = os.path.dirname(os.path.realpath(__file__))  # get the canonical files's path then get the name
    formatter = '%(name)s - %(levelname)s - Line No. : %(lineno)d - %(message)s'
    logModelFile = LoggerCls("log_to_file", "ModelToFile", dir_path+"/ModelLogger.log", "w", formatter, "INFO")
    logModelStream = LoggerCls("log_to_stdout", "ModelToStream", None, "w", formatter, "INFO")

    def __init__(self, config):
        super().__init__(config)
        self.dataset = pd.DataFrame
        self.algorithm = None
        self.k_num_neighbors = None
        self.metric = None

    def load_data(self, dataset_):
        self.dataset = dataset_
        Model.logModelFile.info("pivoted ratings with users who rated >= 150 books. NaN replaced by 0. Dimensions: {}:"
                         .format(self.dataset.shape))
        Model.logModelFile.info("dataset head: \n {}".format(self.dataset.head()))
        return self

    def _set_training_parameters(self):
        self.algorithm = self.config.train.algorithm
        self.radius = self.config.train.radius
        self.k_num_neighbors = self.config.train.k_num_neighbors
        self.metric = self.config.train.metric

    def build(self, ratings, metric):
        pass

    def _findksimilarusers(self, user_id, metric):
        model_knn = NearestNeighbors(algorithm=self.algorithm, radius=self.radius, metric=metric)
        model_knn.fit(self.dataset)
        distances, indices = model_knn.kneighbors(self.dataset.iloc[user_id - 1, :].values.reshape(1, -1),
                                                  n_neighbors=self.k_num_neighbors + 1)
        similarities = 1 - distances.flatten()
        for i in range(0, len(indices.flatten())):
            if indices.flatten()[i] + 1 == user_id:
                continue
            else:
                Model.logModelFile.info('{0}: User {1}, with similarity of {2}'
                                        .format(i, indices.flatten()[i] + 1, similarities.flatten()[i]))

        return similarities, indices

    def _predict_userbased(self, user_id, item_id, metric_sel):
        import numpy as np
        similarities, indices = self._findksimilarusers(user_id, metric_sel)  # similar users based on cosine similarity
        mean_rating = self.dataset.iloc[user_id, ].mean()  # to adjust for zero based indexing
        sum_wt = np.sum(similarities) - 1
        wtd_sum = 0

        for i in range(0, len(indices.flatten())):
            if indices.flatten()[i] + 1 == user_id:
                continue
            else:
                ratings_diff = self.dataset.iloc[indices.flatten()[i], item_id-1] - np.mean(
                    self.dataset.iloc[indices.flatten()[i], :])
                product = ratings_diff * (similarities[i])
                wtd_sum = wtd_sum + product

        prediction = int(round(mean_rating + (wtd_sum / sum_wt)))
        if prediction >= 5:
            Model.logModelStream.info('Predicted rating >= 5 for user {0} -> item {1}: {2}'
                                      .format(user_id, item_id, prediction))
        return prediction

    def _recommendItem(self, user_id, item_id, approach):
        prediction = 0
        self._set_training_parameters()
        number_of_user_ids = self.dataset.shape[0]
        if user_id < 1 or user_id > number_of_user_ids or type(user_id) is not int:
            Model.logModelStream.info("Userid does not exist. Enter numbers from 1-".format(number_of_user_ids))
        else:
            if approach == 'User_based_CF(cosine)':
                prediction = self._predict_userbased(user_id, item_id, str(self.metric[0]))
            elif approach == 'User_based_CF(correlation)':
                prediction = self._predict_userbased(user_id, item_id, str(self.metric[1]))

            Model.logModelFile.info("item_id:{0} | use_id:{1}".format(item_id, user_id))
            if self.dataset.iloc[item_id-1, user_id-1] != 0:
                Model.logModelStream.info('Item already rated')
                # predictions with smaller rating than 5 do not have value for the user
            else:
                if prediction >= 5:
                    Model.logModelStream.info('Item recommended')
                    return
                else:
                    return

    def train(self, user_id, item_id, approach):
        self._recommendItem(user_id, item_id, approach)

    def evaluate(self):
        pass


def main():
    ratings = data.DataAnalysis.main()
    md = Model(CFG)
    Model.logModelStream.info("---Model Logging---")
    md.load_data(ratings)
    Model.logModelStream.info("processed ratings dataset dimensions: {},"
                              .format(ratings.shape))
    # md.logModelFile.info("ratings.shape:".format(ratings.shape))
    approach = "User_based_CF(cosine)"

    # for user_id in range(1, ratings.shape[1]-1): # this is for all the user ids, attention the system will crash
    #     for item_id in range(1, 13): # this is for 13 items
    ''' all users and all items, in module  DataLoader.py i set nrows = 100000, line 63'''
    #         md.train(user_id, item_id, approach)

    md.train(7, 13, approach)  # for user 7 and item 13


if __name__ == '__main__':
    main()
