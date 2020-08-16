CFG = {
    "train": {
        "algorithm": "brute",
        "radius": 0.1, #defualt to 1.0
        "k_num_neighbors": 5,
        "metric": ["cosine", "correlation"]
    }
}


"""
Briefly why selected these metrics and why the metric is very important:
If we use euclidean distance or other  metric based on geometry
we will miss two aligned users if their distance is too far away
because of the decision threshold.
With Pearson correlation or with Cosine similarity the correlation in the first and the
the angle in the second shows the similarity score.
Their flatten vectors in ratings will not get cut because of the threshold.
"""
