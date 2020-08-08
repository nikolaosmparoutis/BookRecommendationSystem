
import pandas as pd


def num_related_fields(foreign_key_1, foreign_key_2):
    ratings_n = ratings[ratings.foreign_key1.isin(books[foreign_key_1])]
    ratings_n = ratings_n[ratings_n[foreign_key_2].isin(users[foreign_key_2])]

    print(ratings.shape)
    print(ratings_n.shape)