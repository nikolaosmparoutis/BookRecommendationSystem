import pandas as pd
import seaborn as sea
import matplotlib.pyplot as plt
from data.DataClean import DataClean
from data.DataLoader import DataLoader
from configurations.LoggerCls import LoggerCls
import os


class DataAnalysis:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    formatter = '%(name)s - %(levelname)s - Line No. : %(lineno)d - %(message)s'
    logData = LoggerCls("log_to_file", "DataAnalysis", dir_path+"/DataLogger.log", "w", formatter, "INFO")

    # Joins of entities to find the difference among the two cases:
    # Some users rated books that does not exist in Books dataset and we remove them
    @staticmethod
    def rows_from_join_on_FKs(foreign_key1, foreign_key2, ratings, users, books):
        ratings_join = ratings[ratings[foreign_key1].isin(books[foreign_key1])]
        ratings_join = ratings_join[ratings_join[foreign_key2].isin(users[foreign_key2])]
        DataAnalysis.logData.info("User who rated non  available book in dataset {0}. Users who rated books in Books dataset {1}".format(ratings.shape, ratings_join.shape))
        # print(ratings_join.shape)
        return ratings_join

    # ratings with zero are removed
    @staticmethod
    def ratings_expl_gathering(ratings_new):
        ratings_explct = ratings_new[ratings_new["Book-Rating"] != 0]
        return ratings_explct

    # hold user ids who exists in raters. The explicit values
    @staticmethod
    def users_expl_gathering(ratings_expl, users):
        ratings_expl = users[users["User-ID"].isin(ratings_expl["User-ID"])]
        return ratings_expl

    @staticmethod
    def plot_ratings_count(explicit_data, x_axis):
        sea.countplot(data=explicit_data, x=x_axis,
                      order=explicit_data[x_axis].value_counts().index)
        plt.show()

    @staticmethod
    # Users who rated at least 150 books
    def get_majority_ratings(ratings_expl):
        counts1 = ratings_expl["User-ID"].value_counts()
        ratings_expl = ratings_expl[ratings_expl["User-ID"].isin(counts1[counts1 >= 150].index)]
        counts2 = ratings_expl["Book-Rating"].value_counts()
        ratings_expl = ratings_expl[ratings_expl["Book-Rating"].isin(counts2[counts2 >= 150].index)]
        return ratings_expl

    @staticmethod
    def to_pivot_table(majority_of_ratings, as_index, as_columns, as_values):
        pivoted_table = pd.pivot_table(majority_of_ratings, index=as_index, columns=as_columns, values=as_values)
        as_columns = pivoted_table.index
        as_index = pivoted_table.columns
        DataAnalysis.logData.info("pivoted_columns: {} ".format(as_columns))
        DataAnalysis.logData.info("pivoted_index: {}".format(as_index))
        DataAnalysis.logData.info("pivoted_table:")
        DataAnalysis.logData.info(format(pivoted_table.head()))
        return pivoted_table

    @staticmethod
    def execute_pipeline_data_analysis(clean_ratings, clean_users, clean_books):
        foreign_key1, foreign_key2 = "ISBN", "User-ID"

        ratings_new = DataAnalysis.rows_from_join_on_FKs(foreign_key1, foreign_key2,
                                                         clean_ratings, clean_users, clean_books)
        ratings_explicit = DataAnalysis.ratings_expl_gathering(ratings_new)
        DataAnalysis.plot_ratings_count(ratings_explicit, "Book-Rating")
        majority_ratings = DataAnalysis.get_majority_ratings(ratings_explicit)
        DataAnalysis.logData.info("ratings from users who rated >= 150 books")
        DataAnalysis.logData.info(majority_ratings.head())
        ratings_pivoted = DataAnalysis.to_pivot_table(majority_ratings, "User-ID", "ISBN", "Book-Rating")
        # replace NaN (absence of rating) with 0 because ML algorithms (except some trees) work with numbers.
        ratings_pivoted = ratings_pivoted.fillna(0)
        DataAnalysis.logData.info("ratings_pivoted.head()" .format(ratings_pivoted.head()))
        # print("ratings_pivoted.head()", ratings_pivoted.head())
        return ratings_pivoted


def main():
    paths = "/home/nikoscf/PycharmProjects/BookRecommendation/configurations/paths.yml"
    load_begin = DataLoader()
    load_begin.read_paths(paths)

    # Uncomment to Execute this one time to get the zip if is .zip, unzip it in absolute dir you set in paths.yaml
    # Then it checks for .csv and remove the redundant zip folder
    # load_begin.check_zip_and_csv()

    books = load_begin.read_data("BX-Books.csv")
    users = load_begin.read_data("BX-Users.csv")
    ratings = load_begin.read_data("BX-Book-Ratings.csv")

    to_drop_columns = ['Image-URL-S', 'Image-URL-M', 'Image-URL-L']
    numeric_col_to_nan = ["Year-Of-Publication"]
    data_books = DataClean(books)
    clean_books = data_books.execute_pipeline_cleaning(to_drop_columns, numeric_col_to_nan)

    to_drop_columns = []
    numeric_col_to_nan = ["User-ID", "Age"]
    data_users = DataClean(users)
    clean_users = data_users.execute_pipeline_cleaning(to_drop_columns, numeric_col_to_nan)

    to_drop_columns = []
    numeric_col_to_nan = ["User-ID", "ISBN", "Book-Rating"]
    data_ratings = DataClean(ratings)
    clean_ratings = data_ratings.execute_pipeline_cleaning(to_drop_columns, numeric_col_to_nan)

    data_analysis = DataAnalysis()
    ratings_pivoted = data_analysis.execute_pipeline_data_analysis(clean_ratings, clean_users, clean_books)
    return ratings_pivoted

