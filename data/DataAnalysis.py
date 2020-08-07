
import pandas as pd


def num_related_fields(foreign_key_1, foreign_key_2):
    ratings_n = ratings[ratings.foreign_key.isin(books[prime_key])]
    ratings_n = ratings_n[ratings_n[foreign_key_2].isin(users[foreign_key_2])]

    print(ratings.shape)
    print(ratings_n.shape)