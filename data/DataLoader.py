# data: 278,858 users |  1,149,780 ratings | 271,379 books.
# http://www2.informatik.uni-freiburg.de/~cziegler/BX/
import os
import pandas as pd


from data.DataClean import DataClean

class DataLoader:
    path_to_file = None
    directory_to_extract_to = None

    def __init__(self):
        self.data = pd.DataFrame()

    @staticmethod
    def read_paths(absolute_path):
        import yaml
        with open(absolute_path, 'r') as yml_file:
            cfg = yaml.load(yml_file, Loader=yaml.FullLoader)
            DataLoader.path_to_file = cfg["path_to_file"]
            DataLoader.directory_to_extract_to = cfg["directory_to_extract_to"]

    @staticmethod
    def unzip_dataset():
        import zipfile
        with zipfile.ZipFile(DataLoader.path_to_file, 'r') as zip_ref:
            zip_ref.extractall(DataLoader.directory_to_extract_to)
        print("The folder unzipped.")
        return

    @staticmethod
    def check_zip_and_csv():
        zip_extension = os.path.splitext(DataLoader.path_to_file)[1]
        if zip_extension != ".zip":
            print("A .zip file does not exist in the given path.")
            return FileNotFoundError
        else:
            DataLoader.unzip_dataset()
            for files in os.listdir(DataLoader.directory_to_extract_to):
                if os.path.splitext(files)[1] != ".csv":
                    print("The file " + files + " is not .csv. This directory accept only .csv datasets")
                    return FileNotFoundError
                else:
                    break
            DataLoader.remove_zip_folder()
            print("The check passed, all datasets are .csv")
            return

    @staticmethod
    def remove_zip_folder():
        os.remove(DataLoader.path_to_file)
        print("The redundant folder .zip removed.")

    def read_data(self, filename):
        try:
            self.data = pd.read_csv(DataLoader.directory_to_extract_to + filename,
                                    sep=";", encoding='latin-1', error_bad_lines=False, warn_bad_lines=False,
                                    low_memory=False, memory_map=True, nrows= 100000
                                    )
        except:
            raise TypeError("Wrong file name.")
        return self.data


paths = "/home/nikoscf/PycharmProjects/BookRecommendation/configurations/paths.yml"
load_begin = DataLoader()
load_begin.read_paths(paths)

# # execute one time to get the zip if is .zip, unzip, check for .csv and remove the redundant zip folder
# # load_begin.check_zip_and_csv()


books = load_begin.read_data("BX-Books.csv")
users = load_begin.read_data("BX-Users.csv")
ratings = load_begin.read_data("BX-Book-Ratings.csv")


to_drop_columns = ['Image-URL-S', 'Image-URL-M', 'Image-URL-L']
numeric_col_to_nan = ["Year-Of-Publication"]
data_books = DataClean(books)
clean_data_books = data_books.execute_pipeline_cleaning(to_drop_columns, numeric_col_to_nan)


to_drop_columns = []
numeric_col_to_nan = ["User-ID", "ISBN", "Book-Rating"]
data_ratings = DataClean(ratings)
clean_data_ratings = data_ratings.execute_pipeline_cleaning(to_drop_columns, numeric_col_to_nan)


to_drop_columns = []
numeric_col_to_nan = ["User-ID", "Age"]
data_users = DataClean(users)
clean_data_users = data_users.execute_pipeline_cleaning(to_drop_columns, numeric_col_to_nan)


# print("data_books:", clean_data_users)
# print("data_users:", clean_data_users)
# print("data_ratings:", clean_data_users)


import seaborn as sea
import matplotlib.pyplot as plt
# from data.DataLoader import DataLoader

# Joins of entities to find the difference among the two cases:
# Some users  rated books that does not exist in Books dataset.
# So we work with the data from the second case.
# class DataAnalysis:


def rows_from_join_on_FKs(foreign_key1, foreign_key2, ratings, users, books):
    ratings_join = ratings[ratings[foreign_key1].isin(books[foreign_key1])]
    ratings_join = ratings_join[ratings_join[foreign_key2].isin(users[foreign_key2])]
    print(ratings.shape)
    print(ratings_join.shape)
    return ratings_join


# ratings with zero are not the absolute truth.
def ratings_expl_gathering(ratings_new):
    ratings_explct = ratings_new[ratings_new["Book-Rating"] != 0]
    return ratings_explct


# hold user ids who exists in raters. The expliciit values
def users_expl_gathering(ratings_expl, users):
    ratings_expl = users[users["User-ID"].isin(ratings_expl["User-ID"])]
    return ratings_expl

def plot_ratings_count(ratings_expl):
    sea.countplot(data=ratings_expl, x="Book-Rating",
                  order=ratings_expl["Book-Rating"].value_counts().index)
    plt.show()

# @staticmethod
def get_majority_ratings(ratings_expl):
    counts1 = ratings_expl["User-ID"].value_counts()
    ratings_expl = ratings_expl[ratings_expl["User-ID"].isin(counts1[counts1>=150].index)]
    counts2 = ratings_expl["Book-Rating"].value_counts()
    ratings_expl = ratings_expl[ratings_expl["Book-Rating"].isin(counts2[counts2>=150].index)]
    return ratings_expl


def to_pivot_table(majority_of_ratings, as_index, as_columns, as_values):
    ratings_pivoted = pd.pivot_table(majority_of_ratings, index=as_index, columns=as_columns, values=as_values)
    as_columns = ratings_pivoted.index
    as_index = ratings_pivoted.columns
    print("ratings_pivoted:")
    print(ratings_pivoted)
    return ratings_pivoted

foreign_key1 = "ISBN"
foreign_key2 = "User-ID"

ratings_new = rows_from_join_on_FKs(foreign_key1, foreign_key2, clean_data_ratings, clean_data_users, clean_data_books)

ratings_explicit = ratings_expl_gathering(ratings_new)
plot_ratings_count(ratings_explicit)
majority_ratings = get_majority_ratings(ratings_explicit)
print(majority_ratings.head())
ratings_pivoted = to_pivot_table(majority_ratings,"User-ID", "ISBN", "Book-Rating")
ratings_pivoted = ratings_pivoted.fillna(0) # replace NaN (absence of rating) with 0 because ML algorithms (except some tree based) respond to numbers.
print(ratings_pivoted.head())




