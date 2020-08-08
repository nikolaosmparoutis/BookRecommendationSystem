
import pandas as pd
import seaborn as sea
import matplotlib.pyplot as plt
from data.DataLoader import DataLoader


# Joins of entities to find the difference among the two cases:
# Some users  rated books that does not exist in Books dataset.
# So we work with the data from the second case.
class DataAnalysis:

    def rows_from_join_on_FKs(foreign_key1, foreign_key2, ratings, users, books):
        ratings_new = ratings[ratings[foreign_key1].isin(books[foreign_key1])]
        ratings_new = ratings_new[ratings_new[foreign_key2].isin(users[foreign_key2])]

        print(ratings.shape)
        print(ratings_new.shape)
        return ratings_new

    # ratings with zero are not the absolute truth.
    def ratings_explicit_gathering(ratings_new):
        ratings_explicit = ratings_new[ratings_new["Book-Rating"] != 0]
        return ratings_explicit


    # hold user ids who exists in raters
    def users_explicit_gathering(ratings_explicit, users):
        users_explicit = users[users["User-ID"].isin(ratings_explicit["User-ID"])]
        return users_explicit


    def plot_ratings_count(ratings_explicit):
        sea.countplot(data=ratings_explicit, x="Book-Rating", order=ratings_explicit["Book-Rating"].value_counts().index)
        plt.show()


foreign_key1 = "ISBN"
foreign_key2 = "User-ID"


ratings_new = rows_from_join_on_FKs(foreign_key1, foreign_key2, ratings, users, books)
ratings_explicit = ratings_explicit_gathering(ratings_new)
plot_ratings_count(ratings_explicit)


