import numpy as np

def pearson_similarity(x, y):

    if len(x) != len(y):
        raise ValueError("Les deux listes doivent avoir la même longueur")
    x = np.array(x)
    y = np.array(y)
    mean_x = np.mean(x)
    mean_y = np.mean(y)
    numerator = np.sum((x - mean_x) * (y - mean_y))
    denominator = np.sqrt(np.sum((x - mean_x) ** 2) * np.sum((y - mean_y) ** 2))

    if denominator == 0:
        return 0
    return numerator / denominator


