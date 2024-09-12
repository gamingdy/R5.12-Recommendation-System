import numpy as np
import pandas as pd


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


def prediction(utilisateur_a_noter, item, liste_u_notes):
    numerator = moyenne(utilisateur_a_noter)
    denominator = 0
    for utilisateur in liste_u_notes:
        numerator += note(utilisateur, item) - moyenne(utilisateur) * pearson_similarity(utilisateur_a_noter, utilisateur)
        denominator += pearson_similarity(utilisateur_a_noter, utilisateur)
    return numerator / denominator


def data_reader(file_path) -> pd.DataFrame:
    return pd.read_excel(file_path, header=None)


def get_liste_utilisateur( data,item):
    resultat = []
    for utilisateur in data:
        if utilisateur[item] != -1:
            resultat.append(utilisateur)


def moyenne(data, utilisateur):
    return np.mean(filtrer(get_user_data(data, utilisateur)))


def note(data, utilisateur, item):
    return get_user_data(data, utilisateur)[item]


def get_user_data(data, user_id):
    return list(map(int, data.loc[user_id].values[0].split()))

def filtrer(utilisateur):
    return list(filter(lambda x:(x>-1),utilisateur))
    